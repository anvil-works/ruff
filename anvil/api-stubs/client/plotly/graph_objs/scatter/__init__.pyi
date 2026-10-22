# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the Plotly catalogue generator in doc/anvil-api-stubs/plotly-stubs.mjs instead, then run:
#   pnpm -F docs build
#
from plotly._base import _PlotlyObject
from typing import Any, Mapping
import plotly.graph_objs.scatter.hoverlabel as _plotly_graph_objs_scatter_hoverlabel
import plotly.graph_objs.scatter.hoverlabel as hoverlabel
import plotly.graph_objs.scatter.legendgrouptitle as _plotly_graph_objs_scatter_legendgrouptitle
import plotly.graph_objs.scatter.legendgrouptitle as legendgrouptitle
import plotly.graph_objs.scatter.marker as _plotly_graph_objs_scatter_marker
import plotly.graph_objs.scatter.marker as marker
import plotly.graph_objs.scatter.selected as _plotly_graph_objs_scatter_selected
import plotly.graph_objs.scatter.selected as selected
import plotly.graph_objs.scatter.unselected as _plotly_graph_objs_scatter_unselected
import plotly.graph_objs.scatter.unselected as unselected

class ErrorX(_PlotlyObject):
    "Create a new 'ErrorX' object"
    array: Any
    "Sets the data corresponding the length of each error bar. Values are plotted relative to the underlying data."
    arrayminus: Any
    "Sets the data corresponding the length of each error bar in the bottom (left) direction for vertical (horizontal) bars Values are plotted relative to the underlying data."
    color: Any
    "Sets the stroke color of the error bars."
    copy_ystyle: bool | Any
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
        copy_ystyle: Any = ...,
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
        "Create a new 'ErrorY' object\n\nArgs:\n    array: Sets the data corresponding the length of each error bar. Values are plotted relative to the underlying data.\n    arrayminus: Sets the data corresponding the length of each error bar in the bottom (left) direction for vertical (horizontal) bars Values are plotted relative to the underlying data.\n    color: Sets the stroke color of the error bars.\n    symmetric: Determines whether or not the error bars have the same length in both direction (top/bottom for vertical bars, left/right for horizontal bars.\n    thickness: Sets the thickness (in px) of the error bars.\n    type: Determines the rule used to generate the error bars. If *constant*, the bar lengths are of a constant value. Set this constant in `value`. If *percent*, the bar lengths correspond to a percentage of underlying data. Set this percentage in `value`. If *sqrt*, the bar lengths correspond to the square of the underlying data. If *data*, the bar lengths are set with data set `array`.\n    value: Sets the value of either the percentage (if `type` is set to *percent*) or the constant (if `type` is set to *constant*) corresponding to the lengths of the error bars.\n    valueminus: Sets the value of either the percentage (if `type` is set to *percent*) or the constant (if `type` is set to *constant*) corresponding to the lengths of the error bars in the bottom (left) direction for vertical (horizontal) bars\n    visible: Determines whether or not this set of error bars is visible.\n    width: Sets the width (in px) of the cross-bar at both ends of the error bars."
        ...

class Fillgradient(_PlotlyObject):
    "Create a new 'Fillgradient' object"
    colorscale: Any
    "Sets the fill gradient colors as a color scale. The color scale is interpreted as a gradient applied in the direction specified by *orientation*, from the lowest to the highest value of the scatter plot along that axis, or from the center to the most distant point from it, if orientation is *radial*."
    start: float | Any
    "Sets the gradient start value. It is given as the absolute position on the axis determined by the orientiation. E.g., if orientation is *horizontal*, the gradient will be horizontal and start from the x-position given by start. If omitted, the gradient starts at the lowest value of the trace along the respective axis. Ignored if orientation is *radial*."
    stop: float | Any
    "Sets the gradient end value. It is given as the absolute position on the axis determined by the orientiation. E.g., if orientation is *horizontal*, the gradient will be horizontal and end at the x-position given by end. If omitted, the gradient ends at the highest value of the trace along the respective axis. Ignored if orientation is *radial*."
    type: Any
    "Sets the type/orientation of the color gradient for the fill. Defaults to *none*."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        colorscale: Any = ...,
        start: Any = ...,
        stop: Any = ...,
        type: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Fillgradient' object\n\nArgs:\n    colorscale: Sets the fill gradient colors as a color scale. The color scale is interpreted as a gradient applied in the direction specified by *orientation*, from the lowest to the highest value of the scatter plot along that axis, or from the center to the most distant point from it, if orientation is *radial*.\n    start: Sets the gradient start value. It is given as the absolute position on the axis determined by the orientiation. E.g., if orientation is *horizontal*, the gradient will be horizontal and start from the x-position given by start. If omitted, the gradient starts at the lowest value of the trace along the respective axis. Ignored if orientation is *radial*.\n    stop: Sets the gradient end value. It is given as the absolute position on the axis determined by the orientiation. E.g., if orientation is *horizontal*, the gradient will be horizontal and end at the x-position given by end. If omitted, the gradient ends at the highest value of the trace along the respective axis. Ignored if orientation is *radial*.\n    type: Sets the type/orientation of the color gradient for the fill. Defaults to *none*."
        ...

