import assert from 'node:assert/strict';
import { test } from 'node:test';
import { readFile } from 'node:fs/promises';
import { withBrowser } from './browser.mjs';

test('member completion uses the receiver at the cursor, including inside an existing name', () => withBrowser(async page => {
    const cases = await page.evaluate(async () => {
        const ty = await import('/dist/wasm/ty_wasm.js');
        await ty.default();
        const workspace = new ty.Workspace('/app', ty.PositionEncoding.Utf16, {});
        const packageFile = workspace.openFile('/app/tools/__init__.py', 'def confirm(): pass\n');
        const api = workspace.openFile('/app/tools/api.py', 'def call() -> str: return "result"\ndef cancel(): pass\n');
        try {
            return [
                ['import tools.api\ntools.api.c¦all()', 'call', 'confirm'],
                ['import tools.api as library\nlibrary.c¦all()', 'call', 'confirm'],
                ['import tools.api\ntools.api.¦call()', 'call', 'confirm'],
                ['import tools.api\ntools.api.¦ call()', 'call', 'confirm'],
                ['import tools.api\ntools.api.c¦all().capitalize()', 'call', 'capitalize'],
                ['import tools.api\ntools.api¦.call()', 'api', 'call'],
                ['import tools.api\n(tools.api).c¦all()', 'call', 'confirm'],
                ['import tools.api\ntools.api.call().up¦per()', 'upper', 'call'],
                ['import tools.api\ntools.api.¦.call()', 'call', 'confirm'],
            ].map(([marked, included, excluded]) => {
                const offset = marked.indexOf('¦');
                const code = marked.replace('¦', '');
                const lines = code.slice(0, offset).split('\n');
                const source = workspace.openFile('/app/main.py', code);
                try {
                    const labels = workspace.completions(source, new ty.Position(lines.length, lines.at(-1).length + 1), false)
                        .map(item => { try { return item.name; } finally { item.free(); } });
                    return { marked, included, excluded, labels };
                } finally { workspace.closeFile(source); }
            });
        } finally { api.free(); packageFile.free(); workspace.free(); }
    });
    for (const { marked, included, excluded, labels } of cases) {
        assert(labels.includes(included), `${marked}: missing ${included}: ${labels.join(', ')}`);
        assert(!labels.includes(excluded), `${marked}: unexpected ${excluded}`);
    }
}));

test('completion exposes native typing-only metadata without hiding explicit type references', () => withBrowser(async page => {
    const items = await page.evaluate(async () => {
        const ty = await import('/dist/wasm/ty_wasm.js');
        await ty.default();
        const workspace = new ty.Workspace('/app', ty.PositionEncoding.Utf16, {});
        const helper = workspace.openFile('/app/helpers.pyi', 'from typing import TYPE_CHECKING, type_check_only\n@type_check_only\nclass Helper: ...\nif TYPE_CHECKING:\n    Alias = str | int\nclass Runtime: ...\n');
        const source = workspace.openFile('/app/main.py', 'import helpers\nhelpers.');
        try {
            return workspace.completions(source, new ty.Position(2, 9), false).map(item => {
                try { return { name: item.name, typingOnly: item.is_type_check_only }; }
                finally { item.free(); }
            });
        } finally { source.free(); helper.free(); workspace.free(); }
    });
    for (const name of ['Helper', 'Alias']) assert.equal(items.find(item => item.name === name)?.typingOnly, true, name);
    assert.equal(items.find(item => item.name === 'Runtime')?.typingOnly, false);
}));

test('typing-only completion metadata follows native TYPE_CHECKING contexts', () => withBrowser(async page => {
    const results = await page.evaluate(async () => {
        const ty = await import('/dist/wasm/ty_wasm.js');
        await ty.default();
        const workspace = new ty.Workspace('/app', ty.PositionEncoding.Utf16, {});
        const helper = workspace.openFile('/app/helpers.pyi', 'from typing import type_check_only\n@type_check_only\nclass Helper: ...\n');
        try {
            return [
                ['import helpers\nhelpers.He¦', true],
                ['from helpers import He¦', true],
                ['from typing import TYPE_CHECKING\nimport helpers\nif TYPE_CHECKING:\n    Alias = helpers.He¦', false],
                ['import typing as t\nif t.TYPE_CHECKING:\n    from helpers import He¦', false],
            ].map(([marked, expected]) => {
                const offset = marked.indexOf('¦'), code = marked.replace('¦', '');
                const lines = code.slice(0, offset).split('\n');
                const source = workspace.openFile('/app/main.py', code);
                try {
                    const items = workspace.completions(source, new ty.Position(lines.length, lines.at(-1).length + 1), false);
                    try { return { marked, expected, actual: items.find(item => item.name === 'Helper')?.requires_type_checking }; }
                    finally { items.forEach(item => item.free()); }
                } finally { workspace.closeFile(source); }
            });
        } finally { helper.free(); workspace.free(); }
    });
    for (const { marked, expected, actual } of results) assert.equal(actual, expected, marked);
}));

