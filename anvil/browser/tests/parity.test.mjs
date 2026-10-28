import assert from 'node:assert/strict';
import { test } from 'node:test';
import { withBrowser } from './browser.mjs';

test('Anvil completion preferences follow API ownership for modules, components and aliases', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const uri = 'file:///app/client_code/main.py';
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: Main\n',
            '/app/client_code/main.py': '',
        } });
        try {
            const result = [];
            for (const source of ['import anvil.server\nanvil.', 'import anvil.server\nanvil.server.',
                'import anvil.users\nanvil.users.', 'from anvil import Button\nbutton = Button()\nbutton.',
                'import anvil.server as api\napi.', 'from anvil import Button as Action\nbutton = Action()\nbutton.',
                'class Local:\n    alpha = 1\n    server = 2\n    call = 3\nanvil = Local()\nanvil.',
                'import anvil.server\nanvil.server.cal']) {
                await session.openDocument(uri, source);
                const lines = source.split('\n');
                const { items } = (await session.query('textDocument/completion', {
                    textDocument: { uri }, position: { line: lines.length - 1, character: lines.at(-1).length },
                })).result;
                result.push(items.slice(0, 5).map(item => item.label));
            }
            return result;
        } finally { session.dispose(); }
    });
    assert.equal(result[0][0], 'server', JSON.stringify(result));
    assert.equal(result[1][0], 'call', JSON.stringify(result));
    assert.equal(result[2][0], 'login_with_form', JSON.stringify(result));
    assert.equal(result[3][0], 'text', JSON.stringify(result));
    assert.equal(result[4][0], 'call', JSON.stringify(result));
    assert.equal(result[5][0], 'text', JSON.stringify(result));
    assert.equal(result[6][0], 'alpha', 'App members with the same spelling must not receive API preferences');
    assert.equal(result[7][0], 'call', 'Prefix matches precede fuzzy matches such as CallContext');
}));

test('Event methods suggest the receiver component events', () => withBrowser(async page => {
    const results = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const uri = 'file:///app/client_code/main.py';
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: Main\n', '/app/client_code/main.py': '',
        } });
        try {
            const results = [];
            for (const component of ['ColumnPanel', 'Button']) {
                for (const method of ['add_event_handler', 'set_event_handler', 'remove_event_handler', 'raise_event', 'get_event_handlers']) {
                    const handler = method.endsWith("event_handler") ? ", lambda **event_args: None" : "";
                    const source = `from anvil import ${component}\nclass Home(${component}):\n    def __init__(self):\n        self.${method}(""${handler})\n`;
                    await session.openDocument(uri, source);
                    const prefix = source.slice(0, source.indexOf('""') + 1).split('\n');
                    const { result } = await session.query('textDocument/completion', {
                        textDocument: { uri }, position: { line: prefix.length - 1, character: prefix.at(-1).length },
                    });
                    results.push({ component, method, labels: result.items.map(item => item.label) });
                }
            }
            return results;
        } finally { session.dispose(); }
    });
    for (const result of results) {
        assert(result.labels.includes('show'), JSON.stringify(result));
        assert(result.labels.includes('hide'), JSON.stringify(result));
        assert.equal(result.labels.includes('click'), result.component === 'Button', JSON.stringify(result));
    }
}));

test('Generated Form event methods suggest custom and lifecycle events after template edits', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const uri = 'file:///app/client_code/Picker/__init__.py';
        const source = 'from ._anvil_designer import PickerTemplate\nclass Picker(PickerTemplate):\n    def probe(self):\n        self.set_event_handler("", lambda **event_args: None)\n';
        const templatePath = '/app/client_code/Picker/form_template.yaml';
        const template = name => JSON.stringify({ class_name: 'Picker', custom_component: true,
            container: { type: 'ColumnPanel' }, components: [], events: [{ name, parameters: [] }] });
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: Main\n', '/app/client_code/Picker/__init__.py': source,
            [templatePath]: template('choose'),
        } });
        const complete = async method => {
            const code = source.replace('set_event_handler', method).replace(', lambda **event_args: None',
                method.endsWith('event_handler') ? ', lambda **event_args: None' : '');
            await session.openDocument(uri, code);
            return (await session.query('textDocument/completion', { textDocument: { uri },
                position: { line: 3, character: code.split('\n')[3].indexOf('""') + 1 } })).result.items.map(item => item.label);
        };
        try {
            const initial = await complete('set_event_handler');
            await session.updateFiles({ [templatePath]: template('selected') });
            const updated = {};
            for (const method of ['set_event_handler', 'add_event_handler', 'remove_event_handler', 'raise_event', 'get_event_handlers'])
                updated[method] = await complete(method);
            const definitions = (await session.query('textDocument/definition', { textDocument: { uri }, position: { line: 3, character: 16 } })).result;
            const hover = (await session.query('textDocument/hover', { textDocument: { uri }, position: { line: 3, character: 16 } })).result;
            await session.updateFiles({ [templatePath]: JSON.stringify({ class_name: 'Picker',
                layout: { type: 'ColumnPanel' }, components_by_slot: {}, slots: {}, events: [{ name: 'slot_event', parameters: [] }] }) });
            const layout = await complete('set_event_handler');
            return { initial, updated, definitions, hover, layout };
        } finally { session.dispose(); }
    });
    assert(result.initial.includes('choose'), JSON.stringify(result));
    for (const [method, labels] of Object.entries(result.updated)) {
        assert(['show', 'hide', 'refreshing_data_bindings', 'selected'].every(name => labels.includes(name)), JSON.stringify({ method, labels }));
        assert(!labels.includes('choose'), 'Removed custom event must not remain suggested');
    }
    assert(result.definitions.some(target => target.uri.endsWith('/_anvil_designer.pyi')), JSON.stringify(result.definitions));
    assert(result.hover.contents.value.includes('[Anvil Docs]'), JSON.stringify(result.hover));
    assert(['show', 'hide', 'refreshing_data_bindings', 'slot_event'].every(name => result.layout.includes(name)), JSON.stringify(result.layout));
}));

test('implicit self members match their own name prefixes without hiding local bindings', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const uri = 'file:///app/client_code/Home/__init__.py';
        const header = 'from ._anvil_designer import HomeTemplate\nfrom typing import Literal\ndef choose(value: Literal["self.name_box"]): pass\nclass Home(HomeTemplate):\n    def probe(self):\n        name_local = "local"\n';
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: Main\n',
            '/app/client_code/Home/form_template.yaml': JSON.stringify({ class_name: 'Home',
                container: { type: 'ColumnPanel' }, components: [{ name: 'name_box', type: 'TextBox', properties: {} }] }),
            '/app/client_code/Home/__init__.py': header,
        } });
        try {
            const complete = async (suffix, offset = suffix.length) => {
                const source = header + suffix;
                await session.openDocument(uri, source);
                const lines = (header + suffix.slice(0, offset)).split('\n');
                return (await session.query('textDocument/completion', { textDocument: { uri },
                    position: { line: lines.length - 1, character: lines.at(-1).length },
                    context: { autoImport: false } })).result.items;
            };
            const matching = {};
            for (const prefix of ['name', 'name_box', 'sel', '']) matching[prefix] = await complete('        ' + prefix);
            return { matching, explicit: await complete('        self.name'), outside: await complete('__cl'),
                dedented: await complete('    '), nested: await complete('        def nested():\n            '),
                module: await complete('self = "text"\nupp'),
                shadowed: await complete('        def nested():\n            if False: self = None\n            name'),
                globalMissing: await complete('        def nested():\n            global self\n            name'),
                global: await complete('self = "text"\nclass Other:\n    def probe(self):\n        def nested():\n            global self\n            upp'),
                string: await complete('        choose("name")', '        choose("name'.length) };
        } finally { session.dispose(); }
    });
    for (const [prefix, items] of Object.entries(result.matching))
        assert(items.some(item => item.label === 'self.name_box'), JSON.stringify({ prefix, labels: items.map(item => item.label) }));
    const names = result.matching.name.map(item => item.label);
    assert(names.includes('name_local'), JSON.stringify(names));
    assert(names.indexOf('name_local') < names.indexOf('self.name_box'), JSON.stringify(names));
    const completion = result.matching.name.find(item => item.label === 'self.name_box');
    assert.equal(completion.insertText ?? completion.label, 'self.name_box');
    assert(result.explicit.some(item => item.label === 'name_box'));
    assert(!result.explicit.some(item => item.label.startsWith('self.')));
    assert(!result.outside.some(item => item.label.startsWith('self.')));
    assert(!result.dedented.some(item => item.label.startsWith('self.')));
    assert(result.nested.some(item => item.label === 'self.name_box'));
    assert(result.module.some(item => item.label === 'self.upper'));
    assert(!result.shadowed.some(item => item.label === 'self.name_box'));
    assert(!result.globalMissing.some(item => item.label.startsWith('self.')));
    assert(result.global.some(item => item.label === 'self.upper'));
    assert(!result.string.some(item => item.label.includes('self.self.')));
}));

