import assert from 'node:assert/strict';
import { test } from 'node:test';
import { withBrowser } from './browser.mjs';

test('supplied API asset controls declarations, completion preferences and runtime policy without fetching defaults', () => withBrowser(async page => {
    const requests = [];
    page.on('request', request => { if (request.url().endsWith('.json')) requests.push(new URL(request.url()).pathname); });
    await page.context().route('**/ide-stubs.json', route => route.fulfill({ contentType: 'application/json', body: JSON.stringify({
        files: {
            'client/anvil/__init__.pyi': 'class Component: ...\nclass Button(Component):\n    def release_marker(self) -> str: ...\n    def another(self) -> None: ...\n',
            'server/anvil/__init__.pyi': 'def server_marker() -> int: ...\n',
        },
        completionPreferences: { 'anvil.Button': { suggestedAttr: 'release_marker' } },
        clientRuntime: { modules: ['locale'] },
    }) }));
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const client = 'file:///app/client_code/main.py';
        const server = 'file:///app/server_code/main.py';
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', apiStubsUrl: '/ide-stubs.json', files: {
            '/app/anvil.yaml': 'package_name: Main\n',
            '/app/client_code/main.py': 'import anvil\nbutton = anvil.Button()\nbutton.',
            '/app/server_code/main.py': 'import anvil\nanvil.',
        } });
        const complete = async (uri, line, character) => (await session.query('textDocument/completion', {
            textDocument: { uri }, position: { line, character }, context: { autoImport: false },
        })).result.items.map(item => item.label);
        try {
            const clientMembers = await complete(client, 2, 7);
            const serverMembers = await complete(server, 1, 6);
            await session.openDocument(client, 'import locale\nimport os\n');
            const diagnostics = (await session.query('textDocument/diagnostic', { textDocument: { uri: client } })).result.items;
            return { clientMembers, serverMembers, diagnostics };
        } finally { session.dispose(); }
    });
    assert.equal(result.clientMembers[0], 'release_marker');
    assert(result.clientMembers.includes('another'));
    assert(result.serverMembers.includes('server_marker'));
    assert(!result.serverMembers.includes('Button'));
    const unsupported = result.diagnostics.filter(item => item.code === 'reportAnvilUnsupportedSkulptImport');
    assert.deepEqual(unsupported.map(item => item.range.start.line), [1]);
    assert.deepEqual(requests, ['/ide-stubs.json']);
}));

test('a missing supplied API asset reports the error without falling back to packaged declarations', () => withBrowser(async page => {
    const requests = [];
    page.on('request', request => { if (request.url().endsWith('.json')) requests.push(new URL(request.url()).pathname); });
    const error = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', apiStubsUrl: '/missing-stubs.json', files: {} });
        try {
            await session.query('textDocument/completion', { textDocument: { uri: 'file:///app/client_code/main.py' }, position: { line: 0, character: 0 } });
        } catch (error) { return String(error); }
        finally { session.dispose(); }
    });
    assert.match(error, /Unable to load Anvil API stubs: 404/);
    assert.deepEqual(requests, ['/missing-stubs.json']);
}));
