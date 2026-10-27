# Native Anvil validation

The Rust backend for `anvil validate` prepares Anvil metadata and runs ty in
process. API stubs travel with the executable. The current canary trial has been
tested on macOS ARM64 and Linux GNU ARM64/x64. Linux x64 was exercised under
emulation; measured Linux performance is ARM64 only. Windows and Intel macOS
builds, release publication and production rollout are pending. See the
[CLI migration checkpoint](../CLI_MIGRATION.md) for the Linux trials.

The dedicated [Anvil release workflow](../../.github/workflows/anvil-release.yml)
builds and tests all five npm platforms and collects one consistent package set.
It has no publication credentials: download the result and publish locally using
the [publication guide](../PUBLISHING.md).

## Run

From the anvil-ruff checkout, with a built sibling anvil-cli:

```sh
cd anvil/native
cargo build --release --locked
cd ../..

ANVIL_TY_TEST_EXECUTABLE="$PWD/anvil/native/target/release/anvil-ty-native" \
  python3 -m unittest discover -s anvil/tests -v

ANVIL_TY="$PWD/anvil/native/target/release/anvil-ty-native" \
  node ../anvil-cli/dist/cli.js --json validate /path/to/app

.venv/bin/python anvil/benchmark.py --runs 5 \
  --native "$PWD/anvil/native/target/release/anvil-ty-native" \
  --output anvil/reports/native-local.json
```

The crate pins Rust 1.99.0 and uses the engine's release settings: fat LTO, 16
codegen units, with single-unit parser, AST and Salsa overrides. Its lockfile starts
from the Ruff lockfile. An unbundled development executable uses the
generated API stubs in `anvil/api-stubs/`. A
bundled executable prefers `../share/anvil-typeshed` relative to its own location.
No compiled JavaScript generator is loaded by the native executable. Python and
Node remain necessary for the development tests, benchmark harness, and existing
CLI respectively.

### API stub source and regeneration

Edit API stubs in the sibling Anvil checkout at
`../anvil/doc/anvil-api-stubs/source/`. That directory is the source of truth.
Regenerate the native snapshot using Anvil's existing generator:

```sh
node anvil/sync-anvil-stubs.mjs
```

`SOURCE.json` records the Anvil revision and hashes of the authoritative source
files, including any uncommitted stub corrections. Keep generated snapshots in
the fork so a build does not require the private Anvil source checkout.

The native development executable reads that snapshot at validation time;
API stub changes alone do not require rebuilding Rust. Existing standalone
bundles retain their packaged stubs, so create a fresh bundle when updating them.
Do not hand-edit generated snapshots or copies inside a bundle.

## npm packages and standalone bundle

After building the release executable, run from the repository root with Python
3.11 or newer and npm:

```sh
python3 anvil/package.py

# Local installation before the packages are published:
npm install ./anvil/dist/anvil-works-anvil-ty-0.1.0-canary.0.tgz \
  ./anvil/dist/anvil-works-anvil-ty-darwin-arm64-0.1.0-canary.0.tgz
```

The public dependency is **`@anvil-works/anvil-ty`**. Its small JavaScript wrapper
selects a native package such as `@anvil-works/anvil-ty-darwin-arm64`; anvil-cli
then starts the executable directly. The native package contains the binary,
client/server API stubs, licences and provenance manifest. Its version and the
wrapper version come from `anvil/npm/package.json`.

The packager emits both npm `.tgz` archives, ready for local installation or
publication, and records their SHA-256 hashes in its JSON output. It also retains
the standalone folder, `.tar.gz` archive and checksum under `anvil/dist/`.
It refuses to overwrite existing artifacts. `--output` selects
another folder; `--binary` selects a prebuilt native executable. Build that binary
on the target platform before packaging; the platform name records the build host,
not a cross-compilation target detected from the binary.

