# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the Plotly catalogue generator in doc/anvil-api-stubs/plotly-stubs.mjs instead, then run:
#   pnpm -F docs build
#
from plotly._base import _PlotlyObject
from typing import Any, Mapping

class Line(_PlotlyObject):
    "Create a new 'Line' object"
    color: Any
    "Sets the marker.line color. It accepts either a specific color or an array of numbers that are mapped to the colorscale relative to the max and min values of the array or relative to `marker.line.cmin` and `marker.line.cmax` if set."
    width: float | Any
    "Sets the width (in px) of the lines bounding the marker points."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        color: Any = ...,
        width: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Line' object\n\nArgs:\n    color: Sets the marker.line color. It accepts either a specific color or an array of numbers that are mapped to the colorscale relative to the max and min values of the array or relative to `marker.line.cmin` and `marker.line.cmax` if set.\n    width: Sets the width (in px) of the lines bounding the marker points."
        ...
