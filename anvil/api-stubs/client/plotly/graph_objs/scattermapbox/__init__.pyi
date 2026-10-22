# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the Plotly catalogue generator in doc/anvil-api-stubs/plotly-stubs.mjs instead, then run:
#   pnpm -F docs build
#
from plotly._base import _PlotlyObject
from typing import Any, Mapping
import plotly.graph_objs.scattermapbox.hoverlabel as _plotly_graph_objs_scattermapbox_hoverlabel
import plotly.graph_objs.scattermapbox.hoverlabel as hoverlabel
import plotly.graph_objs.scattermapbox.legendgrouptitle as _plotly_graph_objs_scattermapbox_legendgrouptitle
import plotly.graph_objs.scattermapbox.legendgrouptitle as legendgrouptitle
import plotly.graph_objs.scattermapbox.marker as _plotly_graph_objs_scattermapbox_marker
import plotly.graph_objs.scattermapbox.marker as marker
import plotly.graph_objs.scattermapbox.selected as _plotly_graph_objs_scattermapbox_selected
import plotly.graph_objs.scattermapbox.selected as selected
import plotly.graph_objs.scattermapbox.unselected as _plotly_graph_objs_scattermapbox_unselected
import plotly.graph_objs.scattermapbox.unselected as unselected

class Cluster(_PlotlyObject):
    "Create a new 'Cluster' object"
    color: Any
    "Sets the color for each cluster step."
    colorsrc: str | Any
    "Sets the source reference on Chart Studio Cloud for `color`."
    enabled: bool | Any
    "Determines whether clustering is enabled or disabled."
    maxzoom: float | Any
    "Sets the maximum zoom level. At zoom levels equal to or greater than this, points will never be clustered."
    opacity: float | Any
    "Sets the marker opacity."
    opacitysrc: str | Any
    "Sets the source reference on Chart Studio Cloud for `opacity`."
    size: float | Any
    "Sets the size for each cluster step."
    sizesrc: str | Any
    "Sets the source reference on Chart Studio Cloud for `size`."
    step: float | Any
    "Sets how many points it takes to create a cluster or advance to the next cluster step. Use this in conjunction with arrays for `size` and / or `color`. If an integer, steps start at multiples of this number. If an array, each step extends from the given value until one less than the next value."
    stepsrc: str | Any
    "Sets the source reference on Chart Studio Cloud for `step`."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        color: Any = ...,
        colorsrc: Any = ...,
        enabled: Any = ...,
        maxzoom: Any = ...,
        opacity: Any = ...,
        opacitysrc: Any = ...,
        size: Any = ...,
        sizesrc: Any = ...,
        step: Any = ...,
        stepsrc: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Cluster' object\n\nArgs:\n    color: Sets the color for each cluster step.\n    colorsrc: Sets the source reference on Chart Studio Cloud for `color`.\n    enabled: Determines whether clustering is enabled or disabled.\n    maxzoom: Sets the maximum zoom level. At zoom levels equal to or greater than this, points will never be clustered.\n    opacity: Sets the marker opacity.\n    opacitysrc: Sets the source reference on Chart Studio Cloud for `opacity`.\n    size: Sets the size for each cluster step.\n    sizesrc: Sets the source reference on Chart Studio Cloud for `size`.\n    step: Sets how many points it takes to create a cluster or advance to the next cluster step. Use this in conjunction with arrays for `size` and / or `color`. If an integer, steps start at multiples of this number. If an array, each step extends from the given value until one less than the next value.\n    stepsrc: Sets the source reference on Chart Studio Cloud for `step`."
        ...

