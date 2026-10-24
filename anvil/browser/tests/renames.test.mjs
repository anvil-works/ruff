import assert from 'node:assert/strict';
import { test } from 'node:test';
import { withBrowser } from './browser.mjs';

function applyEdits(source, edits) {
    const offset = position => source.split('\n').slice(0, position.line).reduce((n, line) => n + line.length + 1, 0) + position.character;
    for (const edit of [...edits].sort((a, b) => offset(b.range.start) - offset(a.range.start)))
        source = source.slice(0, offset(edit.range.start)) + edit.newText + source.slice(offset(edit.range.end));
    return source;
}

test('rename preparation rejects readonly API members while preserving local aliases and Designer components', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const uri = 'file:///app/client_code/Home.py';
        const code = 'from ._anvil_designer import HomeTemplate\nfrom anvil import open_form\nfrom anvil import open_form as show_form\nclass Home(HomeTemplate):\n    def run(self):\n        open_form("Home")\n        show_form("Home")\n        self.refresh_data_bindings()\n        self.button.text = "Hi"\n';
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: Demo\n', '/app/client_code/__init__.py': '',
            '/app/client_code/Home.py': code,
            '/app/client_code/Home.yaml': 'container: {type: ColumnPanel}\ncomponents: [{name: button, type: Button}]\n',
        } });
        const params = name => {
            const offset = code.indexOf(name) + 1;
            const before = code.slice(0, offset).split('\n');
            return { textDocument: { uri }, position: { line: before.length - 1, character: before.at(-1).length } };
        };
        try {
            const prepared = {};
            for (const name of ['open_form(', 'refresh_data_bindings(', 'show_form(', 'button.text'])
                prepared[name] = (await session.query('textDocument/prepareRename', params(name))).result;
            const alias = (await session.query('textDocument/rename', { ...params('show_form('), newName: 'launch_form' })).result;
            const component = (await session.query('textDocument/rename', { ...params('button.text'), newName: 'submit' })).result;
            return { prepared, alias, component, source: (await session.readSource(uri)).result.text, code };
        } finally { session.dispose(); }
    });
    assert.equal(result.prepared['open_form('], null);
    assert.equal(result.prepared['refresh_data_bindings('], null);
    assert(result.prepared['show_form(']?.range);
    assert(result.prepared['button.text']?.range);
    assert(result.alias.documentChanges.every(change => change.textDocument.uri === 'file:///app/client_code/Home.py'));
    const aliased = applyEdits(result.code, result.alias.documentChanges[0].edits);
    assert.match(aliased, /from anvil import open_form as launch_form/);
    assert.match(aliased, /launch_form\("Home"\)/);
    assert.match(aliased, /        open_form\("Home"\)/);
    assert.deepEqual(result.component.componentRenames, [{ formUri: 'file:///app/client_code/Home.py', oldName: 'button', newName: 'submit', eventHandlers: {} }]);
    assert.equal(result.source, result.code);
}));

test('module rename follows resolved imports and preserves explicit aliases and server overrides', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const uri = 'file:///app/client_code/library.py';
        const main = 'from . import library\nfrom .library import greet\nfrom . import library as lib\nvalue = library.greet()\nother = lib.greet()\n';
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: Demo\n',
            '/app/client_code/__init__.py': '',
            '/app/client_code/library.py': 'def greet(): return "client"\n',
            '/app/client_code/main.py': main,
            '/app/server_code/library.py': 'def greet(): return "server"\n',
            '/app/server_code/main.py': 'from . import library\nvalue = library.greet()\n',
        } });
        try {
            const answer = await session.query('anvil/renameResource', { uri, newName: 'helpers', sourceUris: [
                uri, 'file:///app/client_code/main.py', 'file:///app/server_code/library.py', 'file:///app/server_code/main.py',
            ] });
            const before = await session.readSource(uri);
            return { edit: answer.result, before: before.result.text, main };
        } finally { session.dispose(); }
    });
    assert.deepEqual(result.edit.resourceRenames, [{ uri: 'file:///app/client_code/library.py', oldName: 'library', newName: 'helpers' }]);
    const changes = result.edit.documentChanges;
    assert.deepEqual(changes.map(change => change.textDocument.uri), ['file:///app/client_code/main.py']);
    let updated = result.main;
    const offset = position => result.main.split('\n').slice(0, position.line).reduce((n, line) => n + line.length + 1, 0) + position.character;
    for (const edit of [...changes[0].edits].sort((a, b) => offset(b.range.start) - offset(a.range.start)))
        updated = updated.slice(0, offset(edit.range.start)) + edit.newText + updated.slice(offset(edit.range.end));
    assert.equal(updated, 'from . import helpers\nfrom .helpers import greet\nfrom . import helpers as lib\nvalue = helpers.greet()\nother = lib.greet()\n');
    assert.equal(result.before, 'def greet(): return "client"\n');
}));