test('builtin reference classification preserves shadowing and project overrides', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const ty = await import('/dist/wasm/ty_wasm.js');
        await ty.default();
        const workspace = new ty.Workspace('/app', ty.PositionEncoding.Utf16, {});
        const cases = [
            ['¦str(1)', true],
            ['¦missing(1)', false],
            ['from helpers import *\n¦str(1)', true],
            ['from missing import *\n¦str(1)', false],
            ['from bridge import *\n¦str(1)', false],
            ['from dynamic import *\n¦str(1)', false],
            ['from finite import *\n¦str(1)', true],
            ['from finite_shadow import *\n¦str(1)', false],
            ['def f():\n    from helpers import *\n    ¦str(1)', false],
            ['import builtins\nbuiltins.¦str(1)', false],
            ['from api import str\n¦str("greet")', false],
            ['from api import *\n¦str("greet")', false],
            ['if True:\n    from api import *\n¦str("greet")', false],
            ['str = remote\n¦str("greet")', false],
            ['def f(str):\n    ¦str("greet")', false],
        ];
        const api = workspace.openFile('/app/api.py', 'def str(name): return 42\n');
        let helpers = workspace.openFile('/app/helpers.py', 'def helper(): pass\n');
        const bridge = workspace.openFile('/app/bridge.py', 'from missing import *\n');
        const dynamic = workspace.openFile('/app/dynamic.py', 'def __getattr__(name): ...\n__all__ = discover_exports()\n');
        const finite = workspace.openFile('/app/finite.py', '__all__ = ["helper"]\ndef __getattr__(name): ...\n');
        const finiteShadow = workspace.openFile('/app/finite_shadow.py', '__all__ = ["str"]\ndef __getattr__(name): ...\n');
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
            const main = workspace.openFile('/app/main.py', 'from helpers import *\nstr(1)');
            const classify = () => workspace.isBuiltinReference(main, new ty.Position(2, 1));
            const changedExports = [classify()];
            for (const code of ['def str(name): return 42\n', 'def __getattr__(name): ...\n', 'def helper(): pass\n']) {
                workspace.closeFile(helpers);
                helpers = workspace.openFile('/app/helpers.py', code);
                changedExports.push(classify());
            }
            main.free();
            const custom = new ty.Workspace('/custom', ty.PositionEncoding.Utf16, {});
            const override = custom.openFile('/custom/__builtins__.pyi', 'def str(name: str) -> int: ...\n');
            const source = custom.openFile('/custom/main.py', 'str("greet")');
            try {
                return { actual, expected: cases.map(([, expected]) => expected), changedExports,
                    overridden: custom.isBuiltinReference(source, new ty.Position(1, 1)) };
            } finally { source.free(); override.free(); custom.free(); }
        } finally { finiteShadow.free(); finite.free(); dynamic.free(); bridge.free(); helpers.free(); api.free(); workspace.free(); }
    });
    assert.deepEqual(result.actual, result.expected);
    assert.deepEqual(result.changedExports, [true, false, false, true], 'Target edits invalidate the builtin proof without editing its importer');
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

test('delayed completion reuses imported modules and aliases without adding an import', () => withBrowser(async page => {
    const results = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const uri = 'file:///app/main.py';
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/main.py': '', '/app/other.py': 'class Rocket: pass\n',
        } });
        try {
            const results = [];
            for (const [prefix, insertion] of [
                ['', 'Rocket'],
                ['import other\n', 'other.Rocket'],
                ['import other as library\n', 'library.Rocket'],
            ]) {
                const source = prefix + 'RocketLocal = 42\nRock';
                await session.openDocument(uri, source);
                const params = { textDocument: { uri }, position: { line: source.split('\n').length - 1, character: 4 } };
                const ordinary = (await session.query('textDocument/completion', {
                    ...params, context: { autoImport: false },
                })).result.items;
                for (let step = 0; ; step++) {
                    if (step === 1000) throw new Error('Completion preparation did not finish');
                    if ((await session.query('anvil/prepareCompletion', { textDocument: { uri } })).result.complete) break;
                }
                const defaults = (await session.query('textDocument/completion', params)).result.items;
                const delayed = (await session.query('textDocument/completion', {
                    ...params, context: { autoImport: 'only' },
                })).result.items;
                results.push({ prefix, insertion, ordinary, defaults, delayed });
            }
            return results;
        } finally { session.dispose(); }
    });
    for (const { prefix, insertion, ordinary, defaults, delayed } of results) {
        assert(ordinary.some(item => item.label === 'RocketLocal'));
        assert(!ordinary.some(item => (item.insertText ?? item.label) === insertion));
        assert(defaults.some(item => (item.insertText ?? item.label) === insertion), JSON.stringify({ prefix, defaults }));
        const completion = delayed.find(item => (item.insertText ?? item.label) === insertion);
        assert(completion, `Missing delayed suggestion after ${JSON.stringify(prefix)}`);
        assert.equal(!!completion.additionalTextEdits?.length, !prefix);
        assert(!delayed.some(item => item.label === 'RocketLocal'));
    }
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
            for (const source of ['anvil_designer', 'EditorTemp', 'LaxDec',
                'import Main.Editor._anvil_designer as designer\nEditorTemp']) {
                await session.openDocument(uri, source);
                answers.push((await session.query('textDocument/completion', { textDocument: { uri },
                    position: { line: source.split('\n').length - 1, character: source.split('\n').at(-1).length } })).result.items);
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
    assert(!results.answers.flat().some(item => item.label.endsWith('EditorTemplate')),
        'Reusing an existing generated-module import must not suggest its checker declarations');
    assert(results.explicit.some(item => item.label === 'EditorTemplate'));
}));
