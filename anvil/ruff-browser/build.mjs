import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { copyFile, mkdir, readFile, rm, writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';

const root = new URL('./', import.meta.url);
const upstream = JSON.parse(await readFile(new URL('upstream.json', root), 'utf8'));
const pkg = JSON.parse(await readFile(new URL('package.json', root), 'utf8'));
const options = { optLevel: 'z', codegenUnits: 1 };
const files = ['ruff_wasm.js', 'ruff_wasm_bg.wasm', 'ruff_wasm.d.ts', 'LICENSE'];
const hash = bytes => createHash('sha256').update(bytes).digest('hex');
const inputs = async () => {
    const digest = createHash('sha256');
    for (const file of ['build.mjs', 'upstream.json', 'package.json'])
        digest.update(file + '\0').update(await readFile(new URL(file, root))).update('\0');
    return digest.digest('hex');
};
const run = (command, args, overrides = {}) => execFileSync(command, args, {
    cwd: fileURLToPath(root), stdio: 'inherit', ...overrides,
});

if (process.argv.includes('--verify')) {
    const manifest = JSON.parse(await readFile(new URL('build.json', root), 'utf8'));
    assert.equal(manifest.name, pkg.name);
    assert.equal(manifest.version, pkg.version);
    assert.deepEqual(manifest.upstream, upstream);
    assert.deepEqual(manifest.options, options);
    assert.equal(manifest.inputsSha256, await inputs(), 'Build inputs changed; rebuild before packing');
    for (const file of files)
        assert.equal(hash(await readFile(new URL(file, root))), manifest.files[file], `Build output changed: ${file}`);
} else {
    const fingerprint = await inputs();
    await mkdir(new URL('.cache/', root), { recursive: true });
    const archivePath = new URL(`.cache/source-${upstream.revision}.tar.gz`, root);
    let archive;
    try { archive = await readFile(archivePath); }
    catch (error) {
        if (error.code !== 'ENOENT') throw error;
        archive = run('gh', ['api', `repos/astral-sh/ruff/tarball/${upstream.revision}`], {
            stdio: ['ignore', 'pipe', 'inherit'], maxBuffer: 100 * 1024 * 1024,
        });
    }
    assert.equal(hash(archive), upstream.archiveSha256, 'Upstream source archive does not match the pinned checksum');
    await writeFile(archivePath, archive);
    // Re-extract the pinned archive so local cache edits cannot enter a release.
    const source = new URL('.cache/source/', root);
    await rm(source, { recursive: true, force: true });
    await mkdir(source, { recursive: true });
    run('tar', ['-xzf', fileURLToPath(archivePath), '-C', fileURLToPath(source), '--strip-components=1']);
    const output = new URL('.cache/pkg/', root);
    await rm(output, { recursive: true, force: true });
    run('wasm-pack', ['build', fileURLToPath(new URL('crates/ruff_wasm', source)), '--release', '--target', 'web',
        '--out-dir', fileURLToPath(output), '--', '--locked'], {
        cwd: fileURLToPath(source),
        env: { ...process.env, CARGO_BUILD_JOBS: process.env.CARGO_BUILD_JOBS ?? '2',
            BINARYEN_CORES: process.env.BINARYEN_CORES ?? '2',
            CARGO_TARGET_DIR: fileURLToPath(new URL('.cache/target', root)),
            CARGO_PROFILE_RELEASE_OPT_LEVEL: options.optLevel,
            CARGO_PROFILE_RELEASE_CODEGEN_UNITS: String(options.codegenUnits) },
    });
    await copyFile(new URL('LICENSE', source), new URL('LICENSE', output));
    const hashes = {};
    for (const file of files) {
        await copyFile(new URL(file, output), new URL(file, root));
        hashes[file] = hash(await readFile(new URL(file, root)));
    }
    assert.equal(await inputs(), fingerprint, 'Build inputs changed during compilation; rebuild before packing');
    await writeFile(new URL('build.json', root), JSON.stringify({
        name: pkg.name, version: pkg.version, upstream, options, inputsSha256: fingerprint, files: hashes,
    }, null, 2) + '\n');
}
