# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the Plotly catalogue generator in doc/anvil-api-stubs/plotly-stubs.mjs instead, then run:
#   pnpm -F docs build
#
from plotly._base import _PlotlyObject
from typing import Any, Mapping
import plotly.graph_objs.densitymapbox.colorbar as _plotly_graph_objs_densitymapbox_colorbar
import plotly.graph_objs.densitymapbox.colorbar as colorbar
import plotly.graph_objs.densitymapbox.hoverlabel as _plotly_graph_objs_densitymapbox_hoverlabel
import plotly.graph_objs.densitymapbox.hoverlabel as hoverlabel
import plotly.graph_objs.densitymapbox.legendgrouptitle as _plotly_graph_objs_densitymapbox_legendgrouptitle
import plotly.graph_objs.densitymapbox.legendgrouptitle as legendgrouptitle

class ColorBar(_PlotlyObject):
    "Create a new 'ColorBar' object"
    bgcolor: Any
    "Sets the color of padded area."
    bordercolor: Any
    "Sets the axis line color."
    borderwidth: float | Any
    "Sets the width (in px) or the border enclosing this color bar."
    dtick: Any
    "Sets the step in-between ticks on this axis. Use with `tick0`. Must be a positive number, or special strings available to *log* and *date* axes. If the axis `type` is *log*, then ticks are set every 10^(n*dtick) where n is the tick number. For example, to set a tick mark at 1, 10, 100, 1000, ... set dtick to 1. To set tick marks at 1, 100, 10000, ... set dtick to 2. To set tick marks at 1, 5, 25, 125, 625, 3125, ... set dtick to log_10(5), or 0.69897000433. *log* has several special values; *L<f>*, where `f` is a positive number, gives ticks linearly spaced in value (but not position). For example `tick0` = 0.1, `dtick` = *L0.5* will put ticks at 0.1, 0.6, 1.1, 1.6 etc. To show powers of 10 plus small digits between, use *D1* (all digits) or *D2* (only 2 and 5). `tick0` is ignored for *D1* and *D2*. If the axis `type` is *date*, then you must convert the time to milliseconds. For example, to set the interval between ticks to one day, set `dtick` to 86400000.0. *date* also has special values *M<n>* gives ticks spaced by a number of months. `n` must be a positive integer. To set ticks on the 15th of every third month, set `tick0` to *2000-01-15* and `dtick` to *M3*. To set ticks every 4 years, set `dtick` to *M48*"
    exponentformat: Any
    "Determines a formatting rule for the tick exponents. For example, consider the number 1,000,000,000. If *none*, it appears as 1,000,000,000. If *e*, 1e+9. If *E*, 1E+9. If *power*, 1x10^9 (with 9 in a super script). If *SI*, 1G. If *B*, 1B."
    labelalias: Any
    "Replacement text for specific tick or hover labels. For example using {US: 'USA', CA: 'Canada'} changes US to USA and CA to Canada. The labels we would have shown must match the keys exactly, after adding any tickprefix or ticksuffix. For negative numbers the minus sign symbol used (U+2212) is wider than the regular ascii dash. That means you need to use −1 instead of -1. labelalias can be used with any axis type, and both keys (if needed) and values (if desired) can include html-like tags or MathJax."
    len: float | Any
    "Sets the length of the color bar This measure excludes the padding of both ends. That is, the color bar length is this length minus the padding on both ends."
    lenmode: Any
    "Determines whether this color bar's length (i.e. the measure in the color variation direction) is set in units of plot *fraction* or in *pixels. Use `len` to set the value."
    minexponent: float | Any
    "Hide SI prefix for 10^n if |n| is below this number. This only has an effect when `tickformat` is *SI* or *B*."
    nticks: int | Any
    "Specifies the maximum number of ticks for the particular axis. The actual number of ticks will be chosen automatically to be less than or equal to `nticks`. Has an effect only if `tickmode` is set to *auto*."
    orientation: Any
    "Sets the orientation of the colorbar."
    outlinecolor: Any
    "Sets the axis line color."
    outlinewidth: float | Any
    "Sets the width (in px) of the axis line."
    separatethousands: bool | Any
    "If \"true\", even 4-digit integers are separated"
    showexponent: Any
    "If *all*, all exponents are shown besides their significands. If *first*, only the exponent of the first tick is shown. If *last*, only the exponent of the last tick is shown. If *none*, no exponents appear."
    showticklabels: bool | Any
    "Determines whether or not the tick labels are drawn."
    showtickprefix: Any
    "If *all*, all tick labels are displayed with a prefix. If *first*, only the first tick is displayed with a prefix. If *last*, only the last tick is displayed with a suffix. If *none*, tick prefixes are hidden."
    showticksuffix: Any
    "Same as `showtickprefix` but for tick suffixes."
    thickness: float | Any
    "Sets the thickness of the color bar This measure excludes the size of the padding, ticks and labels."
    thicknessmode: Any
    "Determines whether this color bar's thickness (i.e. the measure in the constant color direction) is set in units of plot *fraction* or in *pixels*. Use `thickness` to set the value."
    tick0: Any
    "Sets the placement of the first tick on this axis. Use with `dtick`. If the axis `type` is *log*, then you must take the log of your starting tick (e.g. to set the starting tick to 100, set the `tick0` to 2) except when `dtick`=*L<f>* (see `dtick` for more info). If the axis `type` is *date*, it should be a date string, like date data. If the axis `type` is *category*, it should be a number, using the scale where each category is assigned a serial number from zero in the order it appears."
    tickangle: Any
    "Sets the angle of the tick labels with respect to the horizontal. For example, a `tickangle` of -90 draws the tick labels vertically."
    tickcolor: Any
    "Sets the tick color."
    @property
    def tickfont(self) -> _plotly_graph_objs_densitymapbox_colorbar.Tickfont | Any:
        "Sets the color bar's tick label font"
        ...
    @tickfont.setter
    def tickfont(self, value: Any) -> None: ...
    tickformat: str | Any
    "Sets the tick label formatting rule using d3 formatting mini-languages which are very similar to those in Python. For numbers, see: https://github.com/d3/d3-format/tree/v1.4.5#d3-format. And for dates see: https://github.com/d3/d3-time-format/tree/v2.2.3#locale_format. We add two items to d3's date formatter: *%h* for half of the year as a decimal number as well as *%{n}f* for fractional seconds with n digits. For example, *2016-10-13 09:15:23.456* with tickformat *%H~%M~%S.%2f* would display *09~15~23.46*"
    @property
    def tickformatstop(self) -> _plotly_graph_objs_densitymapbox_colorbar.Tickformatstop | Any:
        ...
    @tickformatstop.setter
    def tickformatstop(self, value: Any) -> None: ...
    ticklabeloverflow: Any
    "Determines how we handle tick labels that would overflow either the graph div or the domain of the axis. The default value for inside tick labels is *hide past domain*. In other cases the default is *hide past div*."
    ticklabelposition: Any
    "Determines where tick labels are drawn relative to the ticks. Left and right options are used when `orientation` is *h*, top and bottom when `orientation` is *v*."
    ticklabelstep: int | Any
    "Sets the spacing between tick labels as compared to the spacing between ticks. A value of 1 (default) means each tick gets a label. A value of 2 means shows every 2nd label. A larger value n means only every nth tick is labeled. `tick0` determines which labels are shown. Not implemented for axes with `type` *log* or *multicategory*, or when `tickmode` is *array*."
    ticklen: float | Any
    "Sets the tick length (in px)."
    tickmode: Any
    "Sets the tick mode for this axis. If *auto*, the number of ticks is set via `nticks`. If *linear*, the placement of the ticks is determined by a starting position `tick0` and a tick step `dtick` (*linear* is the default value if `tick0` and `dtick` are provided). If *array*, the placement of the ticks is set via `tickvals` and the tick text is `ticktext`. (*array* is the default value if `tickvals` is provided)."
    tickprefix: str | Any
    "Sets a tick label prefix."
    ticks: Any
    "Determines whether ticks are drawn or not. If **, this axis' ticks are not drawn. If *outside* (*inside*), this axis' are drawn outside (inside) the axis lines."
    ticksuffix: str | Any
    "Sets a tick label suffix."
    ticktext: Any
    "Sets the text displayed at the ticks position via `tickvals`. Only has an effect if `tickmode` is set to *array*. Used with `tickvals`."
    ticktextsrc: str | Any
    "Sets the source reference on Chart Studio Cloud for `ticktext`."
    tickvals: Any
    "Sets the values at which ticks on this axis appear. Only has an effect if `tickmode` is set to *array*. Used with `ticktext`."
    tickvalssrc: str | Any
    "Sets the source reference on Chart Studio Cloud for `tickvals`."
    tickwidth: float | Any
    "Sets the tick width (in px)."
    @property
    def title(self) -> _plotly_graph_objs_densitymapbox_colorbar.Title | Any:
        ...
    @title.setter
    def title(self, value: Any) -> None: ...
    x: float | Any
    "Sets the x position with respect to `xref` of the color bar (in plot fraction). When `xref` is *paper*, defaults to 1.02 when `orientation` is *v* and 0.5 when `orientation` is *h*. When `xref` is *container*, defaults to *1* when `orientation` is *v* and 0.5 when `orientation` is *h*. Must be between *0* and *1* if `xref` is *container* and between *-2* and *3* if `xref` is *paper*."
    xanchor: Any
    "Sets this color bar's horizontal position anchor. This anchor binds the `x` position to the *left*, *center* or *right* of the color bar. Defaults to *left* when `orientation` is *v* and *center* when `orientation` is *h*."
    xpad: float | Any
    "Sets the amount of padding (in px) along the x direction."
    xref: Any
    "Sets the container `x` refers to. *container* spans the entire `width` of the plot. *paper* refers to the width of the plotting area only."
    y: float | Any
    "Sets the y position with respect to `yref` of the color bar (in plot fraction). When `yref` is *paper*, defaults to 0.5 when `orientation` is *v* and 1.02 when `orientation` is *h*. When `yref` is *container*, defaults to 0.5 when `orientation` is *v* and 1 when `orientation` is *h*. Must be between *0* and *1* if `yref` is *container* and between *-2* and *3* if `yref` is *paper*."
    yanchor: Any
    "Sets this color bar's vertical position anchor This anchor binds the `y` position to the *top*, *middle* or *bottom* of the color bar. Defaults to *middle* when `orientation` is *v* and *bottom* when `orientation` is *h*."
    ypad: float | Any
    "Sets the amount of padding (in px) along the y direction."
    yref: Any
    "Sets the container `y` refers to. *container* spans the entire `height` of the plot. *paper* refers to the height of the plotting area only."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        bgcolor: Any = ...,
        bordercolor: Any = ...,
        borderwidth: Any = ...,
        dtick: Any = ...,
        exponentformat: Any = ...,
        labelalias: Any = ...,
        len: Any = ...,
        lenmode: Any = ...,
        minexponent: Any = ...,
        nticks: Any = ...,
        orientation: Any = ...,
        outlinecolor: Any = ...,
        outlinewidth: Any = ...,
        separatethousands: Any = ...,
        showexponent: Any = ...,
        showticklabels: Any = ...,
        showtickprefix: Any = ...,
        showticksuffix: Any = ...,
        thickness: Any = ...,
        thicknessmode: Any = ...,
        tick0: Any = ...,
        tickangle: Any = ...,
        tickcolor: Any = ...,
        tickfont: Any = ...,
        tickformat: Any = ...,
        tickformatstop: Any = ...,
        ticklabeloverflow: Any = ...,
        ticklabelposition: Any = ...,
        ticklabelstep: Any = ...,
        ticklen: Any = ...,
        tickmode: Any = ...,
        tickprefix: Any = ...,
        ticks: Any = ...,
        ticksuffix: Any = ...,
        ticktext: Any = ...,
        ticktextsrc: Any = ...,
        tickvals: Any = ...,
        tickvalssrc: Any = ...,
        tickwidth: Any = ...,
        title: Any = ...,
        x: Any = ...,
        xanchor: Any = ...,
        xpad: Any = ...,
        xref: Any = ...,
        y: Any = ...,
        yanchor: Any = ...,
        ypad: Any = ...,
        yref: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'ColorBar' object\n\nArgs:\n    bgcolor: Sets the color of padded area.\n    bordercolor: Sets the axis line color.\n    borderwidth: Sets the width (in px) or the border enclosing this color bar.\n    dtick: Sets the step in-between ticks on this axis. Use with `tick0`. Must be a positive number, or special strings available to *log* and *date* axes. If the axis `type` is *log*, then ticks are set every 10^(n*dtick) where n is the tick number. For example, to set a tick mark at 1, 10, 100, 1000, ... set dtick to 1. To set tick marks at 1, 100, 10000, ... set dtick to 2. To set tick marks at 1, 5, 25, 125, 625, 3125, ... set dtick to log_10(5), or 0.69897000433. *log* has several special values; *L<f>*, where `f` is a positive number, gives ticks linearly spaced in value (but not position). For example `tick0` = 0.1, `dtick` = *L0.5* will put ticks at 0.1, 0.6, 1.1, 1.6 etc. To show powers of 10 plus small digits between, use *D1* (all digits) or *D2* (only 2 and 5). `tick0` is ignored for *D1* and *D2*. If the axis `type` is *date*, then you must convert the time to milliseconds. For example, to set the interval between ticks to one day, set `dtick` to 86400000.0. *date* also has special values *M<n>* gives ticks spaced by a number of months. `n` must be a positive integer. To set ticks on the 15th of every third month, set `tick0` to *2000-01-15* and `dtick` to *M3*. To set ticks every 4 years, set `dtick` to *M48*\n    exponentformat: Determines a formatting rule for the tick exponents. For example, consider the number 1,000,000,000. If *none*, it appears as 1,000,000,000. If *e*, 1e+9. If *E*, 1E+9. If *power*, 1x10^9 (with 9 in a super script). If *SI*, 1G. If *B*, 1B.\n    labelalias: Replacement text for specific tick or hover labels. For example using {US: 'USA', CA: 'Canada'} changes US to USA and CA to Canada. The labels we would have shown must match the keys exactly, after adding any tickprefix or ticksuffix. For negative numbers the minus sign symbol used (U+2212) is wider than the regular ascii dash. That means you need to use −1 instead of -1. labelalias can be used with any axis type, and both keys (if needed) and values (if desired) can include html-like tags or MathJax.\n    len: Sets the length of the color bar This measure excludes the padding of both ends. That is, the color bar length is this length minus the padding on both ends.\n    lenmode: Determines whether this color bar's length (i.e. the measure in the color variation direction) is set in units of plot *fraction* or in *pixels. Use `len` to set the value.\n    minexponent: Hide SI prefix for 10^n if |n| is below this number. This only has an effect when `tickformat` is *SI* or *B*.\n    nticks: Specifies the maximum number of ticks for the particular axis. The actual number of ticks will be chosen automatically to be less than or equal to `nticks`. Has an effect only if `tickmode` is set to *auto*.\n    orientation: Sets the orientation of the colorbar.\n    outlinecolor: Sets the axis line color.\n    outlinewidth: Sets the width (in px) of the axis line.\n    separatethousands: If \"true\", even 4-digit integers are separated\n    showexponent: If *all*, all exponents are shown besides their significands. If *first*, only the exponent of the first tick is shown. If *last*, only the exponent of the last tick is shown. If *none*, no exponents appear.\n    showticklabels: Determines whether or not the tick labels are drawn.\n    showtickprefix: If *all*, all tick labels are displayed with a prefix. If *first*, only the first tick is displayed with a prefix. If *last*, only the last tick is displayed with a suffix. If *none*, tick prefixes are hidden.\n    showticksuffix: Same as `showtickprefix` but for tick suffixes.\n    thickness: Sets the thickness of the color bar This measure excludes the size of the padding, ticks and labels.\n    thicknessmode: Determines whether this color bar's thickness (i.e. the measure in the constant color direction) is set in units of plot *fraction* or in *pixels*. Use `thickness` to set the value.\n    tick0: Sets the placement of the first tick on this axis. Use with `dtick`. If the axis `type` is *log*, then you must take the log of your starting tick (e.g. to set the starting tick to 100, set the `tick0` to 2) except when `dtick`=*L<f>* (see `dtick` for more info). If the axis `type` is *date*, it should be a date string, like date data. If the axis `type` is *category*, it should be a number, using the scale where each category is assigned a serial number from zero in the order it appears.\n    tickangle: Sets the angle of the tick labels with respect to the horizontal. For example, a `tickangle` of -90 draws the tick labels vertically.\n    tickcolor: Sets the tick color.\n    tickfont: Sets the color bar's tick label font\n    tickformat: Sets the tick label formatting rule using d3 formatting mini-languages which are very similar to those in Python. For numbers, see: https://github.com/d3/d3-format/tree/v1.4.5#d3-format. And for dates see: https://github.com/d3/d3-time-format/tree/v2.2.3#locale_format. We add two items to d3's date formatter: *%h* for half of the year as a decimal number as well as *%{n}f* for fractional seconds with n digits. For example, *2016-10-13 09:15:23.456* with tickformat *%H~%M~%S.%2f* would display *09~15~23.46*\n    ticklabeloverflow: Determines how we handle tick labels that would overflow either the graph div or the domain of the axis. The default value for inside tick labels is *hide past domain*. In other cases the default is *hide past div*.\n    ticklabelposition: Determines where tick labels are drawn relative to the ticks. Left and right options are used when `orientation` is *h*, top and bottom when `orientation` is *v*.\n    ticklabelstep: Sets the spacing between tick labels as compared to the spacing between ticks. A value of 1 (default) means each tick gets a label. A value of 2 means shows every 2nd label. A larger value n means only every nth tick is labeled. `tick0` determines which labels are shown. Not implemented for axes with `type` *log* or *multicategory*, or when `tickmode` is *array*.\n    ticklen: Sets the tick length (in px).\n    tickmode: Sets the tick mode for this axis. If *auto*, the number of ticks is set via `nticks`. If *linear*, the placement of the ticks is determined by a starting position `tick0` and a tick step `dtick` (*linear* is the default value if `tick0` and `dtick` are provided). If *array*, the placement of the ticks is set via `tickvals` and the tick text is `ticktext`. (*array* is the default value if `tickvals` is provided).\n    tickprefix: Sets a tick label prefix.\n    ticks: Determines whether ticks are drawn or not. If **, this axis' ticks are not drawn. If *outside* (*inside*), this axis' are drawn outside (inside) the axis lines.\n    ticksuffix: Sets a tick label suffix.\n    ticktext: Sets the text displayed at the ticks position via `tickvals`. Only has an effect if `tickmode` is set to *array*. Used with `tickvals`.\n    ticktextsrc: Sets the source reference on Chart Studio Cloud for `ticktext`.\n    tickvals: Sets the values at which ticks on this axis appear. Only has an effect if `tickmode` is set to *array*. Used with `ticktext`.\n    tickvalssrc: Sets the source reference on Chart Studio Cloud for `tickvals`.\n    tickwidth: Sets the tick width (in px).\n    x: Sets the x position with respect to `xref` of the color bar (in plot fraction). When `xref` is *paper*, defaults to 1.02 when `orientation` is *v* and 0.5 when `orientation` is *h*. When `xref` is *container*, defaults to *1* when `orientation` is *v* and 0.5 when `orientation` is *h*. Must be between *0* and *1* if `xref` is *container* and between *-2* and *3* if `xref` is *paper*.\n    xanchor: Sets this color bar's horizontal position anchor. This anchor binds the `x` position to the *left*, *center* or *right* of the color bar. Defaults to *left* when `orientation` is *v* and *center* when `orientation` is *h*.\n    xpad: Sets the amount of padding (in px) along the x direction.\n    xref: Sets the container `x` refers to. *container* spans the entire `width` of the plot. *paper* refers to the width of the plotting area only.\n    y: Sets the y position with respect to `yref` of the color bar (in plot fraction). When `yref` is *paper*, defaults to 0.5 when `orientation` is *v* and 1.02 when `orientation` is *h*. When `yref` is *container*, defaults to 0.5 when `orientation` is *v* and 1 when `orientation` is *h*. Must be between *0* and *1* if `yref` is *container* and between *-2* and *3* if `yref` is *paper*.\n    yanchor: Sets this color bar's vertical position anchor This anchor binds the `y` position to the *top*, *middle* or *bottom* of the color bar. Defaults to *middle* when `orientation` is *v* and *bottom* when `orientation` is *h*.\n    ypad: Sets the amount of padding (in px) along the y direction.\n    yref: Sets the container `y` refers to. *container* spans the entire `height` of the plot. *paper* refers to the height of the plotting area only."
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
    def font(self) -> _plotly_graph_objs_densitymapbox_hoverlabel.Font | Any:
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
    def font(self) -> _plotly_graph_objs_densitymapbox_legendgrouptitle.Font | Any:
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