test('component rename links Python, decorators, default handlers and binding expressions', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const uri = 'file:///app/client_code/Home/__init__.py';
        const code = 'from ._anvil_designer import HomeTemplate\nfrom anvil import handle as on\nclass Home(HomeTemplate):\n    @on(component_name="button", event_name="click")\n    def button_click(self, **event_args):\n        self.button.text = "Hi"\n';
        const main = 'from .Home import Home\nview = Home()\nview.button.text\n';
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: Demo\n', '/app/client_code/__init__.py': '',
            '/app/client_code/Home/__init__.py': code,
            '/app/client_code/Home/form_template.yaml': JSON.stringify({ class_name: 'Home',
                container: { type: 'ColumnPanel', components: [{ name: 'button', type: 'Button', event_bindings: { click: 'button_click' },
                    data_bindings: [{ property: 'tooltip', code: 'self.button.text' }] }] } }),
            '/app/client_code/main.py': main,
        } });
        try {
            const sidebar = (await session.query('anvil/renameComponent', { formUri: uri, componentName: 'button', newName: 'submit' })).result;
            const edit = (await session.query('textDocument/rename', { textDocument: { uri }, position: { line: 5, character: 15 }, newName: 'submit' })).result;
            return { code, main, edit, sidebar };
        }
        finally { session.dispose(); }
    });
    assert.deepEqual(result.edit, result.sidebar);
    const edits = name => result.edit.documentChanges.find(change => change.textDocument.uri.endsWith(name))?.edits ?? [];
    assert.equal(applyEdits(result.code, edits('/Home/__init__.py')), 'from ._anvil_designer import HomeTemplate\nfrom anvil import handle as on\nclass Home(HomeTemplate):\n    @on(component_name="submit", event_name="click")\n    def submit_click(self, **event_args):\n        self.submit.text = "Hi"\n');
    assert.equal(applyEdits(result.main, edits('/main.py')), 'from .Home import Home\nview = Home()\nview.submit.text\n');
    assert.deepEqual(result.edit.componentRenames, [{ formUri: 'file:///app/client_code/Home/__init__.py', oldName: 'button', newName: 'submit', eventHandlers: { button_click: 'submit_click' } }]);
    assert.equal(result.edit.bindingEdits[0].expression, 'self.button.text');
    assert.equal(applyEdits(result.edit.bindingEdits[0].expression, result.edit.bindingEdits[0].edits), 'self.submit.text');
    assert(result.edit.documentChanges.every(change => !change.textDocument.uri.includes('/.anvil/')));
}));

