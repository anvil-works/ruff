# @anvil-works/anvil-ty

The Python checker used by `anvil validate`. This package selects the native
executable for your platform; its companion package includes the Anvil API stubs
and source licences. anvil-cli depends on this package and calls the executable
directly.

The checker requires no Python installation or Rust toolchain at runtime. It
checks client and server code separately and supports Anvil form metadata,
components, events, server callables, tables and cached dependencies. Validation
does not download Anvil app dependencies.

Set `ANVIL_API_STUBS_PATH` to a directory containing generated `client/` and
`server/` API stubs to use those instead of the package's snapshot. Agent-host
sets this to its bundled stubs, so API updates do not require a checker version
change. An unset or blank value uses the package's stubs; an unreadable override
reports an error rather than falling back to older stubs.

For tools integrating the checker:

```js
const { executablePath } = require("@anvil-works/anvil-ty");
```

The checker and package are currently at the canary trial stage. This package
supplies validation; Anvil LSP integration is a separate project.

The tested builds are macOS ARM64 and Linux GNU ARM64/x64. The Linux binaries
require glibc 2.34 or newer; Alpine/musl is unsupported. Intel macOS and Windows
builds are configured in the release workflow and still need their first runner
checks before publication. See
`anvil/PUBLISHING.md` in the source repository for the release prerequisites.
