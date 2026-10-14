# Validation parity

The current integration uses unchanged upstream ty. Generic engine patches from
some historical checkpoints below have been removed; see
[ENGINE_PATTERNS.md](ENGINE_PATTERNS.md) for the accepted typing limitations.
Earlier diagnostic counts and performance results apply to their recorded builds.

The native backend is the implementation target for Anvil validation compatibility.
The Python/JavaScript adapter remains the original comparison experiment. CLI
startup optimizations and Anvil-specific LSP support are deferred.

The [current developer-diagnostic triage](DIAGNOSTIC_TRIAGE.md) assesses the six-app
post-review release corpus, records reduced valid/invalid controls, and identifies
the next source-stub and generic engine corrections separately.

## Migration scope

The migration preserves the existing CLI contract, Anvil metadata and runtime
checks, correct imports and useful Python type checking. ty supplies the general
typing semantics. Exact Pyright wording, diagnostic grouping, checking-mode
presets, first-parameter naming lints (`reportSelfClsParameterName`) and independent
optional-only settings are outside this contract. Prioritize demonstrated typing
errors and failures on valid Anvil apps when considering engine improvements.

## Acceptance boundary

Run the existing CLI with each backend on the same temporary app. Explicit version
probes prevent silent fallback to a bundled checker. Differential tests compare
exit status and every issue returned for the selected file or whole app. Directory
results include both global diagnostics and each file's diagnostics. Custom runtime
checks require identical rules, messages, severity, original paths and UTF-16
ranges. Generic type errors compare equivalent failure, severity, original path
and source line; each engine's rule names, wording and ranges are retained in the
report. Success cases require zero issues or warnings. The tests use real files,
real checkers and the real CLI.

Known differences have explicit expected results for each checker and an
explanation in the report. Passing these regression tests means the difference is
understood and retained, not that the results are equivalent.

```sh
.venv/bin/python anvil/parity.py \
  --output anvil/reports/native-validation-parity.json
```

`--backend` selects another native build, such as the debug executable. The report
preserves fixture sources, normalized CLI responses and executable/source hashes.
It checks correctness; historical performance results do not measure the added
checks. The full native suite also includes the earlier CLI transport tests and
explicit preparation-limit tests:

```sh
ANVIL_TY_TEST_EXECUTABLE="$PWD/anvil/native/target/release/anvil-ty-native" \
  .venv/bin/python -m unittest discover -s anvil/tests -v
```

[Pre-packaging release-build checkpoint](reports/native-current-validation-parity.json): all 98
differential tests pass, with 227 app/file comparisons. Eight CLI
transport/preparation cases and eight additional native-only Anvil cases also
pass, giving 114 tests in total. Of the comparisons, 116 match exactly, 96 match
the generic typing contract, and 15 record known differences: eight optional-only
configuration cases, two missing-runtime-source warnings, three comparisons
covering two baseline typing misses, and two deliberate native decorator checks
missed by the baseline CLI.
These differences are explicit rather than counted as equivalence. Rust Clippy
and formatting, and Python lint and formatting checks pass.

[Fresh performance measurements](reports/native-current-performance.json) use
the same release binary and five measured samples per backend/input/boundary.
All measured synthetic inputs have zero diagnostics on all three backends. On
the 200-Python-file input, native checking is 7.03x faster with 82.0% lower sampled
peak process-tree RSS than Pyright; full `anvil validate` is 4.92x faster with
58.3% lower RSS. These are warm-filesystem, fresh-process synthetic medians,
not a performance claim for arbitrary production apps or incremental editing.
The subsequent standalone bundle adds executable-relative stub lookup. Its new
binary is checked separately; the performance and full parity reports above retain
the hashes of their original pre-packaging binary.

## Standalone CLI trials

`package.py` bundles a prebuilt checker, static API stubs, source licenses, usage
instructions and file/source fingerprints into a relocatable folder and archive.
The packaged executable resolves `../share/anvil-typeshed` beside itself; it no
longer needs a sibling anvil-pyright checkout. Unbundled development builds retain
the existing sibling/`ANVIL_PYRIGHT_ROOT` lookup. The packager refuses to overwrite
artifacts and emits a SHA-256 file beside the archive.