class Hoverlabel(_PlotlyObject):
    "Create a new 'Hoverlabel' object"
    align: Any
    "Sets the horizontal alignment of the text content within hover label box. Has an effect only if the hover label text spans more two or more lines"
    alignsrc: str | Any
    "Sets the source reference on Chart Studio Cloud for `align`."
    bgcolor: Any
    "Sets the background color of the hover labels for this trace"
    bgcolorsrc: str | Any
    "Sets the source reference on Chart Studio Cloud for `bgcolor`."
    bordercolor: Any
    "Sets the border color of the hover labels for this trace."
    bordercolorsrc: str | Any
    "Sets the source reference on Chart Studio Cloud for `bordercolor`."
    @property
    def font(self) -> _plotly_graph_objs_scattermapbox_hoverlabel.Font | Any:
        "Sets the font used in hover labels."
        ...
    @font.setter
    def font(self, value: Any) -> None: ...
    namelength: int | Any
    "Sets the default length (in number of characters) of the trace name in the hover labels for all traces. -1 shows the whole name regardless of length. 0-3 shows the first 0-3 characters, and an integer >3 will show the whole name if it is less than that many characters, but if it is longer, will truncate to `namelength - 3` characters and add an ellipsis."
    namelengthsrc: str | Any
    "Sets the source reference on Chart Studio Cloud for `namelength`."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        align: Any = ...,
        alignsrc: Any = ...,
        bgcolor: Any = ...,
        bgcolorsrc: Any = ...,
        bordercolor: Any = ...,
        bordercolorsrc: Any = ...,
        font: Any = ...,
        namelength: Any = ...,
        namelengthsrc: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Hoverlabel' object\n\nArgs:\n    align: Sets the horizontal alignment of the text content within hover label box. Has an effect only if the hover label text spans more two or more lines\n    alignsrc: Sets the source reference on Chart Studio Cloud for `align`.\n    bgcolor: Sets the background color of the hover labels for this trace\n    bgcolorsrc: Sets the source reference on Chart Studio Cloud for `bgcolor`.\n    bordercolor: Sets the border color of the hover labels for this trace.\n    bordercolorsrc: Sets the source reference on Chart Studio Cloud for `bordercolor`.\n    font: Sets the font used in hover labels.\n    namelength: Sets the default length (in number of characters) of the trace name in the hover labels for all traces. -1 shows the whole name regardless of length. 0-3 shows the first 0-3 characters, and an integer >3 will show the whole name if it is less than that many characters, but if it is longer, will truncate to `namelength - 3` characters and add an ellipsis.\n    namelengthsrc: Sets the source reference on Chart Studio Cloud for `namelength`."
        ...

class Legendgrouptitle(_PlotlyObject):
    "Create a new 'Legendgrouptitle' object"
    @property
    def font(self) -> _plotly_graph_objs_scattermapbox_legendgrouptitle.Font | Any:
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
    "Sets the line color."
    width: float | Any
    "Sets the line width (in px)."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        color: Any = ...,
        width: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Line' object\n\nArgs:\n    color: Sets the line color.\n    width: Sets the line width (in px)."
        ...

