import assert from 'node:assert/strict';
import { test } from 'node:test';
import { withBrowser } from './browser.mjs';

test('server diagnostics follow runtime version changes without changing the Skulpt client', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const server = 'file:///app/server_code/main.py';
        const client = 'file:///app/client_code/main.py';
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: Main\n',
            '/app/.anvil/python-environment.json': JSON.stringify({ server: '3.10' }),
            '/app/server_code/main.py': 'import tomllib\n',
            '/app/client_code/main.py': 'import pathlib\n',
        } });
        const diagnostics = async uri => (await session.query('textDocument/diagnostic', { textDocument: { uri } })).result.items;
        try {
            const before = await diagnostics(server);
            await session.updateFiles({ '/app/.anvil/python-environment.json': JSON.stringify({ server: '3.14' }) });
            const after = await diagnostics(server);
            const skulpt = await diagnostics(client);
            const again = await diagnostics(server);
            await session.openDocument(server, 'import crypt\nimport distutils\n');
            const removedStdlib = await diagnostics(server);
            return { before, after, skulpt, again, removedStdlib };
        } finally { session.dispose(); }
    });
    assert(result.before.some(item => item.code === 'unresolved-import'));
    assert.deepEqual(result.after, []);
    assert.deepEqual(result.again, []);
    assert(result.skulpt.some(item => item.code === 'reportAnvilUnsupportedSkulptImport'));
    assert.equal(result.removedStdlib.filter(item => item.code === 'unresolved-import' && item.severity === 1).length, 2);
}));

test('missing external server typing is informational while app and stdlib imports remain errors', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const server = 'file:///app/server_code/main.py';
        const source = 'import requests\nfrom PIL import Image\nfrom .missing import helper\nimport Main.missing\nimport tomllib\ndef greet(name: str): pass\ngreet(42)\nimport arrow\n';
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: Main\nruntime_options:\n  server_spec:\n    requirements: arrow\n', '/app/client_code/__init__.py': '',
            '/app/server_code/main.py': source,
            '/app/.anvil/python-environment.json': JSON.stringify({ server: '3.10' }),
        } });
        const diagnostics = async () => (await session.query('textDocument/diagnostic', { textDocument: { uri: server } })).result.items;
        try {
            const defaults = await diagnostics();
            await session.updateFiles({ '/app/ty.toml': '[rules]\nunresolved-import = "error"\n' });
            const strict = await diagnostics();
            await session.updateFiles({ '/app/ty.toml': '[analysis]\nallowed-unresolved-imports = ["requests.**", "PIL.**", "arrow.**"]\n' });
            return { defaults, strict, allowed: await diagnostics() };
        } finally { session.dispose(); }
    });
    for (const line of [0, 1, 7]) {
        const item = result.defaults.find(item => item.range.start.line === line);
        assert.equal(item?.severity, 3, JSON.stringify(result.defaults));
        assert.match(item.message, /type information.*unavailable/i);
        assert.doesNotMatch(item.message, /check.*install/i);
        assert.equal(result.strict.find(item => item.range.start.line === line)?.severity, 1);
        assert(!result.allowed.some(item => item.range.start.line === line));
    }
    for (const line of [2, 3, 4])
        assert(result.defaults.some(item => item.range.start.line === line && item.severity === 1), `Missing import at line ${line}`);
    assert(result.defaults.some(item => item.code === 'invalid-argument-type'));
}));

test('invalid Ty configuration is visible and recoverable instead of retaining old rules silently', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const uri = 'file:///app/server_code/main.py';
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: Main\n',
            '/app/client_code/__init__.py': '',
            '/app/server_code/main.py': 'def greet(name: str): pass\ngreet(42)\n',
            '/app/ty.toml': '[rules]\ninvalid-argument-type = "ignore"\n',
        } });
        const diagnostics = async () => (await session.query('textDocument/diagnostic', { textDocument: { uri } })).result.items;
        try {
            await diagnostics();
            const invalid = [];
            for (const [name, text] of [
                ['ty.toml', '[rules\n'],
                ['ty.toml', '[rules]\ninvalid-argument-type = "banana"\n'],
                ['ty.toml', '[analysis]\nrespect-type-ignore-comments = "banana"\n'],
                ['pyproject.toml', '[tool]\nty = false\n'],
                ['pyproject.toml', '[tool]\nty = []\n'],
                ['pyproject.toml', '[tool.ty]\nanalysis = []\n'],
            ]) {
                await session.updateFiles({ '/app/ty.toml': null, [`/app/${name}`]: text });
                invalid.push(await diagnostics());
            }
            await session.updateFiles({ '/app/ty.toml': '[rules]\ninvalid-argument-type = "warn"\n' });
            return { invalid, recovered: await diagnostics() };
        } finally { session.dispose(); }
    });
    for (const diagnostics of result.invalid) {
        assert(diagnostics.some(item => item.code === 'anvil-invalid-ty-config' && /ty.toml|pyproject.toml/.test(item.message)), JSON.stringify(diagnostics));
        assert(diagnostics.some(item => item.code === 'invalid-argument-type'), 'Invalid config must use defaults, not stale rules');
    }
    assert(!result.recovered.some(item => item.code === 'anvil-invalid-ty-config'));
    assert.equal(result.recovered.find(item => item.code === 'invalid-argument-type')?.severity, 2);
}));

