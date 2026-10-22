# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the Plotly catalogue generator in doc/anvil-api-stubs/plotly-stubs.mjs instead, then run:
#   pnpm -F docs build
#
from plotly._base import _PlotlyObject
from typing import Any, Mapping
import plotly.graph_objs.ohlc.decreasing as _plotly_graph_objs_ohlc_decreasing
import plotly.graph_objs.ohlc.decreasing as decreasing
import plotly.graph_objs.ohlc.hoverlabel as _plotly_graph_objs_ohlc_hoverlabel
import plotly.graph_objs.ohlc.hoverlabel as hoverlabel
import plotly.graph_objs.ohlc.increasing as _plotly_graph_objs_ohlc_increasing
import plotly.graph_objs.ohlc.increasing as increasing
import plotly.graph_objs.ohlc.legendgrouptitle as _plotly_graph_objs_ohlc_legendgrouptitle
import plotly.graph_objs.ohlc.legendgrouptitle as legendgrouptitle

class Decreasing(_PlotlyObject):
    "Create a new 'Decreasing' object"
    @property
    def line(self) -> _plotly_graph_objs_ohlc_decreasing.Line | Any:
        ...
    @line.setter
    def line(self, value: Any) -> None: ...
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        line: Any = ...,
        **kwargs: Any,
    ) -> None:
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
    def font(self) -> _plotly_graph_objs_ohlc_hoverlabel.Font | Any:
        "Sets the font used in hover labels."
        ...
    @font.setter
    def font(self, value: Any) -> None: ...
    namelength: int | Any
    "Sets the default length (in number of characters) of the trace name in the hover labels for all traces. -1 shows the whole name regardless of length. 0-3 shows the first 0-3 characters, and an integer >3 will show the whole name if it is less than that many characters, but if it is longer, will truncate to `namelength - 3` characters and add an ellipsis."
    showarrow: bool | Any
    "Sets whether or not to show the hover label arrow/triangle pointing to the data point."
    split: bool | Any
    "Show hover information (open, close, high, low) in separate labels, rather than a single unified label. Default: *false*. When set to *true*, `hovertemplate` is ignored."
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
        split: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Hoverlabel' object\n\nArgs:\n    align: Sets the horizontal alignment of the text content within hover label box. Has an effect only if the hover label text spans more two or more lines\n    bgcolor: Sets the background color of the hover labels for this trace\n    bordercolor: Sets the border color of the hover labels for this trace.\n    font: Sets the font used in hover labels.\n    namelength: Sets the default length (in number of characters) of the trace name in the hover labels for all traces. -1 shows the whole name regardless of length. 0-3 shows the first 0-3 characters, and an integer >3 will show the whole name if it is less than that many characters, but if it is longer, will truncate to `namelength - 3` characters and add an ellipsis.\n    showarrow: Sets whether or not to show the hover label arrow/triangle pointing to the data point.\n    split: Show hover information (open, close, high, low) in separate labels, rather than a single unified label. Default: *false*. When set to *true*, `hovertemplate` is ignored."
        ...

class Increasing(_PlotlyObject):
    "Create a new 'Increasing' object"
    @property
    def line(self) -> _plotly_graph_objs_ohlc_increasing.Line | Any:
        ...
    @line.setter
    def line(self, value: Any) -> None: ...
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        line: Any = ...,
        **kwargs: Any,
    ) -> None:
        ...

class Legendgrouptitle(_PlotlyObject):
    "Create a new 'Legendgrouptitle' object"
    @property
    def font(self) -> _plotly_graph_objs_ohlc_legendgrouptitle.Font | Any:
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
    dash: str | Any
    "Sets the dash style of lines. Set to a dash type string (*solid*, *dot*, *dash*, *longdash*, *dashdot*, or *longdashdot*) or a dash length list in px (eg *5px,10px,2px,2px*). Note that this style setting can also be set per direction via `increasing.line.dash` and `decreasing.line.dash`."
    width: float | Any
    "Sets the line width (in px). Note that this style setting can also be set per direction via `increasing.line.width` and `decreasing.line.width`."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        dash: Any = ...,
        width: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Line' object\n\nArgs:\n    dash: Sets the dash style of lines. Set to a dash type string (*solid*, *dot*, *dash*, *longdash*, *dashdot*, or *longdashdot*) or a dash length list in px (eg *5px,10px,2px,2px*). Note that this style setting can also be set per direction via `increasing.line.dash` and `decreasing.line.dash`.\n    width: Sets the line width (in px). Note that this style setting can also be set per direction via `increasing.line.width` and `decreasing.line.width`."
        ...