test('Form resource rename includes Python classes, templates, startup and custom-component references', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const uri = 'file:///app/client_code/Home/__init__.py';
        const home = 'from ._anvil_designer import HomeTemplate\nclass Home(HomeTemplate):\n    pass\n';
        const main = 'from .Home import Home as Home\nfrom anvil import open_form as show\nvalue = Home()\nshow(form="Ho" "me")\n';
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: Demo\nstartup_form: Home\nstartup: {module: Home}\ndependencies: [{dep_id: widget_library, resolution_hints: {app_id: LIB}}]\n',
            '/app/.anvil/deps/LIB/anvil.yaml': 'package_name: Widgets\n',
            '/app/.anvil/deps/LIB/client_code/Picker.py': 'from ._anvil_designer import PickerTemplate\nclass Picker(PickerTemplate): pass\n',
            '/app/.anvil/deps/LIB/client_code/Picker.yaml': 'container: {type: ColumnPanel}\nproperties: [{name: target, type: form}]\n',
            '/app/client_code/__init__.py': '',
            '/app/client_code/Home/__init__.py': home,
            '/app/client_code/Home/form_template.yaml': 'class_name: Home\ncontainer: {type: ColumnPanel}\n',
            '/app/client_code/Other/__init__.py': 'from ._anvil_designer import OtherTemplate\nclass Other(OtherTemplate): pass\n',
            '/app/client_code/Other/form_template.yaml': 'class_name: Other\ncontainer: {type: ColumnPanel}\ncomponents: [{name: child, type: "form:Home"}, {name: rows, type: RepeatingPanel, properties: {item_template: Home}}, {name: picker, type: "form:widget_library:Picker", properties: {target: Home}}]\n',
            '/app/client_code/main.py': main,
        } });
        try { return { home, main, edit: (await session.query('anvil/renameResource', { uri, newName: 'Welcome', sourceUris: [
            uri, 'file:///app/client_code/Other/__init__.py', 'file:///app/client_code/main.py',
        ] })).result }; }
        finally { session.dispose(); }
    });
    const change = name => result.edit.documentChanges.find(change => change.textDocument.uri === `file:///app/client_code/${name}`)?.edits ?? [];
    assert.equal(applyEdits(result.home, change('Home/__init__.py')), 'from ._anvil_designer import WelcomeTemplate\nclass Welcome(WelcomeTemplate):\n    pass\n');
    assert.equal(applyEdits(result.main, change('main.py')), 'from .Welcome import Welcome as Home\nfrom anvil import open_form as show\nvalue = Home()\nshow(form="Welcome")\n');
    assert(result.edit.formEdits.some(edit => edit.componentName === 'picker' && edit.path.join('.') === 'properties.target' && edit.after === 'Welcome'));
    assert(result.edit.formEdits.some(edit => edit.componentName === 'rows' && edit.path.join('.') === 'properties.item_template' && edit.after === 'Welcome'));
    assert(result.edit.configEdits.some(edit => edit.path.join('.') === 'startup_form' && edit.before === 'Home' && edit.after === 'Welcome'));
    assert(result.edit.configEdits.some(edit => edit.path.join('.') === 'startup.module' && edit.before === 'Home' && edit.after === 'Welcome'));
    assert(result.edit.formEdits.some(edit => edit.formUri.endsWith('/Other/__init__.py') && edit.componentName === 'child' && edit.path.join('.') === 'type' && edit.after === 'form:Welcome'));
}));

test('module rename keeps an explicit local alias even when its spelling matches the old module name', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const uri = 'file:///app/client_code/library.py';
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: Demo\n', '/app/client_code/__init__.py': '',
            '/app/client_code/library.py': 'answer = 42\n',
            '/app/client_code/main.py': 'from . import library as library\nvalue = library.answer\n',
        } });
        try { return (await session.query('anvil/renameResource', { uri, newName: 'helpers',
            sourceUris: [uri, 'file:///app/client_code/main.py'] })).result; }
        finally { session.dispose(); }
    });
    assert.deepEqual(result.documentChanges[0].edits, [{ range: { start: { line: 0, character: 14 }, end: { line: 0, character: 21 } }, newText: 'helpers' }]);
}));

