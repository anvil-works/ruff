# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the Plotly catalogue generator in doc/anvil-api-stubs/plotly-stubs.mjs instead, then run:
#   pnpm -F docs build
#
from plotly._base import _PlotlyObject
from typing import Any, Mapping
import plotly.graph_objs.histogram.hoverlabel as _plotly_graph_objs_histogram_hoverlabel
import plotly.graph_objs.histogram.hoverlabel as hoverlabel
import plotly.graph_objs.histogram.legendgrouptitle as _plotly_graph_objs_histogram_legendgrouptitle
import plotly.graph_objs.histogram.legendgrouptitle as legendgrouptitle
import plotly.graph_objs.histogram.marker as _plotly_graph_objs_histogram_marker
import plotly.graph_objs.histogram.marker as marker
import plotly.graph_objs.histogram.selected as _plotly_graph_objs_histogram_selected
import plotly.graph_objs.histogram.selected as selected
import plotly.graph_objs.histogram.unselected as _plotly_graph_objs_histogram_unselected
import plotly.graph_objs.histogram.unselected as unselected

class Cumulative(_PlotlyObject):
    "Create a new 'Cumulative' object"
    currentbin: Any
    "Only applies if cumulative is enabled. Sets whether the current bin is included, excluded, or has half of its value included in the current cumulative value. *include* is the default for compatibility with various other tools, however it introduces a half-bin bias to the results. *exclude* makes the opposite half-bin bias, and *half* removes it."
    direction: Any
    "Only applies if cumulative is enabled. If *increasing* (default) we sum all prior bins, so the result increases from left to right. If *decreasing* we sum later bins so the result decreases from left to right."
    enabled: bool | Any
    "If true, display the cumulative distribution by summing the binned values. Use the `direction` and `centralbin` attributes to tune the accumulation method. Note: in this mode, the *density* `histnorm` settings behave the same as their equivalents without *density*: ** and *density* both rise to the number of data points, and *probability* and *probability density* both rise to the number of sample points."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        currentbin: Any = ...,
        direction: Any = ...,
        enabled: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Cumulative' object\n\nArgs:\n    currentbin: Only applies if cumulative is enabled. Sets whether the current bin is included, excluded, or has half of its value included in the current cumulative value. *include* is the default for compatibility with various other tools, however it introduces a half-bin bias to the results. *exclude* makes the opposite half-bin bias, and *half* removes it.\n    direction: Only applies if cumulative is enabled. If *increasing* (default) we sum all prior bins, so the result increases from left to right. If *decreasing* we sum later bins so the result decreases from left to right.\n    enabled: If true, display the cumulative distribution by summing the binned values. Use the `direction` and `centralbin` attributes to tune the accumulation method. Note: in this mode, the *density* `histnorm` settings behave the same as their equivalents without *density*: ** and *density* both rise to the number of data points, and *probability* and *probability density* both rise to the number of sample points."
        ...

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

class Hoverlabel(_PlotlyObject):
    "Create a new 'Hoverlabel' object"
    align: Any
    "Sets the horizontal alignment of the text content within hover label box. Has an effect only if the hover label text spans more two or more lines"
    bgcolor: Any
    "Sets the background color of the hover labels for this trace"
    bordercolor: Any
    "Sets the border color of the hover labels for this trace."
    @property
    def font(self) -> _plotly_graph_objs_histogram_hoverlabel.Font | Any:
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

class Insidetextfont(_PlotlyObject):
    "Create a new 'Insidetextfont' object"
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
        "Create a new 'Insidetextfont' object\n\nArgs:\n    family: HTML font family - the typeface that will be applied by the web browser. The web browser can only apply a font if it is available on the system where it runs. Provide multiple font families, separated by commas, to indicate the order in which to apply fonts if they aren't available.\n    lineposition: Sets the kind of decoration line(s) with text, such as an *under*, *over* or *through* as well as combinations e.g. *under+over*, etc.\n    shadow: Sets the shape and color of the shadow behind text. *auto* places minimal shadow and applies contrast text font color. See https://developer.mozilla.org/en-US/docs/Web/CSS/text-shadow for additional options.\n    style: Sets whether a font should be styled with a normal or italic face from its family.\n    textcase: Sets capitalization of text. It can be used to make text appear in all-uppercase or all-lowercase, or with each word capitalized.\n    variant: Sets the variant of the font.\n    weight: Sets the weight (or boldness) of the font."
        ...