Keep `bin/` and `share/` together when extracting or moving the bundle. Its static
client/server API stubs, source licenses, usage instructions and manifest
travel with it. The manifest records binary and bundled-file hashes, upstream
revisions and source hashes at packaging time; it does not claim that an arbitrary
supplied prebuilt binary was built from those sources. No source checkout, Rust
toolchain or Python launcher is needed to run the packaged checker. The new
anvil-cli selects it through the npm dependency; `ANVIL_TY` can select a standalone
executable explicitly. Existing cached Anvil dependencies and
optional Python libraries remain app/environment inputs.

`tests/test_packaging.py` exercises the real packager, installs both npm archives
offline and resolves the executable through `@anvil-works/anvil-ty`. It also
extracts the standalone archive, removes the original bundle and moves it to a
path containing spaces. Through the real CLI, with the old stub checkout
unavailable, it verifies a
valid generated form, an invalid component assignment, original paths, UTF-16
ranges, file targeting and source immutability. The original relocation trial ran on macOS ARM64. Linux GNU ARM64/x64 npm
installation and relocation controls now also pass; published release automation
remains future work.

Packaging, benchmark, parity and corpus harnesses use the same engine snapshot:
the Ruff revision, its complete tracked patch against HEAD and the patch SHA-256.
Untracked engine files are rejected because they would be absent from that patch.
This records local experiments; distribution still requires a published engine
commit on the Ruff fork's `anvil` branch. Existing reports and bundles retain their
historical source records.

The [release-bundle evidence](../reports/native-standalone-packaging.json) verifies
69 bundled file hashes, byte-identical archive reproduction, overwrite refusal
and success/error controls using the installed CLI. All 17 focused native and
packaging tests pass against the packaged release. The
[packaged five-app corpus](../reports/native-standalone-app-corpus.json) preserves
the previous complete native diagnostic results and input fingerprints. Full
differential/performance reports below retain their pre-packaging binary hashes.

## Implementation and boundary

One executable parses the app YAML, reads source files once, generates basic form
designer declarations, mounts source and static stubs into ty's in-memory
filesystem, and checks two separate client/server databases. Client imports cannot
see server source. Server imports see the client namespace overlaid with server
code. It uses ty's regular project checker, default diagnostic rules, and one-shot
CLI optimizations. It converts diagnostic positions directly to UTF-16 using
ty's source index and emits the existing CLI JSON contract with original file
paths. Anvil policy stays outside the unchanged upstream engine. Accepted typing
limitations are described in [engine compatibility](../ENGINE_PATTERNS.md).

The native checker spawns no child processes and writes no temporary source or
stub files. Unlike the first adapter, it has no Python launcher, Node metadata
process, two ty child processes, GitLab JSON translation, or staging cleanup.

Supported inputs include ordinary client/server Python modules, YAML/HTML package
and module forms, built-in/nested components, local custom component references,
typed DOM references, custom properties/constructor keywords, bound/custom events,
basic data bindings, layouts/slots and schema/model-typed items. Native schema
preparation generates typed tables, linked rows and query/write signatures; Users
and Google Drive metadata retain app-specific row/file types. HTML frontmatter
and legacy YAML `HtmlTemplate` DOM references are covered. Static API stubs are
reused. The proof requires a simple app package identifier.

### Property and runtime contracts

Native validation and the IDE share Anvil runtime checks in `anvil/compat`:
duplicate callable/background-task names, portable-class placement, navigation
from `show` handlers, and unsupported Skulpt syntax. Registration checks include
other modules when validating one file. Duplicate detection follows the IDE's
static catalogue of module-level functions in Server Modules; methods, nested
functions and dynamic registration names do not establish known collisions.
API references are resolved through Ty, so aliases work and unrelated user
functions do not trigger Anvil warnings.
Row-model keyword errors use the API stub's explicit `__init_subclass__`
signature and ordinary Ty argument diagnostics.

Python-defined members take precedence over designer property declarations.
Their getter, setter, class-field and constructor annotations determine the types;
unannotated implementations retain ty's ordinary permissive checking. Designer
metadata supplies types for properties without a Python definition. `themeRole`
maps to `str | list[str] | None`, regardless of the property name. Typed property
keywords retain their names, but Python-owned values are not constrained by the
designer's input format. Overrides of actual Python base properties remain checked.