test('ordinary startup module rename updates its configuration', () => withBrowser(async page => {
    const edit = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const uri = 'file:///app/client_code/entry.py';
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: Demo\nstartup: {module: entry}\n',
            '/app/client_code/__init__.py': '', '/app/client_code/entry.py': 'answer = 42\n',
        } });
        try { return (await session.query('anvil/renameResource', { uri, newName: 'start', sourceUris: [uri] })).result; }
        finally { session.dispose(); }
    });
    assert.deepEqual(edit.configEdits, [{ uri: 'file:///app/anvil.yaml', path: ['startup', 'module'], before: 'entry', after: 'start' }]);
}));

test('F2 on an event handler updates stored bindings in legacy Forms and leaves unrelated handlers alone', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const uri = 'file:///app/client_code/Home.py';
        const code = 'from ._anvil_designer import HomeTemplate\nclass Home(HomeTemplate):\n    def clicked(self, **event_args): pass\n';
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: Demo\n', '/app/client_code/__init__.py': '',
            '/app/client_code/Home.py': code,
            '/app/client_code/Home.yaml': 'class_name: Home\ncontainer: {type: ColumnPanel}\ncomponents: [{name: button, type: Button, event_bindings: {click: clicked}}]\n',
        } });
        try { return { code, edit: (await session.query('textDocument/rename', { textDocument: { uri }, position: { line: 2, character: 10 }, newName: 'submitted' })).result }; }
        finally { session.dispose(); }
    });
    assert.deepEqual(result.edit.eventHandlerRenames, [{ formUri: 'file:///app/client_code/Home.py', oldName: 'clicked', newName: 'submitted' }]);
    assert.equal(applyEdits(result.code, result.edit.documentChanges[0].edits), 'from ._anvil_designer import HomeTemplate\nclass Home(HomeTemplate):\n    def submitted(self, **event_args): pass\n');
}));

test('RPC rename follows implicit registrations and explicit public names without changing unrelated strings', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const serverUri = 'file:///app/server_code/jobs.py';
        const clientUri = 'file:///app/client_code/main.py';
        const server = 'import anvil.server as server\n@server.callable(require_user=True)\ndef greet(): return "Hi"\n@server.callable("pub" "lic")\ndef implementation(): return 1\n';
        const client = 'from anvil.server import call as remote\na = remote("gr" "eet")\nb = remote("public")\nc = "greet"\n';
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: Demo\n', '/app/client_code/__init__.py': '',
            '/app/server_code/jobs.py': server, '/app/client_code/main.py': client,
        } });
        try {
            const implicit = (await session.query('textDocument/rename', { textDocument: { uri: serverUri }, position: { line: 2, character: 6 }, newName: 'welcome' })).result;
            const prepared = (await session.query('textDocument/prepareRename', { textDocument: { uri: clientUri }, position: { line: 2, character: 14 } })).result;
            const explicit = (await session.query('textDocument/rename', { textDocument: { uri: clientUri }, position: { line: 2, character: 14 }, newName: 'published' })).result;
            return { implicit, explicit, prepared, server, client };
        } finally { session.dispose(); }
    });
    const updated = (edit, name, source) => applyEdits(source, edit.documentChanges.find(change => change.textDocument.uri.endsWith(name))?.edits ?? []);
    assert.equal(updated(result.implicit, '/main.py', result.client), 'from anvil.server import call as remote\na = remote("welcome")\nb = remote("public")\nc = "greet"\n');
    assert.equal(updated(result.implicit, '/jobs.py', result.server), 'import anvil.server as server\n@server.callable(require_user=True)\ndef welcome(): return "Hi"\n@server.callable("pub" "lic")\ndef implementation(): return 1\n');
    assert.equal(result.prepared.placeholder, 'public');
    assert.equal(updated(result.explicit, '/jobs.py', result.server), 'import anvil.server as server\n@server.callable(require_user=True)\ndef greet(): return "Hi"\n@server.callable("published")\ndef implementation(): return 1\n');
    assert.equal(updated(result.explicit, '/main.py', result.client), 'from anvil.server import call as remote\na = remote("gr" "eet")\nb = remote("published")\nc = "greet"\n');
}));

