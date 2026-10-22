# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the Plotly catalogue generator in doc/anvil-api-stubs/plotly-stubs.mjs instead, then run:
#   pnpm -F docs build
#
from plotly._base import _PlotlyObject
from typing import Any, Mapping

class Center(_PlotlyObject):
    "Create a new 'Center' object"
    x: float | Any
    y: float | Any
    z: float | Any
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        x: Any = ...,
        y: Any = ...,
        z: Any = ...,
        **kwargs: Any,
    ) -> None:
        ...

class Eye(_PlotlyObject):
    "Create a new 'Eye' object"
    x: float | Any
    y: float | Any
    z: float | Any
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        x: Any = ...,
        y: Any = ...,
        z: Any = ...,
        **kwargs: Any,
    ) -> None:
        ...

class Projection(_PlotlyObject):
    "Create a new 'Projection' object"
    type: Any
    "Sets the projection type. The projection type could be either *perspective* or *orthographic*. The default is *perspective*."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        type: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Projection' object\n\nArgs:\n    type: Sets the projection type. The projection type could be either *perspective* or *orthographic*. The default is *perspective*."
        ...

class Up(_PlotlyObject):
    "Create a new 'Up' object"
    x: float | Any
    y: float | Any
    z: float | Any
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        x: Any = ...,
        y: Any = ...,
        z: Any = ...,
        **kwargs: Any,
    ) -> None:
        ...