test('ty.toml overrides pyproject rules and live edits and removal refresh both runtimes', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const source = 'def greet(name: str): pass\ngreet(42)\n';
        const server = 'file:///app/server_code/main.py';
        const client = 'file:///app/client_code/main.py';
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: Main\n',
            '/app/server_code/main.py': source,
            '/app/client_code/main.py': source,
            '/app/pyproject.toml': '[tool.ty.rules]\ninvalid-argument-type = "ignore"\n',
            '/app/ty.toml': '[rules]\ninvalid-argument-type = "warn"\n',
        } });
        const diagnostics = async uri => (await session.query('textDocument/diagnostic', { textDocument: { uri } })).result.items;
        try {
            const warning = await diagnostics(server);
            await session.updateFiles({ '/app/ty.toml': '[rules]\ninvalid-argument-type = "error"\n' });
            const error = await diagnostics(server);
            const clientError = await diagnostics(client);
            await session.updateFiles({ '/app/ty.toml': null });
            const ignored = await diagnostics(server);
            const clientIgnored = await diagnostics(client);
            await session.updateFiles({ '/app/pyproject.toml': null });
            const defaults = await diagnostics(server);
            return { warning, error, clientError, ignored, clientIgnored, defaults };
        } finally { session.dispose(); }
    });
    assert.equal(result.warning.find(item => item.code === 'invalid-argument-type')?.severity, 2);
    for (const key of ['error', 'clientError', 'defaults'])
        assert.equal(result[key].find(item => item.code === 'invalid-argument-type')?.severity, 1, key);
    assert.deepEqual(result.ignored, []);
    assert.deepEqual(result.clientIgnored, []);
}));

test('configuration fallback and removal refresh inactive runtime rules and inferred RPC declarations', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const server = 'file:///app/server_code/rpc.py';
        const client = 'file:///app/client_code/main.py';
        const check = 'def needs_name(name: str): pass\nneeds_name(42)\n';
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: Main\n',
            '/app/server_code/rpc.py': 'import anvil.server\n@anvil.server.callable\ndef greet(): return "Ada"\n' + check,
            '/app/client_code/main.py': 'import anvil.server\n' + check + 'result = anvil.server.call("greet")\nresult.',
            '/app/ty.toml': '[rules]\ninvalid-argument-type = "ignore"\n',
            '/app/pyproject.toml': '[tool.ty.rules]\ninvalid-argument-type = "warn"\n[tool.ty.analysis]\nreturn-type-inference = "never"\n',
        } });
        const diagnostics = async uri => (await session.query('textDocument/diagnostic', { textDocument: { uri } })).result.items;
        const members = async () => (await session.query('textDocument/completion', { textDocument: { uri: client },
            position: { line: 4, character: 7 } })).result.items.map(item => item.label);
        try {
            const initialServer = await diagnostics(server);
            const initialClient = await diagnostics(client);
            const initial = await members();
            await session.updateFiles({ '/app/ty.toml': '[rules]\ninvalid-argument-type = "ignore"\n[analysis]\nreturn-type-inference = "never"\n' });
            const never = await members();
            await session.updateFiles({ '/app/ty.toml': '[rules\n' });
            const invalidServer = await diagnostics(server);
            const invalidClient = await diagnostics(client);
            const fallback = await members();
            await session.updateFiles({ '/app/ty.toml': null });
            const inheritedServer = await diagnostics(server);
            const inheritedClient = await diagnostics(client);
            const inherited = await members();
            await session.updateFiles({ '/app/pyproject.toml': null });
            const defaultsServer = await diagnostics(server);
            const defaultsClient = await diagnostics(client);
            const defaults = await members();
            return { initialServer, initialClient, initial, never, invalidServer, invalidClient, fallback,
                inheritedServer, inheritedClient, inherited, defaultsServer, defaultsClient, defaults };
        } finally { session.dispose(); }
    });
    for (const key of ['initial', 'fallback', 'defaults']) assert(result[key].includes('upper'), key);
    for (const key of ['never', 'inherited']) assert(!result[key].includes('upper'), key);
    for (const key of ['initialServer', 'initialClient']) assert(!result[key].some(item => item.code === 'invalid-argument-type'), key);
    for (const key of ['invalidServer', 'invalidClient']) {
        assert(result[key].some(item => item.code === 'anvil-invalid-ty-config'), key);
        assert.equal(result[key].find(item => item.code === 'invalid-argument-type')?.severity, 1, key);
    }
    for (const key of ['inheritedServer', 'inheritedClient'])
        assert.equal(result[key].find(item => item.code === 'invalid-argument-type')?.severity, 2, key);
    for (const key of ['defaultsServer', 'defaultsClient'])
        assert.equal(result[key].find(item => item.code === 'invalid-argument-type')?.severity, 1, key);
}));
