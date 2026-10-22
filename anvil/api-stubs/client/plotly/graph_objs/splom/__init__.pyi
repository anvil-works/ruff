# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the Plotly catalogue generator in doc/anvil-api-stubs/plotly-stubs.mjs instead, then run:
#   pnpm -F docs build
#
from plotly._base import _PlotlyObject
from typing import Any, Mapping
import plotly.graph_objs.splom.dimension as _plotly_graph_objs_splom_dimension
import plotly.graph_objs.splom.dimension as dimension
import plotly.graph_objs.splom.hoverlabel as _plotly_graph_objs_splom_hoverlabel
import plotly.graph_objs.splom.hoverlabel as hoverlabel
import plotly.graph_objs.splom.legendgrouptitle as _plotly_graph_objs_splom_legendgrouptitle
import plotly.graph_objs.splom.legendgrouptitle as legendgrouptitle
import plotly.graph_objs.splom.marker as _plotly_graph_objs_splom_marker
import plotly.graph_objs.splom.marker as marker
import plotly.graph_objs.splom.selected as _plotly_graph_objs_splom_selected
import plotly.graph_objs.splom.selected as selected
import plotly.graph_objs.splom.unselected as _plotly_graph_objs_splom_unselected
import plotly.graph_objs.splom.unselected as unselected

class Diagonal(_PlotlyObject):
    "Create a new 'Diagonal' object"
    visible: bool | Any
    "Determines whether or not subplots on the diagonal are displayed."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        visible: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Diagonal' object\n\nArgs:\n    visible: Determines whether or not subplots on the diagonal are displayed."
        ...

