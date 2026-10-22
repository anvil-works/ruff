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
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        color: Any = ...,
        opacity: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Marker' object\n\nArgs:\n    color: Sets the marker color of selected points.\n    opacity: Sets the marker opacity of selected points."
        ...

class Textfont(_PlotlyObject):
    "Create a new 'Textfont' object"
    color: Any
    "Sets the text font color of selected points."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        color: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Textfont' object\n\nArgs:\n    color: Sets the text font color of selected points."
        ...