class Legendgrouptitle(_PlotlyObject):
    "Create a new 'Legendgrouptitle' object"
    @property
    def font(self) -> _plotly_graph_objs_histogram_legendgrouptitle.Font | Any:
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
    def colorbar(self) -> _plotly_graph_objs_histogram_marker.ColorBar | Any:
        ...
    @colorbar.setter
    def colorbar(self, value: Any) -> None: ...
    colorscale: Any
    "Sets the colorscale. Has an effect only if in `marker.color` is set to a numerical array. The colorscale must be an array containing arrays mapping a normalized value to an rgb, rgba, hex, hsl, hsla, hwb, or named color string. At minimum, a mapping for the lowest (0) and highest (1) values are required. For example, `[[0, 'rgb(0,0,255)'], [1, 'rgb(255,0,0)']]`. To control the bounds of the colorscale in color space, use `marker.cmin` and `marker.cmax`. Alternatively, `colorscale` may be a palette name string of the following list: Blackbody,Bluered,Blues,Cividis,Earth,Electric,Greens,Greys,Hot,Jet,Picnic,Portland,Rainbow,RdBu,Reds,Viridis,YlGnBu,YlOrRd."
    cornerradius: Any
    "Sets the rounding of corners. May be an integer number of pixels, or a percentage of bar width (as a string ending in %). Defaults to `layout.barcornerradius`. In stack or relative barmode, the first trace to set cornerradius is used for the whole stack."
    @property
    def line(self) -> _plotly_graph_objs_histogram_marker.Line | Any:
        ...
    @line.setter
    def line(self, value: Any) -> None: ...
    opacity: float | Any
    "Sets the opacity of the bars."
    @property
    def pattern(self) -> _plotly_graph_objs_histogram_marker.Pattern | Any:
        "Sets the pattern within the marker."
        ...
    @pattern.setter
    def pattern(self, value: Any) -> None: ...
    reversescale: bool | Any
    "Reverses the color mapping if true. Has an effect only if in `marker.color` is set to a numerical array. If true, `marker.cmin` will correspond to the last color in the array and `marker.cmax` will correspond to the first color."
    showscale: bool | Any
    "Determines whether or not a colorbar is displayed for this trace. Has an effect only if in `marker.color` is set to a numerical array."
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
        cornerradius: Any = ...,
        line: Any = ...,
        opacity: Any = ...,
        pattern: Any = ...,
        reversescale: Any = ...,
        showscale: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Marker' object\n\nArgs:\n    autocolorscale: Determines whether the colorscale is a default palette (`autocolorscale: true`) or the palette determined by `marker.colorscale`. Has an effect only if in `marker.color` is set to a numerical array. In case `colorscale` is unspecified or `autocolorscale` is true, the default palette will be chosen according to whether numbers in the `color` array are all positive, all negative or mixed.\n    cauto: Determines whether or not the color domain is computed with respect to the input data (here in `marker.color`) or the bounds set in `marker.cmin` and `marker.cmax` Has an effect only if in `marker.color` is set to a numerical array. Defaults to `false` when `marker.cmin` and `marker.cmax` are set by the user.\n    cmax: Sets the upper bound of the color domain. Has an effect only if in `marker.color` is set to a numerical array. Value should have the same units as in `marker.color` and if set, `marker.cmin` must be set as well.\n    cmid: Sets the mid-point of the color domain by scaling `marker.cmin` and/or `marker.cmax` to be equidistant to this point. Has an effect only if in `marker.color` is set to a numerical array. Value should have the same units as in `marker.color`. Has no effect when `marker.cauto` is `false`.\n    cmin: Sets the lower bound of the color domain. Has an effect only if in `marker.color` is set to a numerical array. Value should have the same units as in `marker.color` and if set, `marker.cmax` must be set as well.\n    color: Sets the marker color. It accepts either a specific color or an array of numbers that are mapped to the colorscale relative to the max and min values of the array or relative to `marker.cmin` and `marker.cmax` if set.\n    coloraxis: Sets a reference to a shared color axis. References to these shared color axes are *coloraxis*, *coloraxis2*, *coloraxis3*, etc. Settings for these shared color axes are set in the layout, under `layout.coloraxis`, `layout.coloraxis2`, etc. Note that multiple color scales can be linked to the same color axis.\n    colorscale: Sets the colorscale. Has an effect only if in `marker.color` is set to a numerical array. The colorscale must be an array containing arrays mapping a normalized value to an rgb, rgba, hex, hsl, hsla, hwb, or named color string. At minimum, a mapping for the lowest (0) and highest (1) values are required. For example, `[[0, 'rgb(0,0,255)'], [1, 'rgb(255,0,0)']]`. To control the bounds of the colorscale in color space, use `marker.cmin` and `marker.cmax`. Alternatively, `colorscale` may be a palette name string of the following list: Blackbody,Bluered,Blues,Cividis,Earth,Electric,Greens,Greys,Hot,Jet,Picnic,Portland,Rainbow,RdBu,Reds,Viridis,YlGnBu,YlOrRd.\n    cornerradius: Sets the rounding of corners. May be an integer number of pixels, or a percentage of bar width (as a string ending in %). Defaults to `layout.barcornerradius`. In stack or relative barmode, the first trace to set cornerradius is used for the whole stack.\n    opacity: Sets the opacity of the bars.\n    pattern: Sets the pattern within the marker.\n    reversescale: Reverses the color mapping if true. Has an effect only if in `marker.color` is set to a numerical array. If true, `marker.cmin` will correspond to the last color in the array and `marker.cmax` will correspond to the first color.\n    showscale: Determines whether or not a colorbar is displayed for this trace. Has an effect only if in `marker.color` is set to a numerical array."
        ...

