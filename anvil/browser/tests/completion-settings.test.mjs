import assert from 'node:assert/strict';
import { test } from 'node:test';
import { readFile } from 'node:fs/promises';
import { withBrowser } from './browser.mjs';

test('builtin reference classification preserves shadowing and project overrides', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const ty = await import('/dist/wasm/ty_wasm.js');
        await ty.default();
        const workspace = new ty.Workspace('/app', ty.PositionEncoding.Utf16, {});
        const cases = [
            ['¦str(1)', true],
            ['¦missing(1)', false],
            ['import builtins\nbuiltins.¦str(1)', false],
            ['from .api import str\n¦str("greet")', false],
            ['from .api import *\n¦str("greet")', false],
            ['if True:\n    from .api import *\n¦str("greet")', false],
            ['str = remote\n¦str("greet")', false],
            ['def f(str):\n    ¦str("greet")', false],
        ];
        const api = workspace.openFile('/app/api.py', 'def str(name): return 42\n');
        try {
            const actual = cases.map(([marked]) => {
                const offset = marked.indexOf('¦');
                const code = marked.replace('¦', '');
                const source = workspace.openFile('/app/main.py', code);
                const lines = code.slice(0, offset).split('\n');
                try {
                    return workspace.isBuiltinReference(source, new ty.Position(lines.length, lines.at(-1).length + 1));
                } finally { workspace.closeFile(source); }
            });
            const custom = new ty.Workspace('/custom', ty.PositionEncoding.Utf16, {});
            const override = custom.openFile('/custom/__builtins__.pyi', 'def str(name: str) -> int: ...\n');
            const source = custom.openFile('/custom/main.py', 'str("greet")');
            try {
                return { actual, expected: cases.map(([, expected]) => expected),
                    overridden: custom.isBuiltinReference(source, new ty.Position(1, 1)) };
            } finally { source.free(); override.free(); custom.free(); }
        } finally { api.free(); workspace.free(); }
    });
    assert.deepEqual(result.actual, result.expected);
    assert.equal(result.overridden, false);
}));

test('matching scoped names retain their types and builtin precedence', () => withBrowser(async page => {
    const results = await page.evaluate(async () => {
        const ty = await import('/dist/wasm/ty_wasm.js');
        await ty.default();
        const results = [];
        for (const customBuiltins of [false, true]) {
            for (const prefix of ['str', 'Ex', '__file__', 'val']) {
                const workspace = new ty.Workspace('/app', ty.PositionEncoding.Utf16, {});
                const override = customBuiltins ? workspace.openFile('/app/__builtins__.pyi', 'str: int\n') : undefined;
                const source = workspace.openFile('/app/main.py', `value = 42\nvalue_text = "Ada"\n${prefix}`);
                const read = column => workspace.completions(source, new ty.Position(3, column), false).map(item => {
                    try { return { name: item.name, kind: item.kind, detail: item.detail }; }
                    finally { item.free(); }
                });
                try {
                    // Resolve the matching subset first, then compare with an unfiltered
                    // query at the start of the same expression in the same scope.
                    const matching = read(prefix.length + 1);
                    const all = read(1);
                    results.push({ prefix, customBuiltins, matching, all });
                } finally { source.free(); override?.free(); workspace.free(); }
            }
        }
        return results;
    });
    const byName = (a, b) => a.name.localeCompare(b.name);
    for (const { prefix, customBuiltins, matching, all } of results) {
        const pattern = new RegExp([...prefix].join('.*'), 'i');
        const expected = all.filter(item => pattern.test(item.name));
        assert(expected.length, `${prefix} needs a matching suggestion`);
        assert.deepEqual(matching.sort(byName), expected.sort(byName));
        if (prefix === 'str' && customBuiltins) assert.equal(matching.find(item => item.name === 'str').detail, 'int');
        if (prefix === '__file__') assert.equal(matching.find(item => item.name === '__file__').detail, 'str');
    }
}));

test('auto-import search is optional while locals and existing API calls keep working', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const ty = await import('/dist/wasm/ty_wasm.js');
        await ty.default();
        const workspace = new ty.Workspace('/app', ty.PositionEncoding.Utf16, {});
        const source = workspace.openFile('/app/main.py', 'contact = "Ada"\ncont');
        const other = workspace.openFile('/app/other.py', 'class Contact: pass\n');
        const labels = autoImport => {
            const position = new ty.Position(2, 5);
            return workspace.completions(source, position, autoImport).map(item => {
                try { return item.name; } finally { item.free(); }
            });
        };
        try {
            return { local: labels(false), defaults: labels(undefined), imports: labels(true) };
        } finally { source.free(); other.free(); workspace.free(); }
    });
    assert(result.local.includes('contact'));
    assert(!result.local.includes('Contact'), 'Fast completion must not search unimported symbols');
    assert(result.defaults.includes('Contact'), 'Existing two-argument API keeps auto-imports');
    assert(result.imports.includes('Contact'));
}));


