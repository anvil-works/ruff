# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the Plotly catalogue generator in doc/anvil-api-stubs/plotly-stubs.mjs instead, then run:
#   pnpm -F docs build
#
from plotly._base import _PlotlyObject
from typing import Any, Mapping

class X(_PlotlyObject):
    "Create a new 'X' object"
    fill: float | Any
    "Sets the fill ratio of the `slices`. The default fill value of the `slices` is 1 meaning that they are entirely shaded. On the other hand Applying a `fill` ratio less than one would allow the creation of openings parallel to the edges."
    locations: Any
    "Specifies the location(s) of slices on the axis. When not specified slices would be created for all points of the axis x except start and end."
    show: bool | Any
    "Determines whether or not slice planes about the x dimension are drawn."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        fill: Any = ...,
        locations: Any = ...,
        show: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'X' object\n\nArgs:\n    fill: Sets the fill ratio of the `slices`. The default fill value of the `slices` is 1 meaning that they are entirely shaded. On the other hand Applying a `fill` ratio less than one would allow the creation of openings parallel to the edges.\n    locations: Specifies the location(s) of slices on the axis. When not specified slices would be created for all points of the axis x except start and end.\n    show: Determines whether or not slice planes about the x dimension are drawn."
        ...

class Y(_PlotlyObject):
    "Create a new 'Y' object"
    fill: float | Any
    "Sets the fill ratio of the `slices`. The default fill value of the `slices` is 1 meaning that they are entirely shaded. On the other hand Applying a `fill` ratio less than one would allow the creation of openings parallel to the edges."
    locations: Any
    "Specifies the location(s) of slices on the axis. When not specified slices would be created for all points of the axis y except start and end."
    show: bool | Any
    "Determines whether or not slice planes about the y dimension are drawn."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        fill: Any = ...,
        locations: Any = ...,
        show: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Y' object\n\nArgs:\n    fill: Sets the fill ratio of the `slices`. The default fill value of the `slices` is 1 meaning that they are entirely shaded. On the other hand Applying a `fill` ratio less than one would allow the creation of openings parallel to the edges.\n    locations: Specifies the location(s) of slices on the axis. When not specified slices would be created for all points of the axis y except start and end.\n    show: Determines whether or not slice planes about the y dimension are drawn."
        ...

class Z(_PlotlyObject):
    "Create a new 'Z' object"
    fill: float | Any
    "Sets the fill ratio of the `slices`. The default fill value of the `slices` is 1 meaning that they are entirely shaded. On the other hand Applying a `fill` ratio less than one would allow the creation of openings parallel to the edges."
    locations: Any
    "Specifies the location(s) of slices on the axis. When not specified slices would be created for all points of the axis z except start and end."
    show: bool | Any
    "Determines whether or not slice planes about the z dimension are drawn."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        fill: Any = ...,
        locations: Any = ...,
        show: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Z' object\n\nArgs:\n    fill: Sets the fill ratio of the `slices`. The default fill value of the `slices` is 1 meaning that they are entirely shaded. On the other hand Applying a `fill` ratio less than one would allow the creation of openings parallel to the edges.\n    locations: Specifies the location(s) of slices on the axis. When not specified slices would be created for all points of the axis z except start and end.\n    show: Determines whether or not slice planes about the z dimension are drawn."
        ...
