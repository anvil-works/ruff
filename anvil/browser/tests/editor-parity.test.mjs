import assert from 'node:assert/strict';
import { test } from 'node:test';
import { withBrowser } from './browser.mjs';

async function complete(page, sources) {
    return page.evaluate(async sources => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const uri = 'file:///app/client_code/main.py';
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: Main\n', '/app/client_code/__init__.py': '',
            '/app/client_code/main.py': '', '/app/client_code/library.py': 'choice_imported = 42\n',
        } });
        try {
            const results = [];
            for (const marked of sources) {
                const offset = marked.indexOf('¦');
                const source = marked.replace('¦', '');
                const lines = source.slice(0, offset).split('\n');
                await session.openDocument(uri, source);
                const answer = await session.query('textDocument/completion', { textDocument: { uri },
                    position: { line: lines.length - 1, character: lines.at(-1).length },
                    context: { autoImport: false } });
                results.push(answer.result.items);
            }
            return results;
        } finally { session.dispose(); }
    }, sources);
}

test('event names exclude unrelated variables while handler arguments retain them', () => withBrowser(async page => {
    const prefix = 'from anvil import Button\nbutton = Button()\nlocal_value = 42\n';
    const [events, handlers, partial] = await complete(page, [prefix + 'button.add_event_handler(¦)',
        prefix + 'button.add_event_handler("click", ¦)', prefix + 'button.add_event_handler(cl¦)']);
    assert.deepEqual(events.map(item => item.label).sort(), ['"click"', '"hide"', '"show"']);
    assert(handlers.some(item => item.label === 'local_value'));
    assert.deepEqual(partial.map(item => item.label), ['"click"']);
    assert.equal(partial[0].textEdit.newText, '"click"');
    assert.equal(partial[0].textEdit.range.end.character - partial[0].textEdit.range.start.character, 2);
}));

test('locals rank above module bindings and imports', () => withBrowser(async page => {
    const [items] = await complete(page, ['from .library import choice_imported\nchoice_global = 42\n' +
        'def probe():\n    choice_local = 42\n    choice_¦']);
    const labels = items.map(item => item.label);
    assert(labels.indexOf('choice_local') < labels.indexOf('choice_global'), JSON.stringify(labels));
    assert(labels.indexOf('choice_local') < labels.indexOf('choice_imported'), JSON.stringify(labels));
}));

test('own instance members rank above inherited members and expand from self prefixes', () => withBrowser(async page => {
    const prefix = 'class Base:\n    def inherited_a(self): pass\nclass Child(Base):\n' +
        '    def z_local(self): pass\n    def probe(self):\n        ';
    const [members, expanded] = await complete(page, [prefix + 'self.¦', prefix + 'sel¦']);
    const labels = members.map(item => item.label);
    assert(labels.includes('z_local') && labels.includes('inherited_a'), JSON.stringify(labels));
    assert(labels.indexOf('z_local') < labels.indexOf('inherited_a'), JSON.stringify(labels));
    assert(expanded.some(item => item.label === 'self'));
    assert(expanded.some(item => item.label === 'self.z_local'), JSON.stringify(expanded.map(item => item.label)));
    assert(expanded.some(item => item.label === 'self.inherited_a'));
}));

test('property setter decorators expand from @ and a partial property name', () => withBrowser(async page => {
    const prefix = 'class Other:\n    @property\n    def elsewhere(self): return 0\n' +
        'class Example:\n    @property\n    def foo(self): return 42\n    ';
    const [bare, partial, member] = await complete(page, [prefix + '@¦', prefix + '@f¦', prefix + '@foo.¦']);
    for (const items of [bare, partial]) {
        const setter = items.find(item => item.label === 'foo.setter');
        assert(setter, JSON.stringify(items.map(item => item.label)));
        assert.equal(setter.textEdit.newText, 'foo.setter');
        assert.equal(setter.data.insertParentheses, false);
        assert(!items.some(item => item.label === 'elsewhere.setter'));
    }
    assert.equal(partial.find(item => item.label === 'foo.setter').textEdit.range.start.character, 5);
    assert(member.some(item => item.label === 'setter'));
}));
