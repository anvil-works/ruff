import assert from 'node:assert/strict';
import { test } from 'node:test';
import { readFile } from 'node:fs/promises';
import { withBrowser } from './browser.mjs';

test('client syntax restrictions retain the original compatibility policy without duplicate reports', () => withBrowser(async page => {
    const fixtures = JSON.parse(await readFile(new URL('../../tests/client-syntax.json', import.meta.url), 'utf8'));
    const results = await page.evaluate(async fixtures => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const uri = 'file:///app/client_code/main.py';
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: Main\n', '/app/client_code/main.py': '',
        } });
        try {
            const results = [];
            for (const fixture of fixtures) {
                await session.openDocument(uri, fixture.source);
                results.push((await session.query('textDocument/diagnostic', { textDocument: { uri } })).result.items);
            }
            return results;
        } finally { session.dispose(); }
    }, fixtures);
    for (const [index, fixture] of fixtures.entries()) {
        const syntax = results[index].filter(item => ['invalid-syntax', 'reportAnvilUnsupportedSkulptSyntax'].includes(item.code));
        assert.deepEqual(syntax.map(item => item.range.start.line).sort((a, b) => a - b), fixture.lines, fixture.name);
    }
}));

test('client compatibility diagnostics reject async and debug f-strings without restricting server code', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const source = 'async def fetch():\n    return 42\nvalue = 42\ntext = f"{value=}"\n';
        const client = 'file:///app/client_code/main.py';
        const server = 'file:///app/server_code/main.py';
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: Main\n',
            '/app/client_code/main.py': source, '/app/server_code/main.py': source,
        } });
        const diagnostics = async uri => (await session.query('textDocument/diagnostic', { textDocument: { uri } })).result.items;
        try {
            const clientIssues = await diagnostics(client);
            const serverIssues = await diagnostics(server);
            await session.openDocument(client, 'value = 42\ntext = f"{value}"\n');
            return { clientIssues, serverIssues, corrected: await diagnostics(client),
                serverSource: (await session.readSource(server)).result.text, source };
        } finally { session.dispose(); }
    });
    const unsupported = result.clientIssues.filter(item => item.code === 'reportAnvilUnsupportedSkulptSyntax');
    assert.deepEqual(unsupported.map(item => item.range.start.line), [0, 3]);
    assert(unsupported.every(item => item.source === 'anvil' && item.severity === 2));
    assert(!result.serverIssues.some(item => item.code === 'reportAnvilUnsupportedSkulptSyntax'));
    assert.deepEqual(result.corrected, []);
    assert.equal(result.serverSource, result.source);
}));

test('show-handler navigation warnings follow YAML and resolved handle decorators', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const uri = 'file:///app/client_code/Home/__init__.py';
        const source = 'from anvil import open_form as navigate, handle as on\nfrom ._anvil_designer import WelcomeTemplate\n' +
            'class Welcome(WelcomeTemplate):\n    def from_yaml(self, **event_args):\n        navigate("Home")\n' +
            '    @on("", "show")\n    def decorated(self, **event_args):\n        navigate("Home")\n' +
            '    def overridden(self, **event_args):\n        navigate("Home")\n' +
            '    def slotted(self, **event_args):\n        navigate("Home")\n' +
            '    def click(self, **event_args):\n        navigate("Home")\n' +
            'class Other:\n    def from_yaml(self):\n        navigate("Home")\n';
        const template = 'class_name: pkg.Welcome\ncontainer:\n  type: ColumnPanel\n  event_bindings: {show: overridden}\n' +
            '  components:\n  - {name: label, type: Label, event_bindings: {show: from_yaml}}\n' +
            'components_by_slot:\n  body:\n  - {name: slot_label, type: Label, event_bindings: {show: slotted}}\n';
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: Main\n', '/app/client_code/Home/__init__.py': source,
            '/app/client_code/Home/form_template.yaml': template,
        } });
        const diagnostics = async () => (await session.query('textDocument/diagnostic', { textDocument: { uri } })).result.items;
        try {
            const before = await diagnostics();
            await session.updateFiles({ '/app/client_code/Home/form_template.yaml': 'class_name: pkg.Welcome\ncontainer:\n  type: ColumnPanel\ncomponents: []\n' });
            return { before, after: await diagnostics() };
        } finally { session.dispose(); }
    });
    const warnings = items => items.filter(item => item.code === 'reportAnvilOpenFormInShow');
    assert.deepEqual(warnings(result.before).map(item => item.range.start.line), [4, 7, 11]);
    assert.deepEqual(warnings(result.after).map(item => item.range.start.line), [7]);
}));