class Dimension(_PlotlyObject):
    "Create a new 'Dimension' object"
    @property
    def axis(self) -> _plotly_graph_objs_splom_dimension.Axis | Any:
        ...
    @axis.setter
    def axis(self, value: Any) -> None: ...
    label: str | Any
    "Sets the label corresponding to this splom dimension."
    name: str | Any
    "When used in a template, named items are created in the output figure in addition to any items the figure already has in this array. You can modify these items in the output figure by making your own item with `templateitemname` matching this `name` alongside your modifications (including `visible: false` or `enabled: false` to hide it). Has no effect outside of a template."
    templateitemname: str | Any
    "Used to refer to a named item in this array in the template. Named items from the template will be created even without a matching item in the input figure, but you can modify one by making an item with `templateitemname` matching its `name`, alongside your modifications (including `visible: false` or `enabled: false` to hide it). If there is no template or no matching item, this item will be hidden unless you explicitly show it with `visible: true`."
    values: Any
    "Sets the dimension values to be plotted."
    visible: bool | Any
    "Determines whether or not this dimension is shown on the graph. Note that even visible false dimension contribute to the default grid generate by this splom trace."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        axis: Any = ...,
        label: Any = ...,
        name: Any = ...,
        templateitemname: Any = ...,
        values: Any = ...,
        visible: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Dimension' object\n\nArgs:\n    label: Sets the label corresponding to this splom dimension.\n    name: When used in a template, named items are created in the output figure in addition to any items the figure already has in this array. You can modify these items in the output figure by making your own item with `templateitemname` matching this `name` alongside your modifications (including `visible: false` or `enabled: false` to hide it). Has no effect outside of a template.\n    templateitemname: Used to refer to a named item in this array in the template. Named items from the template will be created even without a matching item in the input figure, but you can modify one by making an item with `templateitemname` matching its `name`, alongside your modifications (including `visible: false` or `enabled: false` to hide it). If there is no template or no matching item, this item will be hidden unless you explicitly show it with `visible: true`.\n    values: Sets the dimension values to be plotted.\n    visible: Determines whether or not this dimension is shown on the graph. Note that even visible false dimension contribute to the default grid generate by this splom trace."
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
    def font(self) -> _plotly_graph_objs_splom_hoverlabel.Font | Any:
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
    def font(self) -> _plotly_graph_objs_splom_legendgrouptitle.Font | Any:
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
    angle: Any
    "Sets the marker angle in respect to `angleref`."
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
    def colorbar(self) -> _plotly_graph_objs_splom_marker.ColorBar | Any:
        ...
    @colorbar.setter
    def colorbar(self, value: Any) -> None: ...
    colorscale: Any
    "Sets the colorscale. Has an effect only if in `marker.color` is set to a numerical array. The colorscale must be an array containing arrays mapping a normalized value to an rgb, rgba, hex, hsl, hsla, hwb, or named color string. At minimum, a mapping for the lowest (0) and highest (1) values are required. For example, `[[0, 'rgb(0,0,255)'], [1, 'rgb(255,0,0)']]`. To control the bounds of the colorscale in color space, use `marker.cmin` and `marker.cmax`. Alternatively, `colorscale` may be a palette name string of the following list: Blackbody,Bluered,Blues,Cividis,Earth,Electric,Greens,Greys,Hot,Jet,Picnic,Portland,Rainbow,RdBu,Reds,Viridis,YlGnBu,YlOrRd."
    @property
    def line(self) -> _plotly_graph_objs_splom_marker.Line | Any:
        ...
    @line.setter
    def line(self, value: Any) -> None: ...
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
    symbol: Any
    "Sets the marker symbol type. Adding 100 is equivalent to appending *-open* to a symbol name. Adding 200 is equivalent to appending *-dot* to a symbol name. Adding 300 is equivalent to appending *-open-dot* or *dot-open* to a symbol name."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        angle: Any = ...,
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
        "Create a new 'Marker' object\n\nArgs:\n    angle: Sets the marker angle in respect to `angleref`.\n    autocolorscale: Determines whether the colorscale is a default palette (`autocolorscale: true`) or the palette determined by `marker.colorscale`. Has an effect only if in `marker.color` is set to a numerical array. In case `colorscale` is unspecified or `autocolorscale` is true, the default palette will be chosen according to whether numbers in the `color` array are all positive, all negative or mixed.\n    cauto: Determines whether or not the color domain is computed with respect to the input data (here in `marker.color`) or the bounds set in `marker.cmin` and `marker.cmax` Has an effect only if in `marker.color` is set to a numerical array. Defaults to `false` when `marker.cmin` and `marker.cmax` are set by the user.\n    cmax: Sets the upper bound of the color domain. Has an effect only if in `marker.color` is set to a numerical array. Value should have the same units as in `marker.color` and if set, `marker.cmin` must be set as well.\n    cmid: Sets the mid-point of the color domain by scaling `marker.cmin` and/or `marker.cmax` to be equidistant to this point. Has an effect only if in `marker.color` is set to a numerical array. Value should have the same units as in `marker.color`. Has no effect when `marker.cauto` is `false`.\n    cmin: Sets the lower bound of the color domain. Has an effect only if in `marker.color` is set to a numerical array. Value should have the same units as in `marker.color` and if set, `marker.cmax` must be set as well.\n    color: Sets the marker color. It accepts either a specific color or an array of numbers that are mapped to the colorscale relative to the max and min values of the array or relative to `marker.cmin` and `marker.cmax` if set.\n    coloraxis: Sets a reference to a shared color axis. References to these shared color axes are *coloraxis*, *coloraxis2*, *coloraxis3*, etc. Settings for these shared color axes are set in the layout, under `layout.coloraxis`, `layout.coloraxis2`, etc. Note that multiple color scales can be linked to the same color axis.\n    colorscale: Sets the colorscale. Has an effect only if in `marker.color` is set to a numerical array. The colorscale must be an array containing arrays mapping a normalized value to an rgb, rgba, hex, hsl, hsla, hwb, or named color string. At minimum, a mapping for the lowest (0) and highest (1) values are required. For example, `[[0, 'rgb(0,0,255)'], [1, 'rgb(255,0,0)']]`. To control the bounds of the colorscale in color space, use `marker.cmin` and `marker.cmax`. Alternatively, `colorscale` may be a palette name string of the following list: Blackbody,Bluered,Blues,Cividis,Earth,Electric,Greens,Greys,Hot,Jet,Picnic,Portland,Rainbow,RdBu,Reds,Viridis,YlGnBu,YlOrRd.\n    opacity: Sets the marker opacity.\n    reversescale: Reverses the color mapping if true. Has an effect only if in `marker.color` is set to a numerical array. If true, `marker.cmin` will correspond to the last color in the array and `marker.cmax` will correspond to the first color.\n    showscale: Determines whether or not a colorbar is displayed for this trace. Has an effect only if in `marker.color` is set to a numerical array.\n    size: Sets the marker size (in px).\n    sizemin: Has an effect only if `marker.size` is set to a numerical array. Sets the minimum size (in px) of the rendered marker points.\n    sizemode: Has an effect only if `marker.size` is set to a numerical array. Sets the rule for which the data in `size` is converted to pixels.\n    sizeref: Has an effect only if `marker.size` is set to a numerical array. Sets the scale factor used to determine the rendered size of marker points. Use with `sizemin` and `sizemode`.\n    symbol: Sets the marker symbol type. Adding 100 is equivalent to appending *-open* to a symbol name. Adding 200 is equivalent to appending *-dot* to a symbol name. Adding 300 is equivalent to appending *-open-dot* or *dot-open* to a symbol name."
        ...

class Selected(_PlotlyObject):
    "Create a new 'Selected' object"
    @property
    def marker(self) -> _plotly_graph_objs_splom_selected.Marker | Any:
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
    def marker(self) -> _plotly_graph_objs_splom_unselected.Marker | Any:
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
