import assert from 'node:assert/strict';
import { test } from 'node:test';
import { withBrowser } from './browser.mjs';

test('RPC demand follows builtin-name aliases through re-exports and live rebinding', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const uri = 'file:///app/client_code/main.py';
        const source = 'from .bridge import *\nanswer = str("greet")\nanswer.\n';
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: Main\n', '/app/client_code/__init__.py': '',
            '/app/client_code/main.py': source,
            '/app/client_code/bridge.py': 'from anvil.server import call as str\n',
            '/app/server_code/api.py': 'import anvil.server\n@anvil.server.callable\ndef greet(): return "Ada"\n',
        } });
        const complete = async () => (await session.query('textDocument/completion', {
            textDocument: { uri }, position: { line: 2, character: 7 },
        })).result.items.map(item => item.label);
        try {
            const remote = await complete();
            await session.openDocument('file:///app/client_code/bridge.py', 'def str(name): return 42\n');
            const local = await complete();
            await session.closeDocument('file:///app/client_code/bridge.py');
            return { remote, local, restored: await complete(), source: (await session.readSource(uri)).result.text };
        } finally { session.dispose(); }
    });
    assert(result.remote.includes('upper'));
    assert(result.local.includes('bit_length') && !result.local.includes('upper'));
    assert(result.restored.includes('upper'));
    assert.equal(result.source, 'from .bridge import *\nanswer = str("greet")\nanswer.\n');
}));

test('builtin-spelled RPC calls follow star imports added and removed by an edit', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const uri = 'file:///app/client_code/main.py';
        const source = 'answer = str("greet")\nanswer.\n';
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: Main\n', '/app/client_code/__init__.py': '',
            '/app/client_code/main.py': source,
            '/app/client_code/bridge.py': 'from anvil.server import call as str\n',
            '/app/server_code/api.py': 'import anvil.server\n@anvil.server.callable\ndef greet() -> int: return 42\n',
        } });
        const complete = async code => {
            await session.openDocument(uri, code);
            return (await session.query('textDocument/completion', { textDocument: { uri },
                position: { line: code.trimEnd().split('\n').length - 1, character: 7 },
                context: { autoImport: false } })).result.items.map(item => item.label);
        };
        try {
            return { builtin: await complete(source),
                remote: await complete('from .bridge import *\n' + source),
                restored: await complete(source),
                qualified: await complete('import anvil.server\nanswer = anvil.server.call("greet")\nanswer.\n') };
        } finally { session.dispose(); }
    });
    for (const items of [result.builtin, result.restored]) {
        assert(items.includes('upper') && !items.includes('bit_length'));
    }
    for (const items of [result.remote, result.qualified]) {
        assert(items.includes('bit_length') && !items.includes('upper'));
    }
}));

test('literal RPC keyword completion follows the callable without replacing caller expressions', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const source = 'from anvil.server import call as invoke\nclient_name = "Ada"\ninvoke("say_hello", )\n';
        const server = parameter => `import anvil.server\n@anvil.server.callable\ndef say_hello(${parameter}: str, *, punctuation: str = "!") -> str:\n    return ${parameter} + punctuation\n`;
        const uri = 'file:///app/client_code/main.py';
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: Main\n', '/app/client_code/__init__.py': '',
            '/app/client_code/main.py': source, '/app/server_code/api.py': server('name'),
        } });
        const complete = async code => {
            await session.openDocument(uri, code);
            const lines = code.trimEnd().split('\n');
            return (await session.query('textDocument/completion', { textDocument: { uri },
                position: { line: lines.length - 1, character: lines.at(-1).lastIndexOf(')') } })).result.items;
        };
        try {
            const initial = await complete(source);
            const used = await complete(source.replace(', )', ', name=client_name, pu)'));
            await session.updateFiles({ '/app/server_code/api.py': server('person') });
            const changed = await complete(source);
            const restored = (await session.readSource(uri)).result.text;
            await session.setContext({ kind: 'repl', id: 'rpc', isServer: false,
                code: 'from anvil.server import call\ncall("say_hello", )' });
            const context = (await session.queryContext('rpc', 'textDocument/completion', {
                position: { line: 1, character: 'call("say_hello", '.length },
            })).result.items;
            return { initial, used, changed, context, restored, source };
        } finally { session.dispose(); }
    });
    const labels = items => items.map(item => item.label);
    assert(labels(result.initial).includes('name='), JSON.stringify(labels(result.initial)));
    assert(labels(result.initial).includes('punctuation='));
    assert(labels(result.initial).includes('client_name'), 'Argument expressions retain the caller runtime');
    assert(labels(result.used).includes('punctuation=') && !labels(result.used).includes('name='));
    for (const items of [result.changed, result.context]) {
        assert(labels(items).includes('person=') && !labels(items).includes('name='), JSON.stringify(labels(items)));
        assert(!labels(items).some(label => label.startsWith('_anvil_rpc_')), 'Temporary projection names stay private');
    }
    assert.equal(result.restored, result.source, 'Keyword inference must not change original source');
}));
