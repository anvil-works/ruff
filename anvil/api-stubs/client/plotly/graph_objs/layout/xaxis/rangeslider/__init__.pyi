# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the Plotly catalogue generator in doc/anvil-api-stubs/plotly-stubs.mjs instead, then run:
#   pnpm -F docs build
#
from plotly._base import _PlotlyObject
from typing import Any, Mapping

class YAxis(_PlotlyObject):
    "Create a new 'YAxis' object"
    range: Any
    "Sets the range of this axis for the rangeslider."
    rangemode: Any
    "Determines whether or not the range of this axis in the rangeslider use the same value than in the main plot when zooming in/out. If *auto*, the autorange will be used. If *fixed*, the `range` is used. If *match*, the current range of the corresponding y-axis on the main subplot is used."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        range: Any = ...,
        rangemode: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'YAxis' object\n\nArgs:\n    range: Sets the range of this axis for the rangeslider.\n    rangemode: Determines whether or not the range of this axis in the rangeslider use the same value than in the main plot when zooming in/out. If *auto*, the autorange will be used. If *fixed*, the `range` is used. If *match*, the current range of the corresponding y-axis on the main subplot is used."
        ...