test('incremental index preparation preserves source and follows subsequent symbol edits', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const ty = await import('/dist/wasm/ty_wasm.js');
        await ty.default();
        const workspace = new ty.Workspace('/app', ty.PositionEncoding.Utf16, {});
        const code = 'Rock';
        const source = workspace.openFile('/app/main.py', code);
        let other = workspace.openFile('/app/other.py', 'class Rocket: pass\n');
        const labels = () => workspace.completions(source, new ty.Position(1, 5)).map(item => {
            try { return item.name; } finally { item.free(); }
        });
        try {
            let offset = 0;
            const first = workspace.prepareCompletionIndex(source, offset, 1);
            if (!(first > offset)) throw new Error('The first bounded batch must leave further work');
            offset = first;
            let batches = 1;
            for (;;) {
                const next = workspace.prepareCompletionIndex(source, offset, 8);
                batches++;
                if (next === undefined) break;
                if (!(next > offset && next - offset <= 8)) throw new Error('Index batches must advance within their limit');
                offset = next;
            }
            const prepared = labels();
            workspace.closeFile(other);
            other = workspace.openFile('/app/other.py', 'class RocketShip: pass\n');
            return { batches, prepared, changed: labels(), source: workspace.sourceText(source) };
        } finally { source.free(); other.free(); workspace.free(); }
    });
    assert(result.batches > 1);
    assert(result.prepared.includes('Rocket'));
    assert(!result.changed.includes('Rocket'));
    assert(result.changed.includes('RocketShip'));
    assert.equal(result.source, 'Rock');
}));

test('worker completion can return in-scope suggestions without auto-import search', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/main.py': 'RocketLocal = 42\nRock', '/app/other.py': 'class Rocket: pass\n',
        } });
        try {
            const params = { textDocument: { uri: 'file:///app/main.py' }, position: { line: 1, character: 4 } };
            const ordinary = await session.query('textDocument/completion', { ...params, context: { autoImport: false } });
            const defaults = await session.query('textDocument/completion', params);
            return { ordinary: ordinary.result.items, defaults: defaults.result.items };
        } finally { session.dispose(); }
    });
    assert(result.ordinary.some(item => item.label === 'RocketLocal'));
    assert(!result.ordinary.some(item => item.label === 'Rocket'));
    assert(result.defaults.some(item => item.label === 'Rocket' && item.additionalTextEdits?.length));
}));

test('delayed completion returns imports without repeating ordinary suggestions', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/main.py': 'RocketLocal = 42\nRock', '/app/other.py': 'class Rocket: pass\n',
        } });
        try {
            const params = { textDocument: { uri: 'file:///app/main.py' },
                position: { line: 1, character: 4 }, context: { autoImport: 'only' } };
            const cold = (await session.query('textDocument/completion', params)).result;
            if (!cold.preparationRequired || cold.items.length) throw new Error('Delayed imports must not run a cold search');
            for (let step = 0; step < 1000; step++) {
                if ((await session.query('anvil/prepareCompletion', { textDocument: params.textDocument })).result.complete)
                    return (await session.query('textDocument/completion', params)).result.items;
            }
            throw new Error('Completion preparation did not finish');
        } finally { session.dispose(); }
    });
    assert(result.some(item => item.label === 'Rocket' && item.additionalTextEdits?.length));
    assert(!result.some(item => item.label === 'RocketLocal'));
    assert(result.every(item => item.additionalTextEdits?.length));
}));

test('completion preparation preserves edited types and discovers newly added exports', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const uri = 'file:///app/main.py';
        const source = 'RocketLocal = 42\nRock';
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/main.py': source, '/app/other.py': 'class Rocket: pass\n',
        } });
        const prepare = async () => {
            for (let step = 0; step < 1000; step++) {
                if ((await session.query('anvil/prepareCompletion', { textDocument: { uri } })).result.complete) return;
            }
            throw new Error('Completion preparation did not finish');
        };
        const complete = () => session.query('textDocument/completion', { textDocument: { uri },
            position: { line: 1, character: 4 }, context: { autoImport: 'only' } });
        try {
            await prepare();
            await session.changeDocument(uri, source.replace('42', '"Ada"'));
            const retained = (await session.query('anvil/prepareCompletion', { textDocument: { uri } })).result.complete;
            const initial = await complete();
            await session.updateFiles({ '/app/other.py': 'class RocketRenamed: pass\n',
                '/app/new_package/__init__.py': 'class RocketNew: pass\n' });
            await prepare();
            const changed = await complete();
            return { retained, initial: initial.result.items, changed: changed.result.items,
                source: (await session.readSource(uri)).result.text };
        } finally { session.dispose(); }
    });
    assert(result.retained, 'Ordinary content edits must retain completed preparation');
    assert(result.initial.some(item => item.label === 'Rocket'));
    assert(!result.changed.some(item => item.label === 'Rocket'));
    assert(result.changed.some(item => item.label === 'RocketRenamed'));
    assert(result.changed.some(item => item.label === 'RocketNew'));
    assert.equal(result.source, 'RocketLocal = "Ada"\nRock');
}));

