# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the Plotly catalogue generator in doc/anvil-api-stubs/plotly-stubs.mjs instead, then run:
#   pnpm -F docs build
#
from plotly._base import _PlotlyObject
from typing import Any, Mapping
import plotly.graph_objs.contour.colorbar as _plotly_graph_objs_contour_colorbar
import plotly.graph_objs.contour.colorbar as colorbar
import plotly.graph_objs.contour.contours as _plotly_graph_objs_contour_contours
import plotly.graph_objs.contour.contours as contours
import plotly.graph_objs.contour.hoverlabel as _plotly_graph_objs_contour_hoverlabel
import plotly.graph_objs.contour.hoverlabel as hoverlabel
import plotly.graph_objs.contour.legendgrouptitle as _plotly_graph_objs_contour_legendgrouptitle
import plotly.graph_objs.contour.legendgrouptitle as legendgrouptitle

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
    "Determines a formatting rule for the tick exponents. For example, consider the number 1,000,000,000. If *none*, it appears as 1,000,000,000. If *e*, 1e+9. If *E*, 1E+9. If *power*, 1x10^9 (with 9 in a super script). If *SI*, 1G. If *B*, 1B. *SI* uses prefixes from \"femto\" f (10^-15) to \"tera\" T (10^12). *SI extended* covers instead the full SI range from \"quecto\" q (10^-30) to \"quetta\" Q (10^30). If *SI* or *SI extended* is used and the exponent is beyond the above ranges, the formatting rule will automatically be switched to the power notation."
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
    def tickfont(self) -> _plotly_graph_objs_contour_colorbar.Tickfont | Any:
        "Sets the color bar's tick label font"
        ...
    @tickfont.setter
    def tickfont(self, value: Any) -> None: ...
    tickformat: str | Any
    "Sets the tick label formatting rule using d3 formatting mini-languages which are very similar to those in Python. For numbers, see: https://github.com/d3/d3-format/tree/v1.4.5#d3-format. And for dates see: https://github.com/d3/d3-time-format/tree/v2.2.3#locale_format. We add two items to d3's date formatter: *%h* for half of the year as a decimal number as well as *%{n}f* for fractional seconds with n digits. For example, *2016-10-13 09:15:23.456* with tickformat *%H~%M~%S.%2f* would display *09~15~23.46*"
    @property
    def tickformatstop(self) -> _plotly_graph_objs_contour_colorbar.Tickformatstop | Any:
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
    tickvals: Any
    "Sets the values at which ticks on this axis appear. Only has an effect if `tickmode` is set to *array*. Used with `ticktext`."
    tickwidth: float | Any
    "Sets the tick width (in px)."
    @property
    def title(self) -> _plotly_graph_objs_contour_colorbar.Title | Any:
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
        tickvals: Any = ...,
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
        "Create a new 'ColorBar' object\n\nArgs:\n    bgcolor: Sets the color of padded area.\n    bordercolor: Sets the axis line color.\n    borderwidth: Sets the width (in px) or the border enclosing this color bar.\n    dtick: Sets the step in-between ticks on this axis. Use with `tick0`. Must be a positive number, or special strings available to *log* and *date* axes. If the axis `type` is *log*, then ticks are set every 10^(n*dtick) where n is the tick number. For example, to set a tick mark at 1, 10, 100, 1000, ... set dtick to 1. To set tick marks at 1, 100, 10000, ... set dtick to 2. To set tick marks at 1, 5, 25, 125, 625, 3125, ... set dtick to log_10(5), or 0.69897000433. *log* has several special values; *L<f>*, where `f` is a positive number, gives ticks linearly spaced in value (but not position). For example `tick0` = 0.1, `dtick` = *L0.5* will put ticks at 0.1, 0.6, 1.1, 1.6 etc. To show powers of 10 plus small digits between, use *D1* (all digits) or *D2* (only 2 and 5). `tick0` is ignored for *D1* and *D2*. If the axis `type` is *date*, then you must convert the time to milliseconds. For example, to set the interval between ticks to one day, set `dtick` to 86400000.0. *date* also has special values *M<n>* gives ticks spaced by a number of months. `n` must be a positive integer. To set ticks on the 15th of every third month, set `tick0` to *2000-01-15* and `dtick` to *M3*. To set ticks every 4 years, set `dtick` to *M48*\n    exponentformat: Determines a formatting rule for the tick exponents. For example, consider the number 1,000,000,000. If *none*, it appears as 1,000,000,000. If *e*, 1e+9. If *E*, 1E+9. If *power*, 1x10^9 (with 9 in a super script). If *SI*, 1G. If *B*, 1B. *SI* uses prefixes from \"femto\" f (10^-15) to \"tera\" T (10^12). *SI extended* covers instead the full SI range from \"quecto\" q (10^-30) to \"quetta\" Q (10^30). If *SI* or *SI extended* is used and the exponent is beyond the above ranges, the formatting rule will automatically be switched to the power notation.\n    labelalias: Replacement text for specific tick or hover labels. For example using {US: 'USA', CA: 'Canada'} changes US to USA and CA to Canada. The labels we would have shown must match the keys exactly, after adding any tickprefix or ticksuffix. For negative numbers the minus sign symbol used (U+2212) is wider than the regular ascii dash. That means you need to use −1 instead of -1. labelalias can be used with any axis type, and both keys (if needed) and values (if desired) can include html-like tags or MathJax.\n    len: Sets the length of the color bar This measure excludes the padding of both ends. That is, the color bar length is this length minus the padding on both ends.\n    lenmode: Determines whether this color bar's length (i.e. the measure in the color variation direction) is set in units of plot *fraction* or in *pixels. Use `len` to set the value.\n    minexponent: Hide SI prefix for 10^n if |n| is below this number. This only has an effect when `tickformat` is *SI* or *B*.\n    nticks: Specifies the maximum number of ticks for the particular axis. The actual number of ticks will be chosen automatically to be less than or equal to `nticks`. Has an effect only if `tickmode` is set to *auto*.\n    orientation: Sets the orientation of the colorbar.\n    outlinecolor: Sets the axis line color.\n    outlinewidth: Sets the width (in px) of the axis line.\n    separatethousands: If \"true\", even 4-digit integers are separated\n    showexponent: If *all*, all exponents are shown besides their significands. If *first*, only the exponent of the first tick is shown. If *last*, only the exponent of the last tick is shown. If *none*, no exponents appear.\n    showticklabels: Determines whether or not the tick labels are drawn.\n    showtickprefix: If *all*, all tick labels are displayed with a prefix. If *first*, only the first tick is displayed with a prefix. If *last*, only the last tick is displayed with a suffix. If *none*, tick prefixes are hidden.\n    showticksuffix: Same as `showtickprefix` but for tick suffixes.\n    thickness: Sets the thickness of the color bar This measure excludes the size of the padding, ticks and labels.\n    thicknessmode: Determines whether this color bar's thickness (i.e. the measure in the constant color direction) is set in units of plot *fraction* or in *pixels*. Use `thickness` to set the value.\n    tick0: Sets the placement of the first tick on this axis. Use with `dtick`. If the axis `type` is *log*, then you must take the log of your starting tick (e.g. to set the starting tick to 100, set the `tick0` to 2) except when `dtick`=*L<f>* (see `dtick` for more info). If the axis `type` is *date*, it should be a date string, like date data. If the axis `type` is *category*, it should be a number, using the scale where each category is assigned a serial number from zero in the order it appears.\n    tickangle: Sets the angle of the tick labels with respect to the horizontal. For example, a `tickangle` of -90 draws the tick labels vertically.\n    tickcolor: Sets the tick color.\n    tickfont: Sets the color bar's tick label font\n    tickformat: Sets the tick label formatting rule using d3 formatting mini-languages which are very similar to those in Python. For numbers, see: https://github.com/d3/d3-format/tree/v1.4.5#d3-format. And for dates see: https://github.com/d3/d3-time-format/tree/v2.2.3#locale_format. We add two items to d3's date formatter: *%h* for half of the year as a decimal number as well as *%{n}f* for fractional seconds with n digits. For example, *2016-10-13 09:15:23.456* with tickformat *%H~%M~%S.%2f* would display *09~15~23.46*\n    ticklabeloverflow: Determines how we handle tick labels that would overflow either the graph div or the domain of the axis. The default value for inside tick labels is *hide past domain*. In other cases the default is *hide past div*.\n    ticklabelposition: Determines where tick labels are drawn relative to the ticks. Left and right options are used when `orientation` is *h*, top and bottom when `orientation` is *v*.\n    ticklabelstep: Sets the spacing between tick labels as compared to the spacing between ticks. A value of 1 (default) means each tick gets a label. A value of 2 means shows every 2nd label. A larger value n means only every nth tick is labeled. `tick0` determines which labels are shown. Not implemented for axes with `type` *log* or *multicategory*, or when `tickmode` is *array*.\n    ticklen: Sets the tick length (in px).\n    tickmode: Sets the tick mode for this axis. If *auto*, the number of ticks is set via `nticks`. If *linear*, the placement of the ticks is determined by a starting position `tick0` and a tick step `dtick` (*linear* is the default value if `tick0` and `dtick` are provided). If *array*, the placement of the ticks is set via `tickvals` and the tick text is `ticktext`. (*array* is the default value if `tickvals` is provided).\n    tickprefix: Sets a tick label prefix.\n    ticks: Determines whether ticks are drawn or not. If **, this axis' ticks are not drawn. If *outside* (*inside*), this axis' are drawn outside (inside) the axis lines.\n    ticksuffix: Sets a tick label suffix.\n    ticktext: Sets the text displayed at the ticks position via `tickvals`. Only has an effect if `tickmode` is set to *array*. Used with `tickvals`.\n    tickvals: Sets the values at which ticks on this axis appear. Only has an effect if `tickmode` is set to *array*. Used with `ticktext`.\n    tickwidth: Sets the tick width (in px).\n    x: Sets the x position with respect to `xref` of the color bar (in plot fraction). When `xref` is *paper*, defaults to 1.02 when `orientation` is *v* and 0.5 when `orientation` is *h*. When `xref` is *container*, defaults to *1* when `orientation` is *v* and 0.5 when `orientation` is *h*. Must be between *0* and *1* if `xref` is *container* and between *-2* and *3* if `xref` is *paper*.\n    xanchor: Sets this color bar's horizontal position anchor. This anchor binds the `x` position to the *left*, *center* or *right* of the color bar. Defaults to *left* when `orientation` is *v* and *center* when `orientation` is *h*.\n    xpad: Sets the amount of padding (in px) along the x direction.\n    xref: Sets the container `x` refers to. *container* spans the entire `width` of the plot. *paper* refers to the width of the plotting area only.\n    y: Sets the y position with respect to `yref` of the color bar (in plot fraction). When `yref` is *paper*, defaults to 0.5 when `orientation` is *v* and 1.02 when `orientation` is *h*. When `yref` is *container*, defaults to 0.5 when `orientation` is *v* and 1 when `orientation` is *h*. Must be between *0* and *1* if `yref` is *container* and between *-2* and *3* if `yref` is *paper*.\n    yanchor: Sets this color bar's vertical position anchor This anchor binds the `y` position to the *top*, *middle* or *bottom* of the color bar. Defaults to *middle* when `orientation` is *v* and *bottom* when `orientation` is *h*.\n    ypad: Sets the amount of padding (in px) along the y direction.\n    yref: Sets the container `y` refers to. *container* spans the entire `height` of the plot. *paper* refers to the height of the plotting area only."
        ...

