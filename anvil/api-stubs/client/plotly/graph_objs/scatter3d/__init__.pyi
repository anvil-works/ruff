# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the Plotly catalogue generator in doc/anvil-api-stubs/plotly-stubs.mjs instead, then run:
#   pnpm -F docs build
#
from plotly._base import _PlotlyObject
from typing import Any, Mapping
import plotly.graph_objs.scatter3d.hoverlabel as _plotly_graph_objs_scatter3d_hoverlabel
import plotly.graph_objs.scatter3d.hoverlabel as hoverlabel
import plotly.graph_objs.scatter3d.legendgrouptitle as _plotly_graph_objs_scatter3d_legendgrouptitle
import plotly.graph_objs.scatter3d.legendgrouptitle as legendgrouptitle
import plotly.graph_objs.scatter3d.line as _plotly_graph_objs_scatter3d_line
import plotly.graph_objs.scatter3d.line as line
import plotly.graph_objs.scatter3d.marker as _plotly_graph_objs_scatter3d_marker
import plotly.graph_objs.scatter3d.marker as marker
import plotly.graph_objs.scatter3d.projection as _plotly_graph_objs_scatter3d_projection
import plotly.graph_objs.scatter3d.projection as projection

class ErrorX(_PlotlyObject):
    "Create a new 'ErrorX' object"
    array: Any
    "Sets the data corresponding the length of each error bar. Values are plotted relative to the underlying data."
    arrayminus: Any
    "Sets the data corresponding the length of each error bar in the bottom (left) direction for vertical (horizontal) bars Values are plotted relative to the underlying data."
    color: Any
    "Sets the stroke color of the error bars."
    copy_zstyle: bool | Any
    symmetric: bool | Any
    "Determines whether or not the error bars have the same length in both direction (top/bottom for vertical bars, left/right for horizontal bars."
    thickness: float | Any
    "Sets the thickness (in px) of the error bars."
    traceref: int | Any
    tracerefminus: int | Any
    type: Any
    "Determines the rule used to generate the error bars. If *constant*, the bar lengths are of a constant value. Set this constant in `value`. If *percent*, the bar lengths correspond to a percentage of underlying data. Set this percentage in `value`. If *sqrt*, the bar lengths correspond to the square of the underlying data. If *data*, the bar lengths are set with data set `array`."
    value: float | Any
    "Sets the value of either the percentage (if `type` is set to *percent*) or the constant (if `type` is set to *constant*) corresponding to the lengths of the error bars."
    valueminus: float | Any
    "Sets the value of either the percentage (if `type` is set to *percent*) or the constant (if `type` is set to *constant*) corresponding to the lengths of the error bars in the bottom (left) direction for vertical (horizontal) bars"
    visible: bool | Any
    "Determines whether or not this set of error bars is visible."
    width: float | Any
    "Sets the width (in px) of the cross-bar at both ends of the error bars."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        array: Any = ...,
        arrayminus: Any = ...,
        color: Any = ...,
        copy_zstyle: Any = ...,
        symmetric: Any = ...,
        thickness: Any = ...,
        traceref: Any = ...,
        tracerefminus: Any = ...,
        type: Any = ...,
        value: Any = ...,
        valueminus: Any = ...,
        visible: Any = ...,
        width: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'ErrorX' object\n\nArgs:\n    array: Sets the data corresponding the length of each error bar. Values are plotted relative to the underlying data.\n    arrayminus: Sets the data corresponding the length of each error bar in the bottom (left) direction for vertical (horizontal) bars Values are plotted relative to the underlying data.\n    color: Sets the stroke color of the error bars.\n    symmetric: Determines whether or not the error bars have the same length in both direction (top/bottom for vertical bars, left/right for horizontal bars.\n    thickness: Sets the thickness (in px) of the error bars.\n    type: Determines the rule used to generate the error bars. If *constant*, the bar lengths are of a constant value. Set this constant in `value`. If *percent*, the bar lengths correspond to a percentage of underlying data. Set this percentage in `value`. If *sqrt*, the bar lengths correspond to the square of the underlying data. If *data*, the bar lengths are set with data set `array`.\n    value: Sets the value of either the percentage (if `type` is set to *percent*) or the constant (if `type` is set to *constant*) corresponding to the lengths of the error bars.\n    valueminus: Sets the value of either the percentage (if `type` is set to *percent*) or the constant (if `type` is set to *constant*) corresponding to the lengths of the error bars in the bottom (left) direction for vertical (horizontal) bars\n    visible: Determines whether or not this set of error bars is visible.\n    width: Sets the width (in px) of the cross-bar at both ends of the error bars."
        ...

class ErrorY(_PlotlyObject):
    "Create a new 'ErrorY' object"
    array: Any
    "Sets the data corresponding the length of each error bar. Values are plotted relative to the underlying data."
    arrayminus: Any
    "Sets the data corresponding the length of each error bar in the bottom (left) direction for vertical (horizontal) bars Values are plotted relative to the underlying data."
    color: Any
    "Sets the stroke color of the error bars."
    copy_zstyle: bool | Any
    symmetric: bool | Any
    "Determines whether or not the error bars have the same length in both direction (top/bottom for vertical bars, left/right for horizontal bars."
    thickness: float | Any
    "Sets the thickness (in px) of the error bars."
    traceref: int | Any
    tracerefminus: int | Any
    type: Any
    "Determines the rule used to generate the error bars. If *constant*, the bar lengths are of a constant value. Set this constant in `value`. If *percent*, the bar lengths correspond to a percentage of underlying data. Set this percentage in `value`. If *sqrt*, the bar lengths correspond to the square of the underlying data. If *data*, the bar lengths are set with data set `array`."
    value: float | Any
    "Sets the value of either the percentage (if `type` is set to *percent*) or the constant (if `type` is set to *constant*) corresponding to the lengths of the error bars."
    valueminus: float | Any
    "Sets the value of either the percentage (if `type` is set to *percent*) or the constant (if `type` is set to *constant*) corresponding to the lengths of the error bars in the bottom (left) direction for vertical (horizontal) bars"
    visible: bool | Any
    "Determines whether or not this set of error bars is visible."
    width: float | Any
    "Sets the width (in px) of the cross-bar at both ends of the error bars."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        array: Any = ...,
        arrayminus: Any = ...,
        color: Any = ...,
        copy_zstyle: Any = ...,
        symmetric: Any = ...,
        thickness: Any = ...,
        traceref: Any = ...,
        tracerefminus: Any = ...,
        type: Any = ...,
        value: Any = ...,
        valueminus: Any = ...,
        visible: Any = ...,
        width: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'ErrorY' object\n\nArgs:\n    array: Sets the data corresponding the length of each error bar. Values are plotted relative to the underlying data.\n    arrayminus: Sets the data corresponding the length of each error bar in the bottom (left) direction for vertical (horizontal) bars Values are plotted relative to the underlying data.\n    color: Sets the stroke color of the error bars.\n    symmetric: Determines whether or not the error bars have the same length in both direction (top/bottom for vertical bars, left/right for horizontal bars.\n    thickness: Sets the thickness (in px) of the error bars.\n    type: Determines the rule used to generate the error bars. If *constant*, the bar lengths are of a constant value. Set this constant in `value`. If *percent*, the bar lengths correspond to a percentage of underlying data. Set this percentage in `value`. If *sqrt*, the bar lengths correspond to the square of the underlying data. If *data*, the bar lengths are set with data set `array`.\n    value: Sets the value of either the percentage (if `type` is set to *percent*) or the constant (if `type` is set to *constant*) corresponding to the lengths of the error bars.\n    valueminus: Sets the value of either the percentage (if `type` is set to *percent*) or the constant (if `type` is set to *constant*) corresponding to the lengths of the error bars in the bottom (left) direction for vertical (horizontal) bars\n    visible: Determines whether or not this set of error bars is visible.\n    width: Sets the width (in px) of the cross-bar at both ends of the error bars."
        ...

class ErrorZ(_PlotlyObject):
    "Create a new 'ErrorZ' object"
    array: Any
    "Sets the data corresponding the length of each error bar. Values are plotted relative to the underlying data."
    arrayminus: Any
    "Sets the data corresponding the length of each error bar in the bottom (left) direction for vertical (horizontal) bars Values are plotted relative to the underlying data."
    color: Any
    "Sets the stroke color of the error bars."
    symmetric: bool | Any
    "Determines whether or not the error bars have the same length in both direction (top/bottom for vertical bars, left/right for horizontal bars."
    thickness: float | Any
    "Sets the thickness (in px) of the error bars."
    traceref: int | Any
    tracerefminus: int | Any
    type: Any
    "Determines the rule used to generate the error bars. If *constant*, the bar lengths are of a constant value. Set this constant in `value`. If *percent*, the bar lengths correspond to a percentage of underlying data. Set this percentage in `value`. If *sqrt*, the bar lengths correspond to the square of the underlying data. If *data*, the bar lengths are set with data set `array`."
    value: float | Any
    "Sets the value of either the percentage (if `type` is set to *percent*) or the constant (if `type` is set to *constant*) corresponding to the lengths of the error bars."
    valueminus: float | Any
    "Sets the value of either the percentage (if `type` is set to *percent*) or the constant (if `type` is set to *constant*) corresponding to the lengths of the error bars in the bottom (left) direction for vertical (horizontal) bars"
    visible: bool | Any
    "Determines whether or not this set of error bars is visible."
    width: float | Any
    "Sets the width (in px) of the cross-bar at both ends of the error bars."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        array: Any = ...,
        arrayminus: Any = ...,
        color: Any = ...,
        symmetric: Any = ...,
        thickness: Any = ...,
        traceref: Any = ...,
        tracerefminus: Any = ...,
        type: Any = ...,
        value: Any = ...,
        valueminus: Any = ...,
        visible: Any = ...,
        width: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'ErrorZ' object\n\nArgs:\n    array: Sets the data corresponding the length of each error bar. Values are plotted relative to the underlying data.\n    arrayminus: Sets the data corresponding the length of each error bar in the bottom (left) direction for vertical (horizontal) bars Values are plotted relative to the underlying data.\n    color: Sets the stroke color of the error bars.\n    symmetric: Determines whether or not the error bars have the same length in both direction (top/bottom for vertical bars, left/right for horizontal bars.\n    thickness: Sets the thickness (in px) of the error bars.\n    type: Determines the rule used to generate the error bars. If *constant*, the bar lengths are of a constant value. Set this constant in `value`. If *percent*, the bar lengths correspond to a percentage of underlying data. Set this percentage in `value`. If *sqrt*, the bar lengths correspond to the square of the underlying data. If *data*, the bar lengths are set with data set `array`.\n    value: Sets the value of either the percentage (if `type` is set to *percent*) or the constant (if `type` is set to *constant*) corresponding to the lengths of the error bars.\n    valueminus: Sets the value of either the percentage (if `type` is set to *percent*) or the constant (if `type` is set to *constant*) corresponding to the lengths of the error bars in the bottom (left) direction for vertical (horizontal) bars\n    visible: Determines whether or not this set of error bars is visible.\n    width: Sets the width (in px) of the cross-bar at both ends of the error bars."
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
    def font(self) -> _plotly_graph_objs_scatter3d_hoverlabel.Font | Any:
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
    def font(self) -> _plotly_graph_objs_scatter3d_legendgrouptitle.Font | Any:
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
    autocolorscale: bool | Any
    "Determines whether the colorscale is a default palette (`autocolorscale: true`) or the palette determined by `line.colorscale`. Has an effect only if in `line.color` is set to a numerical array. In case `colorscale` is unspecified or `autocolorscale` is true, the default palette will be chosen according to whether numbers in the `color` array are all positive, all negative or mixed."
    cauto: bool | Any
    "Determines whether or not the color domain is computed with respect to the input data (here in `line.color`) or the bounds set in `line.cmin` and `line.cmax` Has an effect only if in `line.color` is set to a numerical array. Defaults to `false` when `line.cmin` and `line.cmax` are set by the user."
    cmax: float | Any
    "Sets the upper bound of the color domain. Has an effect only if in `line.color` is set to a numerical array. Value should have the same units as in `line.color` and if set, `line.cmin` must be set as well."
    cmid: float | Any
    "Sets the mid-point of the color domain by scaling `line.cmin` and/or `line.cmax` to be equidistant to this point. Has an effect only if in `line.color` is set to a numerical array. Value should have the same units as in `line.color`. Has no effect when `line.cauto` is `false`."
    cmin: float | Any
    "Sets the lower bound of the color domain. Has an effect only if in `line.color` is set to a numerical array. Value should have the same units as in `line.color` and if set, `line.cmax` must be set as well."
    color: Any
    "Sets the line color. It accepts either a specific color or an array of numbers that are mapped to the colorscale relative to the max and min values of the array or relative to `line.cmin` and `line.cmax` if set."
    coloraxis: str | Any
    "Sets a reference to a shared color axis. References to these shared color axes are *coloraxis*, *coloraxis2*, *coloraxis3*, etc. Settings for these shared color axes are set in the layout, under `layout.coloraxis`, `layout.coloraxis2`, etc. Note that multiple color scales can be linked to the same color axis."
    @property
    def colorbar(self) -> _plotly_graph_objs_scatter3d_line.ColorBar | Any:
        ...
    @colorbar.setter
    def colorbar(self, value: Any) -> None: ...
    colorscale: Any
    "Sets the colorscale. Has an effect only if in `line.color` is set to a numerical array. The colorscale must be an array containing arrays mapping a normalized value to an rgb, rgba, hex, hsl, hsla, hwb, or named color string. At minimum, a mapping for the lowest (0) and highest (1) values are required. For example, `[[0, 'rgb(0,0,255)'], [1, 'rgb(255,0,0)']]`. To control the bounds of the colorscale in color space, use `line.cmin` and `line.cmax`. Alternatively, `colorscale` may be a palette name string of the following list: Blackbody,Bluered,Blues,Cividis,Earth,Electric,Greens,Greys,Hot,Jet,Picnic,Portland,Rainbow,RdBu,Reds,Viridis,YlGnBu,YlOrRd."
    dash: Any
    "Sets the dash style of the lines."
    reversescale: bool | Any
    "Reverses the color mapping if true. Has an effect only if in `line.color` is set to a numerical array. If true, `line.cmin` will correspond to the last color in the array and `line.cmax` will correspond to the first color."
    showscale: bool | Any
    "Determines whether or not a colorbar is displayed for this trace. Has an effect only if in `line.color` is set to a numerical array."
    width: float | Any
    "Sets the line width (in px)."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        autocolorscale: Any = ...,
        cauto: Any = ...,
        cmax: Any = ...,
        cmid: Any = ...,
        cmin: Any = ...,
        color: Any = ...,
        coloraxis: Any = ...,
        colorbar: Any = ...,
        colorscale: Any = ...,
        dash: Any = ...,
        reversescale: Any = ...,
        showscale: Any = ...,
        width: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Line' object\n\nArgs:\n    autocolorscale: Determines whether the colorscale is a default palette (`autocolorscale: true`) or the palette determined by `line.colorscale`. Has an effect only if in `line.color` is set to a numerical array. In case `colorscale` is unspecified or `autocolorscale` is true, the default palette will be chosen according to whether numbers in the `color` array are all positive, all negative or mixed.\n    cauto: Determines whether or not the color domain is computed with respect to the input data (here in `line.color`) or the bounds set in `line.cmin` and `line.cmax` Has an effect only if in `line.color` is set to a numerical array. Defaults to `false` when `line.cmin` and `line.cmax` are set by the user.\n    cmax: Sets the upper bound of the color domain. Has an effect only if in `line.color` is set to a numerical array. Value should have the same units as in `line.color` and if set, `line.cmin` must be set as well.\n    cmid: Sets the mid-point of the color domain by scaling `line.cmin` and/or `line.cmax` to be equidistant to this point. Has an effect only if in `line.color` is set to a numerical array. Value should have the same units as in `line.color`. Has no effect when `line.cauto` is `false`.\n    cmin: Sets the lower bound of the color domain. Has an effect only if in `line.color` is set to a numerical array. Value should have the same units as in `line.color` and if set, `line.cmax` must be set as well.\n    color: Sets the line color. It accepts either a specific color or an array of numbers that are mapped to the colorscale relative to the max and min values of the array or relative to `line.cmin` and `line.cmax` if set.\n    coloraxis: Sets a reference to a shared color axis. References to these shared color axes are *coloraxis*, *coloraxis2*, *coloraxis3*, etc. Settings for these shared color axes are set in the layout, under `layout.coloraxis`, `layout.coloraxis2`, etc. Note that multiple color scales can be linked to the same color axis.\n    colorscale: Sets the colorscale. Has an effect only if in `line.color` is set to a numerical array. The colorscale must be an array containing arrays mapping a normalized value to an rgb, rgba, hex, hsl, hsla, hwb, or named color string. At minimum, a mapping for the lowest (0) and highest (1) values are required. For example, `[[0, 'rgb(0,0,255)'], [1, 'rgb(255,0,0)']]`. To control the bounds of the colorscale in color space, use `line.cmin` and `line.cmax`. Alternatively, `colorscale` may be a palette name string of the following list: Blackbody,Bluered,Blues,Cividis,Earth,Electric,Greens,Greys,Hot,Jet,Picnic,Portland,Rainbow,RdBu,Reds,Viridis,YlGnBu,YlOrRd.\n    dash: Sets the dash style of the lines.\n    reversescale: Reverses the color mapping if true. Has an effect only if in `line.color` is set to a numerical array. If true, `line.cmin` will correspond to the last color in the array and `line.cmax` will correspond to the first color.\n    showscale: Determines whether or not a colorbar is displayed for this trace. Has an effect only if in `line.color` is set to a numerical array.\n    width: Sets the line width (in px)."
        ...

class Marker(_PlotlyObject):
    "Create a new 'Marker' object"
    autocolorscale: bool | Any
    "Determines whether the colorscale is a default palette (`autocolorscale: true`) or the palette determined by `marker.colorscale`. Has an effect only if in `marker.color` is set to a numerical array. In case `colorscale` is unspecified or `autocolorscale` is true, the default palette will be chosen according to whether numbers in the `color` array are all positive, all negative or mixed."
    cauto: bool | Any
    "Determines whether or not the color domain is computed with respect to the input data (here in `marker.color`) or the bounds set in `marker.cmin` and `marker.cmax` Has an effect only if in `marker.color` is set to a numerical array. Defaults to `false` when `marker.cmin` and `marker.cmax` are set by the user."
    cmax: float | Any
    "Sets the upper bound of the color domain. Has an effect only if in `marker.color` is set to a numerical array. Value should have the same units as in `marker.color` and if set, `marker.cmin` must be set as well."
    cmid: float | Any
    "Sets the mid-point of the color domain by scaling `marker.cmin` and/or `marker.cmax` to be equidistant to this point. Has an effect only if in `marker.color` is set to a numerical array. Value should have the same units as in `marker.color`. Has no effect when `marker.cauto` is `false`."
    cmin: float | Any
    "Sets the lower bound of the color domain. Has an effect only if in `marker.color` is set to a numerical array. Value should have the same units as in `marker.color` and if set, `marker.cmax` must be set as well."
    color: Any
    "Sets the marker color. It accepts either a specific color or an array of numbers that are mapped to the colorscale relative to the max and min values of the array or relative to `marker.cmin` and `marker.cmax` if set."
    coloraxis: str | Any
    "Sets a reference to a shared color axis. References to these shared color axes are *coloraxis*, *coloraxis2*, *coloraxis3*, etc. Settings for these shared color axes are set in the layout, under `layout.coloraxis`, `layout.coloraxis2`, etc. Note that multiple color scales can be linked to the same color axis."
    @property
    def colorbar(self) -> _plotly_graph_objs_scatter3d_marker.ColorBar | Any:
        ...
    @colorbar.setter
    def colorbar(self, value: Any) -> None: ...
    colorscale: Any
    "Sets the colorscale. Has an effect only if in `marker.color` is set to a numerical array. The colorscale must be an array containing arrays mapping a normalized value to an rgb, rgba, hex, hsl, hsla, hwb, or named color string. At minimum, a mapping for the lowest (0) and highest (1) values are required. For example, `[[0, 'rgb(0,0,255)'], [1, 'rgb(255,0,0)']]`. To control the bounds of the colorscale in color space, use `marker.cmin` and `marker.cmax`. Alternatively, `colorscale` may be a palette name string of the following list: Blackbody,Bluered,Blues,Cividis,Earth,Electric,Greens,Greys,Hot,Jet,Picnic,Portland,Rainbow,RdBu,Reds,Viridis,YlGnBu,YlOrRd."
    @property
    def line(self) -> _plotly_graph_objs_scatter3d_marker.Line | Any:
        ...
    @line.setter
    def line(self, value: Any) -> None: ...
    opacity: float | Any
    "Sets the marker opacity. Note that the marker opacity for scatter3d traces must be a scalar value for performance reasons. To set a blending opacity value (i.e. which is not transparent), set *marker.color* to an rgba color and use its alpha channel."
    reversescale: bool | Any
    "Reverses the color mapping if true. Has an effect only if in `marker.color` is set to a numerical array. If true, `marker.cmin` will correspond to the last color in the array and `marker.cmax` will correspond to the first color."
    showscale: bool | Any
    "Determines whether or not a colorbar is displayed for this trace. Has an effect only if in `marker.color` is set to a numerical array."
    size: float | Any
    "Sets the marker size (in px)."
    sizemin: float | Any
    "Has an effect only if `marker.size` is set to a numerical array. Sets the minimum size (in px) of the rendered marker points."
    sizemode: Any
    "Has an effect only if `marker.size` is set to a numerical array. Sets the rule for which the data in `size` is converted to pixels."
    sizeref: float | Any
    "Has an effect only if `marker.size` is set to a numerical array. Sets the scale factor used to determine the rendered size of marker points. Use with `sizemin` and `sizemode`."
    symbol: Any
    "Sets the marker symbol type."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        autocolorscale: Any = ...,
        cauto: Any = ...,
        cmax: Any = ...,
        cmid: Any = ...,
        cmin: Any = ...,
        color: Any = ...,
        coloraxis: Any = ...,
        colorbar: Any = ...,
        colorscale: Any = ...,
        line: Any = ...,
        opacity: Any = ...,
        reversescale: Any = ...,
        showscale: Any = ...,
        size: Any = ...,
        sizemin: Any = ...,
        sizemode: Any = ...,
        sizeref: Any = ...,
        symbol: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Marker' object\n\nArgs:\n    autocolorscale: Determines whether the colorscale is a default palette (`autocolorscale: true`) or the palette determined by `marker.colorscale`. Has an effect only if in `marker.color` is set to a numerical array. In case `colorscale` is unspecified or `autocolorscale` is true, the default palette will be chosen according to whether numbers in the `color` array are all positive, all negative or mixed.\n    cauto: Determines whether or not the color domain is computed with respect to the input data (here in `marker.color`) or the bounds set in `marker.cmin` and `marker.cmax` Has an effect only if in `marker.color` is set to a numerical array. Defaults to `false` when `marker.cmin` and `marker.cmax` are set by the user.\n    cmax: Sets the upper bound of the color domain. Has an effect only if in `marker.color` is set to a numerical array. Value should have the same units as in `marker.color` and if set, `marker.cmin` must be set as well.\n    cmid: Sets the mid-point of the color domain by scaling `marker.cmin` and/or `marker.cmax` to be equidistant to this point. Has an effect only if in `marker.color` is set to a numerical array. Value should have the same units as in `marker.color`. Has no effect when `marker.cauto` is `false`.\n    cmin: Sets the lower bound of the color domain. Has an effect only if in `marker.color` is set to a numerical array. Value should have the same units as in `marker.color` and if set, `marker.cmax` must be set as well.\n    color: Sets the marker color. It accepts either a specific color or an array of numbers that are mapped to the colorscale relative to the max and min values of the array or relative to `marker.cmin` and `marker.cmax` if set.\n    coloraxis: Sets a reference to a shared color axis. References to these shared color axes are *coloraxis*, *coloraxis2*, *coloraxis3*, etc. Settings for these shared color axes are set in the layout, under `layout.coloraxis`, `layout.coloraxis2`, etc. Note that multiple color scales can be linked to the same color axis.\n    colorscale: Sets the colorscale. Has an effect only if in `marker.color` is set to a numerical array. The colorscale must be an array containing arrays mapping a normalized value to an rgb, rgba, hex, hsl, hsla, hwb, or named color string. At minimum, a mapping for the lowest (0) and highest (1) values are required. For example, `[[0, 'rgb(0,0,255)'], [1, 'rgb(255,0,0)']]`. To control the bounds of the colorscale in color space, use `marker.cmin` and `marker.cmax`. Alternatively, `colorscale` may be a palette name string of the following list: Blackbody,Bluered,Blues,Cividis,Earth,Electric,Greens,Greys,Hot,Jet,Picnic,Portland,Rainbow,RdBu,Reds,Viridis,YlGnBu,YlOrRd.\n    opacity: Sets the marker opacity. Note that the marker opacity for scatter3d traces must be a scalar value for performance reasons. To set a blending opacity value (i.e. which is not transparent), set *marker.color* to an rgba color and use its alpha channel.\n    reversescale: Reverses the color mapping if true. Has an effect only if in `marker.color` is set to a numerical array. If true, `marker.cmin` will correspond to the last color in the array and `marker.cmax` will correspond to the first color.\n    showscale: Determines whether or not a colorbar is displayed for this trace. Has an effect only if in `marker.color` is set to a numerical array.\n    size: Sets the marker size (in px).\n    sizemin: Has an effect only if `marker.size` is set to a numerical array. Sets the minimum size (in px) of the rendered marker points.\n    sizemode: Has an effect only if `marker.size` is set to a numerical array. Sets the rule for which the data in `size` is converted to pixels.\n    sizeref: Has an effect only if `marker.size` is set to a numerical array. Sets the scale factor used to determine the rendered size of marker points. Use with `sizemin` and `sizemode`.\n    symbol: Sets the marker symbol type."
        ...

class Projection(_PlotlyObject):
    "Create a new 'Projection' object"
    @property
    def x(self) -> _plotly_graph_objs_scatter3d_projection.X | Any:
        ...
    @x.setter
    def x(self, value: Any) -> None: ...
    @property
    def y(self) -> _plotly_graph_objs_scatter3d_projection.Y | Any:
        ...
    @y.setter
    def y(self, value: Any) -> None: ...
    @property
    def z(self) -> _plotly_graph_objs_scatter3d_projection.Z | Any:
        ...
    @z.setter
    def z(self, value: Any) -> None: ...
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

class Textfont(_PlotlyObject):
    "Create a new 'Textfont' object"
    color: Any
    family: str | Any
    "HTML font family - the typeface that will be applied by the web browser. The web browser can only apply a font if it is available on the system where it runs. Provide multiple font families, separated by commas, to indicate the order in which to apply fonts if they aren't available."
    size: float | Any
    style: Any
    "Sets whether a font should be styled with a normal or italic face from its family."
    variant: Any
    "Sets the variant of the font."
    weight: int | Any
    "Sets the weight (or boldness) of the font."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        color: Any = ...,
        family: Any = ...,
        size: Any = ...,
        style: Any = ...,
        variant: Any = ...,
        weight: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Textfont' object\n\nArgs:\n    family: HTML font family - the typeface that will be applied by the web browser. The web browser can only apply a font if it is available on the system where it runs. Provide multiple font families, separated by commas, to indicate the order in which to apply fonts if they aren't available.\n    style: Sets whether a font should be styled with a normal or italic face from its family.\n    variant: Sets the variant of the font.\n    weight: Sets the weight (or boldness) of the font."
        ...
