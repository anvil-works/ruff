# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the Plotly catalogue generator in doc/anvil-api-stubs/plotly-stubs.mjs instead, then run:
#   pnpm -F docs build
#
from plotly._base import _PlotlyObject
from typing import Any, Mapping
import plotly.graph_objs.treemap.hoverlabel as _plotly_graph_objs_treemap_hoverlabel
import plotly.graph_objs.treemap.hoverlabel as hoverlabel
import plotly.graph_objs.treemap.legendgrouptitle as _plotly_graph_objs_treemap_legendgrouptitle
import plotly.graph_objs.treemap.legendgrouptitle as legendgrouptitle
import plotly.graph_objs.treemap.marker as _plotly_graph_objs_treemap_marker
import plotly.graph_objs.treemap.marker as marker
import plotly.graph_objs.treemap.pathbar as _plotly_graph_objs_treemap_pathbar
import plotly.graph_objs.treemap.pathbar as pathbar

class Domain(_PlotlyObject):
    "Create a new 'Domain' object"
    column: int | Any
    "If there is a layout grid, use the domain for this column in the grid for this treemap trace."
    row: int | Any
    "If there is a layout grid, use the domain for this row in the grid for this treemap trace."
    x: Any
    "Sets the horizontal domain of this treemap trace (in plot fraction)."
    y: Any
    "Sets the vertical domain of this treemap trace (in plot fraction)."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        column: Any = ...,
        row: Any = ...,
        x: Any = ...,
        y: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Domain' object\n\nArgs:\n    column: If there is a layout grid, use the domain for this column in the grid for this treemap trace.\n    row: If there is a layout grid, use the domain for this row in the grid for this treemap trace.\n    x: Sets the horizontal domain of this treemap trace (in plot fraction).\n    y: Sets the vertical domain of this treemap trace (in plot fraction)."
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
    def font(self) -> _plotly_graph_objs_treemap_hoverlabel.Font | Any:
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
    def font(self) -> _plotly_graph_objs_treemap_legendgrouptitle.Font | Any:
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
    "Determines whether the colorscale is a default palette (`autocolorscale: true`) or the palette determined by `marker.colorscale`. Has an effect only if colors is set to a numerical array. In case `colorscale` is unspecified or `autocolorscale` is true, the default palette will be chosen according to whether numbers in the `color` array are all positive, all negative or mixed."
    cauto: bool | Any
    "Determines whether or not the color domain is computed with respect to the input data (here colors) or the bounds set in `marker.cmin` and `marker.cmax` Has an effect only if colors is set to a numerical array. Defaults to `false` when `marker.cmin` and `marker.cmax` are set by the user."
    cmax: float | Any
    "Sets the upper bound of the color domain. Has an effect only if colors is set to a numerical array. Value should have the same units as colors and if set, `marker.cmin` must be set as well."
    cmid: float | Any
    "Sets the mid-point of the color domain by scaling `marker.cmin` and/or `marker.cmax` to be equidistant to this point. Has an effect only if colors is set to a numerical array. Value should have the same units as colors. Has no effect when `marker.cauto` is `false`."
    cmin: float | Any
    "Sets the lower bound of the color domain. Has an effect only if colors is set to a numerical array. Value should have the same units as colors and if set, `marker.cmax` must be set as well."
    coloraxis: str | Any
    "Sets a reference to a shared color axis. References to these shared color axes are *coloraxis*, *coloraxis2*, *coloraxis3*, etc. Settings for these shared color axes are set in the layout, under `layout.coloraxis`, `layout.coloraxis2`, etc. Note that multiple color scales can be linked to the same color axis."
    @property
    def colorbar(self) -> _plotly_graph_objs_treemap_marker.ColorBar | Any:
        ...
    @colorbar.setter
    def colorbar(self, value: Any) -> None: ...
    colors: Any
    "Sets the color of each sector of this trace. If not specified, the default trace color set is used to pick the sector colors."
    colorscale: Any
    "Sets the colorscale. Has an effect only if colors is set to a numerical array. The colorscale must be an array containing arrays mapping a normalized value to an rgb, rgba, hex, hsl, hsla, hwb, or named color string. At minimum, a mapping for the lowest (0) and highest (1) values are required. For example, `[[0, 'rgb(0,0,255)'], [1, 'rgb(255,0,0)']]`. To control the bounds of the colorscale in color space, use `marker.cmin` and `marker.cmax`. Alternatively, `colorscale` may be a palette name string of the following list: Blackbody,Bluered,Blues,Cividis,Earth,Electric,Greens,Greys,Hot,Jet,Picnic,Portland,Rainbow,RdBu,Reds,Viridis,YlGnBu,YlOrRd."
    cornerradius: float | Any
    "Sets the maximum rounding of corners (in px)."
    depthfade: Any
    "Determines if the sector colors are faded towards the background from the leaves up to the headers. This option is unavailable when a `colorscale` is present, defaults to false when `marker.colors` is set, but otherwise defaults to true. When set to *reversed*, the fading direction is inverted, that is the top elements within hierarchy are drawn with fully saturated colors while the leaves are faded towards the background color."
    @property
    def line(self) -> _plotly_graph_objs_treemap_marker.Line | Any:
        ...
    @line.setter
    def line(self, value: Any) -> None: ...
    @property
    def pad(self) -> _plotly_graph_objs_treemap_marker.Pad | Any:
        ...
    @pad.setter
    def pad(self, value: Any) -> None: ...
    @property
    def pattern(self) -> _plotly_graph_objs_treemap_marker.Pattern | Any:
        "Sets the pattern within the marker."
        ...
    @pattern.setter
    def pattern(self, value: Any) -> None: ...
    reversescale: bool | Any
    "Reverses the color mapping if true. Has an effect only if colors is set to a numerical array. If true, `marker.cmin` will correspond to the last color in the array and `marker.cmax` will correspond to the first color."
    showscale: bool | Any
    "Determines whether or not a colorbar is displayed for this trace. Has an effect only if colors is set to a numerical array."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        autocolorscale: Any = ...,
        cauto: Any = ...,
        cmax: Any = ...,
        cmid: Any = ...,
        cmin: Any = ...,
        coloraxis: Any = ...,
        colorbar: Any = ...,
        colors: Any = ...,
        colorscale: Any = ...,
        cornerradius: Any = ...,
        depthfade: Any = ...,
        line: Any = ...,
        pad: Any = ...,
        pattern: Any = ...,
        reversescale: Any = ...,
        showscale: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Marker' object\n\nArgs:\n    autocolorscale: Determines whether the colorscale is a default palette (`autocolorscale: true`) or the palette determined by `marker.colorscale`. Has an effect only if colors is set to a numerical array. In case `colorscale` is unspecified or `autocolorscale` is true, the default palette will be chosen according to whether numbers in the `color` array are all positive, all negative or mixed.\n    cauto: Determines whether or not the color domain is computed with respect to the input data (here colors) or the bounds set in `marker.cmin` and `marker.cmax` Has an effect only if colors is set to a numerical array. Defaults to `false` when `marker.cmin` and `marker.cmax` are set by the user.\n    cmax: Sets the upper bound of the color domain. Has an effect only if colors is set to a numerical array. Value should have the same units as colors and if set, `marker.cmin` must be set as well.\n    cmid: Sets the mid-point of the color domain by scaling `marker.cmin` and/or `marker.cmax` to be equidistant to this point. Has an effect only if colors is set to a numerical array. Value should have the same units as colors. Has no effect when `marker.cauto` is `false`.\n    cmin: Sets the lower bound of the color domain. Has an effect only if colors is set to a numerical array. Value should have the same units as colors and if set, `marker.cmax` must be set as well.\n    coloraxis: Sets a reference to a shared color axis. References to these shared color axes are *coloraxis*, *coloraxis2*, *coloraxis3*, etc. Settings for these shared color axes are set in the layout, under `layout.coloraxis`, `layout.coloraxis2`, etc. Note that multiple color scales can be linked to the same color axis.\n    colors: Sets the color of each sector of this trace. If not specified, the default trace color set is used to pick the sector colors.\n    colorscale: Sets the colorscale. Has an effect only if colors is set to a numerical array. The colorscale must be an array containing arrays mapping a normalized value to an rgb, rgba, hex, hsl, hsla, hwb, or named color string. At minimum, a mapping for the lowest (0) and highest (1) values are required. For example, `[[0, 'rgb(0,0,255)'], [1, 'rgb(255,0,0)']]`. To control the bounds of the colorscale in color space, use `marker.cmin` and `marker.cmax`. Alternatively, `colorscale` may be a palette name string of the following list: Blackbody,Bluered,Blues,Cividis,Earth,Electric,Greens,Greys,Hot,Jet,Picnic,Portland,Rainbow,RdBu,Reds,Viridis,YlGnBu,YlOrRd.\n    cornerradius: Sets the maximum rounding of corners (in px).\n    depthfade: Determines if the sector colors are faded towards the background from the leaves up to the headers. This option is unavailable when a `colorscale` is present, defaults to false when `marker.colors` is set, but otherwise defaults to true. When set to *reversed*, the fading direction is inverted, that is the top elements within hierarchy are drawn with fully saturated colors while the leaves are faded towards the background color.\n    pattern: Sets the pattern within the marker.\n    reversescale: Reverses the color mapping if true. Has an effect only if colors is set to a numerical array. If true, `marker.cmin` will correspond to the last color in the array and `marker.cmax` will correspond to the first color.\n    showscale: Determines whether or not a colorbar is displayed for this trace. Has an effect only if colors is set to a numerical array."
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