class Marker(_PlotlyObject):
    "Create a new 'Marker' object"
    allowoverlap: bool | Any
    "Flag to draw all symbols, even if they overlap."
    angle: float | Any
    "Sets the marker orientation from true North, in degrees clockwise. When using the *auto* default, no rotation would be applied in perspective views which is different from using a zero angle."
    anglesrc: str | Any
    "Sets the source reference on Chart Studio Cloud for `angle`."
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
    def colorbar(self) -> _plotly_graph_objs_scattermapbox_marker.ColorBar | Any:
        ...
    @colorbar.setter
    def colorbar(self, value: Any) -> None: ...
    colorscale: Any
    "Sets the colorscale. Has an effect only if in `marker.color` is set to a numerical array. The colorscale must be an array containing arrays mapping a normalized value to an rgb, rgba, hex, hsl, hsv, or named color string. At minimum, a mapping for the lowest (0) and highest (1) values are required. For example, `[[0, 'rgb(0,0,255)'], [1, 'rgb(255,0,0)']]`. To control the bounds of the colorscale in color space, use `marker.cmin` and `marker.cmax`. Alternatively, `colorscale` may be a palette name string of the following list: Blackbody,Bluered,Blues,Cividis,Earth,Electric,Greens,Greys,Hot,Jet,Picnic,Portland,Rainbow,RdBu,Reds,Viridis,YlGnBu,YlOrRd."
    colorsrc: str | Any
    "Sets the source reference on Chart Studio Cloud for `color`."
    opacity: float | Any
    "Sets the marker opacity."
    opacitysrc: str | Any
    "Sets the source reference on Chart Studio Cloud for `opacity`."
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
    sizesrc: str | Any
    "Sets the source reference on Chart Studio Cloud for `size`."
    symbol: str | Any
    "Sets the marker symbol. Full list: https://www.mapbox.com/maki-icons/ Note that the array `marker.color` and `marker.size` are only available for *circle* symbols."
    symbolsrc: str | Any
    "Sets the source reference on Chart Studio Cloud for `symbol`."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        allowoverlap: Any = ...,
        angle: Any = ...,
        anglesrc: Any = ...,
        autocolorscale: Any = ...,
        cauto: Any = ...,
        cmax: Any = ...,
        cmid: Any = ...,
        cmin: Any = ...,
        color: Any = ...,
        coloraxis: Any = ...,
        colorbar: Any = ...,
        colorscale: Any = ...,
        colorsrc: Any = ...,
        opacity: Any = ...,
        opacitysrc: Any = ...,
        reversescale: Any = ...,
        showscale: Any = ...,
        size: Any = ...,
        sizemin: Any = ...,
        sizemode: Any = ...,
        sizeref: Any = ...,
        sizesrc: Any = ...,
        symbol: Any = ...,
        symbolsrc: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Marker' object\n\nArgs:\n    allowoverlap: Flag to draw all symbols, even if they overlap.\n    angle: Sets the marker orientation from true North, in degrees clockwise. When using the *auto* default, no rotation would be applied in perspective views which is different from using a zero angle.\n    anglesrc: Sets the source reference on Chart Studio Cloud for `angle`.\n    autocolorscale: Determines whether the colorscale is a default palette (`autocolorscale: true`) or the palette determined by `marker.colorscale`. Has an effect only if in `marker.color` is set to a numerical array. In case `colorscale` is unspecified or `autocolorscale` is true, the default palette will be chosen according to whether numbers in the `color` array are all positive, all negative or mixed.\n    cauto: Determines whether or not the color domain is computed with respect to the input data (here in `marker.color`) or the bounds set in `marker.cmin` and `marker.cmax` Has an effect only if in `marker.color` is set to a numerical array. Defaults to `false` when `marker.cmin` and `marker.cmax` are set by the user.\n    cmax: Sets the upper bound of the color domain. Has an effect only if in `marker.color` is set to a numerical array. Value should have the same units as in `marker.color` and if set, `marker.cmin` must be set as well.\n    cmid: Sets the mid-point of the color domain by scaling `marker.cmin` and/or `marker.cmax` to be equidistant to this point. Has an effect only if in `marker.color` is set to a numerical array. Value should have the same units as in `marker.color`. Has no effect when `marker.cauto` is `false`.\n    cmin: Sets the lower bound of the color domain. Has an effect only if in `marker.color` is set to a numerical array. Value should have the same units as in `marker.color` and if set, `marker.cmax` must be set as well.\n    color: Sets the marker color. It accepts either a specific color or an array of numbers that are mapped to the colorscale relative to the max and min values of the array or relative to `marker.cmin` and `marker.cmax` if set.\n    coloraxis: Sets a reference to a shared color axis. References to these shared color axes are *coloraxis*, *coloraxis2*, *coloraxis3*, etc. Settings for these shared color axes are set in the layout, under `layout.coloraxis`, `layout.coloraxis2`, etc. Note that multiple color scales can be linked to the same color axis.\n    colorscale: Sets the colorscale. Has an effect only if in `marker.color` is set to a numerical array. The colorscale must be an array containing arrays mapping a normalized value to an rgb, rgba, hex, hsl, hsv, or named color string. At minimum, a mapping for the lowest (0) and highest (1) values are required. For example, `[[0, 'rgb(0,0,255)'], [1, 'rgb(255,0,0)']]`. To control the bounds of the colorscale in color space, use `marker.cmin` and `marker.cmax`. Alternatively, `colorscale` may be a palette name string of the following list: Blackbody,Bluered,Blues,Cividis,Earth,Electric,Greens,Greys,Hot,Jet,Picnic,Portland,Rainbow,RdBu,Reds,Viridis,YlGnBu,YlOrRd.\n    colorsrc: Sets the source reference on Chart Studio Cloud for `color`.\n    opacity: Sets the marker opacity.\n    opacitysrc: Sets the source reference on Chart Studio Cloud for `opacity`.\n    reversescale: Reverses the color mapping if true. Has an effect only if in `marker.color` is set to a numerical array. If true, `marker.cmin` will correspond to the last color in the array and `marker.cmax` will correspond to the first color.\n    showscale: Determines whether or not a colorbar is displayed for this trace. Has an effect only if in `marker.color` is set to a numerical array.\n    size: Sets the marker size (in px).\n    sizemin: Has an effect only if `marker.size` is set to a numerical array. Sets the minimum size (in px) of the rendered marker points.\n    sizemode: Has an effect only if `marker.size` is set to a numerical array. Sets the rule for which the data in `size` is converted to pixels.\n    sizeref: Has an effect only if `marker.size` is set to a numerical array. Sets the scale factor used to determine the rendered size of marker points. Use with `sizemin` and `sizemode`.\n    sizesrc: Sets the source reference on Chart Studio Cloud for `size`.\n    symbol: Sets the marker symbol. Full list: https://www.mapbox.com/maki-icons/ Note that the array `marker.color` and `marker.size` are only available for *circle* symbols.\n    symbolsrc: Sets the source reference on Chart Studio Cloud for `symbol`."
        ...