class Outsidetextfont(_PlotlyObject):
    "Create a new 'Outsidetextfont' object"
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
        "Create a new 'Outsidetextfont' object\n\nArgs:\n    family: HTML font family - the typeface that will be applied by the web browser. The web browser can only apply a font if it is available on the system where it runs. Provide multiple font families, separated by commas, to indicate the order in which to apply fonts if they aren't available.\n    lineposition: Sets the kind of decoration line(s) with text, such as an *under*, *over* or *through* as well as combinations e.g. *under+over*, etc.\n    shadow: Sets the shape and color of the shadow behind text. *auto* places minimal shadow and applies contrast text font color. See https://developer.mozilla.org/en-US/docs/Web/CSS/text-shadow for additional options.\n    style: Sets whether a font should be styled with a normal or italic face from its family.\n    textcase: Sets capitalization of text. It can be used to make text appear in all-uppercase or all-lowercase, or with each word capitalized.\n    variant: Sets the variant of the font.\n    weight: Sets the weight (or boldness) of the font."
        ...

class Selected(_PlotlyObject):
    "Create a new 'Selected' object"
    @property
    def marker(self) -> _plotly_graph_objs_histogram_selected.Marker | Any:
        ...
    @marker.setter
    def marker(self, value: Any) -> None: ...
    @property
    def textfont(self) -> _plotly_graph_objs_histogram_selected.Textfont | Any:
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
    def marker(self) -> _plotly_graph_objs_histogram_unselected.Marker | Any:
        ...
    @marker.setter
    def marker(self, value: Any) -> None: ...
    @property
    def textfont(self) -> _plotly_graph_objs_histogram_unselected.Textfont | Any:
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

class XBins(_PlotlyObject):
    "Create a new 'XBins' object"
    end: Any
    "Sets the end value for the x axis bins. The last bin may not end exactly at this value, we increment the bin edge by `size` from `start` until we reach or exceed `end`. Defaults to the maximum data value. Like `start`, for dates use a date string, and for category data `end` is based on the category serial numbers."
    size: Any
    "Sets the size of each x axis bin. Default behavior: If `nbinsx` is 0 or omitted, we choose a nice round bin size such that the number of bins is about the same as the typical number of samples in each bin. If `nbinsx` is provided, we choose a nice round bin size giving no more than that many bins. For date data, use milliseconds or *M<n>* for months, as in `axis.dtick`. For category data, the number of categories to bin together (always defaults to 1). If multiple non-overlaying histograms share a subplot, the first explicit `size` is used and all others discarded. If no `size` is provided, the sample data from all traces is combined to determine `size` as described above."
    start: Any
    "Sets the starting value for the x axis bins. Defaults to the minimum data value, shifted down if necessary to make nice round values and to remove ambiguous bin edges. For example, if most of the data is integers we shift the bin edges 0.5 down, so a `size` of 5 would have a default `start` of -0.5, so it is clear that 0-4 are in the first bin, 5-9 in the second, but continuous data gets a start of 0 and bins [0,5), [5,10) etc. Dates behave similarly, and `start` should be a date string. For category data, `start` is based on the category serial numbers, and defaults to -0.5. If multiple non-overlaying histograms share a subplot, the first explicit `start` is used exactly and all others are shifted down (if necessary) to differ from that one by an integer number of bins."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        end: Any = ...,
        size: Any = ...,
        start: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'XBins' object\n\nArgs:\n    end: Sets the end value for the x axis bins. The last bin may not end exactly at this value, we increment the bin edge by `size` from `start` until we reach or exceed `end`. Defaults to the maximum data value. Like `start`, for dates use a date string, and for category data `end` is based on the category serial numbers.\n    size: Sets the size of each x axis bin. Default behavior: If `nbinsx` is 0 or omitted, we choose a nice round bin size such that the number of bins is about the same as the typical number of samples in each bin. If `nbinsx` is provided, we choose a nice round bin size giving no more than that many bins. For date data, use milliseconds or *M<n>* for months, as in `axis.dtick`. For category data, the number of categories to bin together (always defaults to 1). If multiple non-overlaying histograms share a subplot, the first explicit `size` is used and all others discarded. If no `size` is provided, the sample data from all traces is combined to determine `size` as described above.\n    start: Sets the starting value for the x axis bins. Defaults to the minimum data value, shifted down if necessary to make nice round values and to remove ambiguous bin edges. For example, if most of the data is integers we shift the bin edges 0.5 down, so a `size` of 5 would have a default `start` of -0.5, so it is clear that 0-4 are in the first bin, 5-9 in the second, but continuous data gets a start of 0 and bins [0,5), [5,10) etc. Dates behave similarly, and `start` should be a date string. For category data, `start` is based on the category serial numbers, and defaults to -0.5. If multiple non-overlaying histograms share a subplot, the first explicit `start` is used exactly and all others are shifted down (if necessary) to differ from that one by an integer number of bins."
        ...

