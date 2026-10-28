# Publishing Anvil validation

The checker lives in `anvil-works/ruff`. Its `anvil` branch carries one commit
above upstream `main`, including the Anvil adapter, API stubs and
npm packaging. The local checkout is `/Users/scork/Desktop/Projects/anvil-ruff`.
There is no submodule or separate wrapper repository to push.

All pushing and publishing is performed by Stu. The workflow builds packages
without npm credentials; it does not publish them. A successful five-platform
build is required before checker publication. The CLI registry lockfile can be
finished after the checker exists on npm.

## IDE browser assets

The browser package has its own version in `anvil/browser/package.json`. A
browser-only release does not require new native checker or Python-stub packages.
The next browser candidate is `0.1.0-canary.4`; its typing packs remain
`@anvil-works/python-stubs@0.1.0-canary.1`. The published native checker stays at
`0.1.0-canary.1`. Recheck npm before publication: an existing version cannot be
replaced.

1. Commit the reviewed browser source, including its new package version. From
    that clean checkout, run `pnpm install --frozen-lockfile`, `pnpm build` and
    `pnpm test` in `anvil/browser`. Both WASM modules must use release mode.
1. Inspect `dist/BUILD.json`: it must name the reviewed source revision, the new
    browser version and `sourceDirty: false`. Pack outside the source checkout
    with `pnpm pack --pack-destination "$(mktemp -d)"` and test that exact archive
    through the installed-package browser smoke before publishing it.
1. Before npm publication, push the reviewed source and run Anvil's **Python
    completion performance** workflow on the IDE feature branch, setting
    `ty_ref` to that full source SHA. This compares the candidate with the IDE's
    installed release on the same Linux runner. Require its compatibility and
    performance checks to pass with unchanged budgets.
1. Stu publishes the reviewed archive with
    `npm publish <archive> --access public --tag canary`.
1. Install the exact published browser version in Anvil and regenerate its
    registry lockfile. Update `test/analysis/performance/ty-source.json` to the
    same source revision. Run frontend, installed-package acceptance and
    completion-performance checks before merging. Keep `ty-analysis` off by default.

The browser workflow builds both WASM modules, tests the installed package in
Chrome and uploads an npm archive. It has no npm credentials and never publishes.
The IDE copies the installed package, including lazy packs and licence notices,
under a versioned URL. Its Docker build needs neither Rust nor a sibling checkout.
The native validation workflow remains separate.

## Independent Ruff browser package

`anvil/ruff-browser` builds `@anvil-works/ruff-wasm-web` from the pinned,
unmodified upstream release with size-focused optimisation. It has its own
upstream-based package version and does not require a Ty or native-checker release.
Run `pnpm build`, `pnpm test` and `pnpm pack` there; inspect `build.json` and test
the packed package before Stu publishes it. Its build verifies the upstream
archive checksum; prepack verifies the package inputs and generated output hashes.

## Native release snapshot — 20 October 2026

The checker branch is rebased onto upstream Ruff `main` at `15d1c4116f`; the CLI
branch includes Anvil CLI `master` at `23a534b`. The native Cargo lockfile has been
refreshed for upstream's crate version bump. Bundled API stubs are regenerated
from Anvil `master` at `edfeb809fd`, including `HtmlComponent.attrs`.
The checker candidate remains
`0.1.0-canary.0`; that native package family has since been published. The proposed CLI
version remains `0.8.0-canary.23` and passes its registry version guard. Recheck
availability immediately before publishing.

This native release snapshot predates the browser integration. The browser branch
also exposes generic engine APIs and completion optimisations;
[ENGINE_PATTERNS.md](ENGINE_PATTERNS.md) describes the current differences.
Inference and diagnostics remain upstream. The old method-assignment and built-in
division patches have been removed. See [ENGINE_PATTERNS.md](ENGINE_PATTERNS.md) for the
accepted limitations. Earlier packages and diagnostic reports include those
patches; rebuild release artifacts from the cleaned source before publication.

The checker honours agent-host's `ANVIL_API_STUBS_PATH` for both client and server
API stubs, including designer generation. Agent-host supplies its own generated
snapshot independently of the checker package version.

## Review the sources

