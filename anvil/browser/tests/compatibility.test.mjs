import assert from 'node:assert/strict';
import { test } from 'node:test';
import { withBrowser } from './browser.mjs';

test('bulk table deletion stays documented but out of suggestions without hiding user methods #7554', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const uri = 'file:///app/client_code/main.py';
        const base = 'from anvil.tables import app_tables\nclass Other:\n    def delete_all_rows(self): return "user"\ntable = app_tables.people\nresults = table.search()\nother = Other()\n';
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': JSON.stringify({ package_name: 'Main', db_schema: { people: { columns: [{ name: 'name', type: 'string' }] } } }),
            '/app/client_code/main.py': base,
        } });
        const complete = async expression => {
            await session.openDocument(uri, base + expression);
            return (await session.query('textDocument/completion', { textDocument: { uri },
                position: { line: 6, character: expression.length } })).result.items.map(item => item.label);
        };
        try {
            const table = await complete('table.');
            const results = await complete('results.');
            const call = await complete('app_tables.people.search().');
            const other = await complete('other.');
            const typed = base + 'results.delete_all_rows()\n';
            await session.openDocument(uri, typed);
            const hover = (await session.query('textDocument/hover', { textDocument: { uri }, position: { line: 6, character: 12 } })).result;
            const diagnostics = (await session.query('textDocument/diagnostic', { textDocument: { uri } })).result.items;
            const original = (await session.readSource(uri)).result.text;
            return { table, results, call, other, hover, diagnostics, original, typed };
        } finally { session.dispose(); }
    });
    for (const labels of [result.table, result.results, result.call]) {
        assert(labels.includes('to_csv'));
        assert(!labels.includes('delete_all_rows'));
    }
    assert(result.other.includes('delete_all_rows'));
    assert.match(result.hover.contents.value, /Delete all rows/);
    assert.deepEqual(result.diagnostics.filter(item => item.severity === 1), []);
    assert.equal(result.original, result.typed);
}));

test('inferred event-name types survive authored builtin shadowing without modifying source', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const uri = 'file:///app/client_code/Home/__init__.py';
        const source = 'from ._anvil_designer import HomeTemplate\nstr = "label"\nclass Home(HomeTemplate):\n    def clicked(self, event_name, **args):\n        event_name.upper()\n        args["event_name"].upper()\n';
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: Main\n', '/app/client_code/Home/__init__.py': source,
            '/app/client_code/Home/form_template.yaml': JSON.stringify({ class_name: 'Home', container: { type: 'ColumnPanel' },
                components: [{ name: 'button', type: 'Button', event_bindings: { click: 'clicked' } }] }),
        } });
        try {
            const diagnostics = (await session.query('textDocument/diagnostic', { textDocument: { uri } })).result.items;
            const hover = (await session.query('textDocument/hover', { textDocument: { uri }, position: { line: 4, character: 12 } })).result;
            return { diagnostics, hover, original: (await session.readSource(uri)).result.text, source };
        } finally { session.dispose(); }
    });
    assert.deepEqual(result.diagnostics.filter(item => item.severity === 1), []);
    assert.match(result.hover.contents.value, /str/);
    assert.equal(result.original, result.source);
}));

test('columns containing spaces complete as row keys and never invalid keyword arguments #913', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const uri = 'file:///app/client_code/main.py';
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': JSON.stringify({ package_name: 'Main', db_schema: { people: { columns: [
                { name: 'name', type: 'string' }, { name: 'first name', type: 'string' },
            ] } } }), '/app/client_code/main.py': '',
        } });
        const complete = async expression => {
            await session.openDocument(uri, 'from anvil.tables import app_tables\n' + expression.replace('¦', ''));
            return (await session.query('textDocument/completion', { textDocument: { uri },
                position: { line: 1, character: expression.indexOf('¦') } })).result.items.map(item => item.label);
        };
        try {
            const expression = 'app_tables.people.search(¦)';
            await session.openDocument(uri, 'from anvil.tables import app_tables\n' + expression.replace('¦', ''));
            const keywords = (await session.query('textDocument/completion', { textDocument: { uri }, position: { line: 1, character: expression.indexOf('¦') } })).result.items.map(item => item.label);
            return { keywords, keys: await complete('app_tables.people.search()[0]["¦') };
        } finally { session.dispose(); }
    });
    assert(result.keywords.includes('name='));
    assert(!result.keywords.includes('first name='));
    assert(result.keys.includes('first name'));
}));

