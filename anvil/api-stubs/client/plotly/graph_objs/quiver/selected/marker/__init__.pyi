# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the Plotly catalogue generator in doc/anvil-api-stubs/plotly-stubs.mjs instead, then run:
#   pnpm -F docs build
#
from plotly._base import _PlotlyObject
from typing import Any, Mapping

class Line(_PlotlyObject):
    "Create a new 'Line' object"
    width: float | Any
    "Sets the line width of selected points."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        width: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Line' object\n\nArgs:\n    width: Sets the line width of selected points."
        ...