| Checkout                                   | Branch                               | Purpose                                                |
| ------------------------------------------ | ------------------------------------ | ------------------------------------------------------ |
| `/Users/scork/Desktop/Projects/anvil-ruff` | `anvil`                              | Ruff fork, adapter, stubs and all six checker packages |
| `/Users/scork/Desktop/Projects/anvil-cli`  | `stu-dev/cli/ty-validation`          | CLI integration and startup changes                    |
| `/Users/scork/Desktop/Projects/anvil`      | Independent Anvil development branch | API stub source: `doc/anvil-api-stubs/source/`         |

Read these paths in order:

1. CLI `src/validatePython.ts`: executable selection, process handling and diagnostics.
1. Fork `anvil/native/src/main.rs`: preparation and separate client/server ty databases.
1. Fork `anvil/native/src/forms.rs` and `anvil/compat/src/forms.rs`: native
    loading and shared Designer declarations. Read native `handles.rs`,
    `environments.rs` and `policy.rs` for event bindings, imports and runtimes.
1. Fork [ENGINE_PATTERNS.md](ENGINE_PATTERNS.md): accepted upstream typing limitations.
    Review `git diff main -- crates` against its documented engine differences;
    they expose existing engine behaviour rather than Anvil inference rules.
1. CLI `src/cliProgram.ts`, `src/programBase.ts`, `src/commands/validate.ts`,
    `src/services/depsCache.ts` and `src/CLILogger.ts`: startup and command loading.
1. Fork `anvil/package.py`, `anvil/collect_release.py`, `anvil/npm/package.json`
    and `anvil/npm/index.cjs`: packaging, release consistency and platform selection.
1. Fork `anvil/tests/` and CLI validation/startup tests.

The old wrapper's Git history is preserved locally at
`/Users/scork/Desktop/Projects/anvil-ty-wrapper-history.git`, including its
`stu-dev/ty/development-archive` branch. Private drafts, trial artifacts and
preserved worktree caches are under `anvil/dist/`. These are historical evidence,
not publication artifacts. Rebuild from the selected `anvil` commit.

## Push the checker and obtain its packages

Keep the checker changes on `anvil`; leave `main` tracking upstream.
The checker remote `origin` is `https://github.com/anvil-works/ruff.git`.
`upstream` is Astral's Ruff repository. The personal `fork` remote is retained
for separate upstream contributions; Anvil releases use `origin`.

```sh
cd /Users/scork/Desktop/Projects/anvil-ruff
git status --short
git branch --show-current       # Should be anvil.
git remote -v
git rev-list --count main..anvil  # Should be 1.
git rev-parse HEAD              # Record the release source revision.
gs branch submit --branch anvil --no-publish --dry-run
# Inspect the destination, then push the Anvil branch:
gs branch submit --branch anvil --no-publish
```

`--no-publish` pushes the branch without creating a PR; it does not publish npm packages.

A push to `anvil` affecting the adapter, engine or build configuration starts
[anvil-release.yml](../.github/workflows/anvil-release.yml). The workflow leaves
upstream Ruff release machinery unchanged. It builds/tests macOS ARM64/Intel,
Linux GNU ARM64/x64 and Windows x64. Linux uses a pinned Rust 1.99 Debian 12
container; binaries require glibc 2.34 or newer. Alpine/musl is unsupported.

Each build installs the actual npm archives and relocates them to a path with
spaces. Smoke checks cover imports, forms, row models, custom events,
client/server restrictions and UTF-16 diagnostics. Collection verifies clean,
identical source snapshots, versions and bundled-file hashes before producing
one wrapper and five native packages, with `RELEASE.json` and `SHA256SUMS`.
Windows and Intel Mac still require their first successful runner execution.

```sh
gh run list --repo anvil-works/ruff --workflow anvil-release.yml --branch anvil
# Replace RUN_ID and select a fresh output directory.
gh run download RUN_ID --repo anvil-works/ruff --name anvil-ty-release --dir anvil/dist/release-candidate
cd anvil/dist/release-candidate
shasum -a 256 -c SHA256SUMS
cat RELEASE.json
```

Check that `source_revision` matches the pushed commit. Publish this collected
artifact, not old trial archives or raw per-platform downloads. All checker
npm versions come from `anvil/npm/package.json`. For later releases, update its
version, every optional dependency and the native crate version in
`anvil/native/Cargo.toml` together. Refresh `anvil/native/Cargo.lock` with
`cargo check --manifest-path anvil/native/Cargo.toml` before the locked build.
The current candidate is `0.1.0-canary.1`.