class Selected(_PlotlyObject):
    "Create a new 'Selected' object"
    @property
    def marker(self) -> _plotly_graph_objs_scattermapbox_selected.Marker | Any:
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

class Stream(_PlotlyObject):
    "Create a new 'Stream' object"
    maxpoints: float | Any
    "Sets the maximum number of points to keep on the plots from an incoming stream. If `maxpoints` is set to *50*, only the newest 50 points will be displayed on the plot."
    token: str | Any
    "The stream id number links a data trace on a plot with a stream. See https://chart-studio.plotly.com/settings for more details."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        maxpoints: Any = ...,
        token: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Stream' object\n\nArgs:\n    maxpoints: Sets the maximum number of points to keep on the plots from an incoming stream. If `maxpoints` is set to *50*, only the newest 50 points will be displayed on the plot.\n    token: The stream id number links a data trace on a plot with a stream. See https://chart-studio.plotly.com/settings for more details."
        ...

class Textfont(_PlotlyObject):
    "Create a new 'Textfont' object"
    color: Any
    family: str | Any
    "HTML font family - the typeface that will be applied by the web browser. The web browser will only be able to apply a font if it is available on the system which it operates. Provide multiple font families, separated by commas, to indicate the preference in which to apply fonts if they aren't available on the system. The Chart Studio Cloud (at https://chart-studio.plotly.com or on-premise) generates images on a server, where only a select number of fonts are installed and supported. These include *Arial*, *Balto*, *Courier New*, *Droid Sans*, *Droid Serif*, *Droid Sans Mono*, *Gravitas One*, *Old Standard TT*, *Open Sans*, *Overpass*, *PT Sans Narrow*, *Raleway*, *Times New Roman*."
    size: float | Any
    style: Any
    "Sets whether a font should be styled with a normal or italic face from its family."
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
        weight: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Textfont' object\n\nArgs:\n    family: HTML font family - the typeface that will be applied by the web browser. The web browser will only be able to apply a font if it is available on the system which it operates. Provide multiple font families, separated by commas, to indicate the preference in which to apply fonts if they aren't available on the system. The Chart Studio Cloud (at https://chart-studio.plotly.com or on-premise) generates images on a server, where only a select number of fonts are installed and supported. These include *Arial*, *Balto*, *Courier New*, *Droid Sans*, *Droid Serif*, *Droid Sans Mono*, *Gravitas One*, *Old Standard TT*, *Open Sans*, *Overpass*, *PT Sans Narrow*, *Raleway*, *Times New Roman*.\n    style: Sets whether a font should be styled with a normal or italic face from its family.\n    weight: Sets the weight (or boldness) of the font."
        ...

class Unselected(_PlotlyObject):
    "Create a new 'Unselected' object"
    @property
    def marker(self) -> _plotly_graph_objs_scattermapbox_unselected.Marker | Any:
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
