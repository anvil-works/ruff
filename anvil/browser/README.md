# Anvil ty browser session

This package adapts upstream ty's WASM workspace to the IDE's ordered browser
session API over Comlink. A module worker owns separate client/server analysis databases; source changes and queries
run in message order. Open document text overrides stored files until it closes.
The IDE can opt into this backend; the integration remains unreleased.

Install dependencies, then build the upstream bindings and Anvil compatibility
module from this directory:

```sh
pnpm install --frozen-lockfile
pnpm build
pnpm test
```

`pnpm build` prepares Comlink, lazy packs and both WASM modules in release mode
with locked Cargo dependencies. `dist/BUILD.json` records source revisions and
input/output hashes. `pnpm pack` verifies that the inputs and assets still match
that build; rerun the build after source changes. `pnpm build:comlink` and
`pnpm build:stubs` refresh those assets during development; `pnpm build:wasm` is
the faster development-only engine build. Run the full release build before packing.

The published package contains the session, worker and complete `dist/` assets,
including both WASM binaries and licence notices. Consumers need no Rust, Python
or install scripts. Serve the package contents with JavaScript and WebAssembly
MIME types. The IDE copies them beneath a versioned URL for cache reuse.

Client Plotly declarations live in a content-hashed JSON pack. Only the package
root ships in compatibility WASM, so import completion can discover it without
downloading the catalogue. The first client query with a Plotly import in selected
app/dependency source or a live context fetches the pack before analysis. Read-only
Plotly source requests also load it. The worker retains it across app updates;
failed downloads leave later queries free to retry and do not block edits or
server queries. This does not add server Plotly support.

Server NumPy and pandas use the same loader. `runtime_options.server_spec.requirements`
selects declarations for NumPy 2.5.4 and pandas 3.1.0. Unversioned requirements
choose the newest available version; ranges choose the newest version they admit.
An exact runtime pin can also use a different patch on the same minor line, or
the newest older minor within the same stable major. Exact declaration matches
win; newer minors and different majors are not approximated. For 0.x, approximation
stays within the same minor. Prerelease, post, local and epoch versions require
an admitted declaration version. These choices do not change installation constraints
or prove what is installed. Older declarations can omit newer APIs.
Conditional/URL requirements, includes, constraints,
unsupported pip options and continuation lines wait for resolved environment metadata.
Registry index options do not affect selection. The IDE also supplies
the selected environment catalogue's bundled requirements. These participate in
selection alongside app constraints; absent catalogue metadata does not imply that
an arbitrary base image contains these libraries.

These profiles target current dynamic downlinks. NumPy supplies matching
declarations; pandas uses the public pandas-stubs 3.0.5.260914 source, with common
DataFrame/Series APIs checked against pandas 3.1.0. This does not establish coverage
of every new pandas 3.1 API. The typing package preserves both runtime and source
versions in its catalogue and manifest.

The pandas pack includes dateutil type helpers and loads NumPy as a dependency;
an explicit incompatible NumPy constraint also disables pandas types. Configured
but unused packages expose small import roots and download no catalogue. Imports
in selected server/shared source or a server REPL trigger loading; client Skulpt
queries cannot see these packages. Requirements edits unmount incompatible packs,
while their downloaded bytes remain cached for reuse. The original upstream
`.pyi` and necessary typed `.py` files support normal completion, signatures,
hover and read-only navigation; optional third-party APIs can remain gradual.

The build consumes `@anvil-works/python-stubs/manifest.json` and copies its
content-hashed server packs and licence notices into `dist/`. The separate
`anvil-python-stubs` repository owns wheel selection, extraction recipes, source
checksums and notices. Browser builds consume the installed package without Python
or upstream wheel downloads. No NumPy/pandas-specific inference or Ty engine
patches are involved.

## IDE runtime and diagnostics settings

The IDE supplies `.anvil/python-environment.json` with the selected server Python
version, using the same environment-catalogue lookup as Ruff. Client analysis uses
Python 3.7 and the separate Skulpt import policy; it never inherits server libraries.
Standalone browser callers without environment metadata retain the 3.10 server default.

