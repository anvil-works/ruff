# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the Plotly catalogue generator in doc/anvil-api-stubs/plotly-stubs.mjs instead, then run:
#   pnpm -F docs build
#
from plotly._base import _PlotlyObject
from typing import Any, Mapping

class X(_PlotlyObject):
    "Create a new 'X' object"
    fill: float | Any
    "Sets the fill ratio of the `caps`. The default fill value of the `caps` is 1 meaning that they are entirely shaded. On the other hand Applying a `fill` ratio less than one would allow the creation of openings parallel to the edges."
    show: bool | Any
    "Sets the fill ratio of the `slices`. The default fill value of the x `slices` is 1 meaning that they are entirely shaded. On the other hand Applying a `fill` ratio less than one would allow the creation of openings parallel to the edges."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        fill: Any = ...,
        show: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'X' object\n\nArgs:\n    fill: Sets the fill ratio of the `caps`. The default fill value of the `caps` is 1 meaning that they are entirely shaded. On the other hand Applying a `fill` ratio less than one would allow the creation of openings parallel to the edges.\n    show: Sets the fill ratio of the `slices`. The default fill value of the x `slices` is 1 meaning that they are entirely shaded. On the other hand Applying a `fill` ratio less than one would allow the creation of openings parallel to the edges."
        ...

class Y(_PlotlyObject):
    "Create a new 'Y' object"
    fill: float | Any
    "Sets the fill ratio of the `caps`. The default fill value of the `caps` is 1 meaning that they are entirely shaded. On the other hand Applying a `fill` ratio less than one would allow the creation of openings parallel to the edges."
    show: bool | Any
    "Sets the fill ratio of the `slices`. The default fill value of the y `slices` is 1 meaning that they are entirely shaded. On the other hand Applying a `fill` ratio less than one would allow the creation of openings parallel to the edges."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        fill: Any = ...,
        show: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Y' object\n\nArgs:\n    fill: Sets the fill ratio of the `caps`. The default fill value of the `caps` is 1 meaning that they are entirely shaded. On the other hand Applying a `fill` ratio less than one would allow the creation of openings parallel to the edges.\n    show: Sets the fill ratio of the `slices`. The default fill value of the y `slices` is 1 meaning that they are entirely shaded. On the other hand Applying a `fill` ratio less than one would allow the creation of openings parallel to the edges."
        ...

class Z(_PlotlyObject):
    "Create a new 'Z' object"
    fill: float | Any
    "Sets the fill ratio of the `caps`. The default fill value of the `caps` is 1 meaning that they are entirely shaded. On the other hand Applying a `fill` ratio less than one would allow the creation of openings parallel to the edges."
    show: bool | Any
    "Sets the fill ratio of the `slices`. The default fill value of the z `slices` is 1 meaning that they are entirely shaded. On the other hand Applying a `fill` ratio less than one would allow the creation of openings parallel to the edges."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        fill: Any = ...,
        show: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Z' object\n\nArgs:\n    fill: Sets the fill ratio of the `caps`. The default fill value of the `caps` is 1 meaning that they are entirely shaded. On the other hand Applying a `fill` ratio less than one would allow the creation of openings parallel to the edges.\n    show: Sets the fill ratio of the `slices`. The default fill value of the z `slices` is 1 meaning that they are entirely shaded. On the other hand Applying a `fill` ratio less than one would allow the creation of openings parallel to the edges."
        ...
