import assert from 'node:assert/strict';
import { execFile } from 'node:child_process';
import { mkdtemp, readFile, readdir, rm, writeFile } from 'node:fs/promises';
import { createServer } from 'node:http';
import { createRequire } from 'node:module';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
import { promisify } from 'node:util';
import { chromium } from '@playwright/test';

const exec = promisify(execFile);
const source = fileURLToPath(new URL('../', import.meta.url));

test('an installed browser package serves real completion and lazy library assets without the source checkout', async () => {
    const temporary = await mkdtemp(path.join(tmpdir(), 'anvil browser package '));
    let server, browser;
    try {
        await exec('pnpm', ['pack', '--pack-destination', temporary], { cwd: source });
        const tarball = (await readdir(temporary)).find(name => name.endsWith('.tgz'));
        await writeFile(path.join(temporary, 'package.json'), JSON.stringify({ private: true }));
        await exec('pnpm', ['add', '--offline', '--ignore-scripts', path.join(temporary, tarball)], { cwd: temporary });
        const require = createRequire(path.join(temporary, 'package.json'));
        const installed = path.dirname(require.resolve('@anvil-works/anvil-ty-browser/package.json'));
        assert((await readFile(path.join(installed, 'dist/wasm/ty_wasm_bg.wasm'))).length > 1_000_000);
        assert((await readFile(path.join(installed, 'dist/compat/anvil_ty_compat_bg.wasm'))).length > 100_000);
        const requests = [];
        server = createServer(async (request, response) => {
            if (request.url === '/') { response.end('<!doctype html><title>Installed analysis package</title>'); return; }
            const file = path.resolve(installed, '.' + new URL(request.url, 'http://localhost').pathname);
            if (!file.startsWith(installed + path.sep)) { response.writeHead(404).end(); return; }
            requests.push(file);
            try {
                response.setHeader('Content-Type', file.endsWith('.wasm') ? 'application/wasm' : file.endsWith('.json') ? 'application/json' : 'text/javascript');
                response.end(await readFile(file));
            } catch { response.writeHead(404).end(); }
        });
        await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
        browser = await chromium.launch({ channel: 'chrome', headless: true });
        const page = await browser.newPage();
        await page.goto(`http://127.0.0.1:${server.address().port}/`);
        const ordinary = await page.evaluate(async () => {
            const { BrowserAnalysisSession } = await import('/session.mjs');
            const uri = 'file:///app/server_code/main.py';
            window.analysis = new BrowserAnalysisSession({ workerUrl: '/worker.mjs', rootUri: 'file:///app', files: {
                '/app/anvil.yaml': JSON.stringify({ package_name: 'Main', runtime_options: { server_spec: {
                    base: 'python314', requirements: 'numpy==2.5.4\n',
                } } }),
                '/app/client_code/__init__.py': '',
                '/app/server_code/main.py': 'name = "Ada"\nname.up',
            } });
            return (await window.analysis.query('textDocument/completion', { textDocument: { uri },
                position: { line: 1, character: 7 } })).result.items.map(item => item.label);
        });
        assert(ordinary.includes('upper'));
        assert(!requests.some(file => /\/stubs\/numpy-/.test(file)), 'Unused server libraries stay lazy');
        const numpy = await page.evaluate(async () => {
            const uri = 'file:///app/server_code/main.py';
            try {
                await window.analysis.openDocument(uri, 'import numpy as np\nnp.array([1, 2]).resh');
                return (await window.analysis.query('textDocument/completion', { textDocument: { uri },
                    position: { line: 1, character: 21 } })).result.items.map(item => item.label);
            } finally { window.analysis.dispose(); }
        });
        assert(numpy.includes('reshape'));
        assert.equal(requests.filter(file => /\/stubs\/numpy-/.test(file)).length, 1);
        assert((await readFile(path.join(installed, 'dist/comlink.LICENSE'))).length > 100);
        assert((await readdir(path.join(installed, 'dist/stubs'))).some(name => /numpy.*\.txt$/.test(name)));
    } finally {
        await browser?.close();
        if (server) await new Promise(resolve => server.close(resolve));
        await rm(temporary, { recursive: true, force: true });
    }
});
