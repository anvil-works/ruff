import assert from 'node:assert/strict';
import { test } from 'node:test';
import { withBrowser } from './browser.mjs';

test('client stdlib suggestions and import diagnostics follow Skulpt without restricting server code', () => withBrowser(async page => {
    const result = await page.evaluate(async () => {
        const { BrowserAnalysisSession } = await import('/session.mjs');
        const source = 'import pathlib\nfrom os import path\nimport math\nfrom . import helpers\nimport webbrowser\nimport urllib.request\nimport urllib.parse\nimport collections.abc\nfrom urllib import parse\nfrom collections import abc, namedtuple\nfrom urllib import request\n';
        const session = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
            '/app/anvil.yaml': 'package_name: Main\n', '/app/client_code/__init__.py': '',
            '/app/client_code/main.py': source, '/app/client_code/helpers.py': 'pass\n', '/app/client_code/pathlib.py': 'pass\n', '/app/server_code/main.py': source.replace('from . import helpers', ''),
        }});
        const query = (uri, method, extra = {}) => session.query(method, { textDocument: { uri }, ...extra });
        const client = 'file:///app/client_code/main.py', server = 'file:///app/server_code/main.py';
        try {
            const diagnostics = await query(client, 'textDocument/diagnostic');
            const serverDiagnostics = await query(server, 'textDocument/diagnostic');
            await session.openDocument(client, 'from ');
            const imports = await query(client, 'textDocument/completion', { position: { line: 0, character: 5 } });
            await session.openDocument(server, 'from path');
            await session.openDocument(client, 'from . import path');
            const localImports = await query(client, 'textDocument/completion', { position: { line: 0, character: 18 } });
            const serverImports = await query(server, 'textDocument/completion', { position: { line: 0, character: 9 } });
            await session.openDocument(client, 'from urllib import ');
            const childImports = await query(client, 'textDocument/completion', { position: { line: 0, character: 19 } });
            await session.openDocument(client, 'import urllib.');
            const dottedImports = await query(client, 'textDocument/completion', { position: { line: 0, character: 14 } });
            await session.openDocument(client, 'from .path');
            const relativeImports = await query(client, 'textDocument/completion', { position: { line: 0, character: 10 } });
            return { diagnostics, serverDiagnostics, imports, serverImports, localImports, childImports, dottedImports, relativeImports };
        } finally { session.dispose(); }
    });
    const unsupported = result.diagnostics.result.items.filter(item => item.code === 'reportAnvilUnsupportedSkulptImport');
    assert.deepEqual(unsupported.map(item => [item.range.start.line, item.range.start.character, item.range.end.character]), [[0, 7, 14], [1, 5, 7], [6, 7, 19], [7, 7, 22], [8, 19, 24], [9, 24, 27]]);
    assert(!result.serverDiagnostics.result.items.some(item => item.code === 'reportAnvilUnsupportedSkulptImport'));
    const labels = result.imports.result.items.map(item => item.label);
    for (const name of ['pathlib', 'os', 'subprocess', 'builtins', 'typing', 'aifc']) assert(!labels.includes(name), `${name} is not available to Skulpt`);
    assert(labels.includes('math'));
    assert(labels.includes('webbrowser'));
    assert(result.childImports.result.items.some(item => item.label === 'request'));
    assert(!result.childImports.result.items.some(item => item.label === 'parse'));
    assert(result.dottedImports.result.items.some(item => item.label === 'request'));
    for (const name of ['parse', 'error', 'response', 'robotparser']) assert(!result.dottedImports.result.items.some(item => item.label === name));
    assert(result.localImports.result.items.some(item => item.label === 'pathlib'));
    assert(result.relativeImports.result.items.some(item => item.label === 'pathlib'));
    assert(result.serverImports.result.items.some(item => item.label === 'pathlib'));
}));
