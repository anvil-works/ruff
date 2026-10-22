# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the Plotly catalogue generator in doc/anvil-api-stubs/plotly-stubs.mjs instead, then run:
#   pnpm -F docs build
#
from plotly._base import _PlotlyObject
from typing import Any, Mapping

class X(_PlotlyObject):
    "Create a new 'X' object"
    opacity: float | Any
    "Sets the projection color."
    scale: float | Any
    "Sets the scale factor determining the size of the projection marker points."
    show: bool | Any
    "Sets whether or not projections are shown along the x axis."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        opacity: Any = ...,
        scale: Any = ...,
        show: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'X' object\n\nArgs:\n    opacity: Sets the projection color.\n    scale: Sets the scale factor determining the size of the projection marker points.\n    show: Sets whether or not projections are shown along the x axis."
        ...

class Y(_PlotlyObject):
    "Create a new 'Y' object"
    opacity: float | Any
    "Sets the projection color."
    scale: float | Any
    "Sets the scale factor determining the size of the projection marker points."
    show: bool | Any
    "Sets whether or not projections are shown along the y axis."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        opacity: Any = ...,
        scale: Any = ...,
        show: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Y' object\n\nArgs:\n    opacity: Sets the projection color.\n    scale: Sets the scale factor determining the size of the projection marker points.\n    show: Sets whether or not projections are shown along the y axis."
        ...

class Z(_PlotlyObject):
    "Create a new 'Z' object"
    opacity: float | Any
    "Sets the projection color."
    scale: float | Any
    "Sets the scale factor determining the size of the projection marker points."
    show: bool | Any
    "Sets whether or not projections are shown along the z axis."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        opacity: Any = ...,
        scale: Any = ...,
        show: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Z' object\n\nArgs:\n    opacity: Sets the projection color.\n    scale: Sets the scale factor determining the size of the projection marker points.\n    show: Sets whether or not projections are shown along the z axis."
        ...
