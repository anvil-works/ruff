# Upstream engine compatibility

Anvil validation uses upstream ty without local engine patches. All sources and
tests under `crates/` match `main`; verify with `git diff main -- crates`.
Anvil support lives in the adapter, generated declarations and API stubs under
`anvil/`.

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