test('Callable parameters preserve function references for ordinary Python APIs', () => withBrowser(async page => {
    const item = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const uri = 'file:///app/client_code/main.py';
        const source = 'from typing import Callable\ndef register(callback: Callable[[int], str]): pass\ndef handler(value: int) -> str: return str(value)\nregister(han';
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: Main\n', '/app/client_code/main.py': source,
        } });
        try {
            const lines = source.split('\n');
            const { result } = await session.query('textDocument/completion', {
                textDocument: { uri }, position: { line: lines.length - 1, character: lines.at(-1).length },
            });
            return result.items.find(item => item.label === 'handler');
        } finally { session.dispose(); }
    });
    assert(item, 'The handler function remains a completion candidate');
    assert.equal(item.data?.insertParentheses, false, JSON.stringify(item));
}));

test('Callback completion hints apply to the argument reference, not nested receiver expressions', () => withBrowser(async page => {
    const results = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const uri = 'file:///app/client_code/main.py';
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: Main\n', '/app/client_code/main.py': '',
        } });
        const header = `from typing import Any, Callable, Protocol
class Callback(Protocol):
    def __call__(self) -> str: ...
type CallbackAlias = Callable[[], str]
def handler() -> str: return "ok"
class Hooks:
    handler = staticmethod(handler)
hooks = Hooks()
def register_many(**callbacks: Callable[[], str]): pass
`;
        const cases = [
            ['Callable[[], str] | None', 'register(han¦)', true],
            ['Callable[[], str]', 'register(¦)', true],
            ['CallbackAlias', 'register(callback=han¦)', true],
            ['CallbackAlias', 'register(callback=¦)', true],
            ['Callback', 'register(hooks.han¦)', true],
            ['Any', 'register(han¦)', false],
            ['str', 'register(han¦)', false],
            ['list[Callable[[], str]]', 'register(han¦)', false],
            ['Callable[[], str]', 'register([han¦][0].callback)', false],
            ['Callable[[], str]', 'register((lambda: han¦).callback)', false],
            ['Callable[[], str]', 'register_many(**han¦)', false],
        ];
        try {
            const results = [];
            for (const [type, expression, expected] of cases) {
                const source = header + `def register(callback: ${type}): pass\n` + expression.replace('¦', '');
                await session.openDocument(uri, source);
                const prefix = (header + `def register(callback: ${type}): pass\n` + expression.split('¦')[0]).split('\n');
                const { result } = await session.query('textDocument/completion', {
                    textDocument: { uri }, position: { line: prefix.length - 1, character: prefix.at(-1).length },
                });
                results.push({ expression, type, expected, item: result.items.find(item => item.label === 'handler') });
            }
            return results;
        } finally { session.dispose(); }
    });
    for (const result of results) {
        assert(result.item, JSON.stringify(result));
        assert.equal(result.item.data?.insertParentheses === false, result.expected, JSON.stringify(result));
    }
}));

test('Anvil handler arguments preserve function references while endpoint decorators insert parentheses', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const uri = 'file:///app/client_code/main.py';
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: Main\n', '/app/client_code/main.py': '',
            '/app/server_code/main.py': '',
        } });
        const complete = async (uri, source, label) => {
            await session.openDocument(uri, source);
            const lines = source.split('\n');
            return (await session.query('textDocument/completion', { textDocument: { uri },
                position: { line: lines.length - 1, character: lines.at(-1).length },
            })).result.items.find(item => item.label === label);
        };
        try {
            const handlers = [];
            for (const method of ['set_event_handler', 'add_event_handler', 'remove_event_handler']) {
                const source = `from anvil import Button\ndef handler(**event_args): pass\nbutton = Button()\nbutton.${method}("click", han`;
                handlers.push(await complete(uri, source, 'handler'));
            }
            const decorators = [];
            for (const name of ['callable', 'background_task', 'http_endpoint', 'route'])
                decorators.push(await complete('file:///app/server_code/main.py', '@', `anvil.server.${name}`));
            const nativeDecorators = [];
            for (const [target, source, label] of [
                [uri, 'import anvil\n@anvil.han', 'handle'],
                ['file:///app/server_code/main.py', 'from anvil.server import http_endpoint as endpoint\n@end', 'endpoint'],
                ['file:///app/server_code/main.py', 'import anvil.server as api\n@api.rou', 'route'],
            ]) nativeDecorators.push(await complete(target, source, label));
            const shadowed = await complete(uri, 'from anvil.server import http_endpoint as endpoint\ndef endpoint(fn): return fn\n@end', 'endpoint');
            return { handlers, decorators, nativeDecorators, shadowed };
        } finally { session.dispose(); }
    });
    for (const item of result.handlers) assert.equal(item?.data?.insertParentheses, false, JSON.stringify(item));
    assert.deepEqual(result.decorators.map(item => item?.data?.insertParentheses), [false, false, true, true]);
    for (const item of result.nativeDecorators) assert.equal(item?.data?.insertParentheses, true, JSON.stringify(item));
    assert.equal(result.shadowed.data?.insertParentheses, undefined, 'A local decorator must not inherit an imported API policy');
}));

test('Designer handler inference preserves aliases, original ranges, author annotations and live bindings', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const uri = 'file:///app/client_code/Home/__init__.py';
        const source = 'from ._anvil_designer import HomeTemplate\nfrom anvil import handle; _anvil_handler_types = 42\nclass Home(HomeTemplate):\n    def clicked(self, sender): "😀"; copy = sender; copy.text\n    @handle("button", "show")\n    def decorated(self, sender): sender.text\n';
        const template = (type, bound = true, event = 'click') => JSON.stringify({ class_name: 'Home', container: { type: 'ColumnPanel' },
            components: [{ name: 'button', type, properties: {}, event_bindings: bound ? { [event]: 'clicked' } : {} }] });
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: Main\n',
            '/app/client_code/Home/__init__.py': source,
            '/app/client_code/Home/form_template.yaml': template('Button'),
        } });
        const position = (line, needle, offset = 0) => ({ line, character: source.split('\n')[line].indexOf(needle) + offset });
        const query = async (method, at, extra = {}) => (await session.query('textDocument/' + method, {
            textDocument: { uri }, position: at, ...extra,
        })).result;
        const complete = async (line, at, code = source) => {
            const lines = code.split('\n');
            lines[line] = lines[line].slice(0, at);
            await session.openDocument(uri, lines.join('\n'));
            try { return (await query('completion', { line, character: at })).items.map(item => item.label); }
            finally { await session.closeDocument(uri); }
        };
        try {
            const labels = await complete(3, source.split('\n')[3].indexOf('copy.text') + 5);
            const decorated = await complete(5, source.split('\n')[5].indexOf('sender.text') + 7);
            const hover = await query('hover', position(3, 'sender;', 2));
            const definition = await query('definition', position(3, 'sender;', 2));
            const prepared = await query('prepareRename', position(3, 'sender;', 2));
            const references = await query('references', position(3, 'sender;', 2), { context: { includeDeclaration: true } });
            const rename = await query('rename', position(3, 'sender;', 2), { newName: 'source' });
            const globalCode = source.replace('copy.text', '_anvil');
            const globals = await complete(3, globalCode.split('\n')[3].length, globalCode);
            const completeImport = async module => {
                const code = `from .${module} import _anvil_handler\n`;
                await session.updateFiles({ '/app/client_code/imports.py': code, '/app/client_code/real.py': '_anvil_handler_types_ = 42\n' });
                return (await session.query('textDocument/completion', { textDocument: { uri: 'file:///app/client_code/imports.py' },
                    position: { line: 0, character: code.length - 1 },
                })).result.items.map(item => item.label);
            };
            const imported = await completeImport('Home');
            const realImport = await completeImport('real');
            const original = (await session.readSource(uri)).result.text;
            const diagnostics = await query('diagnostic');
            const symbols = await query('documentSymbol');
            const invalid = source.replace('copy.text', 'copy.not_a_property');
            await session.openDocument(uri, invalid);
            const errors = (await query('diagnostic')).items;
            await session.closeDocument(uri);
            await session.updateFiles({ '/app/client_code/Home/form_template.yaml': template('FileLoader') });
            const updated = await complete(3, source.split('\n')[3].indexOf('copy.text') + 5);
            await session.updateFiles({ '/app/client_code/Home/form_template.yaml': template('FileLoader', true, 'show') });
            const shadowed = await complete(3, source.split('\n')[3].indexOf('copy.text') + 5);
            await session.updateFiles({ '/app/client_code/Home/form_template.yaml': template('FileLoader', false) });
            const unbound = await complete(3, source.split('\n')[3].indexOf('copy.text') + 5);
            const annotated = source.replace('clicked(self, sender)', 'clicked(self, sender: str)');
            await session.openDocument(uri, annotated);
            await session.updateFiles({ '/app/client_code/Home/form_template.yaml': template('Button') });
            const explicit = await complete(3, annotated.split('\n')[3].indexOf('copy.text') + 5, annotated);
            return { imported, realImport, globals, errors, prepared, diagnostics, labels, decorated, hover, definition, references, rename, original, symbols, updated, shadowed, unbound, explicit, source };
        } finally { session.dispose(); }
    });
    assert(result.labels.includes('text') && result.decorated.includes('text'), JSON.stringify(result));
    assert.match(result.hover.contents.value, /Button/);
    assert.deepEqual(result.diagnostics.items.filter(item => item.severity === 1), []);
    const sender = result.source.split('\n')[3].indexOf('sender');
    assert.deepEqual(result.definition, [{ uri: 'file:///app/client_code/Home/__init__.py',
        range: { start: { line: 3, character: sender }, end: { line: 3, character: sender + 6 } } }]);
    assert.deepEqual(result.prepared.range, { start: { line: 3, character: result.source.split('\n')[3].indexOf('sender;') },
        end: { line: 3, character: result.source.split('\n')[3].indexOf('sender;') + 6 } });
    const error = result.errors.find(item => item.code === 'unresolved-attribute');
    assert.equal(error.range.end.character, result.source.split('\n')[3].indexOf('copy.text') + 'copy.not_a_property'.length);
    assert.deepEqual(result.references.map(item => item.range.start.character).sort((a, b) => a - b),
        [sender, result.source.split('\n')[3].indexOf('sender;')]);
    assert.deepEqual(result.rename.documentChanges.flatMap(change => change.edits.map(edit => edit.range)), result.references.map(item => item.range));
    assert.equal(result.original, result.source);
    assert(!result.symbols.some(symbol => symbol.name === '_anvil_handler_types_'));
    assert(result.globals.includes('_anvil_handler_types') && !result.globals.includes('_anvil_handler_types_'), JSON.stringify(result.globals));
    assert(result.imported.includes('_anvil_handler_types') && !result.imported.includes('_anvil_handler_types_'), JSON.stringify(result.imported));
    assert(result.realImport.includes('_anvil_handler_types_'), JSON.stringify(result.realImport));
    assert(!result.labels.includes('clear') && result.updated.includes('clear'));
    assert(!result.unbound.includes('clear'));
    assert(!result.shadowed.includes('clear'), 'Decorated event bindings replace YAML bindings for the same component/event');
    assert(result.explicit.includes('upper') && !result.explicit.includes('text'));
}));