test('package moves include descendants and unsafe rename plans are refused without source mutations', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const home = 'from ._anvil_designer import HomeTemplate\nclass Home(HomeTemplate): pass\nclass Welcome: pass\n';
        const files = {
            '/app/anvil.yaml': 'package_name: Demo\n', '/app/client_code/__init__.py': '',
            '/app/client_code/group/__init__.py': '', '/app/client_code/group/child.py': 'value = 1\n',
            '/app/client_code/main.py': 'from .group.child import value\n',
            '/app/client_code/Home/__init__.py': home,
            '/app/client_code/Home/form_template.yaml': 'container: {type: ColumnPanel}\n',
            '/app/client_code/occupied.py': '',
            '/app/server_code/api.py': 'import anvil.server\n@anvil.server.callable\ndef greet(): pass\n',
            '/app/server_code/other.py': 'import anvil.server\n@anvil.server.callable\ndef greet(): pass\n',
            '/app/client_code/rpc.py': 'import anvil.server\nanvil.server.call("greet")\n',
        };
        const sourceUris = Object.keys(files).filter(path => path.endsWith('.py')).map(path => 'file://' + path);
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files });
        const errors = [];
        try {
            const edit = (await session.query('anvil/renameResource', { uri: 'file:///app/client_code/group/__init__.py', newName: 'folder', sourceUris })).result;
            for (const [method, params] of [
                ['anvil/renameResource', { uri: 'file:///app/client_code/Home/__init__.py', newName: 'Welcome', sourceUris }],
                ['anvil/renameResource', { uri: 'file:///app/client_code/group/__init__.py', newName: 'occupied', sourceUris }],
                ['textDocument/rename', { textDocument: { uri: 'file:///app/client_code/rpc.py' }, position: { line: 1, character: 21 }, newName: 'hello' }],
                ['anvil/renameResource', { uri: 'file:///app/client_code/group/__init__.py', newName: 'folder', sourceUris: sourceUris.filter(uri => !uri.endsWith('/main.py')) }],
            ]) {
                try { await session.query(method, params); errors.push(null); }
                catch (error) { errors.push(String(error)); }
            }
            return { edit, errors, home: (await session.readSource('file:///app/client_code/Home/__init__.py')).result.text };
        } finally { session.dispose(); }
    });
    assert.deepEqual(result.edit.resourceRenames.map(item => [item.oldName, item.newName]), [['group', 'folder'], ['group.child', 'folder.child']]);
    assert.match(result.errors[0], /Form class already exists/);
    assert.match(result.errors[1], /Resource already exists/);
    assert.match(result.errors[2], /ambiguous/);
    assert.match(result.errors[3], /read-only/);
    assert.match(result.home, /class Home\(HomeTemplate\)/);
}));

test('module rename preserves explicit aliases in their own scope only', () => withBrowser(async page => {
    const edit = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const uri = 'file:///app/client_code/library.py';
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: Demo\n', '/app/client_code/__init__.py': '', '/app/client_code/library.py': 'answer = 42\n',
            '/app/client_code/main.py': 'def f():\n    from . import library as library\n    return library.answer\ndef g():\n    from . import library\n    return library.answer\n',
        } });
        try { return (await session.query('anvil/renameResource', { uri, newName: 'helpers', sourceUris: [uri, 'file:///app/client_code/main.py'] })).result; }
        finally { session.dispose(); }
    });
    assert.equal(applyEdits('def f():\n    from . import library as library\n    return library.answer\ndef g():\n    from . import library\n    return library.answer\n', edit.documentChanges[0].edits), 'def f():\n    from . import helpers as library\n    return library.answer\ndef g():\n    from . import helpers\n    return helpers.answer\n');
}));