class Pathbar(_PlotlyObject):
    "Create a new 'Pathbar' object"
    edgeshape: Any
    "Determines which shape is used for edges between `barpath` labels."
    side: Any
    "Determines on which side of the treemap the `pathbar` should be presented."
    @property
    def textfont(self) -> _plotly_graph_objs_treemap_pathbar.Textfont | Any:
        "Sets the font used inside `pathbar`."
        ...
    @textfont.setter
    def textfont(self, value: Any) -> None: ...
    thickness: float | Any
    "Sets the thickness of `pathbar` (in px). If not specified the `pathbar.textfont.size` is used with 3 pixles extra padding on each side."
    visible: bool | Any
    "Determines if the path bar is drawn i.e. outside the trace `domain` and with one pixel gap."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        edgeshape: Any = ...,
        side: Any = ...,
        textfont: Any = ...,
        thickness: Any = ...,
        visible: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Pathbar' object\n\nArgs:\n    edgeshape: Determines which shape is used for edges between `barpath` labels.\n    side: Determines on which side of the treemap the `pathbar` should be presented.\n    textfont: Sets the font used inside `pathbar`.\n    thickness: Sets the thickness of `pathbar` (in px). If not specified the `pathbar.textfont.size` is used with 3 pixles extra padding on each side.\n    visible: Determines if the path bar is drawn i.e. outside the trace `domain` and with one pixel gap."
        ...

