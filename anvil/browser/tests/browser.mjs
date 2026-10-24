import { readFile } from 'node:fs/promises';
import { createServer } from 'node:http';
import { fileURLToPath } from 'node:url';
import { chromium } from '@playwright/test';

export async function withBrowser(run) {
    const root = new URL('../', import.meta.url);
    const server = createServer(async (request, response) => {
        const path = decodeURIComponent(new URL(request.url, 'http://localhost').pathname);
        if (path === '/') { response.end('<!doctype html><title>ty session test</title>'); return; }
        const file = new URL('.' + path, root);
        if (!file.href.startsWith(root.href)) { response.writeHead(404).end(); return; }
        try {
            response.setHeader('Content-Type', path.endsWith('.wasm') ? 'application/wasm' : path.endsWith('.json') ? 'application/json' : 'text/javascript');
            response.end(await readFile(fileURLToPath(file)));
        } catch { response.writeHead(404).end(); }
    });
    await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
    let browser;
    try {
        browser = await chromium.launch({ channel: 'chrome', headless: true });
        const page = await browser.newPage();
        await page.goto(`http://127.0.0.1:${server.address().port}/`);
        return await run(page);
    } finally {
        await browser?.close();
        await new Promise(resolve => server.close(resolve));
    }
}