test('FileLoader event payloads retain nullable types and follow their binding while unrelated handlers remain gradual', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const uri = 'file:///app/client_code/Home/__init__.py';
        const source = expression => `from ._anvil_designer import HomeTemplate\nclass Other:\n    def changed(self, file):\n        if file is not None:\n            ${expression}\nclass Home(HomeTemplate):\n    def changed(self, file, files, **event_args):\n        if file is not None:\n            ${expression}\n`;
        const template = event => JSON.stringify({ class_name: 'Home', container: { type: 'ColumnPanel' },
            components: [{ name: 'upload', type: 'FileLoader', properties: {}, event_bindings: { [event]: 'changed' } }] });
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: Main\n',
            '/app/client_code/Home/__init__.py': source('file.'),
            '/app/client_code/Home/form_template.yaml': template('change'),
        } });
        const complete = async (expression, line = 8) => {
            await session.openDocument(uri, source(expression));
            return (await session.query('textDocument/completion', { textDocument: { uri },
                position: { line, character: 12 + expression.length },
            })).result.items.map(item => item.label);
        };
        try {
            const file = await complete('file.');
            const files = await complete('files[0].');
            const hover = (await session.query('textDocument/hover', { textDocument: { uri }, position: { line: 6, character: 23 } })).result;
            await session.openDocument(uri, source('file.name').replaceAll('if file is not None:', 'if True:'));
            const diagnostics = (await session.query('textDocument/diagnostic', { textDocument: { uri } })).result.items;
            const unrelated = await complete('file.', 4);
            await session.updateFiles({ '/app/client_code/Home/form_template.yaml': template('show') });
            return { file, files, hover, diagnostics, unrelated, rebound: await complete('file.') };
        } finally { session.dispose(); }
    });
    for (const labels of [result.file, result.files])
        assert(['name', 'content_type', 'get_bytes'].every(name => labels.includes(name)), JSON.stringify(labels));
    assert.match(result.hover.contents.value, /Media \| None/);
    assert(result.diagnostics.some(item => item.message.includes('None') && item.message.includes('name')));
    assert(!result.unrelated.includes('get_bytes'));
    assert(!result.rebound.includes('get_bytes'));
}));

test('layout events and Form events infer their distinct sender owners when both binding maps are present', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const uri = 'file:///app/client_code/Home/__init__.py';
        const source = 'from ._anvil_designer import HomeTemplate\nclass Home(HomeTemplate):\n    def own_method(self): return True\n    def form_show(self, sender):\n        sender.\n    def layout_show(self, sender):\n        sender.\n';
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: Main\n',
            '/app/client_code/Home/__init__.py': source,
            '/app/client_code/Home/form_template.yaml': JSON.stringify({ class_name: 'Home', layout: { type: 'form:Layout',
                event_bindings: { show: 'layout_show' }, form_event_bindings: { show: 'form_show' } }, components_by_slot: {} }),
            '/app/client_code/Layout/__init__.py': 'from ._anvil_designer import LayoutTemplate\nclass Layout(LayoutTemplate):\n    def layout_method(self): return True\n',
            '/app/client_code/Layout/form_template.yaml': JSON.stringify({ class_name: 'Layout', container: { type: 'ColumnPanel' }, components: [] }),
        } });
        const complete = async line => (await session.query('textDocument/completion', { textDocument: { uri },
            position: { line, character: 15 },
        })).result.items.map(item => item.label);
        try { return { form: await complete(4), layout: await complete(6) }; }
        finally { session.dispose(); }
    });
    assert(result.form.includes('own_method') && !result.form.includes('layout_method'), JSON.stringify(result.form));
    assert(result.layout.includes('layout_method') && !result.layout.includes('own_method'), JSON.stringify(result.layout));
}));

test('RepeatingPanel children follow current item templates in code and bindings without weakening ordinary containers', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const uri = 'file:///app/client_code/Home/__init__.py';
        const template = child => JSON.stringify({ class_name: 'Home', container: { type: 'ColumnPanel' },
            components: [{ name: 'rows', type: 'RepeatingPanel', properties: { item_template: child } }] });
        const files = {
            '/app/anvil.yaml': 'package_name: Main\n',
            '/app/client_code/Home/__init__.py': 'from ._anvil_designer import HomeTemplate\nclass Home(HomeTemplate):\n    def probe(self):\n        self.rows.get_components()[0].\n',
            '/app/client_code/Home/form_template.yaml': template('Row'),
            '/app/client_code/defaults.py': 'import anvil\npanel = anvil.RepeatingPanel(items=[], visible=True)\nchild: anvil.Component = panel.get_components()[0]\ncontainer = anvil.ColumnPanel()\nother: anvil.Component = container.get_components()[0]\n',
        };
        for (const [name, method] of [['Row', 'greet'], ['Other', 'farewell']]) {
            files[`/app/client_code/${name}/__init__.py`] = `from ._anvil_designer import ${name}Template\nclass ${name}(${name}Template):\n    def ${method}(self): return "yes"\n`;
            files[`/app/client_code/${name}/form_template.yaml`] = JSON.stringify({ class_name: name, container: { type: 'ColumnPanel' }, components: [] });
        }
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files });
        const complete = async () => (await session.query('textDocument/completion', {
            textDocument: { uri }, position: { line: 3, character: 38 },
        })).result.items.map(item => item.label);
        try {
            const before = await complete();
            await session.updateFiles({ '/app/client_code/Home/form_template.yaml': template('Other') });
            const after = await complete();
            const code = 'self.rows.get_components()[0].';
            await session.setContext({ kind: 'binding', id: 'children', formUri: uri, code });
            const binding = (await session.queryContext('children', 'textDocument/completion', { position: { line: 0, character: code.length } })).result.items.map(item => item.label);
            const diagnostics = (await session.query('textDocument/diagnostic', { textDocument: { uri: 'file:///app/client_code/defaults.py' } })).result.items;
            return { before, after, binding, diagnostics };
        } finally { session.dispose(); }
    });
    assert(result.before.includes('greet'), JSON.stringify(result.before));
    assert(result.after.includes('farewell') && !result.after.includes('greet'), JSON.stringify(result.after));
    assert(result.binding.includes('farewell'), JSON.stringify(result.binding));
    assert.deepEqual(result.diagnostics.filter(item => item.severity === 1), []);
}));