class Root(_PlotlyObject):
    "Create a new 'Root' object"
    color: Any
    "sets the color of the root node for a sunburst/treemap/icicle trace. this has no effect when a colorscale is used to set the markers."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        color: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Root' object\n\nArgs:\n    color: sets the color of the root node for a sunburst/treemap/icicle trace. this has no effect when a colorscale is used to set the markers."
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

class Tiling(_PlotlyObject):
    "Create a new 'Tiling' object"
    flip: str | Any
    "Determines if the positions obtained from solver are flipped on each axis."
    packing: Any
    "Determines d3 treemap solver. For more info please refer to https://github.com/d3/d3-hierarchy#treemap-tiling"
    pad: float | Any
    "Sets the inner padding (in px)."
    squarifyratio: float | Any
    "When using *squarify* `packing` algorithm, according to https://github.com/d3/d3-hierarchy/blob/v3.1.1/README.md#squarify_ratio this option specifies the desired aspect ratio of the generated rectangles. The ratio must be specified as a number greater than or equal to one. Note that the orientation of the generated rectangles (tall or wide) is not implied by the ratio; for example, a ratio of two will attempt to produce a mixture of rectangles whose width:height ratio is either 2:1 or 1:2. When using *squarify*, unlike d3 which uses the Golden Ratio i.e. 1.618034, Plotly applies 1 to increase squares in treemap layouts."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        flip: Any = ...,
        packing: Any = ...,
        pad: Any = ...,
        squarifyratio: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Tiling' object\n\nArgs:\n    flip: Determines if the positions obtained from solver are flipped on each axis.\n    packing: Determines d3 treemap solver. For more info please refer to https://github.com/d3/d3-hierarchy#treemap-tiling\n    pad: Sets the inner padding (in px).\n    squarifyratio: When using *squarify* `packing` algorithm, according to https://github.com/d3/d3-hierarchy/blob/v3.1.1/README.md#squarify_ratio this option specifies the desired aspect ratio of the generated rectangles. The ratio must be specified as a number greater than or equal to one. Note that the orientation of the generated rectangles (tall or wide) is not implied by the ratio; for example, a ratio of two will attempt to produce a mixture of rectangles whose width:height ratio is either 2:1 or 1:2. When using *squarify*, unlike d3 which uses the Golden Ratio i.e. 1.618034, Plotly applies 1 to increase squares in treemap layouts."
        ...
