import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { copyFile, readFile, readdir, rm, writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { join, relative, sep } from 'node:path';

const root = new URL('./', import.meta.url);
const manifestUrl = new URL('dist/BUILD.json', root);
const packageJson = JSON.parse(await readFile(new URL('package.json', root), 'utf8'));
const publicFiles = ['session.mjs', 'contexts.mjs', 'forms.mjs', 'source-projection.mjs', 'renames.mjs', 'worker.mjs'];
const engineBuild = { optLevel: 'z', codegenUnits: 1, defaultFeatures: false, features: ['console_error_panic_hook'] };
const hash = source => createHash('sha256').update(source).digest('hex');
const git = args => execFileSync('git', args, { cwd: fileURLToPath(root), encoding: 'utf8' }).trim();
const buildInputs = ['.', '../compat', '../api-stubs', '../../crates', '../../Cargo.toml', '../../Cargo.lock',
    '../../rust-toolchain.toml', '../../.cargo', '../../LICENSE'];
const inputFingerprint = async () => {
    const digest = createHash('sha256');
    const paths = git(['ls-files', '-z', '--cached', '--others', '--exclude-standard', '--', ...buildInputs]).split('\0').filter(Boolean);
    for (const file of [...new Set(paths)].sort()) {
        digest.update(file + '\0').update(await readFile(new URL(file, root))).update('\0');
    }
    digest.update(await readFile(new URL(import.meta.resolve('@anvil-works/python-stubs/manifest.json'))));
    return digest.digest('hex');
};
const command = (file, args, { env = {} } = {}) => execFileSync(file, args, {
    cwd: fileURLToPath(root), stdio: 'inherit',
    env: { ...process.env, CARGO_BUILD_JOBS: process.env.CARGO_BUILD_JOBS ?? '2', ...env },
});

if (process.argv.includes('--verify')) {
    const manifest = JSON.parse(await readFile(manifestUrl, 'utf8'));
    assert.equal(manifest.version, packageJson.version, 'Build the browser assets for this package version');
    assert.equal(manifest.profile, 'release');
    assert.deepEqual(manifest.engineBuild, engineBuild, 'Engine build settings changed; rebuild before packing');
    assert.equal(manifest.inputsSha256, await inputFingerprint(), 'Browser build inputs changed; run pnpm build before packing');
    for (const [file, expected] of Object.entries(manifest.files)) {
        assert.equal(hash(await readFile(new URL(file, root))), expected, `Browser asset changed after its release build: ${file}`);
    }
} else {
    const fingerprint = await inputFingerprint();
    command(process.execPath, ['build-comlink.mjs']);
    command(process.execPath, ['build-stub-packs.mjs']);
    command('wasm-pack', ['build', '../../crates/ty_wasm', '--release', '--target', 'web',
        '--out-dir', '../../anvil/browser/dist/wasm', '--', '--locked', '--no-default-features',
        '--features', engineBuild.features.join(',')], {
        env: { CARGO_PROFILE_RELEASE_OPT_LEVEL: engineBuild.optLevel,
            CARGO_PROFILE_RELEASE_CODEGEN_UNITS: String(engineBuild.codegenUnits) },
    });
    command('wasm-pack', ['build', '../compat', '--release', '--target', 'web',
        '--out-dir', '../browser/dist/compat', '--', '--features', 'browser', '--locked']);
    // wasm-pack's nested ignore files otherwise exclude the binaries from npm.
    for (const directory of ['wasm', 'compat']) await rm(new URL(`dist/${directory}/.gitignore`, root), { force: true });
    await copyFile(new URL('../../LICENSE', root), new URL('dist/ty.LICENSE', root));
    const assets = (await readdir(new URL('dist/', root), { recursive: true, withFileTypes: true }))
        .filter(entry => entry.isFile() && entry.name !== 'BUILD.json')
        .map(entry => relative(fileURLToPath(root), join(entry.parentPath, entry.name)).split(sep).join('/'));
    const files = {};
    for (const file of [...publicFiles, ...assets].sort()) files[file] = hash(await readFile(new URL(file, root)));
    const stubs = JSON.parse(await readFile(new URL('../api-stubs/SOURCE.json', root), 'utf8'));
    const serverManifest = await readFile(new URL(import.meta.resolve('@anvil-works/python-stubs/manifest.json')));
    assert.equal(await inputFingerprint(), fingerprint, 'Browser inputs changed during compilation; rebuild before packing');
    await writeFile(manifestUrl, JSON.stringify({
        version: packageJson.version,
        profile: 'release',
        engineBuild,
        sourceRevision: git(['rev-parse', 'HEAD']),
        sourceDirty: !!git(['status', '--porcelain', '--', ...buildInputs]),
        inputsSha256: fingerprint,
        apiStubsRevision: stubs.revision,
        serverStubsSha256: hash(serverManifest),
        files,
    }, null, 2) + '\n');
}