test('reference usage queries exclude declarations and imports while rename retains import edits', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const uri = 'file:///app/client_code/api.py';
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: Main\n',
            '/app/client_code/api.py': 'def greet(): return "Ada"\n',
            '/app/client_code/bridge.py': 'from .api import greet as greet\n',
            '/app/client_code/main.py': 'from .bridge import greet as welcome\nwelcome()\n',
            '/app/client_code/other.py': 'from .api import greet\ngreet()\n',
            '/app/server_code/api.py': 'def greet(): return 42\n',
            '/app/server_code/registrations.py': 'from anvil.server import callable\n@callable\ndef registered(): return True\n',
        } });
        const params = { textDocument: { uri }, position: { line: 0, character: 6 } };
        try {
            const usages = (await session.query('textDocument/references', { ...params,
                context: { includeDeclaration: false, includeImports: false },
            })).result;
            const all = (await session.query('textDocument/references', { ...params, context: { includeDeclaration: true } })).result;
            const rename = (await session.query('textDocument/rename', { ...params, newName: 'hello' })).result;
            const definition = (await session.query('textDocument/definition', {
                textDocument: { uri: 'file:///app/client_code/main.py' }, position: { line: 1, character: 3 },
            })).result;
            return { usages, all, rename, definition };
        } finally { session.dispose(); }
    });
    assert.deepEqual(result.usages.map(item => [item.uri.split('/').at(-1), item.range.start.line]).sort(),
        [['main.py', 1], ['other.py', 1]]);
    assert(result.all.some(item => item.uri.endsWith('/api.py')));
    assert(result.all.some(item => item.uri.endsWith('/bridge.py')));
    assert(result.rename.documentChanges.some(change => change.textDocument.uri.endsWith('/other.py')));
    assert.deepEqual(result.definition.map(item => item.uri), ['file:///app/client_code/api.py']);
}));

test('Form handle completion offers anonymous components only after Designer gives them a name', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const uri = 'file:///app/client_code/Home/__init__.py';
        const source = args => `from ._anvil_designer import HomeTemplate\nfrom anvil import handle\nclass Home(HomeTemplate):\n    @handle(${args})\n    def clicked(self, **event_args): pass\n`;
        const template = name => JSON.stringify({ class_name: 'Home', container: { type: 'ColumnPanel' }, components: [
            { name: 'button_1', type: 'Button', properties: {} }, { name, type: 'Button', properties: {} },
        ] });
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: Main\n',
            '/app/client_code/Home/__init__.py': source('"", "click"'),
            '/app/client_code/Home/form_template.yaml': template('$component_1'),
        } });
        const complete = async args => {
            const code = source(args);
            const before = code.slice(0, code.indexOf('¦')).split('\n');
            await session.openDocument(uri, code.replace('¦', ''));
            return (await session.query('textDocument/completion', { textDocument: { uri },
                position: { line: before.length - 1, character: before.at(-1).length },
            })).result.items.map(item => item.label);
        };
        try {
            const before = await complete('"¦", "click"');
            const anonymousEvents = await complete('"$component_1", "¦"');
            await session.updateFiles({ '/app/client_code/Home/form_template.yaml': template('button_2') });
            return { before, anonymousEvents, named: await complete('"¦", "click"'), events: await complete('"button_2", "¦"') };
        } finally { session.dispose(); }
    });
    assert(result.before.includes('button_1'), JSON.stringify(result.before));
    assert(!result.before.some(name => name.startsWith('$')), 'Anonymous Designer identities must not appear in completion');
    assert.deepEqual(result.anonymousEvents, []);
    assert(result.named.includes('button_2'), JSON.stringify(result.named));
    assert(['click', 'show', 'hide'].every(name => result.events.includes(name)), JSON.stringify(result.events));
}));

test('dependency Form items retain their own row models and refresh after model changes', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': JSON.stringify({ package_name: 'Main', dependencies: [{ app_id: 'LIB' }],
                db_schema: { people: { columns: [{ name: 'name', type: 'string' }] } } }),
            '/app/client_code/main.py': 'from Library.RowTemplate import RowTemplate\nform = RowTemplate()\nform.item.\n',
            '/app/.anvil/deps/LIB/anvil.yaml': 'package_name: Library\n',
            '/app/.anvil/deps/LIB/client_code/models.py': 'from anvil.tables import app_tables\nclass Person(app_tables.people.Row):\n    def display(self) -> str: return self["name"]\n',
            '/app/.anvil/deps/LIB/client_code/RowTemplate/__init__.py': 'from ._anvil_designer import RowTemplateTemplate\nclass RowTemplate(RowTemplateTemplate): pass\n',
            '/app/.anvil/deps/LIB/client_code/RowTemplate/form_template.yaml': JSON.stringify({ class_name: 'RowTemplate',
                container: { type: 'ColumnPanel' }, components: [], item_type: { table_name: 'people' } }),
        } });
        const complete = async () => (await session.query('textDocument/completion', {
            textDocument: { uri: 'file:///app/client_code/main.py' }, position: { line: 2, character: 10 },
        })).result.items.map(item => item.label);
        try {
            const before = await complete();
            const uri = 'file:///app/.anvil/deps/LIB/client_code/models.py';
            const edited = 'from anvil.tables import app_tables\nclass Person(app_tables.people.Row, attrs=True):\n    def display(self) -> str: return self["name"]\n    def probe(self):\n        self.na\n';
            await session.openDocument(uri, edited);
            const attrs = await complete();
            const ownMethod = (await session.query('textDocument/completion', {
                textDocument: { uri }, position: { line: 4, character: 15 },
            })).result.items.map(item => item.label);
            const original = (await session.readSource(uri)).result.text;
            await session.closeDocument(uri);
            await session.updateFiles({ '/app/client_code/models.py': 'from anvil.tables import app_tables\nclass MainPerson(app_tables.people.Row, attrs=True): pass\n' });
            const mainAttrs = await complete();
            await session.updateFiles({ '/app/.anvil/deps/LIB/client_code/models.py': 'class Person: pass\n' });
            return { before, attrs, ownMethod, original, edited, mainAttrs, after: await complete() };
        } finally { session.dispose(); }
    });
    assert(result.before.includes('display'), JSON.stringify(result.before));
    assert(!result.before.includes('name'));
    assert(result.attrs.includes('name'), JSON.stringify(result.attrs));
    assert(result.ownMethod.includes('name'), JSON.stringify(result.ownMethod));
    assert.equal(result.original, result.edited, 'Read-only views retain the original overlay source');
    assert(!result.mainAttrs.includes('name'), 'Dependency attrs=False must not inherit the main model flag');
    assert(!result.after.includes('display'));
    assert(result.after.includes('update'));
}));

test('RPC results follow inferred server return types and unsaved source changes', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const server = value => `from anvil.server import callable\n@callable\ndef greet(): return ${value}\n`;
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: Main\n',
            '/app/client_code/main.py': 'from anvil.server import call as remote\nanswer = remote("greet")\nanswer.\n',
            '/app/server_code/api.py': server('"Ada"'),
        } });
        const complete = async () => (await session.query('textDocument/completion', {
            textDocument: { uri: 'file:///app/client_code/main.py' }, position: { line: 2, character: 7 },
        })).result.items.map(item => item.label);
        try {
            const before = await complete();
            await session.openDocument('file:///app/server_code/api.py', server('42'));
            const after = await complete();
            await session.closeDocument('file:///app/server_code/api.py');
            return { before, after, restored: await complete() };
        } finally { session.dispose(); }
    });
    assert(result.before.includes('upper'), JSON.stringify(result.before));
    assert(result.after.includes('bit_length'), JSON.stringify(result.after));
    assert(!result.after.includes('upper'));
    assert(result.restored.includes('upper'), JSON.stringify(result.restored));
}));

test('background-task results retain their inferred type through get_return_value', () => withBrowser(async page => {
    const labels = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: Main\n',
            '/app/server_code/tasks.py': 'from anvil.server import background_task as task\n@task("refresh")\ndef refresh_people(): return "done"\n',
            '/app/client_code/__init__.py': '',
            '/app/server_code/caller.py': 'from anvil.server import launch_background_task\ntask = launch_background_task("refresh")\ntask.get_return_value().\n',
        } });
        try {
            return (await session.query('textDocument/completion', {
                textDocument: { uri: 'file:///app/server_code/caller.py' }, position: { line: 2, character: 24 },
            })).result.items.map(item => item.label);
        } finally { session.dispose(); }
    });
    assert(labels.includes('upper'), JSON.stringify(labels));
}));

