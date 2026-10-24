# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the Plotly catalogue generator in doc/anvil-api-stubs/plotly-stubs.mjs instead, then run:
#   pnpm -F docs build
#
from plotly._base import _PlotlyObject
from typing import Any, Mapping
import plotly.graph_objs.surface.contours.x as _plotly_graph_objs_surface_contours_x
import plotly.graph_objs.surface.contours.x as x
import plotly.graph_objs.surface.contours.y as _plotly_graph_objs_surface_contours_y
import plotly.graph_objs.surface.contours.y as y
import plotly.graph_objs.surface.contours.z as _plotly_graph_objs_surface_contours_z
import plotly.graph_objs.surface.contours.z as z

class X(_PlotlyObject):
    "Create a new 'X' object"
    color: Any
    "Sets the color of the contour lines."
    end: float | Any
    "Sets the end contour level value. Must be more than `contours.start`"
    highlight: bool | Any
    "Determines whether or not contour lines about the x dimension are highlighted on hover."
    highlightcolor: Any
    "Sets the color of the highlighted contour lines."
    highlightwidth: float | Any
    "Sets the width of the highlighted contour lines."
    @property
    def project(self) -> _plotly_graph_objs_surface_contours_x.Project | Any:
        ...
    @project.setter
    def project(self, value: Any) -> None: ...
    show: bool | Any
    "Determines whether or not contour lines about the x dimension are drawn."
    size: float | Any
    "Sets the step between each contour level. Must be positive."
    start: float | Any
    "Sets the starting contour level value. Must be less than `contours.end`"
    usecolormap: bool | Any
    "An alternate to *color*. Determines whether or not the contour lines are colored using the trace *colorscale*."
    width: float | Any
    "Sets the width of the contour lines."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        color: Any = ...,
        end: Any = ...,
        highlight: Any = ...,
        highlightcolor: Any = ...,
        highlightwidth: Any = ...,
        project: Any = ...,
        show: Any = ...,
        size: Any = ...,
        start: Any = ...,
        usecolormap: Any = ...,
        width: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'X' object\n\nArgs:\n    color: Sets the color of the contour lines.\n    end: Sets the end contour level value. Must be more than `contours.start`\n    highlight: Determines whether or not contour lines about the x dimension are highlighted on hover.\n    highlightcolor: Sets the color of the highlighted contour lines.\n    highlightwidth: Sets the width of the highlighted contour lines.\n    show: Determines whether or not contour lines about the x dimension are drawn.\n    size: Sets the step between each contour level. Must be positive.\n    start: Sets the starting contour level value. Must be less than `contours.end`\n    usecolormap: An alternate to *color*. Determines whether or not the contour lines are colored using the trace *colorscale*.\n    width: Sets the width of the contour lines."
        ...

class Y(_PlotlyObject):
    "Create a new 'Y' object"
    color: Any
    "Sets the color of the contour lines."
    end: float | Any
    "Sets the end contour level value. Must be more than `contours.start`"
    highlight: bool | Any
    "Determines whether or not contour lines about the y dimension are highlighted on hover."
    highlightcolor: Any
    "Sets the color of the highlighted contour lines."
    highlightwidth: float | Any
    "Sets the width of the highlighted contour lines."
    @property
    def project(self) -> _plotly_graph_objs_surface_contours_y.Project | Any:
        ...
    @project.setter
    def project(self, value: Any) -> None: ...
    show: bool | Any
    "Determines whether or not contour lines about the y dimension are drawn."
    size: float | Any
    "Sets the step between each contour level. Must be positive."
    start: float | Any
    "Sets the starting contour level value. Must be less than `contours.end`"
    usecolormap: bool | Any
    "An alternate to *color*. Determines whether or not the contour lines are colored using the trace *colorscale*."
    width: float | Any
    "Sets the width of the contour lines."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        color: Any = ...,
        end: Any = ...,
        highlight: Any = ...,
        highlightcolor: Any = ...,
        highlightwidth: Any = ...,
        project: Any = ...,
        show: Any = ...,
        size: Any = ...,
        start: Any = ...,
        usecolormap: Any = ...,
        width: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Y' object\n\nArgs:\n    color: Sets the color of the contour lines.\n    end: Sets the end contour level value. Must be more than `contours.start`\n    highlight: Determines whether or not contour lines about the y dimension are highlighted on hover.\n    highlightcolor: Sets the color of the highlighted contour lines.\n    highlightwidth: Sets the width of the highlighted contour lines.\n    show: Determines whether or not contour lines about the y dimension are drawn.\n    size: Sets the step between each contour level. Must be positive.\n    start: Sets the starting contour level value. Must be less than `contours.end`\n    usecolormap: An alternate to *color*. Determines whether or not the contour lines are colored using the trace *colorscale*.\n    width: Sets the width of the contour lines."
        ...

class Z(_PlotlyObject):
    "Create a new 'Z' object"
    color: Any
    "Sets the color of the contour lines."
    end: float | Any
    "Sets the end contour level value. Must be more than `contours.start`"
    highlight: bool | Any
    "Determines whether or not contour lines about the z dimension are highlighted on hover."
    highlightcolor: Any
    "Sets the color of the highlighted contour lines."
    highlightwidth: float | Any
    "Sets the width of the highlighted contour lines."
    @property
    def project(self) -> _plotly_graph_objs_surface_contours_z.Project | Any:
        ...
    @project.setter
    def project(self, value: Any) -> None: ...
    show: bool | Any
    "Determines whether or not contour lines about the z dimension are drawn."
    size: float | Any
    "Sets the step between each contour level. Must be positive."
    start: float | Any
    "Sets the starting contour level value. Must be less than `contours.end`"
    usecolormap: bool | Any
    "An alternate to *color*. Determines whether or not the contour lines are colored using the trace *colorscale*."
    width: float | Any
    "Sets the width of the contour lines."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        color: Any = ...,
        end: Any = ...,
        highlight: Any = ...,
        highlightcolor: Any = ...,
        highlightwidth: Any = ...,
        project: Any = ...,
        show: Any = ...,
        size: Any = ...,
        start: Any = ...,
        usecolormap: Any = ...,
        width: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Z' object\n\nArgs:\n    color: Sets the color of the contour lines.\n    end: Sets the end contour level value. Must be more than `contours.start`\n    highlight: Determines whether or not contour lines about the z dimension are highlighted on hover.\n    highlightcolor: Sets the color of the highlighted contour lines.\n    highlightwidth: Sets the width of the highlighted contour lines.\n    show: Determines whether or not contour lines about the z dimension are drawn.\n    size: Sets the step between each contour level. Must be positive.\n    start: Sets the starting contour level value. Must be less than `contours.end`\n    usecolormap: An alternate to *color*. Determines whether or not the contour lines are colored using the trace *colorscale*.\n    width: Sets the width of the contour lines."
        ...
