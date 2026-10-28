import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { appendFile, copyFile, mkdtemp, rm } from 'node:fs/promises';
import { spawnSync } from 'node:child_process';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { test } from 'node:test';
import { initSync, Workspace, PositionEncoding } from './ruff_wasm.js';

const upstream = JSON.parse(readFileSync(new URL('upstream.json', import.meta.url)));
initSync({ module: readFileSync(new URL('ruff_wasm_bg.wasm', import.meta.url)) });
const workspace = options => new Workspace({ preview: true, 'target-version': 'py37', 'indent-width': 2,
    'output-prefer-rule-codes': true, ...options }, PositionEncoding.Utf16);

test('the package preserves the pinned engine, formatting and lint codes', () => {
    assert.equal(Workspace.version(), upstream.version);
    const current = workspace();
    try {
        assert.equal(current.format("def greet():\n    return 'hello'\n"), 'def greet():\n  return "hello"\n');
        assert(current.check('missing_name\n').some(diagnostic => diagnostic.code === 'F821'));
        assert(current.check('def broken(:\n  pass\n').some(diagnostic => diagnostic.code === 'invalid-syntax'));
    } finally { current.free(); }
});

test('server syntax targeting remains distinct from client syntax', () => {
    const server = workspace({ 'target-version': 'py314' });
    const client = workspace();
    const source = 'name = "world"\ntemplate = t"Hello {name}"\n';
    try {
        assert.deepEqual(server.check(source), []);
        assert.equal(server.format(source), source);
        assert(client.check(source).some(diagnostic => diagnostic.code === 'invalid-syntax'));
    } finally { server.free(); client.free(); }
});

test('diagnostics and import fixes retain CodeMirror UTF-16 coordinates', () => {
    const current = workspace({ lint: { select: ['F', 'I'] } });
    try {
        const source = '"😀é"; missing_name\n';
        const missing = current.check(source).find(diagnostic => diagnostic.code === 'F821');
        assert.equal(missing.start_location.column, source.indexOf('missing_name') + 1);
        const imports = current.check('import sys\nimport os\n').find(diagnostic => diagnostic.code === 'I001');
        assert(imports.fix.edits.some(edit => edit.content === 'import os\nimport sys\n'));
    } finally { current.free(); }
});

test('packing rejects changed build outputs and stale build inputs', async () => {
    const directory = await mkdtemp(join(tmpdir(), 'ruff-package-guard-'));
    try {
        const files = ['build.mjs', 'upstream.json', 'package.json', 'build.json',
            'ruff_wasm.js', 'ruff_wasm_bg.wasm', 'ruff_wasm.d.ts', 'LICENSE'];
        for (const file of files) await copyFile(new URL(file, import.meta.url), join(directory, file));
        const verify = () => spawnSync(process.execPath, ['build.mjs', '--verify'], { cwd: directory, encoding: 'utf8' });
        await appendFile(join(directory, 'ruff_wasm_bg.wasm'), Buffer.from([0]));
        const changedOutput = verify();
        assert.notEqual(changedOutput.status, 0);
        assert.match(changedOutput.stderr, /Build output changed: ruff_wasm_bg.wasm/);
        await copyFile(new URL('ruff_wasm_bg.wasm', import.meta.url), join(directory, 'ruff_wasm_bg.wasm'));
        await appendFile(join(directory, 'build.mjs'), '\n// modified after compilation\n');
        const staleBuild = verify();
        assert.notEqual(staleBuild.status, 0);
        assert.match(staleBuild.stderr, /Build inputs changed/);
    } finally { await rm(directory, { recursive: true, force: true }); }
});