test('RPC result declarations preserve shared type identities and reject server overrides', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: Main\n',
            '/app/client_code/a.py': 'class Person:\n    def alpha(self) -> str: return "a"\n',
            '/app/client_code/b.py': 'class Person:\n    def beta(self) -> str: return "b"\n',
            '/app/client_code/secret.py': 'class Private:\n    def client_only(self) -> str: return "client"\n',
            '/app/server_code/secret.py': 'class Private:\n    def server_only(self) -> str: return "server"\n',
            '/app/server_code/api.py': 'from anvil.server import callable\nfrom Main.a import Person as A\nfrom Main.b import Person as B\nfrom Main.secret import Private\n@callable("first")\ndef first_person(): return A()\n@callable\ndef second(): return B()\n@callable\ndef private(): return Private()\n',
            '/app/client_code/main.py': 'from anvil.server import call\na = call("first")\na.\nb = call("second")\nb.\nprivate = call("private")\nprivate.\n',
        } });
        const complete = async (line, character) => (await session.query('textDocument/completion', {
            textDocument: { uri: 'file:///app/client_code/main.py' }, position: { line, character },
        })).result.items.map(item => item.label);
        try {
            const a = await complete(2, 2), b = await complete(4, 2), privateType = await complete(6, 8);
            const params = { textDocument: { uri: 'file:///app/client_code/a.py' }, position: { line: 0, character: 8 } };
            const references = (await session.query('textDocument/references', { ...params, context: { includeDeclaration: true } })).result;
            const rename = (await session.query('textDocument/rename', { ...params, newName: 'Contact' })).result;
            return { a, b, private: privateType, references, rename };
        }
        finally { session.dispose(); }
    });
    assert(result.a.includes('alpha'), JSON.stringify(result));
    assert(!result.a.includes('beta'));
    assert(result.b.includes('beta'), JSON.stringify(result));
    assert(!result.b.includes('alpha'));
    assert(!result.private.includes('client_only'), 'A distinct client class must not replace the server result type');
    assert(result.references.every(item => !item.uri.includes('/.anvil/analysis/')), 'Derived type declarations must not appear as user references');
    assert.deepEqual(result.rename.documentChanges.map(change => change.textDocument.uri).sort(),
        ['file:///app/client_code/a.py', 'file:///app/server_code/api.py']);
}));

test('plain Python contexts remain usable after a completion with no RPC registrations', () => withBrowser(async page => {
    const labels = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/main.py': 'value = "Ada"\nvalue.\n',
        } });
        try {
            await session.query('textDocument/completion', { textDocument: { uri: 'file:///app/main.py' }, position: { line: 1, character: 6 } });
            await session.setContext({ kind: 'repl', id: 'console', isServer: false, previousCode: 'value = "Ada"\n', code: 'value.' });
            return (await session.queryContext('console', 'textDocument/completion', { position: { line: 0, character: 6 } })).result.items.map(item => item.label);
        } finally { session.dispose(); }
    });
    assert(labels.includes('upper'), JSON.stringify(labels));
}));

test('row-model attributes require an Anvil binding and schema without changing unrelated Python', () => withBrowser(async page => {
    const results = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const local = 'class app_tables:\n    class people:\n        class Row:\n            def __init_subclass__(cls, *, attrs=False): pass\n            def original(self) -> str: return "yes"\nclass Local(app_tables.people.Row, attrs=True): pass\nvalue: int = Local().original()\n';
        const model = 'from anvil.tables import app_tables\nclass Person(app_tables.people.Row, attrs=True): pass\n';
        const schema = { people: { columns: [{ name: 'name', type: 'string' }] } };
        const fixtures = [
            { name: 'unrelated binding', source: local, schema },
            { name: 'shadowed import', source: 'from anvil.tables import app_tables\n' + local, schema },
            { name: 'missing schema', source: model },
            { name: 'legacy array schema', source: model, schema: [] },
        ];
        const result = [];
        for (const fixture of fixtures) {
            const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
                '/app/anvil.yaml': JSON.stringify({ package_name: 'Main', db_schema: fixture.schema }),
                '/app/client_code/models.py': fixture.source,
            } });
            try {
                const diagnostics = (await session.query('textDocument/diagnostic', {
                    textDocument: { uri: 'file:///app/client_code/models.py' },
                })).result.items;
                result.push({ name: fixture.name, errors: diagnostics.filter(item => item.severity === 1) });
            } finally { session.dispose(); }
        }
        return result;
    });
    for (const result of results) {
        assert.deepEqual(result.errors.map(item => item.code),
            result.name.includes('binding') || result.name.includes('shadowed') ? ['invalid-assignment'] : [], JSON.stringify(result));
    }
}));

test('RPC strings navigate to registered callables and link only semantic references', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const client = 'file:///app/client_code/main.py';
        const server = 'file:///app/server_code/api.py';
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: Main\n',
            '/app/client_code/main.py': 'from anvil.server import call as remote\nremote("public")\nremote("public")\nordinary = "public"\nname = "public"\nremote(name)\n',
            '/app/client_code/ordinary.py': 'def call(name): pass\ncall("public")\n',
            '/app/server_code/api.py': 'from anvil.server import callable as register\n@register("public")\ndef implementation(): return "Hello"\nvalue = implementation()\n',
        } });
        const query = async (method, uri, line, character, extra = {}) => (await session.query(method, {
            textDocument: { uri }, position: { line, character }, ...extra,
        })).result;
        try {
            const definition = await query('textDocument/definition', client, 1, 10);
            const references = await query('textDocument/references', client, 1, 10, { context: { includeDeclaration: false } });
            const fromDefinition = await query('textDocument/references', server, 2, 8, { context: { includeDeclaration: false } });
            const variable = await query('textDocument/definition', client, 5, 8);
            const ordinary = await query('textDocument/definition', client, 3, 15);
            await session.updateFiles({ '/app/server_code/other.py': 'from anvil.server import callable\n@callable("public")\ndef other(): pass\n' });
            return { definition, references, fromDefinition, variable, ordinary,
                ambiguous: await query('textDocument/definition', client, 1, 10) };
        } finally { session.dispose(); }
    });
    assert.deepEqual(result.definition.map(item => [item.uri, item.range.start.line]), [['file:///app/server_code/api.py', 2]]);
    const sites = references => references.map(item => [item.uri.split('/').at(-1), item.range.start.line]).sort();
    assert.deepEqual(sites(result.references), [['api.py', 3], ['main.py', 1], ['main.py', 2]]);
    assert.deepEqual(sites(result.fromDefinition), sites(result.references));
    assert.equal(result.variable[0].range.start.line, 4, 'A variable argument retains ordinary Python navigation');
    assert.deepEqual(result.ordinary, []);
    assert.deepEqual(result.ambiguous.map(item => item.uri).sort(), ['file:///app/server_code/api.py', 'file:///app/server_code/other.py']);
}));

test('RepeatingPanel row templates infer table items, refresh and respect explicit or conflicting types', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const parent = (name, table) => `from ._anvil_designer import ${name}Template\nfrom anvil.tables import app_tables\nclass ${name}(${name}Template):\n    def __init__(self):\n        rows = app_tables.${table}.search()\n        self.repeating_panel_1.items = rows\n`;
        const template = name => JSON.stringify({ class_name: name, container: { type: 'ColumnPanel' },
            components: [{ name: 'repeating_panel_1', type: 'RepeatingPanel', properties: { item_template: 'RowTemplate' } }] });
        const rowTemplate = { class_name: 'RowTemplate', container: { type: 'ColumnPanel' }, components: [] };
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': JSON.stringify({ package_name: 'Main', db_schema: {
                people: { columns: [{ name: 'name', type: 'string' }] }, totals: { columns: [{ name: 'name', type: 'number' }] },
            } }),
            '/app/client_code/Home/__init__.py': parent('Home', 'people'),
            '/app/client_code/Home/form_template.yaml': template('Home'),
            '/app/client_code/RowTemplate/__init__.py': 'from ._anvil_designer import RowTemplateTemplate\nclass RowTemplate(RowTemplateTemplate):\n    def probe(self):\n        self.item["name"].\n',
            '/app/client_code/RowTemplate/form_template.yaml': JSON.stringify(rowTemplate),
        } });
        const complete = async () => (await session.query('textDocument/completion', {
            textDocument: { uri: 'file:///app/client_code/RowTemplate/__init__.py' }, position: { line: 3, character: 26 },
        })).result.items.map(item => item.label);
        try {
            const before = await complete();
            await session.openDocument('file:///app/client_code/Home/__init__.py', parent('Home', 'totals'));
            const after = await complete();
            await session.updateFiles({ '/app/client_code/Other/__init__.py': parent('Other', 'people'),
                '/app/client_code/Other/form_template.yaml': template('Other') });
            const conflicting = await complete();
            await session.updateFiles({ '/app/client_code/RowTemplate/form_template.yaml': JSON.stringify({ ...rowTemplate, item_type: { table_name: 'people' } }) });
            return { before, after, conflicting, explicit: await complete() };
        } finally { session.dispose(); }
    });
    assert(result.before.includes('upper'), JSON.stringify(result.before));
    assert(result.after.includes('conjugate'), JSON.stringify(result.after));
    assert(!result.after.includes('upper'));
    assert(!result.conflicting.includes('upper') && !result.conflicting.includes('conjugate'), 'Conflicting parents must not pick an arbitrary table');
    assert(result.explicit.includes('upper'));
}));


