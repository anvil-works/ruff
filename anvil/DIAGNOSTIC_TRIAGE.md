# Developer-visible diagnostic triage

This document records historical trials. The current integration uses unchanged
upstream ty; the three generic engine patches discussed below have been removed.
See [ENGINE_PATTERNS.md](ENGINE_PATTERNS.md) for accepted typing limitations.
Historical reports and diagnostic counts describe their recorded builds.

The historical six-app corpus below was measured on 9 October 2026. The
10 October combined trial applies the two submitted generic corrections, the
audited instance-rebinding correction, and the authoritative stub fixes to an
isolated current-upstream engine. See the
[combined report](reports/2026-10-10-combined-summary.md) for current diagnostics,
performance and source provenance.

The corrected stubs are present in Anvil's `master` at `b716e8f217d7`; its working
tree is clean. This task did not commit or rewrite the Anvil checkout. The earlier
local engine patch and production submodule pin remain untouched. The third
upstream contribution is prepared locally for human review; see
[upstream preparation](upstream/README.md).

The combined engine passes all 501 semantic mdtest files, and its release passes
172 real-CLI acceptance tests. Those controls and the diagnostic review establish
the tested contracts; differing real-app counts do not establish complete parity.
Missing unannotated return inference and dynamic designer bases remain limits of
an opt-in validation trial.

## Evidence

- [Complete six-app CLI outputs](reports/2026-10-09-real-corpus.json).
- [26 reduced CLI scenarios and temporary API variants](reports/2026-10-09-diagnostic-triage.json),
    including sources, executable/stub fingerprints, the local engine patch,
    experiment script, diagnostic messages and verified current outcomes.
- [Source-line difference leads](reports/2026-10-09-diagnostic-differences.json).
    There are 51 native and 569 Pyright candidate diagnostics on lines where the
    other backend reports nothing. This is a navigation aid, not proof of missed
    checks or false positives. Same-line diagnostics can have different meanings;
    one engine can report several issues for a single cause. Source contexts still
    match the measured app fingerprints.

Five pure-Python valid controls run successfully under CPython. The reduced
unannotated optional-return case also reproduces its runtime `AttributeError`.
Neither engine nor Anvil runtime behavior was inferred from diagnostic counts.

## Shared source-stub corrections

| Contract                                                        | Observed problem                                                                                                                                                                                                                                                 | Reduced proof and implementation boundary                                                                                                                                                                                                                                                                                                                                                                                                                          |
| --------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `anvil.is_server_side()` is constant for a checking environment | Routing conditionally reexports a server timer requiring `ms` or the browser timer whose delay defaults to zero. Native combines both possibilities, giving three spurious timer errors and related `document` errors in the corpus                              | Direct browser timer calls pass. The conditional-reexport reproduction fails native and passes Pyright. A complete temporary client API with `Literal[False]` makes native pass; `Literal[True]` preserves the genuine server missing-argument error. The runtime returns `pyFalse` in the client and `True` in the downlink. Express these return types in the client/server source-stub outputs, using the existing generator rather than a special ty predicate |
| Browser `Storage` exposes `getItem`, `setItem` and `removeItem` | The source window stub declares `Storage` twice: the earlier webtypy declaration omits those operations, while a later override supplies them. ty resolves both declarations and rejects supported calls. Four corpus errors affect the client suite and Routing | A temporary snapshot containing one complete declaration removes the valid-call errors. Wrong `setItem` values and incompatible assignments from `getItem` still fail. Correct the authoritative Anvil DOM stub and its regeneration path; do not add an engine exception for this duplicate class                                                                                                                                                                 |

The user wants `raise_event()` to retain its declared `None` contract and does not
want to support callers relying on handler return values. The runtime currently
passes through the last handler result, and the historical temporary `Any` probe
removes Extras' always-falsy-condition warning, but that implementation behavior
does not establish the intended API contract. Keep `-> None` and the warning for
Extras' return-dependent usage. This decision supersedes the initial proposal to
widen the event signatures; the recorded experiment remains evidence only.

The return-type variation proves the reduced environment-dispatch case, not every
cross-environment import or inactive helper body. Integration coverage should also
exercise reexports, the server view of shared client modules, and genuinely
forbidden imports before claiming full guard-sensitive validation.

Source locations:

- `../anvil/doc/anvil-api-stubs/source/anvil/__init__.pyi` for the utility
    contract; its existing client/server section markers are the generation
    boundary.
- `../anvil/doc/anvil-api-stubs/source/anvil/js/window/__init__.pyi` for `Storage`.
    Its misleading generation header has been corrected: maintain the DOM source
    here and rebuild client outputs with `generate-stubs.mjs`.