test('duplicate callable and task warnings follow project registrations after edits', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const prefix = 'from anvil.server import callable as expose, background_task as task\n';
        const first = prefix + '@expose("shared")\ndef first(): pass\n@task("nightly")\ndef first_task(): pass\n';
        const second = prefix + '@expose("shared")\ndef second(): pass\n@task("nightly")\ndef second_task(): pass\n';
        const uri = 'file:///app/server_code/first.py';
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: Main\n', '/app/server_code/first.py': first, '/app/server_code/second.py': second,
            '/app/client_code/__init__.py': '',
            '/app/client_code/shared.py': prefix + '@expose("shared")\ndef shared(): pass\n@task("nightly")\ndef shared_task(): pass\n',
            '/app/server_code/unused.py': prefix + 'def factory():\n    @expose("shared")\n    def inner(): pass\n    return inner\n',
        } });
        const diagnostics = async () => (await session.query('textDocument/diagnostic', { textDocument: { uri } })).result.items;
        try {
            const before = await diagnostics();
            await session.updateFiles({ '/app/server_code/second.py': second.replace('"shared"', '"other"').replace('"nightly"', '"morning"') });
            return { before, after: await diagnostics() };
        } finally { session.dispose(); }
    });
    assert.deepEqual(result.before.map(item => item.code), ['reportAnvilDuplicateCallable', 'reportAnvilDuplicateBackgroundTask']);
    assert(result.before.every(item => item.severity === 2));
    assert.match(result.before[0].message, /shared/);
    assert.match(result.before[1].message, /nightly/);
    assert.deepEqual(result.after, []);
}));

test('portable class placement follows the resolved decorator and original item kind', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const source = 'from anvil.server import portable_class as portable\n@portable\nclass Example:\n    pass\n';
        const files = {
            '/app/anvil.yaml': 'package_name: Main\n',
            '/app/client_code/main.py': source,
            '/app/server_code/main.py': source,
            '/app/client_code/Home/__init__.py': source.replace('Example', 'Home'),
            '/app/client_code/Home/form_template.yaml': 'container:\n  type: ColumnPanel\ncomponents: []\n',
            '/app/server_code/ordinary.py': 'def portable(cls): return cls\n@portable\nclass Example:\n    pass\n',
        };
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files });
        try {
            const results = {};
            for (const path of Object.keys(files).filter(path => path.endsWith('.py')))
                results[path] = (await session.query('textDocument/diagnostic', { textDocument: { uri: 'file://' + path } })).result.items;
            return results;
        } finally { session.dispose(); }
    });
    for (const path of ['/app/server_code/main.py', '/app/client_code/Home/__init__.py']) {
        const issues = result[path].filter(item => item.code === 'reportAnvilPortableClassPlacement');
        assert.equal(issues.length, 1, JSON.stringify(result[path]));
        assert.equal(issues[0].range.start.line, 1);
        assert.equal(issues[0].severity, 2);
    }
    assert.deepEqual(result['/app/client_code/main.py'], []);
    assert.deepEqual(result['/app/server_code/ordinary.py'], []);
}));

test('row model options reject unknown keywords and accept supported options in both runtimes', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': JSON.stringify({ package_name: 'Main', db_schema: { people: { columns: [{ name: 'name', type: 'string' }] } } }),
            '/app/client_code/models.py': '', '/app/server_code/models.py': '',
        } });
        const results = [];
        try {
            for (const directory of ['client_code', 'server_code']) {
                const uri = `file:///app/${directory}/models.py`;
                const source = 'from anvil.tables import app_tables\nclass Person(app_tables.people.Row, attr=True, client_writable=True, surprise=True):\n    pass\n';
                await session.openDocument(uri, source);
                const invalid = (await session.query('textDocument/diagnostic', { textDocument: { uri } })).result.items;
                await session.openDocument(uri, source.replace('attr=True, client_writable=True, surprise=True', 'attrs=True, client_writable=True, metaclass=type'));
                const corrected = (await session.query('textDocument/diagnostic', { textDocument: { uri } })).result.items;
                results.push({ invalid, corrected });
            }
            return results;
        } finally { session.dispose(); }
    });
    for (const { invalid, corrected } of result) {
        assert.deepEqual(invalid.map(item => item.code), ['unknown-argument', 'unknown-argument']);
        assert.match(invalid[0].message, /attr/);
        assert.match(invalid[1].message, /surprise/);
        assert.deepEqual(corrected, []);
    }
}));