test('table Row return annotations retain keys for calls and models without matching unrelated types #4076', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const uri = 'file:///app/client_code/main.py';
        const base = 'from anvil.tables import app_tables\nclass Person(app_tables.people.Row, attrs=True):\n    def display_name(self): return self.name\ndef lookup(name: str = "Ada") -> app_tables.people.Row:\n    row = app_tables.people.get(name=name)\n    assert row is not None\n    return row\ndef model() -> Person:\n    row = app_tables.people.get()\n    assert row is not None\n    return row\ndef text() -> str: return "Ada"\nclass _Row_people: pass\ndef unrelated() -> _Row_people: return _Row_people()\n';
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': JSON.stringify({ package_name: 'Main', db_schema: { people: { columns: [
                { name: 'name', type: 'string' }, { name: 'first name', type: 'string' },
            ] } } }), '/app/client_code/main.py': base,
        } });
        const complete = async marked => {
            const offset = marked.indexOf('¦');
            const code = base + marked.replace('¦', '');
            await session.openDocument(uri, code);
            const items = (await session.query('textDocument/completion', { textDocument: { uri },
                position: { line: 14, character: offset } })).result.items;
            return { items, code, original: (await session.readSource(uri)).result.text };
        };
        try { return { raw: await complete('lookup()["¦"]'), model: await complete('model()["¦"]'),
            empty: await complete('model()[¦]'),
            partial: await complete('"😀"; lookup("Ada")["fi¦"]'), value: await complete('lookup()["name"].¦'),
            text: await complete('text()["¦"]'), unrelated: await complete('unrelated()["¦"]') }; }
        finally { session.dispose(); }
    });
    for (const value of [result.raw, result.model])
        assert(['name', 'first name'].every(name => value.items.some(item => item.label === name)));
    assert.deepEqual(result.empty.items.map(item => item.label).sort(), ['"first name"', '"name"']);
    assert.deepEqual(result.empty.items.find(item => item.label === '"name"').textEdit, {
        range: { start: { line: 14, character: 8 }, end: { line: 14, character: 8 } }, newText: '"name"',
    });
    assert.deepEqual(result.partial.items.map(item => item.label), ['first name']);
    assert.equal(result.partial.items[0].textEdit.range.start.character, '"😀"; lookup("Ada")["'.length);
    assert(result.value.items.some(item => item.label === 'upper'));
    for (const value of [result.text, result.unrelated])
        assert(!value.items.some(item => ['name', 'first name'].includes(item.label)));
    for (const value of Object.values(result)) assert.equal(value.original, value.code);
}));

test('DatePicker dates expose date members and retain optionality #2049', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const uri = 'file:///app/client_code/main.py';
        const base = 'import anvil\nimport datetime\npicker = anvil.DatePicker()\npicker.date = "2026-10-21"\npicker.date = datetime.datetime.now()\nvalue = picker.date\nif value is not None:\n    value.';
        const session = new BrowserAnalysisSession({workerUrl:'/worker.mjs',rootUri:'file:///app',files:{'/app/anvil.yaml':'package_name: Main\n','/app/client_code/main.py':base}});
        try {
            const items = (await session.query('textDocument/completion', {textDocument:{uri},position:{line:7,character:10}})).result.items;
            await session.changeDocument(uri, base.replace('    value.', '    value.isoformat()\n'));
            const diagnostics = (await session.query('textDocument/diagnostic',{textDocument:{uri}})).result.items;
            const hover = (await session.query('textDocument/hover',{textDocument:{uri},position:{line:5,character:3}})).result;
            return {items,diagnostics,hover};
        } finally {session.dispose();}
    });
    for(const name of ['isoformat','year']) assert(result.items.some(item=>item.label===name));
    assert.match(result.hover.contents.value,/date.*None|None.*date/s);
    assert.deepEqual(result.diagnostics.filter(item=>item.severity===1),[]);
}));

test('generated read-only sources are stable before semantic queries', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
    const { BrowserAnalysisSession } = await import('/session.mjs');
    const row = 'from ._anvil_designer import RowTemplateTemplate\nclass RowTemplate(RowTemplateTemplate): pass\n';
    const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
        '/app/anvil.yaml': JSON.stringify({ package_name: 'Main' }),
        '/app/client_code/Home/__init__.py': 'from ._anvil_designer import HomeTemplate\nclass Home(HomeTemplate):\n    def __init__(self):\n        self.rows.items = [{"name": "Ada"}]\n',
        '/app/client_code/Home/form_template.yaml': JSON.stringify({ class_name: 'Home', container: { type: 'ColumnPanel' }, components: [
            { name: 'rows', type: 'RepeatingPanel', properties: { item_template: 'RowTemplate' } },
        ] }),
        '/app/client_code/RowTemplate/__init__.py': row,
        '/app/client_code/RowTemplate/form_template.yaml': JSON.stringify({ class_name: 'RowTemplate', container: { type: 'ColumnPanel' }, components: [] }),
    } });
    try {
        const uri = 'file:///app/.anvil/analysis/client/Main/RowTemplate/_anvil_designer.pyi';
        const before = await session.readSource(uri);
        const hover = await session.query('textDocument/hover', { textDocument: { uri }, position: { line: 4, character: 6 } });
        const after = await session.readSource(uri);
        return { before, hover, after, same: before.result.text === after.result.text };
    } finally { session.dispose(); }
    });
    assert.equal(result.before.result.text, result.after.result.text);
    assert.match(result.before.result.text, /_anvil_form_items/);
}));
