import { createHash } from 'node:crypto';
import { mkdir, readFile, readdir, rm, writeFile } from 'node:fs/promises';

// Keep the large client catalogue separate from the eagerly loaded WASM. The
// content hash lets browsers cache a pack without mixing declaration revisions.
const root = new URL('../api-stubs/client/', import.meta.url);
const paths = (await readdir(new URL('plotly/', root), { recursive: true }))
    .map(path => path.replaceAll('\\', '/')).filter(path => path.endsWith('.pyi')).sort();
const files = {};
for (const path of paths) files[`plotly/${path}`] = await readFile(new URL(`plotly/${path}`, root), 'utf8');
const output = new URL('./dist/stubs/', import.meta.url);
await mkdir(output, { recursive: true });
const packs = [];
async function writePack(id, source, metadata) {
    const hash = createHash('sha256').update(source).digest('hex');
    const filename = `${id}-${hash}.json`;
    await writeFile(new URL(filename, output), source);
    packs.push({ id, ...metadata, url: `./stubs/${filename}` });
}
await writePack('plotly-client', JSON.stringify(files), { server: false, modules: ['plotly'] });
const serverManifest = new URL(import.meta.resolve('@anvil-works/python-stubs/manifest.json'));
const { packs: serverPacks } = JSON.parse(await readFile(serverManifest, 'utf8'));
for (const pack of serverPacks) {
    const source = await readFile(new URL(pack.url, serverManifest));
    if (createHash('sha256').update(source).digest('hex') !== pack.sha256) throw new Error(`Invalid typing pack: ${pack.id}`);
    await writePack(pack.id, source, { server: true, modules: pack.modules, version: pack.version, dependencies: pack.dependencies });
}
// Licence notices travel with the browser assets, not just the build inputs.
const licences = await readdir(new URL('LICENSES/', serverManifest));
for (const filename of licences) {
    await writeFile(new URL(filename, output), await readFile(new URL(`LICENSES/${filename}`, serverManifest)));
}
await writeFile(new URL('./dist/stub-packs.mjs', import.meta.url),
    `export const stubPacks = ${JSON.stringify(packs)}.map(pack => ({...pack, url: new URL(pack.url, import.meta.url)}));\n`);
// Standalone browser sessions have a separate default asset. The IDE supplies
// its own generated asset and omits this default from its copied engine files.
const apiRoot = new URL('../api-stubs/', import.meta.url);
const apiFiles = {};
for (const environment of ['client', 'server']) {
    const paths = (await readdir(new URL(`${environment}/`, apiRoot), { recursive: true }))
        .map(path => path.replaceAll('\\', '/')).filter(path => path.endsWith('.pyi')).sort();
    for (const path of paths) {
        if (environment === 'client' && path.startsWith('plotly/') && path !== 'plotly/__init__.pyi') continue;
        apiFiles[`${environment}/${path}`] = await readFile(new URL(`${environment}/${path}`, apiRoot), 'utf8');
    }
}
await writeFile(new URL('./dist/api-stubs.json', import.meta.url), JSON.stringify({
    files: apiFiles,
    completionPreferences: JSON.parse(await readFile(new URL('completion-preferences.json', apiRoot))),
    clientRuntime: JSON.parse(await readFile(new URL('client-runtime.json', apiRoot))),
}) + '\n');
for (const previous of await readdir(output)) {
    if ((!packs.some(pack => pack.url === `./stubs/${previous}`) && /-[a-f0-9]{64}\.json$/.test(previous)) ||
        (previous.endsWith('.txt') && !licences.includes(previous))) {
        await rm(new URL(previous, output));
    }
}