test('Form dictionary items preserve keys and value types across live edits with unrelated data modules', () => withBrowser(async page => {
    // Ty's WASM filesystem has millisecond revisions. Exercise every snapshot
    // and live update in one tick so freshness never relies on elapsed time.
    await page.route('**/worker.mjs', async route => {
        const response = await route.fetch();
        await route.fulfill({ response, body: 'Date.now = () => 1000000000000;\n' + await response.text() });
    });
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const unrelated = Object.fromEntries(Array.from({ length: 50 }, (_, index) => [`/app/client_code/unrelated${index}.py`,
            Array.from({ length: 10 }, (_, record) => `record${record} = {"unrelated_name": "unused", "unrelated_age": 42}`).join('\n')]));
        const producer = (name, age) => `from .RowTemplate import RowTemplate\nrow = RowTemplate(item={"name": ${name}, "age": ${age}})\n`;
        const formUri = 'file:///app/client_code/RowTemplate/__init__.py';
        const source = 'from ._anvil_designer import RowTemplateTemplate\nclass RowTemplate(RowTemplateTemplate):\n    def probe(self):\n        self.item["name"].\n';
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: Main\n',
            ...unrelated,
            '/app/client_code/main.py': producer('"Ada"', '42'),
            '/app/client_code/RowTemplate/__init__.py': source,
            '/app/client_code/RowTemplate/form_template.yaml': JSON.stringify({ class_name: 'RowTemplate', container: { type: 'ColumnPanel' }, components: [] }),
        } });
        const binding = async code => {
            await session.setContext({ kind: 'binding', id: 'row', formUri, code });
            return (await session.queryContext('row', 'textDocument/completion', {
                position: { line: 0, character: code.endsWith(']') ? code.length - 2 : code.length },
            })).result.items.map(item => item.label);
        };
        try {
            const code = (await session.query('textDocument/completion', { textDocument: { uri: formUri }, position: { line: 3, character: 26 } })).result.items.map(item => item.label);
            const keys = await binding('self.item[""]');
            const name = await binding('self.item["name"].');
            const age = await binding('self.item["age"].');
            await session.updateFiles({ '/app/client_code/other.py': producer('"Grace"', '100') });
            const sameShape = await binding('self.item["name"].');
            await session.updateFiles({ '/app/client_code/other.py': null });
            await session.openDocument('file:///app/client_code/main.py', producer('42', '"forty two"'));
            const changed = await binding('self.item["name"].');
            const original = (await session.readSource(formUri)).result.text;
            await session.closeDocument('file:///app/client_code/main.py');
            return { code, keys, name, age, sameShape, changed, original, source, restored: await binding('self.item["name"].') };
        } finally { session.dispose(); }
    });
    assert(result.code.includes('upper'));
    assert(result.keys.includes('name') && result.keys.includes('age'));
    assert(result.name.includes('upper') && !result.name.includes('bit_length'));
    assert(result.age.includes('bit_length') && !result.age.includes('upper'));
    assert(result.sameShape.includes('upper'), 'Different literal data with the same dictionary schema is compatible');
    assert(result.changed.includes('bit_length') && !result.changed.includes('upper'));
    assert(result.restored.includes('upper'), JSON.stringify(result.restored));
    assert.equal(result.original, result.source, 'Analysis instrumentation must not alter source views');
}));

test('Form item inference preserves ordinary Python mapping operations and keeps generated references out of rename', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const uri = 'file:///app/client_code/RowTemplate/__init__.py';
        const source = 'from ._anvil_designer import RowTemplateTemplate\nclass RowTemplate(RowTemplateTemplate):\n    def probe(self):\n        self.item.\n';
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: Main\n',
            '/app/client_code/main.py': 'from .RowTemplate import RowTemplate\nrow = RowTemplate(item=next(iter({"name": "Ada"}.values())))\n',
            '/app/client_code/RowTemplate/__init__.py': source,
            '/app/client_code/RowTemplate/form_template.yaml': JSON.stringify({ class_name: 'RowTemplate', container: { type: 'ColumnPanel' }, components: [] }),
        } });
        const complete = async () => (await session.query('textDocument/completion', { textDocument: { uri }, position: { line: 3, character: 18 } })).result.items.map(item => item.label);
        try {
            const values = await complete();
            await session.updateFiles({ '/app/client_code/RowTemplate/__init__.py': source + '\nclass Utility:\n    @staticmethod\n    def RowTemplate(*, item): return item\n',
                '/app/client_code/main.py': 'from .RowTemplate import Utility\nrow = Utility.RowTemplate(item=42)\n' });
            const unrelated = await complete();
            await session.updateFiles({ '/app/client_code/RowTemplate/__init__.py': source });
            await session.updateFiles({ '/app/client_code/main.py': 'from .RowTemplate import RowTemplate\nclass Person:\n    name: str\nrow = RowTemplate(item=Person())\n' });
            const object = await complete();
            const params = { textDocument: { uri: 'file:///app/client_code/main.py' }, position: { line: 1, character: 8 } };
            const references = (await session.query('textDocument/references', params)).result;
            const rename = (await session.query('textDocument/rename', { ...params, newName: 'Customer' })).result;
            return { values, unrelated, object, references, rename };
        } finally { session.dispose(); }
    });
    assert(result.values.includes('upper'), 'dict.values() must retain the ordinary str element type');
    assert(!result.unrelated.includes('bit_length'), 'A same-named method is not the Form constructor');
    assert(result.object.includes('name'));
    assert(result.references.every(reference => reference.uri === 'file:///app/client_code/main.py'));
    assert.deepEqual(result.rename.documentChanges.map(change => change.textDocument.uri), ['file:///app/client_code/main.py']);
    assert.equal(result.rename.documentChanges[0].edits.length, 2);
}));


test('RPC-populated Form items use current server return types for panels and direct construction', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const server = value => `from anvil.server import callable\n@callable\ndef people(): return ${value}\n`;
        const uri = 'file:///app/client_code/RowTemplate/__init__.py';
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: Main\n',
            '/app/server_code/api.py': server('["Ada"]'),
            '/app/client_code/Home/__init__.py': 'from ._anvil_designer import HomeTemplate\nfrom anvil.server import call\nclass Home(HomeTemplate):\n    def __init__(self):\n        self.rows.items = call("people")\n',
            '/app/client_code/Home/form_template.yaml': JSON.stringify({ class_name: 'Home', container: { type: 'ColumnPanel' },
                components: [{ name: 'rows', type: 'RepeatingPanel', properties: { item_template: 'RowTemplate' } }] }),
            '/app/client_code/RowTemplate/__init__.py': 'from ._anvil_designer import RowTemplateTemplate\nclass RowTemplate(RowTemplateTemplate):\n    def probe(self):\n        self.item.\n',
            '/app/client_code/RowTemplate/form_template.yaml': JSON.stringify({ class_name: 'RowTemplate', container: { type: 'ColumnPanel' }, components: [] }),
        } });
        const complete = async () => (await session.query('textDocument/completion', { textDocument: { uri }, position: { line: 3, character: 18 } })).result.items.map(item => item.label);
        try {
            const panel = await complete();
            await session.updateFiles({
                '/app/client_code/shared.py': 'def people(): return ["Ada"]\n',
                '/app/server_code/api.py': 'from anvil.server import callable\nfrom Main.shared import people as shared_people\n@callable\ndef people(): return shared_people()\n',
            });
            const shared = await complete();
            await session.openDocument('file:///app/client_code/shared.py', 'def people(): return [42]\n');
            const sharedEdit = await complete();
            await session.closeDocument('file:///app/client_code/shared.py');
            const sharedClosed = await complete();
            await session.updateFiles({ '/app/client_code/Home/__init__.py': 'from anvil.server import call\nfrom ..RowTemplate import RowTemplate\nrow = RowTemplate(item=call("people"))\n',
                '/app/server_code/api.py': server('"Ada"') });
            const direct = await complete();
            await session.openDocument('file:///app/server_code/api.py', server('42'));
            return { panel, shared, sharedEdit, sharedClosed, direct, edited: await complete() };
        } finally { session.dispose(); }
    });
    assert(result.panel.includes('upper'));
    assert(result.shared.includes('upper'));
    assert(result.sharedEdit.includes('bit_length') && !result.sharedEdit.includes('upper'));
    assert(result.sharedClosed.includes('upper') && !result.sharedClosed.includes('bit_length'));
    assert(result.direct.includes('upper'));
    assert(result.edited.includes('bit_length') && !result.edited.includes('upper'));
}));


test('generated modules preserve valid app package identities', () => withBrowser(async page => {
    const results = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const results = [];
        for (const packageName of ['Main', '_anvil_form_items', '_anvil_rpc_return_0', '_anvil_js_components']) {
            const source = 'from ._anvil_designer import RowTemplateTemplate\nclass RowTemplate(RowTemplateTemplate):\n    def probe(self):\n        self.item.\n';
            const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
                '/app/anvil.yaml': JSON.stringify({ package_name: packageName }),
                '/app/client_code/main.py': 'from .RowTemplate import RowTemplate\nrow = RowTemplate(item="Ada")\nimport anvil.server\nanvil.server.call("greet").\nfrom .Widget import Widget\nWidget().\n',
                '/app/client_code/RowTemplate/__init__.py': source,
                '/app/client_code/RowTemplate/form_template.yaml': JSON.stringify({ class_name: 'RowTemplate', container: { type: 'ColumnPanel' }, components: [] }),
                '/app/.anvil/js-components.json': JSON.stringify({ components: [{ name: `${packageName}.Widget`, properties: [{ name: 'custom_property' }] }] }),
                '/app/server_code/tasks.py': 'import anvil.server\n@anvil.server.callable\ndef greet():\n    return "Ada"\n',
            } });
            try {
                const complete = async (uri, line, character) => (await session.query('textDocument/completion', {
                    textDocument: { uri }, position: { line, character },
                })).result.items.map(item => item.label);
                results.push({ packageName,
                    item: await complete('file:///app/client_code/RowTemplate/__init__.py', 3, 18),
                    rpc: await complete('file:///app/client_code/main.py', 3, 27),
                    js: await complete('file:///app/client_code/main.py', 5, 9),
                    source: (await session.readSource('file:///app/client_code/RowTemplate/__init__.py')).result.text,
                    original: source,
                });
            } finally { session.dispose(); }
        }
        return results;
    });
    for (const result of results) {
        assert(result.item.includes('upper'), `${result.packageName}: Form item lost its type`);
        assert(result.rpc.includes('upper'), `${result.packageName}: RPC result lost its type`);
        assert(result.js.includes('custom_property'), `${result.packageName}: JS component lost its declaration`);
        assert.equal(result.source, result.original);
    }
}));


