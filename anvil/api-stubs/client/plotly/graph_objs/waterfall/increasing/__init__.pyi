# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the Plotly catalogue generator in doc/anvil-api-stubs/plotly-stubs.mjs instead, then run:
#   pnpm -F docs build
#
from plotly._base import _PlotlyObject
from typing import Any, Mapping
import plotly.graph_objs.waterfall.increasing.marker as _plotly_graph_objs_waterfall_increasing_marker
import plotly.graph_objs.waterfall.increasing.marker as marker

class Marker(_PlotlyObject):
    "Create a new 'Marker' object"
    color: Any
    "Sets the marker color of all increasing values."
    @property
    def line(self) -> _plotly_graph_objs_waterfall_increasing_marker.Line | Any:
        ...
    @line.setter
    def line(self, value: Any) -> None: ...
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        color: Any = ...,
        line: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Marker' object\n\nArgs:\n    color: Sets the marker color of all increasing values."
        ...
