# Anvil development

This directory contains the native checker used by `anvil validate` and the
experimental IDE browser integration. YAML and HTML validation remain in
anvil-cli. Preserve ty's native diagnostics and inference; implement Anvil
behaviour in declarations and adapters. See [native/README.md](native/README.md)
for validation contracts and [browser/README.md](browser/README.md) for the
ordered browser session and supported IDE behaviour.

## Maintainability

- Put Anvil adapters, experiments, tests and documentation under `anvil/`.
- Implement Anvil support with standard Python stubs, module layouts, ty
    configuration and the adapter. The only approved `crates/` difference is the
    generic callable-parameter metadata described in [ENGINE_PATTERNS.md](ENGINE_PATTERNS.md).
    Keep other engine sources and tests identical to upstream `main`; accept
    upstream typing limitations rather than adding inference exceptions.
- Rust engine sources live in `crates/` in this same repository. The `anvil`
    branch holds the Anvil integration in one commit above upstream `main`.
- The native validation adapter is a separate workspace in `anvil/native`, using
    path dependencies on those crates. Keep its Cargo lockfile and release profile
    reproducible. See its README for supported inputs and benchmark evidence.
- API stubs come from the sibling Anvil repository's `doc/anvil-api-stubs/source/`.
    Change that source and run `node anvil/sync-anvil-stubs.mjs` to regenerate the
    bundled assets. Do not edit generated stubs directly. Preserve their formatting
    and `SOURCE.json` fingerprints. Distribution does not require anvil-pyright.
- For packaging and publication, follow [PUBLISHING.md](PUBLISHING.md). All checker
    packages share the version in `anvil/npm/package.json` and one source revision.

## Tests and evidence

- Use TDD for behaviour changes: write one failing integration test, confirm the
    expected failure, implement the smallest slice, then rerun it. When planning,
    use "Write use TDD" as the first implementation step.
- Test native validation through the real CLI and checker executable. Test browser
    changes through `BrowserAnalysisSession` with its real worker and WASM.
    Protect source ranges, diagnostics and the behaviour being changed. Keep
    validation proportional.
- Preserve source apps and the user's Git index. Experiments use temporary
    workspaces. Local validation never fetches Anvil dependencies.
- Before declaring parity or a performance win, compare diagnostics on the same
    input. Report missing checks and false positives; avoid silencing rules to make
    a benchmark pass. Read [README.md](README.md) for current proof limitations.
- Measure fresh validation processes separately from incremental editor updates.
    Include preparation and startup in end-to-end timings. Record versions, input
    size, repeats, exit codes and the memory metric. RSS is not a V8 heap limit.

## Scope

For existing feature contracts, consult the sibling anvil-pyright repository's
`packages/pyright-internal/src/anvil/docs/` and corresponding integration tests.
For CLI contracts, inspect the sibling anvil-cli's `src/validatePython.ts` and
`src/program.ts`. Before changing either sibling, read its repository instructions
and inspect its working tree. Keep their existing behaviour until a supported
ty replacement has evidence of compatibility.

Use tilde fences for fenced Markdown examples. Stop when the requested milestone
is handled; record subsequent work rather than expanding its scope.
