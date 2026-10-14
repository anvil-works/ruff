# Publication review — 14 October 2026

This historical review predates the removal of all local engine patches. The
current engine sources and tests match upstream `main`; see
[ENGINE_PATTERNS.md](ENGINE_PATTERNS.md) and rebuild packages before publication.

This report records the earlier two-repository review. The current source layout
and publication instructions are in [PUBLISHING.md](PUBLISHING.md). The consolidated
Ruff branch is reviewed below; earlier findings are retained as historical context.

## Consolidated Ruff fork review

Two independent reviewers inspected the complete local branch against upstream
`main` (`d298e5155a`), with comparisons to the previous wrapper and engine sources
to distinguish consolidation changes. Standards and Spec reviews found no
remaining blockers after correcting duplicated Python script metadata and the
native version message. The version now comes from Cargo, matching npm's canary.

The adapter, engine dependencies, API assets and npm packages now use one checkout
and source revision. Removing the extra revision helper and nested source manifest
avoids duplicated release state. The existing collector and installed-package
tests protect meaningful release behaviour; further test scaffolding is unnecessary.

Changed-file hooks, workflow schema/security checks and actionlint pass. All 12
changed engine mdtest files pass without snapshot changes. The native checker
passes its locked release build and unit test. The existing acceptance suite runs
188 cases: 185 pass, with the three release-only smoke checks skipped until package
archives are selected. The relocated npm-package test passes, including real CLI
validation and unchanged app inputs.

Windows/Intel runner execution and the publication-dependent CLI lockfile remain
the release prerequisites in [PUBLISHING.md](PUBLISHING.md). Earlier trial archives
are historical; rebuild packages from the consolidated commit before upload.

## Follow-up status

The findings below prompted the current local release changes. Windows import
aliases, row-model discovery and component-event lookup now share a module-name
conversion accepting both path separators. Linux npm metadata declares glibc,
and manifest paths remain consistent across OSes.

The dedicated Anvil workflow builds/tests five platforms and collects six npm
archives for local publication. It uses read-only repository permissions and no
publishing credentials. The user performs all pushing and publishing.

Two independent follow-up reviewers reported no blocking Standards or Spec
findings. The optional Standards suggestion to test a corrupted bundle hash was
implemented: collection rejects it before writing publication output. Workflow
syntax/security checks and installed Mac release smoke checks pass. Windows and
Intel Mac execution still require the first successful GitHub build.

## Original review

Two independent reviewers inspected the native adapter and CLI working changes
against fork `7300c73` and CLI `64343ca`. Neither changed files or posted comments.
This report records the publication decision before source commits.

## Standards

No hard violations of documented coding standards were found. Anvil code stays
under `anvil/`, the engine uses a committed remote pin, and CLI command/cache
extraction preserves shared logic.

Two concerns remain:

- Windows nested paths can generate invalid Python imports because module-name
    conversion replaces `/` only. Use path components in `native/src/imports.rs`,
    `models.rs` and `handles.rs` before releasing Windows.
- Linux metadata declares OS/CPU but does not distinguish glibc from musl. The
    tested binaries require glibc >=2.34. Add `libc: ["glibc"]` to Linux package
    metadata before upload. The package README now states the supported boundary.

The latter is a package compatibility judgement, rather than a hard documented
coding-standard violation. No further actionable CLI standards issues were found.

## Spec

One concrete blocker: the wrapper advertises Windows x64, but OS-native nested
paths retain backslashes in generated Python import names. This affects module
aliases, row-model imports and custom-component event lookup. It needs a fix and
Windows validation before claiming that platform works.

No further concrete spec violations were found. Checker replacement, CLI
contracts, narrow startup dispatch, Python-owned property precedence,
client/server separation, events and runtime selection match the agreed scope.

The already-known missing Windows/Intel Mac builds and registry-dependent CLI
lockfile remain prerequisites. The reused CLI version has been advanced locally
to the next available canary, `.23`; recheck availability at publication time.

Standards: two publication concerns, worst Windows import generation. Spec: one
blocker, Windows import generation. See [PUBLISHING.md](PUBLISHING.md) for the
release order. These source commits are ready for inspection, not a complete
five-platform release.