class Fillpattern(_PlotlyObject):
    "Create a new 'Fillpattern' object"
    bgcolor: Any
    "When there is no colorscale sets the color of background pattern fill. Defaults to a `marker.color` background when `fillmode` is *overlay*. Otherwise, defaults to a transparent background."
    fgcolor: Any
    "When there is no colorscale sets the color of foreground pattern fill. Defaults to a `marker.color` background when `fillmode` is *replace*. Otherwise, defaults to dark grey or white to increase contrast with the `bgcolor`."
    fgopacity: float | Any
    "Sets the opacity of the foreground pattern fill. Defaults to a 0.5 when `fillmode` is *overlay*. Otherwise, defaults to 1."
    fillmode: Any
    "Determines whether `marker.color` should be used as a default to `bgcolor` or a `fgcolor`."
    path: str | Any
    "Sets a custom path for pattern fill. Use with no `shape` or `solidity`, provide an SVG path string for the regions of the square from (0,0) to (`size`,`size`) to color."
    shape: Any
    "Sets the shape of the pattern fill. By default, no pattern is used for filling the area."
    size: float | Any
    "Sets the size of unit squares of the pattern fill in pixels, which corresponds to the interval of repetition of the pattern."
    solidity: float | Any
    "Sets the solidity of the pattern fill. Solidity is roughly the fraction of the area filled by the pattern. Solidity of 0 shows only the background color without pattern and solidty of 1 shows only the foreground color without pattern."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        bgcolor: Any = ...,
        fgcolor: Any = ...,
        fgopacity: Any = ...,
        fillmode: Any = ...,
        path: Any = ...,
        shape: Any = ...,
        size: Any = ...,
        solidity: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Fillpattern' object\n\nArgs:\n    bgcolor: When there is no colorscale sets the color of background pattern fill. Defaults to a `marker.color` background when `fillmode` is *overlay*. Otherwise, defaults to a transparent background.\n    fgcolor: When there is no colorscale sets the color of foreground pattern fill. Defaults to a `marker.color` background when `fillmode` is *replace*. Otherwise, defaults to dark grey or white to increase contrast with the `bgcolor`.\n    fgopacity: Sets the opacity of the foreground pattern fill. Defaults to a 0.5 when `fillmode` is *overlay*. Otherwise, defaults to 1.\n    fillmode: Determines whether `marker.color` should be used as a default to `bgcolor` or a `fgcolor`.\n    path: Sets a custom path for pattern fill. Use with no `shape` or `solidity`, provide an SVG path string for the regions of the square from (0,0) to (`size`,`size`) to color.\n    shape: Sets the shape of the pattern fill. By default, no pattern is used for filling the area.\n    size: Sets the size of unit squares of the pattern fill in pixels, which corresponds to the interval of repetition of the pattern.\n    solidity: Sets the solidity of the pattern fill. Solidity is roughly the fraction of the area filled by the pattern. Solidity of 0 shows only the background color without pattern and solidty of 1 shows only the foreground color without pattern."
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
    def font(self) -> _plotly_graph_objs_scatter_hoverlabel.Font | Any:
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
    def font(self) -> _plotly_graph_objs_scatter_legendgrouptitle.Font | Any:
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
    backoff: float | Any
    "Sets the line back off from the end point of the nth line segment (in px). This option is useful e.g. to avoid overlap with arrowhead markers. With *auto* the lines would trim before markers if `marker.angleref` is set to *previous*."
    color: Any
    "Sets the line color."
    dash: str | Any
    "Sets the dash style of lines. Set to a dash type string (*solid*, *dot*, *dash*, *longdash*, *dashdot*, or *longdashdot*) or a dash length list in px (eg *5px,10px,2px,2px*)."
    shape: Any
    "Determines the line shape. With *spline* the lines are drawn using spline interpolation. The other available values correspond to step-wise line shapes."
    simplify: bool | Any
    "Simplifies lines by removing nearly-collinear points. When transitioning lines, it may be desirable to disable this so that the number of points along the resulting SVG path is unaffected."
    smoothing: float | Any
    "Has an effect only if `shape` is set to *spline* Sets the amount of smoothing. *0* corresponds to no smoothing (equivalent to a *linear* shape)."
    width: float | Any
    "Sets the line width (in px)."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        backoff: Any = ...,
        color: Any = ...,
        dash: Any = ...,
        shape: Any = ...,
        simplify: Any = ...,
        smoothing: Any = ...,
        width: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Line' object\n\nArgs:\n    backoff: Sets the line back off from the end point of the nth line segment (in px). This option is useful e.g. to avoid overlap with arrowhead markers. With *auto* the lines would trim before markers if `marker.angleref` is set to *previous*.\n    color: Sets the line color.\n    dash: Sets the dash style of lines. Set to a dash type string (*solid*, *dot*, *dash*, *longdash*, *dashdot*, or *longdashdot*) or a dash length list in px (eg *5px,10px,2px,2px*).\n    shape: Determines the line shape. With *spline* the lines are drawn using spline interpolation. The other available values correspond to step-wise line shapes.\n    simplify: Simplifies lines by removing nearly-collinear points. When transitioning lines, it may be desirable to disable this so that the number of points along the resulting SVG path is unaffected.\n    smoothing: Has an effect only if `shape` is set to *spline* Sets the amount of smoothing. *0* corresponds to no smoothing (equivalent to a *linear* shape).\n    width: Sets the line width (in px)."
        ...