`get_design_component` preserves the component class passed to it, allowing
subclasses to retain their inherited API checks.

Server checking selects Python from `runtime_options.server_spec.base`: public
`python312`, `python313`, `python314` and the four `python310-*` images map to their
registered versions. The two `python37-*` legacy images select 3.7. An explicit
`pythonVersion` in the existing JSON/TOML configuration takes precedence for server
checking and describes custom or redefined image IDs. Unknown image IDs require
that setting. Client checking remains at 3.10. Apps without image metadata retain
the previous 3.10 approximation; exact support for older sandbox/Python 2 runtimes
is outside this migration.

The real-CLI property, class-preservation, runtime and relocated-bundle tests cover
these contracts, including invalid values and a server type alias without an
available host Python interpreter.

String-key column names, including spaces, keywords, quotes and Unicode, retain
their declared indexing and buffered-change types. Typed keyword dictionaries
support queries, add_row and update when column names cannot be parameters.
Other unsupported generated Python identifiers are rejected explicitly. The native
backend checks Skulpt imports, import spelling, unknown callable/task names and
false decorator origins. Cached dependency code and forms share the same native
preparation path; discovery follows package/directory hints with a legacy fallback,
and server namespaces overlay client modules. Validation never fetches dependencies.

Anonymous runtime component names such as `$component_1` do not generate Python
attributes; their named descendants and event targets remain available. The first
[real-project trials](../VALIDATION_PARITY.md#real-project-trials) exposed this
preparation failure and now record 13 selected projects, controlled local
dependency fixtures and remaining developer-noise priorities. The
`anvil-ty-native-0.1.0-macos-arm64-project-trials` bundle includes this fix; the
original standalone trial bundle is preserved as its earlier checkpoint.

`@anvil.handle` checks literal component/event targets against form metadata.
Missing components and invalid events warn by default; the
`reportAnvilUnknownComponent` and `reportAnvilInvalidEvent` settings can promote
them to errors or disable them. Nested/slotted components, layout and form
targets, inherited events, declared custom-component events, imported decorator
aliases are supported. All event names starting with `x-` are accepted, including
names not declared in YAML. Dynamic expressions and code-only custom component events
remain unproven. The native check deliberately fixes the baseline CLI's missed
missing-component warning.

Chained JSONC/TOML configurations preserve base settings and child overrides;
JSON takes precedence and ancestor TOML discovery is supported. Severity settings
cover false decorators, variable/attribute assignments, argument/return types,
undefined names, call binding, method overrides, missing imports and unused
type-ignore comments. Invalid parameter defaults use argument policy; abstract
instantiation follows its own setting. Optional-value errors use ty's native rule
categories and the corresponding ordinary mapped settings. Independent Pyright
`reportOptional*` settings are outside the migration contract.
Inline/file-level `type: ignore` comments suppress
runtime checks and can be disabled; rule-specific `pyright: ignore` applies the
tested mappings and preserves unrelated diagnostics. The tested `off` mode retains
runtime import restrictions and explicit mapped rule overrides. Whole-app selection
and explicit targets honor include/exclude rules; ignore suppresses diagnostics
while preserving imported types. Other modes,
multiline suppressions and broader rule/glob mappings remain unproven.
See [validation parity](../VALIDATION_PARITY.md) for differential evidence and
the remaining contracts.

Project stubs load from `typings/` or a configured `stubPath`, replacing the default
when explicit. They retain declared types; ty does not reproduce Pyright's
missing-runtime-source warning for stub-only libraries. Explicit `extraPaths` and
`venvPath`/`venv` resolve external libraries through read-only disk access, while
Anvil source and generated declarations remain in memory. Configured paths retain
their declaring configuration directory. `PYTHONPATH`, host and activated
environments also retain library types. CPython Unix/framework user-site paths
honor `PYTHONUSERBASE` and `PYTHONNOUSERSITE`; explicit virtual environments remain
isolated from user-site packages. Homebrew `libexec/bin` interpreter symlinks are
normalized before ty discovers their installation prefix. Windows user-site layout
and virtual environments opting into system/user sites remain unported.

Absolute imports prefer standard-library stubs over same-named app shims,
matching Pyright. Relative and qualified imports still reach the app's own
modules. A separate in-memory search root preserves bare app imports and their
runtime restrictions. Bare imports re-export canonical definitions so class
identity is preserved; direct private imports and `__all__` are covered. Existing
ty package-local fallback is enabled through in-memory metadata markers and
retains independently typed helpers in different packages. Layout form event
bindings require implementations in
both YAML and HTML. Legacy array schemas retain the baseline's generic table API
and do not block Python validation; YAML validity remains the CLI's responsibility.

Designer declarations include component attributes, property getters/setters and
typed `__init__`/`init_components` keywords when custom properties are declared.
Forms without custom properties accept `Any` keywords. Bound handler stubs use
flexible signatures to preserve Anvil's permitted overrides, while concrete user
method annotations still govern direct calls. Unannotated handler body arguments
remain unknown in both checkers; explicit sender annotations retain meaningful
checking. Server row-model discovery excludes client modules hidden by server
overlays, preserving schema types when a client model is no longer visible.
Full argument inference and model
corpus equivalence remain unproven. The YAML parser (`serde_yaml`) is an
experiment dependency; choose a maintained parser before packaging a production
adapter. Read the [first proof's parity findings](../README.md) before using this
as a replacement.

Six shared integration cases pass through the real CLI for both adapters: a valid
form/server app without source mutations; a UTF-16 type-error range; a generated
component property type error; file targeting; EOF syntax errors; and forbidden
client imports of server source. Two native-only cases check explicit rejection
acceptance of spaced column names and module forms when
another file is targeted. Version probes prevent silent fallback to Pyright.

The additional differential acceptance suite compares native and anvil-pyright
through the real CLI. It checks messages, rule names, severity, UTF-16 ranges and
exit status for the ported runtime checks, including valid controls. It also covers
form preparation, valid custom properties and meaningful generic type errors.
Generic errors require equivalent severity, file and line, while retaining each
engine's wording and ranges. Run `anvil/parity.py` from the repository root to
preserve its sources and outputs. The pre-packaging release checkpoint contains 114
real-CLI tests, with 227 differential comparisons and explicitly recorded
engine/configuration differences and deliberate native improvements. Native-only
CLI cases live in `test_handles.py`, `test_column_names.py` and `test_packaging.py`.

[Recorded CLI contract results](../reports/native-contract.json) capture the six
shared tests using the native debug build and the first adapter. After normalizing
app paths and timestamps, the complete CLI results match in all six cases. This
includes messages, rules, severities and ranges; performance uses the release
build below.

## Measurement

The [post-review performance summary](../reports/2026-10-09-performance-summary.md)
records the current release on synthetic inputs and six real apps, including
diagnostic differences and the local engine patch. The measurements below are an
earlier checkpoint retained for comparison.

The [earlier full-feature measurements](../reports/native-current-performance.json)
use the same release binary as the 114-test acceptance checkpoint and refreshed
five-app corpus. Each backend receives one warm-up and five measured fresh
processes per input/boundary, with rotating order. Every measured sample has zero
errors and warnings. The report records fixture fingerprints, every native Rust
source, the harness/adapters, CLI bundle, static stubs and release binary, plus
per-sample diagnostics, time and process-tree RSS.
The subsequent packaging build adds bundled stub lookup; these measurements
describe the fingerprinted pre-packaging binary, not the new artifact.

| Python files | Boundary          |  Pyright time / RSS |   Native time / RSS | Speedup / RSS reduction |
| -----------: | ----------------- | ------------------: | ------------------: | ----------------------: |
|           20 | Semantic checker  | 0.562 s / 219.0 MiB |  0.078 s / 44.4 MiB |           7.22x / 79.7% |
|           20 | Full CLI validate | 1.255 s / 299.7 MiB | 0.336 s / 137.2 MiB |           3.73x / 54.2% |
|          200 | Semantic checker  | 0.980 s / 262.8 MiB |  0.139 s / 47.2 MiB |           7.03x / 82.0% |
|          200 | Full CLI validate | 1.861 s / 350.2 MiB | 0.378 s / 146.0 MiB |           4.92x / 58.3% |

These are medians on the same 10/100-form synthetic workloads, with the current
validation features enabled. They do not establish performance on arbitrary
production metadata, incremental editing or cold filesystem caches. Historical
measurements below use an earlier, narrower preparation implementation and a
different run; comparing timings across those batches does not isolate feature
cost.

The benchmark runs Pyright, the Python/Node ty adapter, and this release executable
on the same 10/100-form synthetic inputs, as fresh processes. It measures the
semantic-checker boundary and full `anvil validate` separately. Each backend gets
one warm-up followed by five runs with rotating execution order. It records all
diagnostics, exit statuses, individual samples, executable/source/lockfile hashes,
stub fingerprints, and repository revisions.

Both ty implementations use Ruff commit
`19cb997763936be5bd7f3f791965366a99b3989b`: the native path dependencies and the
submodule pin of the installed ty 0.0.85 release (`d7fc5ef88`). The core type
checker is unchanged. Preparation implementations and generated declarations
differ within the stated feature boundary, so this compares complete pipelines;
it does not isolate JavaScript runtime overhead from generation and filesystem
work.

RSS is the sampled peak sum across the process tree, every 2 ms. Shared pages can
be counted more than once and short peaks can be missed. Filesystem caches are
warm. Results do not establish production-app parity, incremental performance,
or browser/LSP performance.

## Results: 8 October 2026

These are historical measurements of the initial native binary. They do not
measure subsequent runtime checks, forms, schemas, services or row models.

[Pooled summary](../reports/native-summary.json),
[first raw batch](../reports/2026-10-08-native.json), and
[larger-fixture repeat](../reports/2026-10-08-native-repeat.json).

The larger full-CLI batch was noisy, so it was repeated once. The table pools all
samples from both batches without removing outliers: five runs per backend for
20 Python files, ten for 200. All three backends return zero errors and warnings
on these inputs. These are the same 10/100 YAML forms plus 10/100 server callable
modules used by the first proof, on the same arm64 Mac with 32 GiB RAM.

| Python files | Boundary          | Pyright time / RSS | First ty adapter time / RSS | Native time / RSS |
| -----------: | ----------------- | -----------------: | --------------------------: | ----------------: |
|           20 | Semantic checker  |  0.510 s / 219 MiB |            0.239 s / 76 MiB |  0.068 s / 42 MiB |
|           20 | Full CLI validate |  0.883 s / 308 MiB |           0.473 s / 163 MiB | 0.273 s / 134 MiB |
|          200 | Semantic checker  |  0.981 s / 261 MiB |            0.413 s / 82 MiB |  0.098 s / 47 MiB |
|          200 | Full CLI validate |  1.631 s / 354 MiB |           0.777 s / 177 MiB | 0.341 s / 140 MiB |

On the 200-file input, native preparation is **4.22x faster than the first ty
adapter at the semantic-checker boundary**, and **2.28x faster through the full
CLI**. Relative to Pyright, the complete native proof is **10.02x faster for the
checker** and **4.79x faster through the CLI**. Sampled peak RSS falls about 43%
versus the first adapter for the checker, and 21% through the full CLI; the
corresponding reductions versus Pyright are about 82% and 60%.

This supports porting preparation into a native Anvil layer. The remaining CLI
startup and validation work still contributes appreciable cost. Full metadata
generation and checker-feature parity will add work beyond this bounded proof;
these figures are not a projection for an arbitrary production app.

## Follow-up

The [phase profiles and targeted experiments](../profiling/README.md) locate the
remaining cost: CLI startup dominates, with lazy prompt/spinner imports giving a
measured further improvement in a throwaway loader prototype.

Use the measured pipeline benefit to decide how far to port Anvil metadata
preparation. Add each remaining feature behind a failing real-CLI acceptance case,
using the existing Anvil generator/checker as the compatibility oracle. Keep
standard stubs and module layout ahead of engine hooks. Package the static stubs
independently before distributing this executable. LSP integration remains a
separate project.