class YBins(_PlotlyObject):
    "Create a new 'YBins' object"
    end: Any
    "Sets the end value for the y axis bins. The last bin may not end exactly at this value, we increment the bin edge by `size` from `start` until we reach or exceed `end`. Defaults to the maximum data value. Like `start`, for dates use a date string, and for category data `end` is based on the category serial numbers."
    size: Any
    "Sets the size of each y axis bin. Default behavior: If `nbinsy` is 0 or omitted, we choose a nice round bin size such that the number of bins is about the same as the typical number of samples in each bin. If `nbinsy` is provided, we choose a nice round bin size giving no more than that many bins. For date data, use milliseconds or *M<n>* for months, as in `axis.dtick`. For category data, the number of categories to bin together (always defaults to 1). If multiple non-overlaying histograms share a subplot, the first explicit `size` is used and all others discarded. If no `size` is provided, the sample data from all traces is combined to determine `size` as described above."
    start: Any
    "Sets the starting value for the y axis bins. Defaults to the minimum data value, shifted down if necessary to make nice round values and to remove ambiguous bin edges. For example, if most of the data is integers we shift the bin edges 0.5 down, so a `size` of 5 would have a default `start` of -0.5, so it is clear that 0-4 are in the first bin, 5-9 in the second, but continuous data gets a start of 0 and bins [0,5), [5,10) etc. Dates behave similarly, and `start` should be a date string. For category data, `start` is based on the category serial numbers, and defaults to -0.5. If multiple non-overlaying histograms share a subplot, the first explicit `start` is used exactly and all others are shifted down (if necessary) to differ from that one by an integer number of bins."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        end: Any = ...,
        size: Any = ...,
        start: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'YBins' object\n\nArgs:\n    end: Sets the end value for the y axis bins. The last bin may not end exactly at this value, we increment the bin edge by `size` from `start` until we reach or exceed `end`. Defaults to the maximum data value. Like `start`, for dates use a date string, and for category data `end` is based on the category serial numbers.\n    size: Sets the size of each y axis bin. Default behavior: If `nbinsy` is 0 or omitted, we choose a nice round bin size such that the number of bins is about the same as the typical number of samples in each bin. If `nbinsy` is provided, we choose a nice round bin size giving no more than that many bins. For date data, use milliseconds or *M<n>* for months, as in `axis.dtick`. For category data, the number of categories to bin together (always defaults to 1). If multiple non-overlaying histograms share a subplot, the first explicit `size` is used and all others discarded. If no `size` is provided, the sample data from all traces is combined to determine `size` as described above.\n    start: Sets the starting value for the y axis bins. Defaults to the minimum data value, shifted down if necessary to make nice round values and to remove ambiguous bin edges. For example, if most of the data is integers we shift the bin edges 0.5 down, so a `size` of 5 would have a default `start` of -0.5, so it is clear that 0-4 are in the first bin, 5-9 in the second, but continuous data gets a start of 0 and bins [0,5), [5,10) etc. Dates behave similarly, and `start` should be a date string. For category data, `start` is based on the category serial numbers, and defaults to -0.5. If multiple non-overlaying histograms share a subplot, the first explicit `start` is used exactly and all others are shifted down (if necessary) to differ from that one by an integer number of bins."
        ...