## Publish the six checker packages

From the downloaded directory, inspect each upload:

```sh
npm whoami
version=$(node -p "require('./RELEASE.json').version")
for platform in darwin-arm64 darwin-x64 linux-arm64 linux-x64 win32-x64; do
  npm publish "anvil-works-anvil-ty-${platform}-${version}.tgz" --access public --tag canary --dry-run
done
npm publish "anvil-works-anvil-ty-${version}.tgz" --access public --tag canary --dry-run
```

After review, publish platforms first and the wrapper last:

```sh
(
  set -e
  version=$(node -p "require('./RELEASE.json').version")
  for platform in darwin-arm64 darwin-x64 linux-arm64 linux-x64 win32-x64; do
    npm publish "anvil-works-anvil-ty-${platform}-${version}.tgz" --access public --tag canary
  done
  npm publish "anvil-works-anvil-ty-${version}.tgz" --access public --tag canary
)
```

The block stops on failure. npm cannot publish six packages atomically. If an
upload is interrupted, publish only the remaining archives at the same version,
keeping the wrapper last. Verify a fresh install of the exact wrapper version.

## Finish the CLI lockfile and publish its canary

The CLI already declares `@anvil-works/anvil-ty` at `0.1.0-canary.0`. Its registry
lockfile must be regenerated after checker publication. Source proposes
`0.8.0-canary.23`; recheck availability before publishing. Older trial CLI
archives carry the already-published `.22` and must not be uploaded.

```sh
cd /Users/scork/Desktop/Projects/anvil-cli
pnpm install --lockfile-only
pnpm install --frozen-lockfile
pnpm typecheck
pnpm build
source tests/setup-test-env.sh
PATH="/opt/homebrew/bin:$PATH" pnpm rstest run \
  --include 'tests/{validatePython,validateHtml,cli.json-startup,cli.dispatch,CLILogger.interactive}.test.ts'
npm_config_tag=canary node scripts/validate-release-version.mjs
npm pack --dry-run
```

The explicit test include selects the current checkout's tests, including when local
`.scratch/` notes contain copies of older source trees.

Check that the lockfile contains the native packages and no Pyright dependency.
Commit and push the generated lockfile, plus any required version change. Before
publishing, check `git status --short`: pnpm also counts untracked files. Private
research notes can remain in `.scratch/` with `/.scratch/` added to the local
`.git/info/exclude`; keep them out of the release commit. Review any remaining
changes before publishing.

Use the `stu-dev/cli/ty-validation` branch in the CLI checkout:

```sh
git branch --show-current  # Should be stu-dev/cli/ty-validation.
git add pnpm-lock.yaml package.json
gs commit create -m "Prepare native validation canary release"
gs branch submit --branch stu-dev/cli/ty-validation --no-publish --dry-run
gs branch submit --branch stu-dev/cli/ty-validation --no-publish
git status --short
pnpm publish --tag canary --publish-branch stu-dev/cli/ty-validation --dry-run
pnpm publish --tag canary --publish-branch stu-dev/cli/ty-validation
```

The CLI's own `PUBLISHING.md` remains authoritative for release policy. Install
its exact canary in a clean directory and exercise valid/error controls before
updating agent-host dependencies. Once that acceptance passes, merge the CLI
changes into its `master` branch and prepare a stable release under its normal
version policy. Keep the checker fork on `anvil`; publishing as `latest` and
production rollout are subsequent decisions.

## Local checker builds

Use Rust 1.99.0, Python 3.11+ and Node/npm. Run from the fork root with a fresh
output directory:

```sh
cargo build --manifest-path anvil/native/Cargo.toml --release --locked
cargo test --manifest-path anvil/native/Cargo.toml --locked
python3 anvil/package.py --output anvil/dist/local-candidate/bundle
ANVIL_RELEASE_PACKAGES=anvil/dist/local-candidate python3 anvil/tests/test_release_smoke.py -v
```

On Windows use `python`. The packager selects its host OS/CPU and the `.exe`
extension automatically. Package binaries on their matching target host.