test('REPL completion preparation needs no cursor position and preserves history locals', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/main.py': '', '/app/other.py': 'class Rocket: pass\n',
        } });
        try {
            await session.setContext({ kind: 'repl', id: 'console', isServer: false,
                previousCode: 'RocketLocal = 42\n', code: 'Rock' });
            for (let step = 0; step < 1000; step++) {
                if ((await session.queryContext('console', 'anvil/prepareCompletion', {})).result.complete) {
                    return (await session.queryContext('console', 'textDocument/completion', {
                        position: { line: 0, character: 4 }, context: { autoImport: false },
                    })).result.items;
                }
            }
            throw new Error('Context preparation did not finish');
        } finally { session.dispose(); }
    });
    assert(result.some(item => item.label === 'RocketLocal'));
    assert(!result.some(item => item.label === 'Rocket'));
}));


test('ordinary completion and import diagnostics never start hidden auto-import searches', () => withBrowser(async page => {
    const wasm = await readFile(new URL('../dist/wasm/ty_wasm.js', import.meta.url), 'utf8');
    await page.route('**/dist/wasm/ty_wasm.js', route => route.fulfill({ contentType: 'text/javascript', body: wasm + `
const ordinaryCompletions = Workspace.prototype.completions;
Workspace.prototype.completions = function(file, position, autoImport) {
    if (autoImport !== false) throw new Error('Ordinary request enabled native auto-import search');
    return ordinaryCompletions.call(this, file, position, autoImport);
};` }));
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const uri = 'file:///app/client_code/main.py';
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: Main\n', '/app/client_code/__init__.py': '', '/app/client_code/main.py': '',
            '/app/client_code/Editor/__init__.py': 'from ._anvil_designer import EditorTemplate\nclass Editor(EditorTemplate):\n    def __init__(self, *, title: str): pass\n',
            '/app/client_code/Editor/form_template.yaml': 'container: {type: ColumnPanel}\ncomponents: []\n',
            '/app/server_code/api.py': 'import anvil.server\n@anvil.server.callable\ndef greet(name: str) -> str: return name\n',
        } });
        const complete = async source => {
            await session.openDocument(uri, source);
            const lines = source.split('\n');
            return (await session.query('textDocument/completion', { textDocument: { uri },
                position: { line: lines.length - 1, character: lines.at(-1).lastIndexOf(')') },
                context: { autoImport: false } })).result.items.map(item => item.label);
        };
        try {
            const form = await complete('from anvil import open_form\nopen_form("Editor", tit)');
            const rpc = await complete('import anvil.server\nanvil.server.call("greet", na)');
            await session.openDocument(uri, 'from collections import abc\n');
            await session.query('textDocument/diagnostic', { textDocument: { uri } });
            return { form, rpc };
        } finally { session.dispose(); }
    });
    assert(result.form.includes('title='));
    assert(result.rpc.includes('name='));
}));

test('auto-imports exclude generated Form declarations and checker helpers but retain app and library symbols', () => withBrowser(async page => {
    const results = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const uri = 'file:///app/client_code/main.py';
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: Main\n', '/app/client_code/__init__.py': '', '/app/client_code/main.py': '',
            '/app/client_code/Editor/__init__.py': 'from ._anvil_designer import EditorTemplate\nclass Editor(EditorTemplate): pass\n',
            '/app/client_code/Editor/form_template.yaml': 'container: {type: ColumnPanel}\ncomponents: []\n',
            '/app/client_code/domain.py': 'class LaxDecimalPrice: pass\n', '/app/server_code/main.py': '',
        } });
        try {
            const answers = [];
            for (const prefix of ['anvil_designer', 'EditorTemp', 'LaxDec']) {
                await session.openDocument(uri, prefix);
                answers.push((await session.query('textDocument/completion', { textDocument: { uri },
                    position: { line: 0, character: prefix.length } })).result.items);
            }
            const server = 'file:///app/server_code/main.py';
            await session.openDocument(server, 'Decim');
            answers.push((await session.query('textDocument/completion', { textDocument: { uri: server },
                position: { line: 0, character: 5 } })).result.items);
            const code = 'from .Editor._anvil_designer import EditorTemp';
            await session.changeDocument(uri, code);
            const explicit = (await session.query('textDocument/completion', { textDocument: { uri },
                position: { line: 0, character: code.length }, context: { autoImport: false } })).result.items;
            return { answers, explicit };
        } finally { session.dispose(); }
    });
    const imports = results.answers.flat().filter(item => item.additionalTextEdits?.length);
    assert(imports.some(item => item.label === 'LaxDecimalPrice'), 'Public app type should remain importable');
    assert(imports.some(item => item.label === 'Decimal' && item.labelDetails?.description === 'decimal'),
        'Server standard-library types should remain importable');
    assert(!imports.some(item => /(?:^|\.)_anvil_designer(?:\.|$)/.test(item.labelDetails?.description ?? item.label)),
        JSON.stringify(imports.map(item => [item.label, item.labelDetails])));
    assert(!imports.some(item => item.labelDetails?.description?.startsWith('ty_extensions')),
        JSON.stringify(imports.map(item => [item.label, item.labelDetails])));
    assert(results.explicit.some(item => item.label === 'EditorTemplate'));
}));