test('component rename updates inherited handler metadata and refuses a union of distinct component owners', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const uri = 'file:///app/client_code/Home.py';
        const files = {
            '/app/anvil.yaml': 'package_name: Demo\n', '/app/client_code/__init__.py': '',
            '/app/client_code/Home.py': 'from ._anvil_designer import HomeTemplate\nclass Home(HomeTemplate):\n    def button_click(self, **event_args): pass\n',
            '/app/client_code/Home.yaml': 'container: {type: ColumnPanel}\ncomponents: [{name: button, type: Button, event_bindings: {click: button_click}}]\n',
            '/app/client_code/Child.py': 'from .Home import Home\nfrom anvil import handle\nclass Child(Home):\n    @handle("button", "click")\n    def button_click(self, **event_args): pass\n',
            '/app/client_code/Child.yaml': 'container: {type: ColumnPanel, event_bindings: {show: button_click}}\n',
            '/app/client_code/Other.py': 'from ._anvil_designer import OtherTemplate\nclass Other(OtherTemplate): pass\n',
            '/app/client_code/Other.yaml': 'container: {type: ColumnPanel}\ncomponents: [{name: button, type: Button}]\n',
            '/app/client_code/main.py': 'from .Home import Home\nfrom .Other import Other\ndef change(view: Home | Other):\n    view.button.text = "Hi"\n',
        };
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files });
        try {
            let ambiguous;
            try { await session.query('textDocument/rename', { textDocument: { uri: 'file:///app/client_code/main.py' }, position: { line: 3, character: 11 }, newName: 'submit' }); }
            catch (error) { ambiguous = String(error); }
            let sidebarAmbiguous;
            try { await session.query('anvil/renameComponent', { formUri: uri, componentName: 'button', newName: 'submit' }); }
            catch (error) { sidebarAmbiguous = String(error); }
            await session.updateFiles({ '/app/client_code/main.py': null });
            await session.updateFiles({
                '/app/client_code/Home.py': 'from ._anvil_designer import HomeTemplate\nfrom .Other import Other\nclass Home(HomeTemplate):\n    other_view: Other\n    def button_click(self, **event_args): pass\n',
                '/app/client_code/Home.yaml': 'container: {type: ColumnPanel, data_bindings: [{property: tag, code: "(self if self.tag else self.other_view).button.text"}]}\ncomponents: [{name: button, type: Button, event_bindings: {click: button_click}}]\n',
            });
            let bindingAmbiguous;
            try { await session.query('anvil/renameComponent', { formUri: uri, componentName: 'button', newName: 'submit' }); }
            catch (error) { bindingAmbiguous = String(error); }
            await session.updateFiles({ '/app/client_code/Home.yaml': files['/app/client_code/Home.yaml'] });
            const edit = (await session.query('anvil/renameComponent', { formUri: uri, componentName: 'button', newName: 'submit' })).result;
            return { ambiguous, sidebarAmbiguous, bindingAmbiguous, edit };
        } finally { session.dispose(); }
    });
    assert.match(result.ambiguous, /ambiguous component/);
    assert.match(result.sidebarAmbiguous, /ambiguous component/);
    assert.match(result.bindingAmbiguous, /ambiguous component/);
    assert(result.edit.eventHandlerRenames.some(rename => rename.formUri.endsWith('/Child.py') && rename.oldName === 'button_click' && rename.newName === 'submit_click'));
}));

test('promoting an anonymous component updates decorators in subclasses', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: Demo\n', '/app/client_code/__init__.py': '',
            '/app/client_code/Home.py': 'from ._anvil_designer import HomeTemplate\nclass Home(HomeTemplate): pass\n',
            '/app/client_code/Home.yaml': 'container: {type: ColumnPanel}\ncomponents: [{name: $component_1, type: Button}]\n',
            '/app/client_code/child.py': 'from .Home import Home\nfrom anvil import handle\nclass Child(Home):\n    @handle("$component_1", "click")\n    def clicked(self, **event_args): pass\n',
        } });
        try { return (await session.query('anvil/renameComponent', { formUri: 'file:///app/client_code/Home.py', componentName: '$component_1', newName: 'submit' })).result; }
        finally { session.dispose(); }
    });
    assert(result.documentChanges.some(change => change.textDocument.uri.endsWith('/child.py') && change.edits.some(edit => edit.newText === '"submit"')));
}));
