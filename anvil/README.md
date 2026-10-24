# Anvil validation proof

This directory contains Anvil's native Python checker, built on ty in this Ruff
fork. It replaces the semantic-checker subprocess used by `anvil validate`.
The CLI continues to validate YAML and HTML structure. See
[VALIDATION_PARITY.md](VALIDATION_PARITY.md) for supported Anvil behaviour and
accepted differences from Pyright.

The older JavaScript/Python proof and its measurements are retained below as
historical evidence. Current implementation and release instructions follow.

## Current checker

The maintained implementation is the native adapter in `anvil/native/`, using
upstream engine crates from this Ruff repository. The `anvil` branch
contains the Anvil changes above upstream `main`. See [native/README.md](native/README.md) for its
behaviour and [PUBLISHING.md](PUBLISHING.md) for build and release instructions.
The JavaScript/Python proof below is retained for historical comparisons and
still needs anvil-pyright's compiled generators. Production packaging does not.

Inference patches used in earlier trials have been removed. The browser adds
only generic callable-parameter metadata to signature help. See
[ENGINE_PATTERNS.md](ENGINE_PATTERNS.md) for accepted upstream typing limitations;
historical diagnostic counts and packaged binaries describe their recorded sources.

Browser IDE integration is being developed in [browser/](browser/README.md).
It uses upstream ty WASM and shares portable Anvil declarations with the native
adapter through `anvil/compat`. The browser's supported slice and outstanding
compatibility work are recorded separately from CLI validation parity.

## Historical proof: run locally

The development layout has sibling `anvil-ruff`, `anvil-pyright` and `anvil-cli`
checkouts. The latter two need their existing builds and dependencies. The proof
loads generators from anvil-pyright's `packages/pyright-internal/out/`; rebuilding
those TypeScript sources changes the proof's input. It does not run Pyright to
prepare an app.

From `anvil-ruff`:

```sh
uv venv .venv
uv pip install --no-config --python .venv/bin/python ty==0.0.85 psutil==7.2.2
ANVIL_TY_TEST_EXECUTABLE="$PWD/anvil/anvil-ty" \
  .venv/bin/python -m unittest discover -s anvil/tests -v

ANVIL_PYRIGHT="$PWD/anvil/anvil-ty" \
  node ../anvil-cli/dist/cli.js --json validate /path/to/app
```

`ANVIL_PYRIGHT_ROOT` overrides the sibling anvil-pyright location. The launcher
uses the repository's `.venv`, so activating it is unnecessary. The pinned
prebuilt ty release is used for this experiment; no Rust engine changes or
source-build performance claims are involved.

Tests now default to the native debug executable; build it with
`cargo build --locked --manifest-path anvil/native/Cargo.toml` first. To run the
original adapter's shared tests explicitly, set
`ANVIL_TY_TEST_EXECUTABLE="$PWD/anvil/anvil-ty"`. Native-only tests use the
executable's version capability rather than its filename.

## How the proof works

`prepare.cjs` reuses the existing Anvil API stubs and form/table/users/Drive stub
generators. It stages code under the app's Python package name in temporary
workspaces. Client and server checks run separately with their respective stubs;
the client workspace contains no server source. Source apps are left untouched.

`validate.py` invokes native ty, translates GitLab-format diagnostics to the
CLI's Pyright-shaped JSON contract, and maps temporary paths back to source files.
It preserves error/warning severities and converts Unicode scalar columns to
UTF-16 source ranges. Rules retain ty's names. `anvil-cli` continues to handle
YAML/HTML structure validation, diagnostic grouping and exit status.

This separation lets us evaluate the engine using existing Anvil metadata logic.
Distribution needs independent packaging of those generators or a port; the
proof still requires Node and anvil-pyright's compiled internals.

## First measurements

[Raw samples and diagnostic results](reports/2026-10-08.json), measured on
8 October 2026 on an arm64 Mac with 32 GiB RAM, using ty 0.0.85 and
anvil-pyright 0.0.4-canary.3. Each number is the median of five fresh processes,
after one warm-up, alternating backend order. Filesystem caches are warm.

| Input                         | Measurement       | Pyright time | ty proof time | Speedup | Pyright RSS | ty proof RSS |
| ----------------------------- | ----------------- | -----------: | ------------: | ------: | ----------: | -----------: |
| 10 YAML forms + 10 services   | Semantic checker  |      0.565 s |       0.243 s |   2.32x |     218 MiB |       77 MiB |
| 10 YAML forms + 10 services   | Full CLI validate |      0.931 s |       0.491 s |   1.90x |     302 MiB |      165 MiB |
| 100 YAML forms + 100 services | Semantic checker  |      1.019 s |       0.402 s |   2.53x |     259 MiB |       82 MiB |
| 100 YAML forms + 100 services | Full CLI validate |      1.323 s |       0.691 s |   1.92x |     351 MiB |      175 MiB |

