# Size-focused Ruff for the IDE

`@anvil-works/ruff-wasm-web` packages unmodified upstream Ruff with Rust's
size-focused optimisation (`z`, one codegen unit). It preserves the web package's
JavaScript API, lint rules, formatting options and UTF-16 diagnostic support.
Ty is not included. No Anvil-specific lint or inference patches are applied.

The package version identifies both the upstream release and our packaging
revision: `0.17.1-anvil.0` contains Ruff 0.17.1. `Workspace.version()` returns the
upstream version. The pin and source archive checksum are in `upstream.json`.

## Build and check

Install the pinned Rust toolchain through rustup, wasm-pack and the GitHub CLI.
From this directory:

```sh
pnpm build
pnpm test
pnpm pack --pack-destination /path/to/release-artifacts
```

The build verifies and extracts the upstream archive, then builds only its
`ruff_wasm` crate. Source and Cargo artifacts remain in the ignored `.cache/`
directory. Generated JS, declarations, WASM and licence are not checked into Git.
`build.json` records source identity, optimisation settings, build-input hash and
output hashes. Packing refuses stale or modified build outputs.

To upgrade, update the upstream version, full commit and archive checksum in
`upstream.json`, and the package version in `package.json`. Rebuild and compare
lint results, fixes, formatting and timing against that exact upstream npm
release before publishing. Keep this package independent of Ty/native checker
releases. Stu performs source pushes and npm publication.
