# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the Plotly catalogue generator in doc/anvil-api-stubs/plotly-stubs.mjs instead, then run:
#   pnpm -F docs build
#
from plotly._base import _PlotlyObject
from typing import Any, Mapping

class Marker(_PlotlyObject):
    "Create a new 'Marker' object"
    color: Any
    "Sets the marker color of selected points."
    opacity: float | Any
    "Sets the marker opacity of selected points."
    size: float | Any
    "Sets the marker size of selected points."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        color: Any = ...,
        opacity: Any = ...,
        size: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Marker' object\n\nArgs:\n    color: Sets the marker color of selected points.\n    opacity: Sets the marker opacity of selected points.\n    size: Sets the marker size of selected points."
        ...