test('Form-name completion follows resolved aliases, selected dependencies and current templates', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const uri = 'file:///app/client_code/main.py';
        const source = 'from anvil import open_form as show\nshow(form="")\n';
        const template = name => JSON.stringify({ class_name: name, container: { type: 'ColumnPanel' }, components: [] });
        const files = {
            '/app/anvil.yaml': JSON.stringify({ package_name: 'Main', dependencies: [{ app_id: 'LIB' }] }),
            '/app/client_code/main.py': source,
            '/app/client_code/Home/__init__.py': 'from ._anvil_designer import HomeTemplate\nclass Home(HomeTemplate): pass\n',
            '/app/client_code/Home/form_template.yaml': template('Home'),
            '/app/.anvil/deps/LIB/anvil.yaml': 'package_name: Library\n',
            '/app/.anvil/deps/LIB/client_code/Card/__init__.py': 'from ._anvil_designer import CardTemplate\nclass Card(CardTemplate): pass\n',
            '/app/.anvil/deps/LIB/client_code/Card/form_template.yaml': template('Card'),
        };
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files });
        const complete = async character => (await session.query('textDocument/completion', {
            textDocument: { uri }, position: { line: 1, character },
        })).result.items;
        try {
            const initial = await complete(11);
            await session.updateFiles({
                '/app/anvil.yaml': 'package_name: Main\n',
                '/app/client_code/Home/__init__.py': null,
                '/app/client_code/Home/form_template.yaml': null,
                '/app/client_code/Dashboard/__init__.py': 'from ._anvil_designer import DashboardTemplate\nclass Dashboard(DashboardTemplate): pass\n',
                '/app/client_code/Dashboard/form_template.yaml': template('Dashboard'),
            });
            const changed = await complete(11);
            await session.openDocument(uri, 'def show(form): pass\nshow(form="")\n');
            const unrelated = await complete(11);
            return { initial, changed, unrelated };
        } finally { session.dispose(); }
    });
    assert.deepEqual(result.initial.map(item => item.label).sort(), ['Home', 'Library.Card']);
    assert(result.initial.every(item => item.textEdit.range.start.character === 11 && item.textEdit.range.end.character === 11));
    assert.deepEqual(result.changed.map(item => item.label), ['Dashboard']);
    assert(!result.unrelated.some(item => item.label === 'Dashboard'));
}));


test('secret and key names follow semantic APIs, selected dependencies and live configuration', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const uri = 'file:///app/server_code/main.py';
        const source = 'from anvil.secrets import get_secret as secret\nsecret(secret_name="")\n';
        const config = names => JSON.stringify({ package_name: 'Main', dependencies: [{ app_id: 'LIB' }], secrets: names });
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': config({ 'api_"token': { type: 'secret' }, signing: { type: 'key' } }),
            '/app/server_code/main.py': source,
            '/app/.anvil/deps/LIB/anvil.yaml': JSON.stringify({ package_name: 'Library', secrets: { dep_token: { type: 'secret' }, dep_key: { type: 'key' } } }),
            '/app/.anvil/deps/LIB/client_code/__init__.py': '',
            '/app/.anvil/deps/UNUSED/anvil.yaml': JSON.stringify({ package_name: 'Unused', secrets: { cached_only: { type: 'secret' } } }),
        } });
        const complete = async code => {
            await session.openDocument(uri, code);
            return (await session.query('textDocument/completion', { textDocument: { uri }, position: { line: 1, character: code.split('\n')[1].indexOf('"') + 1 } })).result.items;
        };
        try {
            const names = await complete(source);
            const keys = await complete('from anvil.secrets import encrypt_with_key as encrypt\nencrypt(key_name="", value="hello")\n');
            await session.updateFiles({ '/app/anvil.yaml': config({ rotated: { type: 'secret' } }) });
            const changed = await complete(source);
            const unrelated = await complete('def secret(secret_name): pass\nsecret(secret_name="")\n');
            return { names, keys, changed, unrelated };
        } finally { session.dispose(); }
    });
    assert.deepEqual(result.names.map(item => item.label).sort(), ['api_"token', 'dep_token']);
    assert.equal(result.names.find(item => item.label === 'api_"token').textEdit.newText, 'api_\\"token');
    assert.deepEqual(result.keys.map(item => item.label).sort(), ['dep_key', 'signing']);
    assert.deepEqual(result.changed.map(item => item.label).sort(), ['dep_token', 'rotated']);
    assert(!result.unrelated.some(item => ['dep_token', 'rotated'].includes(item.label)));
}));


test('email handler annotations preserve aliases, author types and original UTF-16 edits', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const uri = 'file:///app/server_code/mail.py';
        const source = 'from anvil.email import handle_message as incoming\n_anvil_email_message = "public"\n@incoming(require_dkim=True)\ndef received(mail): "😀"; copy = mail; copy.subject\n@incoming\ndef explicit(mail: str): mail.upper()\ndef ordinary(mail): mail.subject\n';
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: Main\n', '/app/client_code/__init__.py': '', '/app/server_code/mail.py': source,
        } });
        const query = async (method, line, character, extra = {}) => (await session.query('textDocument/' + method, {
            textDocument: { uri }, position: { line, character }, ...extra,
        })).result;
        try {
            const line = source.split('\n')[3];
            const at = line.indexOf('mail;') + 2;
            const hover = await query('hover', 3, at);
            const rename = await query('rename', 3, at, { newName: 'message' });
            const author = await query('hover', 5, 30);
            const unrelated = await query('hover', 6, 24);
            const original = (await session.readSource(uri)).result.text;
            await session.updateFiles({ '/app/server_code/mail.py': source.replace('@incoming(require_dkim=True)', '# no registration') });
            const removed = await query('hover', 3, at);
            return { hover, rename, author, unrelated, original, source, removed, at };
        } finally { session.dispose(); }
    });
    assert.match(result.hover.contents.value, /Message/);
    assert.match(result.author.contents.value, /str/);
    assert(!result.unrelated?.contents.value.includes('Message'));
    assert(!result.removed?.contents.value.includes('Message'));
    assert.equal(result.original, result.source);
    assert.equal(result.rename.documentChanges.length, 1);
    const edits = result.rename.documentChanges[0].edits;
    assert.equal(edits.length, 2);
    assert(edits.some(edit => edit.range.start.line === 3 && edit.range.start.character === result.at - 2));
}));


test('event kwargs preserve root and union senders, nullable payloads, explicit arguments and unknown extras', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const uri = 'file:///app/client_code/Home/__init__.py';
        const source = [
            'from ._anvil_designer import HomeTemplate',
            'class Home(HomeTemplate):',
            '    def own_method(self): return True',
            '    def root(self, **args): args["sender"].own_method()',
            '    def shared(self, **args): args["sender"].text',
            '    def changed(self, **args):',
            '        if args["file"] is not None: args["file"].get_bytes()',
            '    def explicit(self, sender, **args): args["sender"].missing',
            '    def annotated(self, **args: str): args["sender"].upper()',
            '    def custom(self, **args): args["custom_payload"].anything()',
            '    def invoke(self): self.shared(); self.changed(file=None); self.custom(extra=1)',
            '',
        ].join('\n');
        const template = JSON.stringify({ class_name: 'Home', container: { type: 'ColumnPanel' }, event_bindings: { show: 'root' }, components: [
            { name: 'button', type: 'Button', event_bindings: { click: 'shared' } },
            { name: 'text', type: 'TextBox', event_bindings: { change: 'shared' } },
            { name: 'upload', type: 'FileLoader', event_bindings: { change: 'changed' } },
            { name: 'other', type: 'Button', event_bindings: { show: 'explicit', hide: 'annotated', click: 'custom' } },
        ] });
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: Main\n', '/app/client_code/Home/__init__.py': source,
            '/app/client_code/Home/form_template.yaml': template,
        } });
        const complete = async (line, member) => {
            const lines = source.split('\n');
            const character = lines[line].indexOf('.' + member) + 1;
            lines[line] = lines[line].slice(0, character);
            await session.openDocument(uri, lines.join('\n'));
            try { return (await session.query('textDocument/completion', {
                textDocument: { uri }, position: { line, character },
            })).result.items.map(item => item.label); }
            finally { await session.closeDocument(uri); }
        };
        try {
            const root = await complete(3, 'own_method');
            const shared = await complete(4, 'text');
            const file = await complete(6, 'get_bytes');
            const explicit = await complete(7, 'missing');
            const annotated = await complete(8, 'upper');
            const diagnostics = (await session.query('textDocument/diagnostic', { textDocument: { uri } })).result.items;
            const original = (await session.readSource(uri)).result.text;
            return { root, shared, file, explicit, annotated, diagnostics, original, source };
        } finally { session.dispose(); }
    });
    assert(result.root.includes('own_method'), JSON.stringify({ labels: result.root, diagnostics: result.diagnostics }));
    assert(result.shared.includes('text') && !result.shared.includes('get_bytes'));
    assert(result.file.includes('get_bytes'));
    assert(!result.explicit.includes('text'), 'An explicitly consumed sender is absent from kwargs');
    assert(result.annotated.includes('upper') && !result.annotated.includes('text'));
    assert.deepEqual(result.diagnostics.filter(item => item.severity === 1), []);
    assert.equal(result.original, result.source);
}));


