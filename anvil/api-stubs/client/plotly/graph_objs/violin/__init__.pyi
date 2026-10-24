# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the Plotly catalogue generator in doc/anvil-api-stubs/plotly-stubs.mjs instead, then run:
#   pnpm -F docs build
#
from plotly._base import _PlotlyObject
from typing import Any, Mapping
import plotly.graph_objs.violin.box as _plotly_graph_objs_violin_box
import plotly.graph_objs.violin.box as box
import plotly.graph_objs.violin.hoverlabel as _plotly_graph_objs_violin_hoverlabel
import plotly.graph_objs.violin.hoverlabel as hoverlabel
import plotly.graph_objs.violin.legendgrouptitle as _plotly_graph_objs_violin_legendgrouptitle
import plotly.graph_objs.violin.legendgrouptitle as legendgrouptitle
import plotly.graph_objs.violin.marker as _plotly_graph_objs_violin_marker
import plotly.graph_objs.violin.marker as marker
import plotly.graph_objs.violin.selected as _plotly_graph_objs_violin_selected
import plotly.graph_objs.violin.selected as selected
import plotly.graph_objs.violin.unselected as _plotly_graph_objs_violin_unselected
import plotly.graph_objs.violin.unselected as unselected

class Box(_PlotlyObject):
    "Create a new 'Box' object"
    fillcolor: Any
    "Sets the inner box plot fill color."
    @property
    def line(self) -> _plotly_graph_objs_violin_box.Line | Any:
        ...
    @line.setter
    def line(self, value: Any) -> None: ...
    visible: bool | Any
    "Determines if an miniature box plot is drawn inside the violins. "
    width: float | Any
    "Sets the width of the inner box plots relative to the violins' width. For example, with 1, the inner box plots are as wide as the violins."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        fillcolor: Any = ...,
        line: Any = ...,
        visible: Any = ...,
        width: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Box' object\n\nArgs:\n    fillcolor: Sets the inner box plot fill color.\n    visible: Determines if an miniature box plot is drawn inside the violins. \n    width: Sets the width of the inner box plots relative to the violins' width. For example, with 1, the inner box plots are as wide as the violins."
        ...

class Hoverlabel(_PlotlyObject):
    "Create a new 'Hoverlabel' object"
    align: Any
    "Sets the horizontal alignment of the text content within hover label box. Has an effect only if the hover label text spans more two or more lines"
    bgcolor: Any
    "Sets the background color of the hover labels for this trace"
    bordercolor: Any
    "Sets the border color of the hover labels for this trace."
    @property
    def font(self) -> _plotly_graph_objs_violin_hoverlabel.Font | Any:
        "Sets the font used in hover labels."
        ...
    @font.setter
    def font(self, value: Any) -> None: ...
    namelength: int | Any
    "Sets the default length (in number of characters) of the trace name in the hover labels for all traces. -1 shows the whole name regardless of length. 0-3 shows the first 0-3 characters, and an integer >3 will show the whole name if it is less than that many characters, but if it is longer, will truncate to `namelength - 3` characters and add an ellipsis."
    showarrow: bool | Any
    "Sets whether or not to show the hover label arrow/triangle pointing to the data point."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        align: Any = ...,
        bgcolor: Any = ...,
        bordercolor: Any = ...,
        font: Any = ...,
        namelength: Any = ...,
        showarrow: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Hoverlabel' object\n\nArgs:\n    align: Sets the horizontal alignment of the text content within hover label box. Has an effect only if the hover label text spans more two or more lines\n    bgcolor: Sets the background color of the hover labels for this trace\n    bordercolor: Sets the border color of the hover labels for this trace.\n    font: Sets the font used in hover labels.\n    namelength: Sets the default length (in number of characters) of the trace name in the hover labels for all traces. -1 shows the whole name regardless of length. 0-3 shows the first 0-3 characters, and an integer >3 will show the whole name if it is less than that many characters, but if it is longer, will truncate to `namelength - 3` characters and add an ellipsis.\n    showarrow: Sets whether or not to show the hover label arrow/triangle pointing to the data point."
        ...

