# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the Plotly catalogue generator in doc/anvil-api-stubs/plotly-stubs.mjs instead, then run:
#   pnpm -F docs build
#
from plotly._base import _PlotlyObject
from typing import Any, Mapping

class Line(_PlotlyObject):
    "Create a new 'Line' object"
    color: Any
    "Sets the base color of unselected lines. in connection with `unselected.line.opacity`."
    opacity: float | Any
    "Sets the opacity of unselected lines. The default *auto* decreases the opacity smoothly as the number of lines increases. Use *1* to achieve exact `unselected.line.color`."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        color: Any = ...,
        opacity: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Line' object\n\nArgs:\n    color: Sets the base color of unselected lines. in connection with `unselected.line.opacity`.\n    opacity: Sets the opacity of unselected lines. The default *auto* decreases the opacity smoothly as the number of lines increases. Use *1* to achieve exact `unselected.line.color`."
        ...