test('open_form keywords use inherited dependency constructors and preserve current Form analysis', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const uri = 'file:///app/client_code/Home/__init__.py';
        const code = call => 'from ._anvil_designer import HomeTemplate\nfrom anvil import open_form as show\nclass Home(HomeTemplate):\n    def __init__(self, *, salutation: str): pass\n    def clicked(self, sender, **args): "😀"; ' + call + '\n';
        const initialSource = code('show("Library.Editor", )');
        const template = name => JSON.stringify({ class_name: name, container: { type: 'ColumnPanel' }, components: name === 'Home'
            ? [{ name: 'button', type: 'Button', event_bindings: { click: 'clicked' } }] : [] });
        const base = title => `class Base:\n    def __init__(self, *, ${title}: str, count: int = 1): pass\n`;
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': JSON.stringify({ package_name: 'Main', dependencies: [{ app_id: 'LIB' }] }),
            '/app/client_code/Home/__init__.py': initialSource,
            '/app/client_code/Home/form_template.yaml': template('Home'),
            '/app/.anvil/deps/LIB/anvil.yaml': 'package_name: Library\n',
            '/app/.anvil/deps/LIB/client_code/base.py': base('title'),
            '/app/.anvil/deps/LIB/client_code/Editor/__init__.py': 'from ..base import Base\nclass Editor(Base): pass\n',
            '/app/.anvil/deps/LIB/client_code/Editor/form_template.yaml': template('Editor'),
        } });
        const complete = async source => {
            await session.openDocument(uri, source);
            const line = source.trimEnd().split('\n').length - 1;
            return (await session.query('textDocument/completion', { textDocument: { uri },
                position: { line, character: source.split('\n')[line].lastIndexOf(')') },
            })).result.items;
        };
        try {
            const initial = await complete(initialSource);
            const self = await complete(code('show("Home", )'));
            const moduleScope = await complete('"""Preview the editor."""\nfrom __future__ import annotations\nfrom anvil import open_form as show\nshow("Library.Editor", )\n');
            const keyword = await complete(code('show(title="hello", form="Library.Editor", )'));
            await session.updateFiles({ '/app/.anvil/deps/LIB/client_code/base.py': base('caption') });
            const changed = await complete(initialSource);
            const original = (await session.readSource(uri)).result.text;
            const definitions = (await session.query('textDocument/definition', { textDocument: { uri }, position: { line: 1, character: 18 } })).result;
            const unrelated = await complete(code('unknown = lambda form, **kwargs: None; unknown("Library.Editor", )'));
            return { initial, self, moduleScope, keyword, changed, original, initialSource, definitions, unrelated };
        } finally { session.dispose(); }
    });
    const labels = items => items.map(item => item.label);
    assert(labels(result.initial).includes('title=') && labels(result.initial).includes('count='));
    assert(labels(result.self).includes('salutation='));
    assert(labels(result.moduleScope).includes('title=') && labels(result.moduleScope).includes('count='));
    assert(!labels(result.initial).includes('form='));
    assert(labels(result.keyword).includes('count=') && !labels(result.keyword).includes('title='));
    assert(labels(result.changed).includes('caption=') && !labels(result.changed).includes('title='));
    assert(!labels(result.unrelated).some(label => ['caption=', 'count='].includes(label)));
    assert(!result.initial.some(item => item.label.startsWith('_anvil_open_form_')));
    assert.equal(result.original, result.initialSource);
    assert(result.definitions.some(target => target.uri.endsWith('/anvil/__init__.pyi')));
}));

test('RPC result methods infer further RPC calls on their first completion', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const code = 'import anvil.server\nanvil.server.call("customer").display().';
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: Main\n',
            '/app/client_code/models.py': 'import anvil.server\nclass Customer:\n    def display(self): return anvil.server.call("label")\n',
            '/app/server_code/api.py': 'from anvil.server import callable\nfrom Main.models import Customer\n@callable\ndef customer(): return Customer()\n@callable\ndef label(): return "Ada"\n',
            '/app/client_code/main.py': code,
        } });
        try {
            const complete = () => session.query('textDocument/completion', {
                textDocument: { uri: 'file:///app/client_code/main.py' }, position: { line: 1, character: code.split('\n')[1].length },
            });
            const first = await complete();
            await session.openDocument('file:///app/server_code/api.py', 'from anvil.server import callable\nfrom Main.models import Customer\n@callable\ndef customer(): return Customer()\n@callable\ndef label(): return 42\n');
            return { first: first.result.items.map(item => item.label), edited: (await complete()).result.items.map(item => item.label) };
        } finally { session.dispose(); }
    });
    assert(result.first.includes('upper') && !result.first.includes('bit_length'));
    assert(result.edited.includes('bit_length') && !result.edited.includes('upper'));
}));

test('handler aliases follow package re-exports and edited source positions', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const uri = 'file:///app/client_code/Home/__init__.py';
        const source = 'from ._anvil_designer import HomeTemplate\nfrom .. import event as bind\nclass Home(HomeTemplate):\n    @bind("button", "click")\n    def clicked(self, sender):\n        sender.';
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: Main\n', '/app/client_code/__init__.py': 'from anvil import handle as event\n',
            '/app/client_code/Home/__init__.py': source,
            '/app/client_code/Home/form_template.yaml': JSON.stringify({ class_name: 'Home', container: { type: 'ColumnPanel' }, components: [{ name: 'button', type: 'Button' }] }),
        } });
        const complete = async code => {
            const lines = code.split('\n');
            const response = await session.query('textDocument/completion', { textDocument: { uri },
                position: { line: lines.length - 1, character: lines.at(-1).length } });
            return response.result.items.map(item => item.label);
        };
        try {
            const initial = await complete(source);
            await session.openDocument('file:///app/client_code/__init__.py', 'def event(*args, **kwargs): return lambda fn: fn\n');
            const rebound = await complete(source);
            const shifted = '# moved down — 😀\n' + source;
            await session.openDocument(uri, shifted);
            await session.closeDocument('file:///app/client_code/__init__.py');
            const restored = await complete(shifted);
            const definition = (await session.query('textDocument/definition', { textDocument: { uri }, position: { line: 6, character: 10 } })).result;
            return { initial, rebound, restored, definition, original: (await session.readSource(uri)).result.text, shifted };
        } finally { session.dispose(); }
    });
    assert(result.initial.includes('text'));
    assert(!result.rebound.includes('text'));
    assert(result.restored.includes('text'));
    assert.equal(result.definition[0].range.start.line, 5);
    assert.equal(result.original, result.shifted);
}));


test('fresh REPL RPC completion follows its own expression and edited producer', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const server = value => `from anvil.server import callable\n@callable\ndef greet(): return ${value}\n`;
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: Main\n',
            '/app/client_code/__init__.py': '',
            '/app/server_code/api.py': server('"Ada"'),
        } });
        const complete = async code => {
            await session.setContext({ kind: 'repl', id: 'console', isServer: false,
                previousCode: 'import anvil.server\n', code });
            return (await session.queryContext('console', 'textDocument/completion', {
                position: { line: 0, character: code.length },
            })).result.items.map(item => item.label);
        };
        try {
            const before = await complete('anvil.server.call("greet").');
            await session.updateFiles({ '/app/server_code/api.py': server('42') });
            const after = await complete('anvil.server.call("greet").');
            const replaced = await complete('"Ada".');
            return { before, after, replaced };
        } finally { session.dispose(); }
    });
    assert(result.before.includes('upper'), JSON.stringify(result.before));
    assert(result.after.includes('bit_length') && !result.after.includes('upper'), JSON.stringify(result.after));
    assert(result.replaced.includes('upper') && !result.replaced.includes('bit_length'), JSON.stringify(result.replaced));
}));
