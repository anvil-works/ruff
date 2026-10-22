#!/usr/bin/env node
// Refresh distributable API stubs using Anvil's authoritative generator.
import { createHash } from 'node:crypto';
import { execFileSync } from 'node:child_process';
import { readFile, readdir, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const directory = path.dirname(fileURLToPath(import.meta.url));
// Accept a source checkout so feature worktrees can bundle the committed master stubs.
const anvil = process.argv[2] ? path.resolve(process.argv[2]) : path.resolve(directory, '../../anvil');
const source = path.join(anvil, 'doc/anvil-api-stubs/source');
const outputRoot = path.join(directory, 'api-stubs');
const { generateStubs } = await import(pathToFileURL(path.join(anvil, 'doc/anvil-api-stubs/generate-stubs.mjs')));
const result = await generateStubs({ outputRoot });
const files = {};
for (const entry of await readdir(source, { recursive: true, withFileTypes: true })) {
    if (!entry.isFile() || !entry.name.endsWith('.pyi')) continue;
    const filename = path.join(entry.parentPath, entry.name);
    files[path.relative(source, filename)] = createHash('sha256').update(await readFile(filename)).digest('hex');
}
// The generated docs depend on the catalogue as well as the handwritten types.
const inputs = {};
for (const filename of ['doc/dist/index.json', 'doc/anvil-api-stubs/generate-stubs.mjs',
    'doc/anvil-api-stubs/stub_documentation.py', 'doc/anvil-api-stubs/plotly-stubs.mjs',
    'doc/anvil-api-stubs/completion-preferences.mjs',
    'doc/anvil-api-stubs/completion-priorities.json', 'website/static/_/redirects.yaml']) {
    inputs[filename] = createHash('sha256').update(await readFile(path.join(anvil, filename))).digest('hex');
}
await writeFile(path.join(outputRoot, 'SOURCE.json'), JSON.stringify({
    repository: 'https://github.com/anvil-works/anvil',
    revision: execFileSync('git', ['-C', anvil, 'rev-parse', 'HEAD'], { encoding: 'utf8' }).trim(),
    files: Object.fromEntries(Object.entries(files).sort(([a], [b]) => a.localeCompare(b))),
    inputs,
}, null, 2) + '\n');
console.log(`Generated ${result.clientCount} client and ${result.serverCount} server stubs (${result.changed} changed)`);