class Marker(_PlotlyObject):
    "Create a new 'Marker' object"
    angle: Any
    "Sets the marker angle in respect to `angleref`."
    angleref: Any
    "Sets the reference for marker angle. With *previous*, angle 0 points along the line from the previous point to this one. With *up*, angle 0 points toward the top of the screen."
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
    def colorbar(self) -> _plotly_graph_objs_scatter_marker.ColorBar | Any:
        ...
    @colorbar.setter
    def colorbar(self, value: Any) -> None: ...
    colorscale: Any
    "Sets the colorscale. Has an effect only if in `marker.color` is set to a numerical array. The colorscale must be an array containing arrays mapping a normalized value to an rgb, rgba, hex, hsl, hsla, hwb, or named color string. At minimum, a mapping for the lowest (0) and highest (1) values are required. For example, `[[0, 'rgb(0,0,255)'], [1, 'rgb(255,0,0)']]`. To control the bounds of the colorscale in color space, use `marker.cmin` and `marker.cmax`. Alternatively, `colorscale` may be a palette name string of the following list: Blackbody,Bluered,Blues,Cividis,Earth,Electric,Greens,Greys,Hot,Jet,Picnic,Portland,Rainbow,RdBu,Reds,Viridis,YlGnBu,YlOrRd."
    @property
    def gradient(self) -> _plotly_graph_objs_scatter_marker.Gradient | Any:
        ...
    @gradient.setter
    def gradient(self, value: Any) -> None: ...
    @property
    def line(self) -> _plotly_graph_objs_scatter_marker.Line | Any:
        ...
    @line.setter
    def line(self, value: Any) -> None: ...
    maxdisplayed: float | Any
    "Sets a maximum number of points to be drawn on the graph. *0* corresponds to no limit."
    opacity: float | Any
    "Sets the marker opacity."
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
    standoff: float | Any
    "Moves the marker away from the data point in the direction of `angle` (in px). This can be useful for example if you have another marker at this location and you want to point an arrowhead marker at it."
    symbol: Any
    "Sets the marker symbol type. Adding 100 is equivalent to appending *-open* to a symbol name. Adding 200 is equivalent to appending *-dot* to a symbol name. Adding 300 is equivalent to appending *-open-dot* or *dot-open* to a symbol name."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        angle: Any = ...,
        angleref: Any = ...,
        autocolorscale: Any = ...,
        cauto: Any = ...,
        cmax: Any = ...,
        cmid: Any = ...,
        cmin: Any = ...,
        color: Any = ...,
        coloraxis: Any = ...,
        colorbar: Any = ...,
        colorscale: Any = ...,
        gradient: Any = ...,
        line: Any = ...,
        maxdisplayed: Any = ...,
        opacity: Any = ...,
        reversescale: Any = ...,
        showscale: Any = ...,
        size: Any = ...,
        sizemin: Any = ...,
        sizemode: Any = ...,
        sizeref: Any = ...,
        standoff: Any = ...,
        symbol: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Marker' object\n\nArgs:\n    angle: Sets the marker angle in respect to `angleref`.\n    angleref: Sets the reference for marker angle. With *previous*, angle 0 points along the line from the previous point to this one. With *up*, angle 0 points toward the top of the screen.\n    autocolorscale: Determines whether the colorscale is a default palette (`autocolorscale: true`) or the palette determined by `marker.colorscale`. Has an effect only if in `marker.color` is set to a numerical array. In case `colorscale` is unspecified or `autocolorscale` is true, the default palette will be chosen according to whether numbers in the `color` array are all positive, all negative or mixed.\n    cauto: Determines whether or not the color domain is computed with respect to the input data (here in `marker.color`) or the bounds set in `marker.cmin` and `marker.cmax` Has an effect only if in `marker.color` is set to a numerical array. Defaults to `false` when `marker.cmin` and `marker.cmax` are set by the user.\n    cmax: Sets the upper bound of the color domain. Has an effect only if in `marker.color` is set to a numerical array. Value should have the same units as in `marker.color` and if set, `marker.cmin` must be set as well.\n    cmid: Sets the mid-point of the color domain by scaling `marker.cmin` and/or `marker.cmax` to be equidistant to this point. Has an effect only if in `marker.color` is set to a numerical array. Value should have the same units as in `marker.color`. Has no effect when `marker.cauto` is `false`.\n    cmin: Sets the lower bound of the color domain. Has an effect only if in `marker.color` is set to a numerical array. Value should have the same units as in `marker.color` and if set, `marker.cmax` must be set as well.\n    color: Sets the marker color. It accepts either a specific color or an array of numbers that are mapped to the colorscale relative to the max and min values of the array or relative to `marker.cmin` and `marker.cmax` if set.\n    coloraxis: Sets a reference to a shared color axis. References to these shared color axes are *coloraxis*, *coloraxis2*, *coloraxis3*, etc. Settings for these shared color axes are set in the layout, under `layout.coloraxis`, `layout.coloraxis2`, etc. Note that multiple color scales can be linked to the same color axis.\n    colorscale: Sets the colorscale. Has an effect only if in `marker.color` is set to a numerical array. The colorscale must be an array containing arrays mapping a normalized value to an rgb, rgba, hex, hsl, hsla, hwb, or named color string. At minimum, a mapping for the lowest (0) and highest (1) values are required. For example, `[[0, 'rgb(0,0,255)'], [1, 'rgb(255,0,0)']]`. To control the bounds of the colorscale in color space, use `marker.cmin` and `marker.cmax`. Alternatively, `colorscale` may be a palette name string of the following list: Blackbody,Bluered,Blues,Cividis,Earth,Electric,Greens,Greys,Hot,Jet,Picnic,Portland,Rainbow,RdBu,Reds,Viridis,YlGnBu,YlOrRd.\n    maxdisplayed: Sets a maximum number of points to be drawn on the graph. *0* corresponds to no limit.\n    opacity: Sets the marker opacity.\n    reversescale: Reverses the color mapping if true. Has an effect only if in `marker.color` is set to a numerical array. If true, `marker.cmin` will correspond to the last color in the array and `marker.cmax` will correspond to the first color.\n    showscale: Determines whether or not a colorbar is displayed for this trace. Has an effect only if in `marker.color` is set to a numerical array.\n    size: Sets the marker size (in px).\n    sizemin: Has an effect only if `marker.size` is set to a numerical array. Sets the minimum size (in px) of the rendered marker points.\n    sizemode: Has an effect only if `marker.size` is set to a numerical array. Sets the rule for which the data in `size` is converted to pixels.\n    sizeref: Has an effect only if `marker.size` is set to a numerical array. Sets the scale factor used to determine the rendered size of marker points. Use with `sizemin` and `sizemode`.\n    standoff: Moves the marker away from the data point in the direction of `angle` (in px). This can be useful for example if you have another marker at this location and you want to point an arrowhead marker at it.\n    symbol: Sets the marker symbol type. Adding 100 is equivalent to appending *-open* to a symbol name. Adding 200 is equivalent to appending *-dot* to a symbol name. Adding 300 is equivalent to appending *-open-dot* or *dot-open* to a symbol name."
        ...

