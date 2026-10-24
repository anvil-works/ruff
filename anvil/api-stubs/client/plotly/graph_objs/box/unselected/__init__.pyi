# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the Plotly catalogue generator in doc/anvil-api-stubs/plotly-stubs.mjs instead, then run:
#   pnpm -F docs build
#
from plotly._base import _PlotlyObject
from typing import Any, Mapping

class Marker(_PlotlyObject):
    "Create a new 'Marker' object"
    color: Any
    "Sets the marker color of unselected points, applied only when a selection exists."
    opacity: float | Any
    "Sets the marker opacity of unselected points, applied only when a selection exists."
    size: float | Any
    "Sets the marker size of unselected points, applied only when a selection exists."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        color: Any = ...,
        opacity: Any = ...,
        size: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Marker' object\n\nArgs:\n    color: Sets the marker color of unselected points, applied only when a selection exists.\n    opacity: Sets the marker opacity of unselected points, applied only when a selection exists.\n    size: Sets the marker size of unselected points, applied only when a selection exists."
        ...
