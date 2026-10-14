# Native CLI migration checkpoint

The local npm-installed CLI uses the native checker by default and contains no anvil-pyright package. Nothing has been published to npm.

## Source and branches

- CLI: `/Users/scork/Desktop/Projects/anvil-cli`, branch `stu-dev/cli/ty-validation`. The CLILogger startup change has its own commit; checker migration and command loading follow it.
- Checker source: `/Users/scork/Desktop/Projects/anvil-ruff`, branch `anvil`, remote `origin` at `anvil-works/ruff`. Engine, adapter, stubs and packaging share one commit above upstream `main`. See [PUBLISHING.md](PUBLISHING.md) for the release order.
- Personal upstream PR branches retain `s-cork/ruff` as their separate destination. No third upstream PR was opened.
- The old wrapper history is archived at `/Users/scork/Desktop/Projects/anvil-ty-wrapper-history.git`. Historical reports remain on its `stu-dev/ty/development-archive` branch. Private drafts and caches are under `anvil/dist/`.
- Authoritative `get_design_component` correction is now present on Anvil master in `dd56b9b25b`; this turn made no commits in Anvil.

## Behaviour

- `get_design_component` preserves the input component class, rejects an instance argument, and retains inherited member checks.
- Python-defined form members supersede designer declarations. Constructor and property annotations govern runtime values; unannotated implementations retain ordinary ty checking. Metadata still types properties without Python definitions. Real base-property overrides are checked.
- The designer type `themeRole` accepts `str | list[str] | None`, including on properties with other names.
- Server versions follow registered public image IDs; explicit JSON/TOML `pythonVersion` describes custom or redefined images. Unknown IDs require it. Client checking stays at 3.10. Missing image metadata retains the previous 3.10 approximation.
- API assets are generated with Anvil’s existing generator into the fork. Source revision and file hashes are recorded; packaging no longer requires anvil-pyright.
- The CLI resolves the platform executable from the npm package and spawns it directly. `ANVIL_TY` and `ANVIL_TY_TIMEOUT_MS` are supported; existing checker/timeout overrides remain for migration scripts. V8 heap handling was removed from semantic validation.

## Validation

The checks and measurements below describe earlier source snapshots. After the
upstream refresh and worktree consolidation, the native adapter passes
`cargo check --manifest-path anvil/native/Cargo.toml --locked`. Release artifacts
must be rebuilt from the consolidated source before publication; the older local
archives do not establish validation or performance for this revision.

- 180 real-CLI acceptance cases passed before the final argument-grouping refactor. Focused property/runtime/dependency cases were rerun after it.
- 41 CLI tests passed, as did the 3 existing startup tests, TypeScript checking and the CLI build.
- Native Clippy with warnings denied passed for the adapter. The existing unfulfilled lint expectation warning in the upstream parser dependency remains.
- Relocated bundle checks passed, including generated forms, invalid assignments, UTF-16 ranges, file targets and unchanged inputs.
- The packager now emits installable npm archives for `@anvil-works/anvil-ty` and the matching platform package. Offline installation of those archives passed the real CLI's valid-form and invalid-assignment controls, including paths containing spaces.
- Fresh npm installation in `/tmp/anvil-ty-installed-cli` succeeded. It resolves the native engine without overrides and includes no Pyright package.

## Real-app performance

Five fresh processes per checker and CLI case, warm caches, alternating order. RSS is peak memory of the process tree. Both CLI comparisons use a 768 MiB Node heap limit. These apps have different diagnostics across the two engines; timings do not establish complete semantic parity. All original app inputs were unchanged.

| App                | Pyright CLI | Native CLI | Speed | Less peak RSS | Native diagnostics before → now |
| ------------------ | ----------: | ---------: | ----: | ------------: | ------------------------------: |
| tests_runtime_v3   |      1.766s |     0.404s | 4.38× |         57.0% |                       188 → 188 |
| anvil-extras       |      2.487s |     0.553s | 4.50× |         61.1% |                       394 → 318 |
| tabulator          |      1.192s |     0.257s | 4.64× |         57.4% |                         57 → 56 |
| ExampleTabulator   |      1.070s |     0.265s | 4.03× |         59.2% |                           5 → 5 |
| Routing_API_Design |      1.412s |     0.296s | 4.77× |         59.0% |                         63 → 62 |
| material-3-theme-2 |      2.247s |     0.400s | 5.62× |         56.9% |                       483 → 483 |

Measurements used the release artifact before the final call-input grouping tidy-up. The manifest records that exact binary and source snapshot. The diagnostic reductions in Extras come from removing artificial designer restrictions on Python-owned property inputs, with typed-property negative controls retained; Tabulator loses one false override, and Routing loses one unsupported-base warning.

Full measurements and diagnostic outputs: `anvil/reports/2026-10-13-cli-native-performance.json` in the archived wrapper history.

## Linux agent-host validation — 13 October 2026

Linux GNU ARM64 and x64 release packages have now been built and installed from
npm archives in disposable agent-host containers. Both passed 17 focused Anvil
contract tests. Fresh installations select their own native package with no checker
overrides or source checkout; valid/error/edit controls and relocation of the whole
installation to a path containing spaces passed. The x64 checks ran under Docker
emulation on an ARM Mac and are functional compatibility evidence only.

Linux ARM measurements used the current agent-host image (Node 26.10.0), two CPUs,
1 GiB container memory and the existing 256 MiB Node heap limit. The six real apps
were 4.8–6.6 times faster than the Pyright backend, with 51–54% less peak validation
process-tree RSS. These are direct validation commands, not full agent/eval runs.
Native outputs exactly match the previous macOS corpus after path normalisation.
The startup change's Linux timings were variable on larger apps; the paired
follow-up and primary measurements are both retained.

The x64 trial's npm 11.19.1 failed during packing/installing under Node 26.5.0.
Those npm operations succeeded using Node 24.18.0; validation and the 17 contract
tests still ran under Node 26.5.0. No fork code change was needed. The x64 compiler
also needed `libc6-dev-amd64-cross` alongside `gcc-x86-64-linux-gnu`.

Artifacts: `anvil/dist/linux-validation-2026-10-13` in this checkout. Measurements
and logs: `anvil/reports/2026-10-13-linux-agent-host-summary.md` in the archived
wrapper history. Packages are local trial artifacts; npm publication, the CLI
registry lockfile update and production rollout remain pending.

## Before release

- Windows path-to-module conversions now share a separator-independent implementation. Linux package metadata now restricts installation to glibc, and source manifest paths use forward slashes on every platform. The dedicated `anvil-release.yml` workflow builds/tests/packages all five targets and produces one download for local publication. Windows and Intel Mac still need their first runner execution. Native Linux x64 performance remains unmeasured; this is separate from compatibility validation.
- Publish the platform packages and wrapper together, then regenerate the CLI pnpm lockfile. Its package.json declares the proposed canary; the lockfile still contains the old published dependency until the new package is available.
- Push the reviewed source branches and rebuild packages from them. CLI source proposes `0.8.0-canary.23`; existing local CLI trial archives carry the already-published `0.8.0-canary.22` and must not be published.
- Existing accepted ty/Pyright differences, including unannotated return inference and DOM coercion checks, remain. This work makes no LSP changes.
