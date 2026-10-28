# Upstream engine compatibility

Anvil uses upstream ty inference and diagnostics. Anvil-specific support lives
in the adapter, generated declarations and API stubs under `anvil/`.

Generic WASM API extensions expose existing engine behaviour:

- `active_parameter_expects_callable` on signature help uses native alias
    expansion, materialisation and callable conversion. It lets completion insert
    a callback reference without `()`, including for ordinary Python APIs.
- `Workspace.completions` accepts an optional `auto_import` boolean. It selects
    the existing completion setting; omitting it retains upstream auto-imports.
- An optional fourth `receiver` argument adds qualified members of a visible
    binding to ordinary bare-name completions. For example, `receiver="self"` matches
    `self.name_box` for `name`, `name_box`, `sel` or an empty prefix. The query uses
    the binding's inferred type and enclosing scope, including an indented blank
    line inside a function. Strings, imports and explicit attribute expressions
    retain their ordinary completion path. It reads existing source without
    temporarily inserting `self.`, which would invalidate incremental analysis.
    Expansion runs inside the existing scoped completion collection. A symbol-table
    lookup finds the binding before inferring its type; other names need no extra
    inference. The adapter decides when to request it; omitting the argument keeps
    ordinary upstream completion and inference unchanged.
- Completion items expose optional `scope_depth` and `inheritance_depth` numbers.
    These identify the declaration's distance in the already visited enclosing
    scopes or class MRO. Native inference, member deduplication and ranking stay
    unchanged. The browser adapter uses this provenance to rank local bindings
    and own-class members ahead of outer or inherited ones.
- `Workspace.isBuiltinReference` returns `true` only for a bare name proven to
    use a standard builtin. It exposes the existing semantic binding check without
    inferring the reference's type. Shadowed names, attributes, project builtin
    overrides and unknown star imports return `false`. Resolved leaf-module star
    imports use upstream's binding table; re-export chains, invalid nested stars
    and unbounded module `__getattr__` retain the conservative fallback. This is a
    conservative proof: `false` means callers must use ordinary resolution, not
    that the reference cannot be a builtin. The RPC adapter uses it to avoid
    resolving standard builtin calls as possible server calls. The star-import
    check is cached per program file, with resolver and imported-source
    invalidation, so probing several calls does not repeatedly scan the file.
    The adapter uses existing parsed call ranges to skip this proof for attribute
    calls, which still use ordinary API resolution.

These do not change inference rules. Keep these API extensions separate from Anvil
compatibility logic and remove each local difference when an equivalent upstream
API becomes available.
Review engine differences with `git diff main -- crates`.

## Browser build capabilities

`ty_wasm` makes its existing formatter dependency and `Workspace.format` export
optional through a default-enabled `format` Cargo feature. Normal builds keep
the formatting API. Anvil's browser release disables it because the IDE uses
Ruff for formatting; its type inference and other language services are unchanged.
Remove this local build extension when upstream provides the same option.

## Completion work

Scoped completion applies its existing name matcher before resolving module
members, including builtins. The module-member implementation is shared with
ordinary attribute/import lookup; those callers retain the unfiltered path.
Matching declarations, synthetic members and builtin precedence stay unchanged.
This reduces first-use completion work without changing inference rules or
suppressing candidates.

## Completion index preparation

`Workspace.prepareCompletionIndex(file, offset, batch_size)` exposes batches of
the cached public-symbol index used by native auto-import search. It returns the
next offset, or no offset when complete. The batch size bounds the number of
modules visited, not elapsed time. This is a generic API; it does not change
inference, imports, candidate selection or source text.

The browser adapter keeps a preparation cursor per native workspace and visits
eight modules per request. Changed module paths or options restart the cursor;
ordinary content edits retain it and use native incremental invalidation. The IDE
yields between requests and pauses future batches while typing. Its ordinary
completion source disables auto-import search; a separate source requests imports
after a typing pause and preparation. The adapter refuses a cold import-only query
and requests preparation again, including after lazy library loads. Native type
analysis and matching still have a first-use cost after the index is prepared.

Keep this API isolated from Anvil compatibility logic, and remove the local API
when upstream provides an equivalent. The editor's performance suite and browser
interaction tests cover the scheduling policy; the browser package tests cover
phase isolation, readiness, body edits, exported-name changes and added modules.

## Accepted typing limitations

- **Method assignment through `cls: type[Base]`.** ty can reject a replacement
    accepted on a concrete class. The broader rule proposed in
    [Ruff #29276](https://github.com/astral-sh/ruff/pull/29276) was rejected because
    a subclass can have a more specific signature. Routing's `__init_subclass__`
    pattern can therefore produce a diagnostic.
- **Method replacement on an instance.** ty can retain the declared method's
    `self` parameter when checking an instance-assigned function, causing assignment
    and call diagnostics for patterns used by Tabulator. The experimental local
    correction was never submitted upstream and is not part of this fork.
- **Built-in true division.** Numeric stub annotations can widen a float division
    result to `int | float`. On Python 3.10 this can produce an `is_integer` attribute
    error. [Ruff #29275](https://github.com/astral-sh/ruff/pull/29275) was closed over
    the limited practical benefit and the special-case approach.

Earlier trial reports and packages include these engine patches. Their recorded
sources and diagnostic counts do not describe a build of the current integration.
Keep diagnostics visible; address affected app annotations or use a targeted
suppression where appropriate rather than adding engine exceptions.

## Design-component class identity

`get_design_component` support comes from Anvil's authoritative API stub, which
preserves the input component class. It needs no engine change.
`anvil/tests/test_engine_patterns.py` checks inherited members and rejects an
instance argument through the real CLI. Arbitrary dynamic Python class bases
retain ordinary ty behaviour.

## Browser filesystem revisions

The upstream WASM filesystem uses millisecond timestamps for file and directory
revisions. The adapter closes and reopens changed files so several inference
snapshots within one tick cannot retain stale source. Generated Form item types
live in one module mounted before the first query; updating it avoids discovery
of newly created sibling modules within a cached directory. Tests freeze the
worker clock across inference, producer edits and restoration. No engine patch
or production clock override is required.