The real-CLI packaging case in `tests/test_packaging.py` extracts and relocates the
archive to a path containing spaces and removes the original bundle. With the
legacy checkout path unavailable, it checks a valid generated form, rejects an
invalid component-property assignment, preserves original file/UTF-16 ranges and
does not write to the source app. Build and trial commands are in
[native/README.md](native/README.md#standalone-cli-trial-bundle).

[Release-bundle evidence](reports/native-standalone-packaging.json) verifies all
69 bundled file hashes, a byte-identical rebuild of the archive, preservation of
existing artifacts and valid/error controls through the installed
`anvil 0.8.0-canary.22`. The packaged release passes the 16 existing native
transport/event/schema cases and the new packaging integration case: 17 focused
tests. Rust Clippy/formatting and Python lint/formatting pass.

[Packaged five-app comparison](reports/native-standalone-app-corpus.json) retains
the same inputs and complete native CLI results as the pre-packaging corpus, with
unchanged source fingerprints. Packaging adds no validation behavior changes on
those apps. The 98-test differential suite and performance benchmark were not
rerun for this resource-location change; their existing reports remain tied to the
previous binary.

The [earlier 103-test checkpoint](reports/native-validation-parity.json) and
[earlier corpus](reports/native-app-corpus.json) predate the decorator/string-key
and model-visibility work. They are retained as historical evidence; their old
source/binary fingerprints do not describe the current checker.

## Decorator and string-key follow-up

`@anvil.handle` now warns when a literal component name is absent from the form
metadata (`reportAnvilUnknownComponent`) or a literal event is unsupported by
that component (`reportAnvilInvalidEvent`). Both settings accept `warning`,
`error` or `none`, and selective ignore comments use the existing suppression
path. YAML/HTML metadata is collected alongside designer generation, before
checking, so the baseline CLI's registry timing does not hide these warnings.

Nested/slotted component names, the implicit layout target, inherited show/hide
events, empty-string form targets and declared custom-component events are
handled. All event names beginning with `x-` are accepted, including names not
declared in YAML. Semantic decorator resolution recognises imported aliases and
leaves unrelated decorators with the same name alone. Dynamic argument
expressions are not rejected. Forms without template metadata and code-only
custom component event declarations remain outside the proven event contract.
The event catalog starts from `componentEvents.ts`, with corrections against
the sibling runtime sources for Canvas reset, DataGrid page_changed, TextArea
pressed_enter and Plot deselect. The runtime's `Component.$verifyEventName`
establishes the `x-` exception.

Columns containing spaces, Python keywords, quotes or Unicode no longer fail
preparation. Functional TypedDict declarations preserve buffered-change keys;
tables with non-identifier column names use typed unpacked keyword dictionaries
for writes and queries. Literal row indexing retains its declared return type,
and invalid add_row/update values are rejected in client and server code. Column
attributes are generated only when the name is a valid Python expression name.
Table Python names and other generated identifiers retain their existing guards.

The real-CLI cases are in `tests/test_handles.py` and
`tests/test_column_names.py`. The differential missing-component case explicitly
records the new native warning as a deliberate improvement over the baseline.

Focused verification passes: 25 real-CLI tests against the updated release
executable, covering the new cases, all eight transport/preparation cases and
affected schema/model/Users cases. Five existing configuration/suppression
differential tests also pass against the debug executable. Rust Clippy with
warnings denied, Rust formatting, and Python lint/format checks pass.

[Fresh five-app comparison](reports/native-handle-column-corpus.json) uses the
updated debug executable. Native diagnostic counts are unchanged on every app;
the new handle checks add no warnings on these inputs. All original source
fingerprints remain unchanged. This is correctness evidence, not a timing run.

## Handler inference and model visibility

[Real-CLI inference probes](reports/native-handler-inference.json) demonstrate a
shared limitation: both engines accept an unannotated handler assigning an
integer to `sender.text` and assigning event dictionary values to incompatible
annotations. Both reject incorrect assignments through an explicitly annotated
`sender: anvil.Button`, and accept the annotated valid control. Pyright's
`formDiagnosticSuppressions.ts` removes missing/unknown-parameter diagnostics
for generated handler overrides; it does not infer those body parameter types.
Useful unannotated handler inference is future typing work, not a missing
current CLI contract to reproduce.

Model discovery now follows source visibility. Server model registrations scan
only client modules that are not replaced by server modules, then server code.
A server module replacing a client model module no longer causes generated
table returns to import the hidden class and degrade to unknown types. The
new differential case rejects an incompatible server row-column assignment
and accepts its valid control. Existing visible client-model fallback and
server-specific registrations remain supported.

Further dependency cases prove that identical module/class names in the app
and a cached dependency remain distinct in both environments, with independent
server overlays. Cached custom-component events are read from the referenced
dependency's metadata; valid declared and undeclared `x-` events pass, while an
invalid built-in-style event warns. That extra warning is an explicit native
improvement over the baseline CLI.

## First ported checks

| Contract                                                    | Native implementation                                                                                                              | Differential evidence                                                                                                                                             |
| ----------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Unsupported Skulpt stdlib imports are errors in client code | `checks.rs` visits ty's parsed import statements; ports the existing known-stdlib-minus-supported policy                           | Dotted imports, aliases, `from` imports and nested function imports; supported modules, relative local modules, server imports and stub-only imports remain valid |
| Unknown server callable names produce warnings              | `callables.rs` scans registrations before checking call sites; preserves `call`/`call_s` qualified and `server` shorthand patterns | Known names and dynamic names pass; unknown literals warn with identical ranges, including an emoji before the call                                               |
| Unknown background task names produce warnings              | Separate callable and task registries                                                                                              | Known tasks and explicitly renamed callables in an unselected server module; unknown tasks warn                                                                   |
| Decorators named `callable` must resolve to the Anvil API   | ty's `SemanticModel`, inferred expression type and defining file identify the real API function                                    | Local lookalike decorators warn; genuine imported aliases register without warnings                                                                               |
| False-decorator severity is configurable                    | JSONC configuration reader and a small custom-rule policy                                                                          | Promotion to error changes CLI exit status; boolean `false` disables the warning in a commented config with a trailing comma                                      |

These additions live entirely in `anvil/native`; neither Ruff nor anvil-cli was
modified. Runtime checks reuse ty's parsed modules and semantic queries. Client
and server databases remain separate. The server registration pass also runs for
a client-only target, and diagnostics from unselected files are not emitted.

## Form preparation batch

The native form generator is isolated in `forms.rs`; `dom.rs` ports the existing
HTML tag-to-DOM-type mapping. Both produce ordinary Python declarations consumed
by ty, without engine changes or preparation subprocesses. HTML uses an HTML5
parser; the generator does not attempt to reproduce Anvil's full serialization
parser. The subsequent form batch adds component event bindings, custom events,
basic data bindings, layouts/slots and schema/model-typed items.

| Contract                                 | Differential evidence                                                                                                                                         |
| ---------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| YAML and HTML package/module forms       | Python imports and component attributes resolve, including multiple module forms sharing a designer module with a package form                                |
| Built-in and nested component attributes | Generated declarations expose real Anvil component types; invalid assignments still fail                                                                      |
| HTML named fragments                     | `anvil:name` exposes `HtmlComponent`, with `.html` and `.classes`; DOM-only `.text` is rejected. A sole ordinary root is the form itself                      |
| Typed DOM references                     | `anvil:dom-node` keys retain their element types separately for each form; hyphenated keys work; unknown keys and assignments of input `.value` to `int` fail |
| Legacy YAML `HtmlTemplate` DOM           | `container.properties.html` with `anvil-name` produces typed DOM references                                                                                   |
| Custom properties and constructors       | YAML properties and HTML frontmatter produce property setters and constructor keyword types; enum values outside the declared set fail                        |
| Local custom components                  | Package-qualified and legacy `form:` references preserve the referenced form's declared enum property types; valid assignments pass and invalid values fail   |

YAML takes precedence when both template formats exist. Designer declarations are
combined per source directory, with separate property and DOM types per form.
Local and dependency references import the concrete form class. Cached dependency
forms receive the same generated designer declarations. The static API stubs still come from the sibling fork.

## Events, layouts and schemas

| Contract                 | Implementation and evidence                                                                                                                                                                                                                                                                          |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Bound component handlers | Abstract generated methods catch missing implementations. Flexible base signatures permit explicit sender parameters, `**event_args`, direct calls and return values, matching the baseline's designer-specific override exception. Concrete user method annotations still reject bad arguments      |
| HTML event bindings      | `on:` on Anvil components and `anvil:on:` on named HTML fragments supply handler names; `self.` is stripped. DOM `anvil:on-dom:` remains separate                                                                                                                                                    |
| Data binding form APIs   | YAML/HTML binding metadata is accepted; forms expose `item` and `refresh_data_bindings`. Binding expression strings are not type-checked by the baseline generator. A custom property named `item` retains its declared type                                                                         |
| Custom events            | Declared event methods receive TypedDict keyword arguments when parameters exist, with typed form sender and string event name; custom parameter values are `Any`, matching YAML's lack of type information                                                                                          |
| Layouts and slots        | YAML/HTML layout references expose the concrete layout's properties; layout setters accept `anvil.Component`. Slot mappings accept real components and reject invalid arguments. YAML `components_by_slot` joins ordinary component declarations                                                     |
| Layout form events       | YAML `layout.form_event_bindings` and HTML `on:` on layout forms require handler implementations. HTML `on:layout:` maps to a separate binding field ignored by the baseline designer                                                                                                                |
| Table schemas            | Native `tables.rs` replaces the static API's generic `app_tables` declarations with row/table classes, typed columns, literal row/table indexing, updates, buffered changes and query/write signatures. Search iterators and linked rows retain target table types, including differing Python names |
| Users and Drive          | Native `services.rs` maps Users return annotations to the configured schema row, preserving optionality and parameter types; Drive app files retain spreadsheet/folder/file types in both environments                                                                                               |
| Row models               | `models.rs` scans the existing syntactic model patterns. Table return types, Users results and form items use registered model classes. The concrete `Table.Row` is a type alias so ty permits subclassing, while table methods can return the model without a circular base type                    |

Unannotated bound-handler argument inference is a shared limitation documented
above. Complete event/query/model corpus equivalence remains unproven.
Unsupported table Python names and other generated identifiers retain guards;
arbitrary string column names are supported.

## Dependencies and import spelling

`dependencies.rs` reads declared apps from `.anvil/deps` without fetching or
modifying the cache. Its two-pass resolver reserves package or directory hint
matches before assigning unused entries to legacy declarations. Dependency code
and designer stubs are mounted under their own package names; server code overlays
client code, with client-only modules retained as a fallback. Dependency server
callables are registered even for an app-only validation target. Form references
resolve dependency IDs and package names to concrete imported classes.

An additional in-memory search root exposes bare app imports through re-export
stubs, retaining the canonical definitions and their class identities. Direct
imports retain private names and names excluded from `__all__`; wildcard imports
respect the original `__all__` list. `checks.rs` then emits the exact runtime
restriction. Standard
library names available in Python 3.10 are omitted from this bare namespace;
Pyright prefers their standard-library stubs. Qualified and relative imports
continue to resolve the original app modules. This covers module/package shims
such as `typing.py`, `math.py` and `collections`, without hiding a local
`annotationlib` module unavailable in the target Python version.
Empty in-memory `ty.toml` markers enable ty's existing package-local import
fallback. Same-named helpers in separate packages resolve independently, retain
their types and receive the baseline runtime restriction. No metadata files are
written to the app.
`client_code` checkout imports also retain types and are rejected in both
environments. Relative and app-package-qualified imports pass; server code can
use bare imports and the merged client namespace. A whole-app case exercises
form structure validation and schema-generated types together, including an
incompatible item-field assignment.

Project stubs resolve from `typings/` or a configured `stubPath`, with the latter
replacing the default. Stub declarations retain their types rather than supplying
an `Any` fallback. Configured `stubPath`, `extraPaths` and `venvPath` paths resolve
from their declaring configuration file. Inherited `extraPaths` load typed library source
without making it part of the app validation target. Explicit `venvPath`/`venv`
settings use ty's existing environment discovery to load installed library types.
The system adapter keeps Anvil app files in memory and reads external libraries
from disk without copying an environment or spawning an interpreter. `PYTHONPATH`
retains library types. Host and activated environment discovery delegate to ty;
Homebrew's `libexec/bin` interpreter facade is normalized before discovery.
CPython user-site discovery follows Unix/framework layouts and honors
`PYTHONUSERBASE` and `PYTHONNOUSERSITE`. Explicit virtual environments keep user-site
packages outside their namespace. The focused user-site evidence runs against the
host macOS framework interpreter; Windows user-site layout and virtual environments
opting into system/user sites remain unported. Pyright's
missing-runtime-source warning for a stub-only library is outside the migration
contract; ty accepts the stub without that warning.

## Diagnostic settings and inline suppressions

`policy.rs` translates explicit assignment, argument, return, attribute,
undefined-name, call-binding, method-override and missing-import settings, as well
as the existing false-decorator setting. Invalid parameter defaults follow
`reportArgumentType`. Attribute writes use their AST context to apply
`reportAttributeAccessIssue` independently of `reportAssignmentType`, including
property descriptors and rule-specific ignore comments. ty still emits its own
rule names; the temporary classification is removed before JSON output.
Abstract-class instantiation follows `reportAbstractUsage` independently of plain
call errors. ty groups optional-value failures with ordinary attribute, call,
indexing and iteration errors. The corresponding ordinary mapped setting applies
to the entire ty category. Independent `reportOptionalMemberAccess`,
`reportOptionalCall`, `reportOptionalSubscript`, `reportOptionalIterable` and
`reportOptionalOperand` settings, including their rule-specific ignore names, are
outside the migration contract. Differential cases record the retained native
errors when an optional-only Pyright setting disables the baseline error. Mixed
union failures retain ty's diagnostic grouping rather than synthesizing Pyright's
number of diagnostics.

Operator errors remain visible under the default policy. Separate ordinary
`reportOperatorIssue` settings are also unported.

Chained JSONC and TOML configurations resolve each relative `extends` path from
its containing file, applying base files before child overrides. JSON takes
precedence over `pyproject.toml`; TOML reads `[tool.anvil-pyright]`,
`[tool.basedpyright]` or `[tool.pyright]`. Ancestor TOML discovery and fallback
through unrelated project metadata preserve the declaring directory for globs.
The tested `off` mode disables generic rules and unknown-call/task
checks while retaining the baseline's runtime import restrictions; explicit mapped
rule settings can re-enable their checks. Other Pyright checking-mode presets are
outside scope.

`include`, `exclude` and `ignore` use file/directory globs rooted at their declaring
configuration file. Whole-app selection respects `include`; explicit targets
override it. `exclude` applies to either selection, while `ignore` suppresses all
diagnostics without removing modules from import resolution. Inherited ignore
globs cover nested files and Anvil runtime checks. Broader glob/configuration
corpus equivalence remains unproven. Unused `type: ignore` comments
follow the baseline default of no diagnostic; an explicit severity enables them.
Generic rule names and messages remain engine-specific in the evidence.

`suppressions.rs` reads comment tokens from ty's existing parse, preserving source
apps and avoiding matching text inside Python strings. Inline and file-level `type: ignore`
comments suppress Anvil runtime diagnostics. `enableTypeIgnoreComments: false`
applies to both ty and the adapter; `pyright: ignore` remains active. Comments consumed by Anvil checks
do not produce ty's false unused-ignore warning. Rule-specific `pyright: ignore`
comments match the ported generic rule mappings or the existing Anvil rule names;
nonmatching diagnostics remain visible. This is targeted compatibility, not a
complete reproduction of Pyright's suppression and configuration policy.

## Local app corpus

`anvil/corpus.py` runs both checkers through the real CLI on temporary copies of
local apps. It records checker/source fingerprints, input-file hashes, raw CLI
outputs and diagnostic counts, and verifies that original input files remain
unchanged. It records differences rather than declaring the apps equivalent.
Copies are independent of configurations outside the app directory.

```sh
.venv/bin/python anvil/corpus.py /path/to/app /path/to/another-app \
  --output anvil/reports/native-app-corpus.json
```

Initial app checks exposed the standard-library shim collision covered above.
Broader optional-value, property, override and ordinary Python inference
differences remain. A legacy app also demonstrated that native preparation must
continue after array-shaped `db_schema` metadata: the baseline ignores that
format and uses generic static tables. The CLI's separate YAML validation rejects
the format; the native checker now preserves subsequent Python diagnostics.

[Pre-packaging five-app results](reports/native-current-app-corpus.json) use the same
release binary as the current acceptance checkpoint. All source-file checks
passed. The counts
below exclude the CLI's independent YAML/HTML diagnostics; equal counts alone
do not establish equivalence.

| App                      | Pyright checker diagnostics | Native checker diagnostics |
| ------------------------ | --------------------------: | -------------------------: |
| anvil_lit                |                          12 |                         11 |
| xstate-anvil             |                          84 |                         72 |
| TicketingApp             |                          67 |                         55 |
| TodoList legacy template |                           5 |                          5 |
| HTML memory fixture      |                           6 |                          6 |

The legacy template's `_template` imports resolve through package-local fallback
and emit the same runtime import restrictions. TicketingApp's
`plotly.graph_objs` import resolves through host/user-site discovery, removing the
previous native missing-import error. Anvil-specific diagnostics match exactly
across all five apps, and all source fingerprints remain unchanged.

TicketingApp still exposes missing property-override checks: ty's override pass
currently checks function members and skips property members. Optional-value and
ordinary inference differences also remain. These are migration gaps to reduce
into cases; native diagnostic grouping and unsupported Pyright-specific settings
are accepted differences under the scope above.

## Baseline discrepancies discovered

The compatibility oracle is the built anvil-pyright executable, with source and
tests used to explain its behavior. These observations need explicit decisions in
later parity work:

- Aliased decorators in an unselected, unimported server module can be missed by
    anvil-pyright's eager registration. Its syntax pass recognizes canonical names;
    alias correction happens during type checking. The native registration pass
    resolves every registration semantically, so it can recognize these aliases.
    The differential alias case uses a selected file, where both checkers agree.

- The current `getDiagLevelDiagnosticRules()` in anvil-pyright exposes only
    `reportAnvilFalseCallableDecorator` from the custom Anvil rules. Overrides for
    unknown-call and Skulpt rules are therefore ignored by the baseline, despite
    broader configuration claims in feature docs. The native port follows this
    observed behavior. The tested assignment, missing-import and unused-ignore overrides are supported;
    general checking modes and broader configuration remain unported.

- An invalid `@anvil.handle('missing', 'click')` in a package form emits no
    warning through the built one-shot CLI in the recorded case. Source-level
    integration tests populate the form registry before binding, which the normal
    CLI does not guarantee. Native preparation now collects the metadata before
    checking and emits the warning. The differential case preserves the baseline
    miss as an explicit, deliberate improvement rather than equivalence.

- The baseline's combined-designer logic does not retain functional
    `_DomNodes = TypedDict(...)` declarations when combining multiple forms. The
    native generator uses distinct declarations per form. The positive shared-DOM
    test passes on both checkers, but only the native declaration currently
    guarantees those key maps remain available in the combined namespace. Negative
    key/type cases use single-form namespaces, where both enforce the contract.

- The historical `anvil_memory_app` fixture lives under the baseline fork's
    `packages/` directory. The parent `pyproject.toml` ignores/excludes that directory,
    so its in-checkout success masks Python errors. Copying its actual source and
    templates into a temporary app outside that parent configuration makes both
    checkers reject the six DOM-only attribute assignments across its two forms.
    This is now a differential case, with fixture sources and outputs in the report.
    The initial fixture timing remains excluded from performance comparisons. The
    synthetic benchmark apps were already generated outside the checkout.

- When client and server model subclasses coexist for one table, the recorded
    baseline accepts an incompatible server-result assignment. Native uses the
    server model's declared return type and rejects it. This case is marked
    `known-difference`, with expected counts and exit codes for both checkers.
    Native continues to prefer server models with a fallback to visible client
    modules; this is the source-level intended scoping policy, and is stronger
    than the observed result.

- The baseline accepts an incompatible assignment from an annotated function in
    an unselected server module. The native checker preserves the declared return
    type. Recorded variants reproduce this both with and without the defining file
    in `ignore`; the ignored module itself emits no diagnostics. Both variants are
    `known-difference` cases. Native keeps the stronger caller check.

## Remaining validation contracts

The ported batches do not yet constitute a complete replacement. Preparation
guards explicitly reject unported metadata.

| Area                     | Baseline contracts to port or prove                                                                                                                             | Current gap                                                                                                                                                                                                                                                                                                                                    |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Form preparation         | YAML and HTML; package and module forms; nested/custom components; form references; DOM node types                                                              | Core forms, local/dependency references and layouts/slots covered; incomplete templates and full HTML parser equivalence remain                                                                                                                                                                                                                |
| Form typing and events   | Properties and constructor signatures; item models; bound handlers; data bindings; `@anvil.handle` component/event checks; generated-form diagnostic exceptions | Properties, items, bindings, custom events, flexible handler overrides and literal handle targets covered; complete handler argument inference, code-only custom events and configuration corpus unproven                                                                                                                                      |
| Data tables and services | Schema-generated table/row types; query behavior; users table and Google Drive; registered model subclasses and methods                                         | Core declarations and arbitrary string column keys covered; broader query/accelerated API corpus, model edge cases and config interactions unproven; unsupported generated identifiers retain guards                                                                                                                                           |
| Dependencies             | Local cache discovery and package hints; flattened namespaces; dependency-specific client/server imports, forms and callable registrations                      | Local cache discovery, package/directory hints with legacy fallback, client/server overlay, forms and callable registrations covered; broader cache/model/namespace corpus unproven; no network fetching                                                                                                                                       |
| Import restrictions      | Server-to-client imports; app-package imports; rejected bare client imports and checkout-directory imports; dependencies and namespace collisions               | Bare client and checkout-directory restrictions match exact diagnostics; relative/package imports and server-to-client fallback preserve types; broader dependency/collision cases remain                                                                                                                                                      |
| Diagnostic policy        | Checking modes, general Python rules, config inheritance/overrides, include/exclude/ignore, inline suppressions and source selection                            | Tested generic/custom severity settings, attribute/variable assignment separation, JSONC/TOML inheritance/discovery, off mode and inline/file-level ignores; include/exclude/ignore globs and explicit targets covered; other checking-mode presets and optional-only rules are outside scope; broader supported suppression/glob cases remain |
| API and Python typing    | Ordinary assignments/calls, overloads, decorators, subclassing and Anvil APIs under each environment                                                            | Reused API stubs and a few integration examples; corpus equivalence unproven                                                                                                                                                                                                                                                                   |
| CLI operations           | Full-app/directory/file selection; nested apps; global errors/warnings; malformed input; dependency warnings; checker failures                                  | Transport cases, whole-app form/table validation, directory targeting and dependency cache warnings covered; complete CLI corpus not migrated                                                                                                                                                                                                  |

## Real-project trials

The first selection contains 13 distinct local projects: Anvil Extras, Tabulator,
the older `anvil-router` library and current Routing API Design checkout, Material
3 Theme, runtime v2/v3 client tests, Ticketing App v3, PopoverRewrite, M3 App 47,
RoutingExample, ExampleTabulator and ReactivePersistenceTabulatorDemo. The
`../routing` path is a symlink to `anvil-apps-local/Routing_API_Design`, so the old
and new routing libraries are recorded separately.

Both checkers ran through the real CLI on temporary copies. Original app files
remain unchanged. Initial reports use the standalone release from the packaging
milestone; follow-up dependency trials use the debug executable after the
anonymous-component fix. None of these runs are performance measurements.

- [Libraries and client suites](reports/native-real-projects-initial.json)
- [Standalone demos](reports/native-real-demos-initial.json)
- [Older routing library](reports/native-routing-library-initial.json)
- [Local dependency fixtures](reports/native-real-projects-local-dependencies.json)

The dependency trials supply existing local copies of the declared packages in
temporary `.anvil/deps` directories, with a trial manifest. They preserve original
app configuration and record each dependency source and file hash. They never
fetch dependencies and do not assert that the local checkouts match the declared
cloud revisions. RoutingExample's legacy dependency is supplied by local
HashRouting. This removes cache warnings and import failures caused by absent
local caches from the developer-noise investigation.

The counts below include CLI YAML/HTML diagnostics and intentional test failures;
they describe the inputs, not a quality score. Dependency demos use the controlled
local-cache runs. Runtime v3 remains incomplete because preparation encounters an
intentionally invalid `MissingPackage.Nope` component in
`FormSpecTests/UnknownPackageComponent/form_template.html`. Its small native count
does not establish fewer false positives: Python checking has not run.

| Project                                                        | Pyright diagnostics |  Native diagnostics |
| -------------------------------------------------------------- | ------------------: | ------------------: |
| Anvil Extras                                                   |                 564 |                 400 |
| Tabulator                                                      |                  76 |                  60 |
| Routing API Design                                             |                  95 |                  89 |
| Older anvil-router                                             |                  39 |                  31 |
| Material 3 Theme                                               |                1133 |                 498 |
| Client tests v2                                                |                 876 |                 772 |
| Client tests v3, with local dependency                         |                 207 | preparation aborted |
| Ticketing App v3                                               |                 135 |                  74 |
| PopoverRewrite                                                 |                  58 |                  54 |
| M3 App 47                                                      |                   0 |                   0 |
| RoutingExample, with local dependency                          |                   9 |                   9 |
| ExampleTabulator, with local dependency                        |                   8 |                   5 |
| ReactivePersistenceTabulatorDemo, with five local dependencies |                  31 |                  11 |

### Confirmed preparation fix

Anonymous runtime names such as `$component_1` previously caused a global
`invalid component identifier` failure. The generator now omits their Python
attribute declarations while preserving child traversal, type resolution,
event bindings and handle-target metadata. Named descendants retain real types.
The reduced real-CLI differential case accepts a nested label and an anonymous
container's `show` handler on both checkers, then rejects assigning an integer to
the label's text. The original runtime v3 input now progresses past these names;
missing caches and then its deliberate unknown-package fixture were the next
preparation blockers at that checkpoint. The per-form isolation checkpoint below
supersedes the unknown-package abort.

[Updated release checkpoint](reports/native-real-project-trial-checkpoint.json)
passes 18 focused real-CLI tests: 16 existing native cases, the packaging case
and the new anonymous-component differential case with valid/invalid controls.
The fixed executable is bundled under
`anvil/dist/anvil-ty-native-0.1.0-macos-arm64-project-trials`, preserving the earlier
archive. Rust Clippy and formatting, Python lint/formatting and source-fingerprint
checks pass. The full differential suite and performance measurements remain their
previous, separately fingerprinted checkpoints.

### Developer-noise priorities

| Pattern                                                                           | Evidence and classification                                                                                                                         | Next action                                                                                                                                                                      |
| --------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| One unpreparable form stops Python checking for the app                           | Runtime v3 deliberately includes an unknown-package form                                                                                            | Fixed: report preparation failure on its owning Python form and continue checking other selected files                                                                           |
| API signatures omit constructor/layout operations                                 | ExampleTabulator uses deprecated `spacing_above`/`spacing_below`; the reactive demo reports missing `Slot.clear`                                    | Fixed `Link`'s `ColumnPanel` inheritance, legacy spacing `None` values, and `Slot.clear`/`get_components` in Anvil's source stubs, then regenerated/synced; no engine relaxation |
| Browser interop is stricter than runtime coercion and selector knowledge          | Extras/Tabulator have repeated `Element.style` and nullable-selector diagnostics; M3 numeric style opacity is rejected                              | Accepted for this milestone; preserve current checking                                                                                                                           |
| Framework-created attributes are absent from static form types                    | Legacy RoutingExample/HashRouting reports `url_dict` and `url_hash`                                                                                 | Accepted for this milestone. The requested routing target is the newer `Routing_API_Design`, already included in the library trials                                              |
| Untyped custom-event declarations reject ordinary callback overrides              | ReactiveTabulator's `row_click(self, sender, **event_args)` conflicts with the generated base method in both checkers                               | Fixed in native designer-stub generation: unparameterized events use a gradual callback signature. Typed event parameters and concrete method calls retain their checks          |
| Instance-assigned callbacks retain a method's `self` parameter                    | Tabulator's rebinding pattern reduces to plain Python that runs and passes Pyright, but ty reports an assignment error and incorrect call arguments | Accepted upstream limitation; the experimental engine patch has been removed. See [engine compatibility](ENGINE_PATTERNS.md)                                                     |
| Property initialization loses the relationship between dictionary keys and values | Extras' heterogeneous property dictionaries produce value unions rejected by typed `init_components` parameters                                     | Use explicit dictionary typing where needed; not a checker priority for this milestone                                                                                           |
| M3's setter decorator and return annotations                                      | `@anvil_prop @property` consumes a callback with `(self, value)`; both checkers flag the convention                                                 | Treat as an autocompleter convention; no special handling in ty's engine                                                                                                         |

### Custom-event callback checkpoint

The native generator now gives unparameterized custom-event methods the same
gradual signature used for ordinary bound handlers: `*args: Any`,
`**event_args: Any`, returning `Any`. Event metadata without parameter types does
not constrain an override's explicit sender or return type. Parameterized events
keep their existing generated signatures.

Three focused custom-event integration tests pass through the real CLI, including
a valid explicitly typed sender/return override and an invalid concrete sender
argument. Existing typed-event and dependency-event checks pass. Rust Clippy and
formatting, and Python lint/formatting pass. The engine remains unchanged.

The [reactive demo recheck](reports/native-custom-event-demo-fix.json) uses identical
app and local dependency inputs to the preceding trial. Native diagnostics fall
from 11 to 10: only the `row_click` override error disappears. Original projects
remain untouched. This checkpoint uses the debug executable; the existing release
bundles and full-suite/performance checkpoints predate this fix.

The [callback rebinding probe](reports/native-callback-rebinding-probe.json)
records two plain-Python reproductions, executable/source fingerprints, successful
Python execution and clean Pyright validation. ty incorrectly retains `self` when
a function is assigned to an instance method attribute. The subsequent
local engine patch addressed these reduced cases independently of generated
Anvil stubs. That patch has since been removed; see
[engine compatibility](ENGINE_PATTERNS.md). `get_design_component` class identity
is supported by the authoritative API stub.

### Per-form preparation and source-stub checkpoint

Template parsing and designer generation now isolate errors per form. A failed
form receives an `invalid-form-template` error on its owning Python source, with
the template path and reason in the message. The CLI routes checker diagnostics
only to Python files, so attaching it directly to the template would lose the
error. A gradual placeholder for that form's template avoids missing-designer
import/member cascades while retaining checks in its Python body. Other forms
keep their normal generated types. Only selected sources own preparation
diagnostics; targeting an unrelated valid file remains successful.

The real-CLI regression covers an invalid HTML form alongside a typed YAML form
and server module, verifies that all three Python bodies are checked, and checks
valid/invalid file targets. The [runtime v3 recheck](reports/native-client-v3-form-isolation.json)
uses the same app and local dependency inputs as the preceding trial. Python
checking now completes: native reports 197 diagnostics, including 19 CLI template
diagnostics and one form preparation error, with no global preparation failure.
The preceding count of 20 was incomplete because Python checking aborted. This
report predates the subsequent API stub refresh.

`Slot.clear()` exists in `runtime/client/js/runner/python-objects.ts`, accepts no
arguments and returns `None`, but was absent from the API stubs. Its declaration
is added in the Anvil checkout's `doc/anvil-api-stubs/source/anvil/__init__.pyi`.
The existing generator and Pyright sync script rebuild the snapshots; the
Pyright CLI build refreshes its bundled copy. Native development reads the synced
API snapshot at runtime. The source edit remains uncommitted on Anvil's `master`.
The sync also carries existing Anvil source changes absent from the preceding
Pyright snapshot; those are not newly authored stub changes in this checkpoint.

The differential CLI test accepts `Slot.clear()` on both checkers and rejects a
positional argument. Existing standalone bundles and performance/full-suite
reports retain their earlier fingerprints and have not been rebuilt for this
checkpoint.

Useful failures remain in the sample. For example, Slider's explicitly annotated
string return conflicts with its numeric return, while missing tables/modules and
wrong arguments require checking against each app's actual schema and runtime.
Intentional invalid-value and missing-form tests are not valid-pattern false
positives. A diagnosis shared by Pyright and ty still needs review when it reports
a supported runtime pattern; the baseline itself is noisy on these inputs.

### Remaining source-stub fixes

The follow-up addresses the other verified API gaps in Anvil's source directory:

- `Link` inherits `ColumnPanel`, as both the runtime implementation and docs index
    specify. Generated constructors now inherit legacy spacing and panel properties,
    and ordinary container operations are available.
- `spacing_above` and `spacing_below` accept `None`. The shared legacy runtime
    setters remove all spacing classes for that value. Getter/setter declarations
    across the existing component stubs reflect this, and the constructor generator
    derives the updated parameter types. Unsupported strings and integer assignments
    remain checked.
- `Slot.get_components()` returns a list of components, complementing the preceding
    `clear()` fix. The runtime supports both operations with no arguments.
- `anvil.history.Location` is declared for client and server. Browser history
    navigation, properties and listener callbacks are declared only on the client;
    server history objects remain placeholders without those operations. Client
    keyword-only constructors and server positional constructors retain their distinct
    signatures. This module is absent from the docs index; its client implementation
    and downlink Python implementation supply the contracts.
- Custom exception transport exposes `AnvilWrappedError` in both environments.
    `_register_exception_type` retains an undocumented private compatibility
    signature for existing routing code, pending portable exceptions. Serializable `startup_data` is
    available only on the client. `AppResponder` and its typed app-loading responses
    are available only on the server, as the runtime and docs index specify.

Seven focused differential CLI tests pass against the refreshed bundled Pyright
stubs and native development executable. They cover supported calls, invalid
arguments/assignments and client/server availability. The generator is idempotent,
the sync check passes, and bundled CLI stubs match the generated snapshot. Source
edits remain unstaged and uncommitted on Anvil's `master`.

The [affected-app corpus recheck](reports/native-source-stub-fixes-corpus.json)
records adapter/binary/API source fingerprints and unchanged original inputs:

| App                                                       | Previous native diagnostics | Current native diagnostics |
| --------------------------------------------------------- | --------------------------- | -------------------------- |
| ReactivePersistenceTabulatorDemo, with local dependencies | 11                          | 3                          |
| ExampleTabulator, with local dependency                   | 5                           | 5                          |
| Routing_API_Design                                        | 89                          | 76                         |

These counts include the preceding callback/preparation fixes and current Anvil
source updates. ExampleTabulator's two unknown spacing-argument errors become one
invalid-value diagnostic for the capitalized string `"None"`; a deprecation warning
for its Notification `style` argument is also visible after the source snapshot
refresh. The supported spacing choices remain lowercase enum strings or Python
`None`. The routing recheck retains a generic ty limitation for subclassing a class
returned by `get_design_component`, and catches a possibly `None` path passed to
`Location`. Server-only HTTP operations inside client source, optional dependencies,
accepted DOM patterns and dynamic routing attributes remain separate diagnostics.
No checker rules were suppressed and original apps were not edited.

## Next batches

1. Write use TDD: reduce each genuine Anvil compatibility failure found in CLI
    trials into a real-CLI case before implementing it.
1. Use the standalone checker/stub bundle for side-by-side CLI trials; release
    automation and builds for additional platforms remain future work.
1. Extend representative app coverage, especially dependency/model registration
    interactions and table/query variants. Preserve native ty semantics for
    Pyright-specific differences.
1. Consider unannotated event-handler body inference as a new typing feature;
    both current checkers share this limitation. LSP integration remains separate.

Baseline references: sibling anvil-pyright's `skulptModules.ts`,
`serverCallDetection.ts`, `serverCallValidation.ts`, `decoratorValidator.ts`,
`common/configOptions.ts`, and the `anvil.*` integration tests. Architecture docs
for forms, component events, models, imports and callables describe the broader
contracts; LSP completion/navigation features are outside this milestone.