App extra files `ty.toml` or `[tool.ty]` in `pyproject.toml` configure native Ty
`rules` and `analysis` settings. `ty.toml` wins, including when empty or invalid.
The IDE does not yet support Ty filesystem settings or per-file overrides: their
paths do not directly describe Anvil's generated module layout. It reports these
as configuration warnings rather than silently ignoring them. For example:

```toml
[rules]
invalid-argument-type = "warn"

[analysis]
allowed-unresolved-imports = ["my_external_library.**"]
```

The adapter parses changed TOML once, validates native options in an empty Ty
workspace, and applies them to both runtime databases as each is selected. It does
not reparse configuration on completion. Malformed TOML or invalid option values
produce a warning naming the config file and use defaults until corrected. Unknown
rule names produce Ty's own configuration warnings; unknown nested keys follow
upstream deserialization behaviour.

By default, unresolved absolute external server imports are informational: the
browser may lack declarations for an installed library. Relative imports, Anvil/app
package imports and stdlib imports retain native errors. The informational message
asks the user to check installation; it does not claim that an unresolved package
is installed. Explicit `unresolved-import` or `all` rule settings take precedence.
Unavailable declarations retain Ty's gradual Unknown inference; resolved types
are not replaced with Any. Configured `allowed-unresolved-imports` uses native Ty
semantics. Client imports retain the existing Skulpt checks.

The IDE combines Ty with Ruff: Ty owns semantic names/types/calls, while Ruff owns
syntax, style and unused-code checks. Default Ruff F821/F823/F405 reports are
disabled only for app editors using semantic analysis. Explicit Ruff config is
preserved, as are normal Ruff checks with the feature flag off or in extra Python
files. Distinct Ty errors on one line are retained.

Anvil runtime warnings come from `anvil/compat`, shared with native validation.
They cover duplicate callable/background-task registrations, portable classes
outside ordinary Modules, navigation during `show` handlers, and syntax that
Skulpt cannot execute. Show handlers follow YAML bindings and resolved `handle`
decorators, including their precedence over YAML bindings; aliases retain their
meaning. Duplicate detection covers statically named module-level functions in
Server Modules. Row-model keyword validation uses the API stub's explicit `__init_subclass__` signature. Generic missing-receiver and
setter-name lint rules remain separate Ruff work.

