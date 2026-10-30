import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { test } from 'node:test';
import { withBrowser } from './browser.mjs';

test('supplied client runtime modules control completion and diagnostics without restricting server imports', () => withBrowser(async page => {
    const stubs = JSON.parse(await readFile(new URL('../dist/api-stubs.json', import.meta.url)));
    stubs.clientRuntime = { modules: ['locale'] };
    await page.context().route('**/runtime-stubs.json', route => route.fulfill({ contentType: 'application/json', body: JSON.stringify(stubs) }));
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const client = 'file:///app/client_code/main.py';
        const server = 'file:///app/server_code/main.py';
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app',
            apiStubsUrl: '/runtime-stubs.json', files: {
                '/app/anvil.yaml': 'package_name: Main\n',
                '/app/client_code/main.py': 'from locale import LC_TIME, setlocale\nimport locale\nlocale.',
                '/app/server_code/main.py': 'import math\nimport os\n',
            },
        });
        const diagnostics = async uri => (await session.query('textDocument/diagnostic', { textDocument: { uri } })).result.items;
        try {
            const localeIssues = await diagnostics(client);
            const members = (await session.query('textDocument/completion', { textDocument: { uri: client },
                position: { line: 2, character: 7 }, context: { autoImport: false } })).result.items.map(item => item.label);
            await session.openDocument(client, 'import math\n');
            const mathIssues = await diagnostics(client);
            await session.openDocument(client, 'from ');
            const imports = (await session.query('textDocument/completion', { textDocument: { uri: client },
                position: { line: 0, character: 5 }, context: { autoImport: false } })).result.items.map(item => item.label);
            return { localeIssues, members, mathIssues, imports, serverIssues: await diagnostics(server) };
        } finally { session.dispose(); }
    });
    const unsupported = items => items.filter(item => item.code === 'reportAnvilUnsupportedSkulptImport');
    assert.deepEqual(unsupported(result.localeIssues), []);
    assert(result.members.includes('setlocale'));
    assert.equal(unsupported(result.mathIssues).length, 1);
    assert(result.imports.includes('locale'));
    assert(!result.imports.includes('math'));
    assert.deepEqual(unsupported(result.serverIssues), []);
}));

test('malformed supplied runtime metadata is reported instead of using bundled defaults', () => withBrowser(async page => {
    const stubs = JSON.parse(await readFile(new URL('../dist/api-stubs.json', import.meta.url)));
    stubs.clientRuntime = { modules: 'locale' };
    await page.context().route('**/runtime-stubs.json', route => route.fulfill({ contentType: 'application/json', body: JSON.stringify(stubs) }));
    const error = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app',
            apiStubsUrl: '/runtime-stubs.json', files: { '/app/anvil.yaml': 'package_name: Main\n' },
        });
        try {
            await session.query('textDocument/diagnostic', { textDocument: { uri: 'file:///app/client_code/main.py' } });
            return undefined;
        } catch (error) { return String(error); }
        finally { session.dispose(); }
    });
    assert.match(error, /Invalid client runtime metadata/);
}));
