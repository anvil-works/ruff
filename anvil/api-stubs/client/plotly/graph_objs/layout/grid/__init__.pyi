# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the Plotly catalogue generator in doc/anvil-api-stubs/plotly-stubs.mjs instead, then run:
#   pnpm -F docs build
#
from plotly._base import _PlotlyObject
from typing import Any, Mapping

class Domain(_PlotlyObject):
    "Create a new 'Domain' object"
    x: Any
    "Sets the horizontal domain of this grid subplot (in plot fraction). The first and last cells end exactly at the domain edges, with no grout around the edges."
    y: Any
    "Sets the vertical domain of this grid subplot (in plot fraction). The first and last cells end exactly at the domain edges, with no grout around the edges."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        x: Any = ...,
        y: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Domain' object\n\nArgs:\n    x: Sets the horizontal domain of this grid subplot (in plot fraction). The first and last cells end exactly at the domain edges, with no grout around the edges.\n    y: Sets the vertical domain of this grid subplot (in plot fraction). The first and last cells end exactly at the domain edges, with no grout around the edges."
        ...