The build pins `@anvil-works/python-stubs@0.1.0-canary.1` from npm. Publish that
reviewed package before running a clean hosted browser build. The browser workflow
builds and tests the installed archive, then uploads it for review; it never
publishes to npm. See [publication order](../PUBLISHING.md#ide-browser-assets).

Serve this directory with JavaScript and WebAssembly MIME types. Create a
`BrowserAnalysisSession` from `session.mjs`, passing the URL of `worker.mjs`, a
`file:` project root URI and a map of absolute paths to source strings.

Comlink handles request correlation and remote exceptions. The session preserves
ordered source updates and revision checks, rejects pending calls on worker failure
or disposal, and releases its Comlink proxy when stopping. Per-query cancellation
discards the result without stopping the shared analysis worker. Each in-order
update attempt consumes a revision. A rejected update restores its input batch
and rebuilds the previous workspace before accepting later edits; its caller
still receives the error. Initialization or worker failure stops the session.

Completion, definition, references, prepare-rename, cross-file Python rename,
signature help and pull diagnostics use upstream ty APIs. `anvil/readSource`
reads supplied project files and ty's vendored typeshed files for read-only
previews. IDE-owned app source mappings identify editable app items.

Completion defaults to upstream auto-import search. Optional
`context.autoImport: false` returns ordinary suggestions without that search;
`context.autoImport: "only"` returns only native suggestions with import edits.
Import-only queries return `preparationRequired: true` and no items until the
current workspace index is ready. The IDE calls `anvil/prepareCompletion` with
`textDocument.uri` in yielded batches until `{ complete: true }`, then retries.
Context preparation uses `queryContext(id, "anvil/prepareCompletion", {})` and
needs no cursor. Module-path or option changes reset readiness; body edits keep
native incremental caches. Scheduling and the typing pause belong to the IDE,
not the browser session. See [engine compatibility](../ENGINE_PATTERNS.md).

Rename refuses vendored files, `.pyi` files and generated/dependency paths,
including required edits to those sources. Anvil compatibility planning adds linked
component, handler, binding, RPC and Form/module resource renames. Ordinary Python
renames require a valid identifier; explicit RPC string names retain their API
semantics. Ambiguous ownership refuses the operation.
References and ordinary rename include server callers of client declarations.
Explicit local aliases retain ty's normal symbol ownership.

`anvil/compat` shares Form rendering with the native CLI adapter. Browser
preparation supplies in-memory source and YAML templates. IDE projects include
`.anvil/dependencies.json`: `roots` lists selected cache-root paths in runtime
order, and `ids` maps logical dependency IDs to those paths. This preserves the
server's direct/transitive selection and remapped IDs. Callers without this file
retain the native adapter's declaration-matching policy. Unselected cached apps
are excluded from analysis and Anvil metadata/refactoring scans.
Client queries see client modules and API stubs. Server queries also see server
modules, which take precedence over client modules with the same Python identity.
The worker retains each native workspace and restores the matching source
projections when switching runtimes.
Dependency additions, source reloads and removals take effect through `updateFiles`.
New directories in the current search roots rebuild the WASM workspace: upstream's
file API does not refresh newly created ancestor directories after a failed import.
This preserves dependency, context and unsaved source state; ordinary content edits
remain incremental. The generic signature metadata extension is described in
[ENGINE_PATTERNS.md](../ENGINE_PATTERNS.md).

Ordinary Python edits validate and patch cached prepared sources. Inferred RPC,
Form-item and handler declarations track their producer/import inputs; unrelated
edits retain them. Literal RPC consumers infer only their needed returns, while
project refactoring requests complete inference. Parameter contracts stay lazy.
The Anvil editor repository's `bench:analysis` command protects this path with
source-edit and visible-menu budgets, fresh-type assertions and same-run comparisons.
Run it before adopting browser changes into the IDE; cached completion alone does
not establish acceptable typing latency.

Canonical app-package paths map back to original source
identities, without mounting duplicate Python files. Invalid Form templates report
preparation diagnostics and remain correctable. Preparation owns one selected
Form catalogue, reused by inference, completion and rename. Read-only analysis
can use invalid-template fallbacks; metadata-dependent renames refuse incomplete
Form metadata. Immutable API class/event facts are parsed once per preparation
and borrowed by all Form renderers. Original Python files and read-only
previews retain their text. Only the analysis copy replaces a row model's `.Row`
base with the equal-width private `._AR` alias for `attrs=True`; every source
position is preserved. Plain rows and `attrs=False` models remain key-only.
This projection requires a schema-backed table and a direct, unshadowed Anvil
`app_tables`/`tables` import. Nested model definitions and dynamic/re-exported
bindings retain the upstream gradual typing limitations.
Generated sources can be read after an intervening query in the other runtime.

Table declarations use the shared schema and row-model renderer. Column-key
completions identify the receiver through ty and return complete, escaped string
replacement edits. ty's existing return-type inference option is enabled.
Linked rows retain the target table's registered model. Query combinators inherit
column keyword completions from their enclosing table search, get or view
restriction, including aliased callees; value expressions keep normal Python
completion. A `get()` result must be narrowed from `None` before its row members
are offered by ty.
Column attributes require a model declared with `attrs=True`; typed row keys and
custom model methods remain available without it. Dependency Forms use their own
discovered row models. RepeatingPanel row templates infer `item` from parent
`.items` assignments, including table searches, ordinary iterables, comprehensions
and function-returned collections. Direct `RowTemplate(item=...)` calls also
supply an item type. The same types reach binding editors. Literal dictionaries
with unique string keys become TypedDicts so each key retains its value type;
dynamic keys, unpacking and lambda-produced dictionaries retain ordinary ty
inference. Explicit item configuration wins; conflicting or unknown assignments
do not choose an arbitrary parent. RepeatingPanel `get_components()` uses its current
row Form type, including in bindings. Ordinary Containers retain Component.
Designer and semantically resolved `@anvil.handle` bindings supply `sender` types
for unannotated handler parameters. Typed `raise_event` overloads supply payload
arguments; currently FileLoader `change` declares `file: Media | None` and
`files: list[Media]`. As with optional table rows, narrow `file` before completing
Media members. Explicit parameter annotations win and unknown event payloads stay
gradual. Analysis-only quoted annotations and generated type aliases let ordinary
ty inference carry these types through local aliases and hover. A column map
preserves original completion edits, navigation, rename and diagnostic positions;
read-only source and outlines retain the original code. Unannotated yield-based generator functions
remain gradual.
Users return values use the configured user table and its row model. Configured
Drive files receive declarations from the same service renderers as the native
adapter. Schema and service metadata updates refresh these declarations.
`@anvil.handle(...)` completes named components in the containing Form and event
names from the component's API stub and custom Form event metadata. Callee and
Form identities are resolved through ty; unrelated same-named functions/classes
do not receive these suggestions. Anonymous components are omitted; the Designer
gives them a name when adding an event handler.

The component's event literals also supply suggestions for `add_event_handler`,
`set_event_handler`, `remove_event_handler`, `raise_event` and `get_event_handlers`.
The stubs retain a string alternative for custom `x-` event names.

Callable parameters preserve function references when accepting completion;
ordinary value parameters still allow insertion of `()`. The worker obtains
this hint once from native signature help, including for Python callbacks outside
the Anvil API. It applies only to the argument's reference, not expressions inside
its receiver, a list, a lambda or an unpacked mapping. REPL and binding contexts
preserve the hint. It does not filter the menu to callable suggestions.

`open_form` completes local Form names and package-qualified dependency Forms
from the current prepared catalogue, including aliased API calls. Once a literal
Form is selected, an analysis copy calls its actual class so Ty supplies custom
and inherited constructor keywords. The copy is restored before normal Python
completion. Configured secret/key names follow the resolved secrets API and the
selected apps' configuration; no secret values enter the IDE analysis project. Contextual
completion shares parsed call facts between its component, Form and query-column
consumers. RPC contract selection and source projection currently parse their own
call facts.

Unannotated Form handler parameters and `**event_args` receive analysis-only
annotations from resolved bindings. Known kwargs fields use standard open
TypedDicts; unknown event payloads remain gradual, nullable payloads need normal
narrowing, and explicit author annotations take precedence. Incoming email
handlers infer their first unannotated parameter as `anvil.email.Message` when
the decorator resolves to the real server API. Generated declarations preserve
the editor's original source and UTF-16 ranges.

The worker owns a preparation cache: unchanged Python model discovery and Form
rendering are reused; source, template and configuration changes invalidate the
affected declarations. These caches contain Anvil declarations, not Python types.

File outlines and workspace symbol search parse current original Python source
with Ruff. Form handlers, endpoints and background-task metadata use Ruff syntax
facts and ty's resolved decorator identities, including import and assignment
aliases. Form ownership follows the template's declared class or source filename.

`setContext`, `queryContext` and `closeContext` support REPL history and typed
Form binding expressions. Completion edits map back to the current input;
items requiring edits to generated imports or history are omitted. Projection
generations reject obsolete completion items after updates, moves and reopening.
Context paths avoid app modules, and ordinary rename refuses edits to a live
generated context. Bindings refresh with Form metadata and recover when a
missing Form returns.

HTML and YAML Forms share native template parsing and rendering. HTML structure
supplies component and DOM declarations, with tag-specific node types. Cached
IDE YAML preserves Designer component identities and reads DOM nodes from its
serialized HTML; legacy HtmlTemplate YAML retains `anvil-name` node declarations.
YAML takes precedence when both exported template formats exist.

Designer-registered JS components have separate class stubs and namespace
exports, restricted to selected app/dependency packages. Properties, methods,
constructors and container layout arguments follow Designer metadata. Exports
append to the analysis copy of Python modules, preserving original source ranges
and inference. Appended ranges retain generated, read-only identities for
navigation and required rename edits; completions cannot edit those ranges.
Generated diagnostics remain visible with their generated source location.

RPC/task name completion resolves the API callee and registration decorators
through ty, including aliases. It reads current selected server files and
unsaved overlays. A worker-owned registration cache invalidates with project
source changes; context input edits reuse it. String edits preserve UTF-16
positions, and raw literals are replaced as complete literals. Server-owned
modules retain precedence over client JS namespace exports.

RPC/task result declarations come from ty's machine-readable annotation edits on
small inference functions. Each export gets an isolated type-alias module and
literal-name overloads in `anvil.server`; task results flow through
`BackgroundTaskState[T].get_return_value()`. Server bodies stay in the server
namespace. A result with unavailable or different client import identities keeps
`Any`. Inference does not supply concrete call arguments, and unsupported types
or ambiguous names keep the broad fallback. Source/metadata updates discard both
these declarations and inferred Form items; context-only edits reuse them.

Unique literal `call`/`call_s` registrations also expose portable parameter
contracts for signature help, native argument diagnostics and keyword completion.
Completion prepares only the callable being queried. Ty supplies unused keyword
names from the same analysis-only call projection; ordinary value suggestions
still come from the caller's runtime. Server edits refresh those contracts, and
REPL/binding contexts use the same path. Dynamic, ambiguous and overloaded names
retain the generic API signature. Unavailable server-only parameter types remain
gradual, and inferred generic relationships are not specialised by actual arguments.

Form item inference temporarily exports source expressions, asks ty to annotate
small functions and restores the source before serving a query. One scoped
owner restores temporary replacements in `finally`; inferred annotations and
declarations become the cached result only after inference completes. Ordinary ty
results remain authoritative; dictionary shape projection is only selected for a
root dictionary item, preserving operations such as `dict.values()`. One stable
private module (normally `_anvil_form_items.pyi`) holds the inferred declarations in separate class
namespaces, isolating imports with the same spelling. Generated type imports are
excluded from user references and rename edits. Dictionary projection is limited
to producer modules and their resolved client imports; unrelated data modules do
not create field inference work. Generated inference module names avoid selected
app/dependency package names; their imports use the allocated identity.

Definition and references also recognise semantic RPC/task string calls and
explicit registration names. Definition offers every possible owner for an
ambiguous name; rename still refuses ambiguity. Ordinary string values and local
functions with similar names are excluded. Variable call arguments retain normal
Python navigation.

Reference requests honour `context.includeDeclaration`. The IDE additionally
passes `context.includeImports: false` for usage navigation. Reference collection
follows explicit import aliases and omits import sites from that view; these
display options do not filter rename edits. Definition destinations retain ty's
normal resolution; further import-skipping differences are optional IDE polish.

Shared IDE completion regressions run against Ty and legacy. The separate
`test:analysis parity-targets` command currently has no unfinished targets.
Default `**event_args["sender"]`, incoming email Message inference, custom
constructor keywords through `open_form`, secret names, RepeatingPanel children,
explicit handler parameters, narrowed FileLoader arguments and Form names run in
the normal shared suite. Nullable FileLoader is an
accepted difference, requiring narrowing before Media member completion.
`test:analysis legacy-editor` exercises the production editor hook with the flag
off for RepeatingPanel, sender and narrowed FileLoader cases. These fixtures do
not establish exhaustive app parity; representative existing apps and additional
service/dependency variants still need validation. The Pyright comparison
backend's override-snippet fixture is unsupported. Native CLI behaviour is
protected by its integration tests. The generic WASM API extensions expose
callable-parameter metadata and the existing auto-import completion setting;
inference remains upstream. See [engine compatibility](../ENGINE_PATTERNS.md).

## Additional language requests

`textDocument/typeDefinition` maps native type targets back to original sources.
`textDocument/codeAction` recomputes the current diagnostic, obtains upstream
import/fix/ignore actions and returns complete current-file edits. If any edit
cannot map to original source, the entire action is omitted. Read-only sources
return no edit actions. There is no fix-all or safety classification.
`textDocument/inlayHint` exposes inferred type and parameter labels without
applying their insertion edits. The IDE owns the opt-in display preference.
These requests use upstream WASM APIs; no engine changes are required.