class Contours(_PlotlyObject):
    "Create a new 'Contours' object"
    coloring: Any
    "Determines the coloring method showing the contour values. If *fill*, coloring is done evenly between each contour level If *heatmap*, a heatmap gradient coloring is applied between each contour level. If *lines*, coloring is done on the contour lines. If *none*, no coloring is applied on this trace."
    end: float | Any
    "Sets the end contour level value. Must be more than `contours.start`"
    @property
    def impliedEdits(self) -> _plotly_graph_objs_contour_contours.Impliededits | Any:
        ...
    @impliedEdits.setter
    def impliedEdits(self, value: Any) -> None: ...
    @property
    def labelfont(self) -> _plotly_graph_objs_contour_contours.Labelfont | Any:
        "Sets the font used for labeling the contour levels. The default color comes from the lines, if shown. The default family and size come from `layout.font`."
        ...
    @labelfont.setter
    def labelfont(self, value: Any) -> None: ...
    labelformat: str | Any
    "Sets the contour label formatting rule using d3 formatting mini-languages which are very similar to those in Python. For numbers, see: https://github.com/d3/d3-format/tree/v1.4.5#d3-format."
    operation: Any
    "Sets the constraint operation. *=* keeps regions equal to `value` *<* and *<=* keep regions less than `value` *>* and *>=* keep regions greater than `value` *[]*, *()*, *[)*, and *(]* keep regions inside `value[0]` to `value[1]` *][*, *)(*, *](*, *)[* keep regions outside `value[0]` to value[1]` Open vs. closed intervals make no difference to constraint display, but all versions are allowed."
    showlabels: bool | Any
    "Determines whether to label the contour lines with their values."
    showlines: bool | Any
    "Determines whether or not the contour lines are drawn. Has an effect only if `contours.coloring` is set to *fill*."
    size: float | Any
    "Sets the step between each contour level. Must be positive."
    start: float | Any
    "Sets the starting contour level value. Must be less than `contours.end`"
    type: Any
    "If `levels`, the data is represented as a contour plot with multiple levels displayed. If `constraint`, the data is represented as constraints with the invalid region shaded as specified by the `operation` and `value` parameters."
    value: Any
    "Sets the value or values of the constraint boundary. When `operation` is set to one of the comparison values (`=,<,>=,>,<=`) *value* is expected to be a number. When `operation` is set to one of the interval values (`[],(),[),(],][,)(,](,)[`) *value* is expected to be an array of two numbers where the first is the lower bound and the second is the upper bound."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        coloring: Any = ...,
        end: Any = ...,
        impliedEdits: Any = ...,
        labelfont: Any = ...,
        labelformat: Any = ...,
        operation: Any = ...,
        showlabels: Any = ...,
        showlines: Any = ...,
        size: Any = ...,
        start: Any = ...,
        type: Any = ...,
        value: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Contours' object\n\nArgs:\n    coloring: Determines the coloring method showing the contour values. If *fill*, coloring is done evenly between each contour level If *heatmap*, a heatmap gradient coloring is applied between each contour level. If *lines*, coloring is done on the contour lines. If *none*, no coloring is applied on this trace.\n    end: Sets the end contour level value. Must be more than `contours.start`\n    labelfont: Sets the font used for labeling the contour levels. The default color comes from the lines, if shown. The default family and size come from `layout.font`.\n    labelformat: Sets the contour label formatting rule using d3 formatting mini-languages which are very similar to those in Python. For numbers, see: https://github.com/d3/d3-format/tree/v1.4.5#d3-format.\n    operation: Sets the constraint operation. *=* keeps regions equal to `value` *<* and *<=* keep regions less than `value` *>* and *>=* keep regions greater than `value` *[]*, *()*, *[)*, and *(]* keep regions inside `value[0]` to `value[1]` *][*, *)(*, *](*, *)[* keep regions outside `value[0]` to value[1]` Open vs. closed intervals make no difference to constraint display, but all versions are allowed.\n    showlabels: Determines whether to label the contour lines with their values.\n    showlines: Determines whether or not the contour lines are drawn. Has an effect only if `contours.coloring` is set to *fill*.\n    size: Sets the step between each contour level. Must be positive.\n    start: Sets the starting contour level value. Must be less than `contours.end`\n    type: If `levels`, the data is represented as a contour plot with multiple levels displayed. If `constraint`, the data is represented as constraints with the invalid region shaded as specified by the `operation` and `value` parameters.\n    value: Sets the value or values of the constraint boundary. When `operation` is set to one of the comparison values (`=,<,>=,>,<=`) *value* is expected to be a number. When `operation` is set to one of the interval values (`[],(),[),(],][,)(,](,)[`) *value* is expected to be an array of two numbers where the first is the lower bound and the second is the upper bound."
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
    def font(self) -> _plotly_graph_objs_contour_hoverlabel.Font | Any:
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
    def font(self) -> _plotly_graph_objs_contour_legendgrouptitle.Font | Any:
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
    "Sets the color of the contour level. Has no effect if `contours.coloring` is set to *lines*."
    dash: str | Any
    "Sets the dash style of lines. Set to a dash type string (*solid*, *dot*, *dash*, *longdash*, *dashdot*, or *longdashdot*) or a dash length list in px (eg *5px,10px,2px,2px*)."
    smoothing: float | Any
    "Sets the amount of smoothing for the contour lines, where *0* corresponds to no smoothing."
    width: float | Any
    "Sets the contour line width in (in px) Defaults to *0.5* when `contours.type` is *levels*. Defaults to *2* when `contour.type` is *constraint*."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        color: Any = ...,
        dash: Any = ...,
        smoothing: Any = ...,
        width: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Line' object\n\nArgs:\n    color: Sets the color of the contour level. Has no effect if `contours.coloring` is set to *lines*.\n    dash: Sets the dash style of lines. Set to a dash type string (*solid*, *dot*, *dash*, *longdash*, *dashdot*, or *longdashdot*) or a dash length list in px (eg *5px,10px,2px,2px*).\n    smoothing: Sets the amount of smoothing for the contour lines, where *0* corresponds to no smoothing.\n    width: Sets the contour line width in (in px) Defaults to *0.5* when `contours.type` is *levels*. Defaults to *2* when `contour.type` is *constraint*."
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