- Runtime evidence: `../anvil/runtime/client/js/modules/_anvil/open-form.ts`,
    `../anvil/runtime/downlink/python/anvil/__init__.py`,
    `../anvil/runtime/client/js/components/Component.ts`, and
    `../anvil/runtime/client/js/@Sk/namespace.d.ts`.

Implementation follows the user's source-of-truth instruction: edit in the Anvil
checkout, rebuild with the existing scripts, sync the consuming repository, and
originally leave source changes uncommitted on Anvil's `master`. They are now
present in the clean `master` checkout; this task did not commit them. The source generator's 15
tests pass and the consumer sync check passes.

## Generic correctness candidates

**Conditional float division.** Extras' Slider constructs a float, optionally
divides it by 100, then calls `.is_integer()`. The constructor-only control passes
both engines. Adding the division produces a native unresolved-attribute error
for a possible `int`, although every runtime value in this example is a float.
The reduced CPython controls pass. This is a generic numeric-inference candidate
for a separate upstream issue/fix; it does not need Anvil adapter policy.

**Class-level rebinding through `cls`.** An annotated compatible replacement
assigned in `__init_subclass__` passes Pyright and runs correctly, but native rejects
it. Assigning the same unbound replacement to the exact class passes both engines.
A replacement returning the wrong type fails both. This concerns the class receiver
and differs from the already implemented instance-method rebinding fix. Keep the
negative control and investigate it as a separate generic engine correction.
The unannotated minimal case is also noisy on Pyright, so it cannot alone establish
the native false positive.

## Meaningful checking loss

ExampleTabulator's name helpers may fall off the end and return `None`. Pyright
infers that possibility and rejects `.capitalize()`; native accepts those two
calls. The reduced unannotated example passes native checking but raises an
`AttributeError` at runtime. Adding `-> str | None` makes both engines reject it.

Both the pinned engine and upstream baseline use `Unknown` for this unannotated
return. This is missing return inference, rather than an inferred `str` that
incorrectly discarded `None`. Upstream tracks the feature in
[ty #128](https://github.com/astral-sh/ty/issues/128), including implicit `None`
and method-inheritance considerations.

This is ordinary Python checking that is weaker on this input, not Pyright-specific
wording or a bespoke lint. Annotate important nullable APIs as `-> str | None` and
handle the absent value at the call site. Record the unannotated gap as a limitation
of an opt-in trial and follow the upstream feature; do not add an Anvil-specific
return-inference workaround. The previously documented dynamic designer-base loss
remains another separate limit.

## Differences that do not justify new fork behavior

- Browser coercion, nullable DOM lookups, dynamically supplied attributes,
    heterogeneous dictionaries and Material 3's autocompleter decorator convention
    retain the decisions already recorded in `VALIDATION_PARITY.md`.
- Property-override diagnostics account for much of the Pyright excess. Preserve
    ty's own checks rather than reproduce the volume of Pyright messages. Reduced
    annotated compatibility controls remain the appropriate acceptance boundary.
- Extras' namedtuple aliases are valid Python but produce a native
    `mismatched-type-name` warning; native still exits successfully. This is a
    non-blocking advisory-policy choice, separate from type-safety corrections.
- The modal unit tests deliberately use ignored positional options and duplicate
    `content` arguments to exercise runtime compatibility warnings. Direct reduced
    calls are rejected by both engines; this is not new production-pattern noise.
- Generic `Component` does not universally expose visual properties. The runtime
    base implements event/hooks APIs. Both reduced checkers reject `visible` on
    that generic annotation; widening every component in the stubs is not supported
    by that runtime contract.
- Native accepts arbitrary browser-global extensions that Pyright flags. Keep
    that accepted interop difference rather than copying the baseline warnings.
- Intentional invalid forms and Notification values remain useful failures;
    deprecation warnings remain visible. A native-only message is not automatically
    a false positive.

## Remaining boundary

The stub proofs are real-CLI regressions. The numeric and class-receiver fixes are
submitted as [Ruff #29275](https://github.com/astral-sh/ruff/pull/29275) and
[#29276](https://github.com/astral-sh/ruff/pull/29276). The instance fix is committed
on its own local branch, reviewed and tested, but not submitted. All three are
combined in the isolated trial; none changes the production Anvil engine pin.

The fresh corpus removes the expected Storage, float-division, environment-dispatch
and class-receiver false positives. New upstream property-override checks expose
three `role` contracts where YAML declares `str` but the app reuses a property
returning `str | list[str] | None`. A remaining nullable DOM-head access replaces
an earlier broader `document` error. These are recorded explicitly rather than
silencing a rule. The source projects remain untouched.

Before distributing the combined engine, establish a published engine commit and
Anvil fork source revision. Keep the unannotated-return and dynamic-base
checking gaps visible in any opt-in trial.