class Legendgrouptitle(_PlotlyObject):
    "Create a new 'Legendgrouptitle' object"
    @property
    def font(self) -> _plotly_graph_objs_violin_legendgrouptitle.Font | Any:
        "Sets this legend group's title font."
        ...
    @font.setter
    def font(self, value: Any) -> None: ...
    text: str | Any
    "Sets the title of the legend group."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        font: Any = ...,
        text: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Legendgrouptitle' object\n\nArgs:\n    font: Sets this legend group's title font.\n    text: Sets the title of the legend group."
        ...

class Line(_PlotlyObject):
    "Create a new 'Line' object"
    color: Any
    "Sets the color of line bounding the violin(s)."
    width: float | Any
    "Sets the width (in px) of line bounding the violin(s)."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        color: Any = ...,
        width: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Line' object\n\nArgs:\n    color: Sets the color of line bounding the violin(s).\n    width: Sets the width (in px) of line bounding the violin(s)."
        ...

class Marker(_PlotlyObject):
    "Create a new 'Marker' object"
    angle: Any
    "Sets the marker angle in respect to `angleref`."
    color: Any
    "Sets the marker color. It accepts either a specific color or an array of numbers that are mapped to the colorscale relative to the max and min values of the array or relative to `marker.cmin` and `marker.cmax` if set."
    @property
    def line(self) -> _plotly_graph_objs_violin_marker.Line | Any:
        ...
    @line.setter
    def line(self, value: Any) -> None: ...
    opacity: float | Any
    "Sets the marker opacity."
    outliercolor: Any
    "Sets the color of the outlier sample points."
    size: float | Any
    "Sets the marker size (in px)."
    symbol: Any
    "Sets the marker symbol type. Adding 100 is equivalent to appending *-open* to a symbol name. Adding 200 is equivalent to appending *-dot* to a symbol name. Adding 300 is equivalent to appending *-open-dot* or *dot-open* to a symbol name."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        angle: Any = ...,
        color: Any = ...,
        line: Any = ...,
        opacity: Any = ...,
        outliercolor: Any = ...,
        size: Any = ...,
        symbol: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Marker' object\n\nArgs:\n    angle: Sets the marker angle in respect to `angleref`.\n    color: Sets the marker color. It accepts either a specific color or an array of numbers that are mapped to the colorscale relative to the max and min values of the array or relative to `marker.cmin` and `marker.cmax` if set.\n    opacity: Sets the marker opacity.\n    outliercolor: Sets the color of the outlier sample points.\n    size: Sets the marker size (in px).\n    symbol: Sets the marker symbol type. Adding 100 is equivalent to appending *-open* to a symbol name. Adding 200 is equivalent to appending *-dot* to a symbol name. Adding 300 is equivalent to appending *-open-dot* or *dot-open* to a symbol name."
        ...

class Meanline(_PlotlyObject):
    "Create a new 'Meanline' object"
    color: Any
    "Sets the mean line color."
    visible: bool | Any
    "Determines if a line corresponding to the sample's mean is shown inside the violins. If `box.visible` is turned on, the mean line is drawn inside the inner box. Otherwise, the mean line is drawn from one side of the violin to other."
    width: float | Any
    "Sets the mean line width."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        color: Any = ...,
        visible: Any = ...,
        width: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Meanline' object\n\nArgs:\n    color: Sets the mean line color.\n    visible: Determines if a line corresponding to the sample's mean is shown inside the violins. If `box.visible` is turned on, the mean line is drawn inside the inner box. Otherwise, the mean line is drawn from one side of the violin to other.\n    width: Sets the mean line width."
        ...

class Selected(_PlotlyObject):
    "Create a new 'Selected' object"
    @property
    def marker(self) -> _plotly_graph_objs_violin_selected.Marker | Any:
        ...
    @marker.setter
    def marker(self, value: Any) -> None: ...
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        marker: Any = ...,
        **kwargs: Any,
    ) -> None:
        ...

class Unselected(_PlotlyObject):
    "Create a new 'Unselected' object"
    @property
    def marker(self) -> _plotly_graph_objs_violin_unselected.Marker | Any:
        ...
    @marker.setter
    def marker(self, value: Any) -> None: ...
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        marker: Any = ...,
        **kwargs: Any,
    ) -> None:
        ...
