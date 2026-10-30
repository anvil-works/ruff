import assert from 'node:assert/strict';
import { execFile } from 'node:child_process';
import { copyFile, mkdir, mkdtemp, readFile, rm, symlink, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { test } from 'node:test';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { promisify } from 'node:util';

const exec = promisify(execFile);
const browser = fileURLToPath(new URL('../', import.meta.url));

test('browser assets consume installed server typing packs without vendored snapshots or Python', async () => {
    const temporary = await mkdtemp(path.join(tmpdir(), 'anvil browser stub package '));
    try {
        const fixture = path.join(temporary, 'anvil/browser');
        const plotly = path.join(temporary, 'anvil/api-stubs/client/plotly');
        await mkdir(fixture, { recursive: true });
        await mkdir(plotly, { recursive: true });
        await mkdir(path.join(temporary, 'anvil/api-stubs/server'), { recursive: true });
        await writeFile(path.join(plotly, '__init__.pyi'), 'class Figure: ...\n');
        await copyFile(path.join(browser, '../api-stubs/completion-preferences.json'),
            path.join(temporary, 'anvil/api-stubs/completion-preferences.json'));
        await copyFile(path.join(browser, '../api-stubs/client-runtime.json'),
            path.join(temporary, 'anvil/api-stubs/client-runtime.json'));
        await copyFile(path.join(browser, 'build-stub-packs.mjs'), path.join(fixture, 'build-stub-packs.mjs'));
        await symlink(path.join(browser, 'node_modules'), path.join(fixture, 'node_modules'), 'dir');
        await exec(process.execPath, [path.join(fixture, 'build-stub-packs.mjs')], {
            cwd: fixture, env: { ...process.env, PATH: '' },
        });
        const { stubPacks } = await import(pathToFileURL(path.join(fixture, 'dist/stub-packs.mjs')));
        const { files, completionPreferences, clientRuntime } = JSON.parse(await readFile(path.join(fixture, 'dist/api-stubs.json')));
        assert.match(files['client/plotly/__init__.pyi'], /class Figure/);
        assert.equal(completionPreferences['anvil.server'].suggestedAttr, 'call');
        assert(clientRuntime.modules.includes('base64'));
        for (const id of ['numpy', 'pandas']) {
            const pack = stubPacks.find(pack => pack.id === id);
            assert.equal(pack.server, true);
            assert(Object.keys(JSON.parse(await readFile(pack.url))).length > 100, id);
        }
    } finally {
        await rm(temporary, { recursive: true, force: true });
    }
});
