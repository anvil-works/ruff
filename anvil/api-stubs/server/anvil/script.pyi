# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the source file in doc/anvil-api-stubs/source/ instead, then run:
#   pnpm -F docs build
#
# Type stubs for anvil.script module
# Generated files: server/anvil/script.pyi

from typing import Any

args: tuple[Any, ...]
"""The positional arguments this script was launched with (also available as sys.argv[1:],
except that Media arguments appear in sys.argv as the names of temporary files containing
their content).

Only readable from a running script (args passed via anvil.server.run_script() or anvil.server.launch_background_task()).

[Anvil Docs](https://anvil.works/docs/background-tasks)"""

return_value: Any
"""Set this from your script to return a value to anvil.server.run_script(). Defaults to None.

[Anvil Docs](https://anvil.works/docs/background-tasks)"""