class Selected(_PlotlyObject):
    "Create a new 'Selected' object"
    @property
    def marker(self) -> _plotly_graph_objs_scatter_selected.Marker | Any:
        ...
    @marker.setter
    def marker(self, value: Any) -> None: ...
    @property
    def textfont(self) -> _plotly_graph_objs_scatter_selected.Textfont | Any:
        ...
    @textfont.setter
    def textfont(self, value: Any) -> None: ...
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        marker: Any = ...,
        textfont: Any = ...,
        **kwargs: Any,
    ) -> None:
        ...

class Textfont(_PlotlyObject):
    "Create a new 'Textfont' object"
    color: Any
    family: str | Any
    "HTML font family - the typeface that will be applied by the web browser. The web browser can only apply a font if it is available on the system where it runs. Provide multiple font families, separated by commas, to indicate the order in which to apply fonts if they aren't available."
    lineposition: str | Any
    "Sets the kind of decoration line(s) with text, such as an *under*, *over* or *through* as well as combinations e.g. *under+over*, etc."
    shadow: str | Any
    "Sets the shape and color of the shadow behind text. *auto* places minimal shadow and applies contrast text font color. See https://developer.mozilla.org/en-US/docs/Web/CSS/text-shadow for additional options."
    size: float | Any
    style: Any
    "Sets whether a font should be styled with a normal or italic face from its family."
    textcase: Any
    "Sets capitalization of text. It can be used to make text appear in all-uppercase or all-lowercase, or with each word capitalized."
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
        lineposition: Any = ...,
        shadow: Any = ...,
        size: Any = ...,
        style: Any = ...,
        textcase: Any = ...,
        variant: Any = ...,
        weight: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Textfont' object\n\nArgs:\n    family: HTML font family - the typeface that will be applied by the web browser. The web browser can only apply a font if it is available on the system where it runs. Provide multiple font families, separated by commas, to indicate the order in which to apply fonts if they aren't available.\n    lineposition: Sets the kind of decoration line(s) with text, such as an *under*, *over* or *through* as well as combinations e.g. *under+over*, etc.\n    shadow: Sets the shape and color of the shadow behind text. *auto* places minimal shadow and applies contrast text font color. See https://developer.mozilla.org/en-US/docs/Web/CSS/text-shadow for additional options.\n    style: Sets whether a font should be styled with a normal or italic face from its family.\n    textcase: Sets capitalization of text. It can be used to make text appear in all-uppercase or all-lowercase, or with each word capitalized.\n    variant: Sets the variant of the font.\n    weight: Sets the weight (or boldness) of the font."
        ...

class Unselected(_PlotlyObject):
    "Create a new 'Unselected' object"
    @property
    def marker(self) -> _plotly_graph_objs_scatter_unselected.Marker | Any:
        ...
    @marker.setter
    def marker(self, value: Any) -> None: ...
    @property
    def textfont(self) -> _plotly_graph_objs_scatter_unselected.Textfont | Any:
        ...
    @textfont.setter
    def textfont(self, value: Any) -> None: ...
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        marker: Any = ...,
        textfont: Any = ...,
        **kwargs: Any,
    ) -> None:
        ...
