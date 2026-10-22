# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the Plotly catalogue generator in doc/anvil-api-stubs/plotly-stubs.mjs instead, then run:
#   pnpm -F docs build
#
from plotly._base import _PlotlyObject
from typing import Any, Mapping
import plotly.graph_objs.scattersmith.hoverlabel as _plotly_graph_objs_scattersmith_hoverlabel
import plotly.graph_objs.scattersmith.hoverlabel as hoverlabel
import plotly.graph_objs.scattersmith.legendgrouptitle as _plotly_graph_objs_scattersmith_legendgrouptitle
import plotly.graph_objs.scattersmith.legendgrouptitle as legendgrouptitle
import plotly.graph_objs.scattersmith.marker as _plotly_graph_objs_scattersmith_marker
import plotly.graph_objs.scattersmith.marker as marker
import plotly.graph_objs.scattersmith.selected as _plotly_graph_objs_scattersmith_selected
import plotly.graph_objs.scattersmith.selected as selected
import plotly.graph_objs.scattersmith.unselected as _plotly_graph_objs_scattersmith_unselected
import plotly.graph_objs.scattersmith.unselected as unselected

class Hoverlabel(_PlotlyObject):
    "Create a new 'Hoverlabel' object"
    align: Any
    "Sets the horizontal alignment of the text content within hover label box. Has an effect only if the hover label text spans more two or more lines"
    bgcolor: Any
    "Sets the background color of the hover labels for this trace"
    bordercolor: Any
    "Sets the border color of the hover labels for this trace."
    @property
    def font(self) -> _plotly_graph_objs_scattersmith_hoverlabel.Font | Any:
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
    def font(self) -> _plotly_graph_objs_scattersmith_legendgrouptitle.Font | Any:
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
        smoothing: Any = ...,
        width: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Line' object\n\nArgs:\n    backoff: Sets the line back off from the end point of the nth line segment (in px). This option is useful e.g. to avoid overlap with arrowhead markers. With *auto* the lines would trim before markers if `marker.angleref` is set to *previous*.\n    color: Sets the line color.\n    dash: Sets the dash style of lines. Set to a dash type string (*solid*, *dot*, *dash*, *longdash*, *dashdot*, or *longdashdot*) or a dash length list in px (eg *5px,10px,2px,2px*).\n    shape: Determines the line shape. With *spline* the lines are drawn using spline interpolation. The other available values correspond to step-wise line shapes.\n    smoothing: Has an effect only if `shape` is set to *spline* Sets the amount of smoothing. *0* corresponds to no smoothing (equivalent to a *linear* shape).\n    width: Sets the line width (in px)."
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
    def colorbar(self) -> _plotly_graph_objs_scattersmith_marker.ColorBar | Any:
        ...
    @colorbar.setter
    def colorbar(self, value: Any) -> None: ...
    colorscale: Any
    "Sets the colorscale. Has an effect only if in `marker.color` is set to a numerical array. The colorscale must be an array containing arrays mapping a normalized value to an rgb, rgba, hex, hsl, hsla, hwb, or named color string. At minimum, a mapping for the lowest (0) and highest (1) values are required. For example, `[[0, 'rgb(0,0,255)'], [1, 'rgb(255,0,0)']]`. To control the bounds of the colorscale in color space, use `marker.cmin` and `marker.cmax`. Alternatively, `colorscale` may be a palette name string of the following list: Blackbody,Bluered,Blues,Cividis,Earth,Electric,Greens,Greys,Hot,Jet,Picnic,Portland,Rainbow,RdBu,Reds,Viridis,YlGnBu,YlOrRd."
    @property
    def gradient(self) -> _plotly_graph_objs_scattersmith_marker.Gradient | Any:
        ...
    @gradient.setter
    def gradient(self, value: Any) -> None: ...
    @property
    def line(self) -> _plotly_graph_objs_scattersmith_marker.Line | Any:
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
    def marker(self) -> _plotly_graph_objs_scattersmith_selected.Marker | Any:
        ...
    @marker.setter
    def marker(self, value: Any) -> None: ...
    @property
    def textfont(self) -> _plotly_graph_objs_scattersmith_selected.Textfont | Any:
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
    def marker(self) -> _plotly_graph_objs_scattersmith_unselected.Marker | Any:
        ...
    @marker.setter
    def marker(self, value: Any) -> None: ...
    @property
    def textfont(self) -> _plotly_graph_objs_scattersmith_unselected.Textfont | Any:
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