Both backends return zero errors and warnings on these synthetic inputs. The
semantic-checker measurement includes preparation, adapter startup and both ty
processes. The full CLI measurement also includes CLI startup, executable probing
and YAML validation. These inputs demonstrate a working slice, not validation
parity or representative production-app performance.

RSS is the highest sampled **sum of resident memory across the command's process
tree**, sampled every 2 ms. Shared pages may be counted more than once and brief
peaks may be missed. It is neither a V8 heap figure nor exact unique physical
memory. Cold-cache, incremental editor and browser/WASM performance are unmeasured.

The existing `anvil_memory_app` fixture also ran in the initial report. That
recorded Pyright build passes; ty reports six
unresolved HTML-component attribute assignments (`disabled` and `text`). Its
timings remain in the raw report, but are excluded from the table because the
validation results differ.

The baseline fixture's in-checkout success was caused by the parent
`pyproject.toml` ignoring/excluding `packages/`. Current differential tests copy
the actual fixture outside that configuration; both checkers then reject its six
DOM-only attribute assignments. Its original timing remains excluded. Synthetic
benchmark apps already ran in temporary directories outside the checkout.

Repeat the measurements:

```sh
.venv/bin/python anvil/benchmark.py --runs 5 \
  --app ../anvil-pyright/packages/pyright-internal/src/tests/benchmarkData/anvil_memory_app \
  --output anvil/reports/local.json
```

The report records exit codes, diagnostics, individual samples, repository
revisions and versions. New runs also fingerprint the baseline bundle and compiled
Anvil generator modules. Recheck diagnostics before interpreting timings.

## Compatibility evidence and remaining work

Six shared real-CLI integration tests cover a valid app with a YAML form and server
decorator, a type error with original paths/UTF-16 ranges, EOF syntax errors,
single-file targeting, generated component property types, and a client import of
a server module. The adapter's
version probe is checked explicitly to prevent the CLI falling back to Pyright
and producing a misleading green test.

[Additional diagnostic probes](reports/parity-probes.json) include their source
inputs and both outputs. Two concrete losses are already visible: the proof misses
Pyright's unknown-server-call warning and its unsupported Skulpt import error.
Those two losses are now addressed in the native backend, with explicit
differential tests; this adapter retains its original limitations.
The RPC argument and handle-component probes were accepted by both backends;
those observations are inconclusive and must be replaced with cases from existing
integration tests before assessing those features.

| Area                              | Current evidence or limitation                                                                                                           |
| --------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| CLI transport                     | Real `anvil validate` accepts the adapter; source paths, ranges and file targeting are tested.                                           |
| Ordinary Python typing            | Valid and invalid examples work; comprehensive equivalence is unproven.                                                                  |
| API environment separation        | Client/server stubs are reused; one forbidden client import is tested.                                                                   |
| Form templates                    | Basic package YAML forms are tested. HTML attribute behaviour differs. Module forms and complex form-reference context remain unproven.  |
| Data tables, users and Drive      | Existing generators are reused. Model registration and behavioural parity are unproven.                                                  |
| Server callables/background tasks | Decorator API stubs resolve; custom tracking, call validation and unknown-call diagnostics are not ported.                               |
| Events and constructors           | Generated declarations are present; Anvil checker hooks and special diagnostic policy are not ported.                                    |
| Runtime restrictions              | Skulpt import restrictions are missing; other Anvil import policies require explicit coverage.                                           |
| Dependencies                      | Local dependency-cache resolution is missing; declared dependencies produce an app-level proof-limit warning. No network fetch occurs.   |
| Configuration                     | The proof assumes Python 3.10 and a simple app package identifier. Pyright configuration, suppressions and rule policy are not migrated. |
| LSP/browser                       | Future work; no Anvil-specific changes in this milestone.                                                                                |

## Next validation slice

The native backend now has the first runtime checks and a differential CLI
acceptance suite. Follow [the validation parity plan](VALIDATION_PARITY.md) for
the current contract inventory and next TDD slices: richer forms, tables/services,
dependencies and diagnostic policy. Establish corpus equivalence before reporting
an overall replacement speedup. Packaging still needs independently distributed
stubs and metadata preparation.

The maintained fork is `anvil-works/ruff`, with the adapter and engine in the
same checkout and source revision. `anvil-works/ty` and its old Ruff submodule
are no longer the publication source.
