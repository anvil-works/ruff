# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the Plotly catalogue generator in doc/anvil-api-stubs/plotly-stubs.mjs instead, then run:
#   pnpm -F docs build
#
from plotly._base import _PlotlyObject
from typing import Any, Mapping
import plotly.graph_objs.layout.polar.angularaxis as _plotly_graph_objs_layout_polar_angularaxis
import plotly.graph_objs.layout.polar.angularaxis as angularaxis
import plotly.graph_objs.layout.polar.radialaxis as _plotly_graph_objs_layout_polar_radialaxis
import plotly.graph_objs.layout.polar.radialaxis as radialaxis

class AngularAxis(_PlotlyObject):
    "Create a new 'AngularAxis' object"
    autotypenumbers: Any
    "Using *strict* a numeric string in trace data is not converted to a number. Using *convert types* a numeric string in trace data may be treated as a number during automatic axis `type` detection. Defaults to layout.autotypenumbers."
    categoryarray: Any
    "Sets the order in which categories on this axis appear. Only has an effect if `categoryorder` is set to *array*. Used with `categoryorder`."
    categoryorder: Any
    "Specifies the ordering logic for the case of categorical variables. By default, plotly uses *trace*, which specifies the order that is present in the data supplied. Set `categoryorder` to *category ascending* or *category descending* if order should be determined by the alphanumerical order of the category names. Set `categoryorder` to *array* to derive the ordering from the attribute `categoryarray`. If a category is not found in the `categoryarray` array, the sorting behavior for that attribute will be identical to the *trace* mode. The unspecified categories will follow the categories in `categoryarray`. Set `categoryorder` to *total ascending* or *total descending* if order should be determined by the numerical order of the values. Similarly, the order can be determined by the min, max, sum, mean, geometric mean or median of all the values."
    color: Any
    "Sets default for all colors associated with this axis all at once: line, font, tick, and grid colors. Grid color is lightened by blending this with the plot background Individual pieces can override this."
    direction: Any
    "Sets the direction corresponding to positive angles."
    dtick: Any
    "Sets the step in-between ticks on this axis. Use with `tick0`. Must be a positive number, or special strings available to *log* and *date* axes. If the axis `type` is *log*, then ticks are set every 10^(n*dtick) where n is the tick number. For example, to set a tick mark at 1, 10, 100, 1000, ... set dtick to 1. To set tick marks at 1, 100, 10000, ... set dtick to 2. To set tick marks at 1, 5, 25, 125, 625, 3125, ... set dtick to log_10(5), or 0.69897000433. *log* has several special values; *L<f>*, where `f` is a positive number, gives ticks linearly spaced in value (but not position). For example `tick0` = 0.1, `dtick` = *L0.5* will put ticks at 0.1, 0.6, 1.1, 1.6 etc. To show powers of 10 plus small digits between, use *D1* (all digits) or *D2* (only 2 and 5). `tick0` is ignored for *D1* and *D2*. If the axis `type` is *date*, then you must convert the time to milliseconds. For example, to set the interval between ticks to one day, set `dtick` to 86400000.0. *date* also has special values *M<n>* gives ticks spaced by a number of months. `n` must be a positive integer. To set ticks on the 15th of every third month, set `tick0` to *2000-01-15* and `dtick` to *M3*. To set ticks every 4 years, set `dtick` to *M48*"
    exponentformat: Any
    "Determines a formatting rule for the tick exponents. For example, consider the number 1,000,000,000. If *none*, it appears as 1,000,000,000. If *e*, 1e+9. If *E*, 1E+9. If *power*, 1x10^9 (with 9 in a super script). If *SI*, 1G. If *B*, 1B. *SI* uses prefixes from \"femto\" f (10^-15) to \"tera\" T (10^12). *SI extended* covers instead the full SI range from \"quecto\" q (10^-30) to \"quetta\" Q (10^30). If *SI* or *SI extended* is used and the exponent is beyond the above ranges, the formatting rule will automatically be switched to the power notation."
    gridcolor: Any
    "Sets the color of the grid lines."
    griddash: str | Any
    "Sets the dash style of lines. Set to a dash type string (*solid*, *dot*, *dash*, *longdash*, *dashdot*, or *longdashdot*) or a dash length list in px (eg *5px,10px,2px,2px*)."
    gridwidth: float | Any
    "Sets the width (in px) of the grid lines."
    hoverformat: str | Any
    "Sets the hover text formatting rule using d3 formatting mini-languages which are very similar to those in Python. For numbers, see: https://github.com/d3/d3-format/tree/v1.4.5#d3-format. And for dates see: https://github.com/d3/d3-time-format/tree/v2.2.3#locale_format. We add two items to d3's date formatter: *%h* for half of the year as a decimal number as well as *%{n}f* for fractional seconds with n digits. For example, *2016-10-13 09:15:23.456* with tickformat *%H~%M~%S.%2f* would display *09~15~23.46*"
    labelalias: Any
    "Replacement text for specific tick or hover labels. For example using {US: 'USA', CA: 'Canada'} changes US to USA and CA to Canada. The labels we would have shown must match the keys exactly, after adding any tickprefix or ticksuffix. For negative numbers the minus sign symbol used (U+2212) is wider than the regular ascii dash. That means you need to use −1 instead of -1. labelalias can be used with any axis type, and both keys (if needed) and values (if desired) can include html-like tags or MathJax."
    layer: Any
    "Sets the layer on which this axis is displayed. If *above traces*, this axis is displayed above all the subplot's traces If *below traces*, this axis is displayed below all the subplot's traces, but above the grid lines. Useful when used together with scatter-like traces with `cliponaxis` set to *false* to show markers and/or text nodes above this axis."
    linecolor: Any
    "Sets the axis line color."
    linewidth: float | Any
    "Sets the width (in px) of the axis line."
    minexponent: float | Any
    "Hide SI prefix for 10^n if |n| is below this number. This only has an effect when `tickformat` is *SI* or *B*."
    minorloglabels: Any
    "Determines how minor log labels are displayed. If *small digits*, small digits i.e. 2 or 5 are displayed. If *complete*, complete digits are displayed. If *none*, no labels are displayed."
    nticks: int | Any
    "Specifies the maximum number of ticks for the particular axis. The actual number of ticks will be chosen automatically to be less than or equal to `nticks`. Has an effect only if `tickmode` is set to *auto*."
    period: float | Any
    "Set the angular period. Has an effect only when `angularaxis.type` is *category*."
    rotation: Any
    "Sets that start position (in degrees) of the angular axis By default, polar subplots with `direction` set to *counterclockwise* get a `rotation` of *0* which corresponds to due East (like what mathematicians prefer). In turn, polar with `direction` set to *clockwise* get a rotation of *90* which corresponds to due North (like on a compass),"
    separatethousands: bool | Any
    "If \"true\", even 4-digit integers are separated"
    showexponent: Any
    "If *all*, all exponents are shown besides their significands. If *first*, only the exponent of the first tick is shown. If *last*, only the exponent of the last tick is shown. If *none*, no exponents appear."
    showgrid: bool | Any
    "Determines whether or not grid lines are drawn. If *true*, the grid lines are drawn at every tick mark."
    showline: bool | Any
    "Determines whether or not a line bounding this axis is drawn."
    showticklabels: bool | Any
    "Determines whether or not the tick labels are drawn."
    showtickprefix: Any
    "If *all*, all tick labels are displayed with a prefix. If *first*, only the first tick is displayed with a prefix. If *last*, only the last tick is displayed with a suffix. If *none*, tick prefixes are hidden."
    showticksuffix: Any
    "Same as `showtickprefix` but for tick suffixes."
    thetaunit: Any
    "Sets the format unit of the formatted *theta* values. Has an effect only when `angularaxis.type` is *linear*."
    tick0: Any
    "Sets the placement of the first tick on this axis. Use with `dtick`. If the axis `type` is *log*, then you must take the log of your starting tick (e.g. to set the starting tick to 100, set the `tick0` to 2) except when `dtick`=*L<f>* (see `dtick` for more info). If the axis `type` is *date*, it should be a date string, like date data. If the axis `type` is *category*, it should be a number, using the scale where each category is assigned a serial number from zero in the order it appears."
    tickangle: Any
    "Sets the angle of the tick labels with respect to the horizontal. For example, a `tickangle` of -90 draws the tick labels vertically."
    tickcolor: Any
    "Sets the tick color."
    @property
    def tickfont(self) -> _plotly_graph_objs_layout_polar_angularaxis.Tickfont | Any:
        "Sets the tick font."
        ...
    @tickfont.setter
    def tickfont(self, value: Any) -> None: ...
    tickformat: str | Any
    "Sets the tick label formatting rule using d3 formatting mini-languages which are very similar to those in Python. For numbers, see: https://github.com/d3/d3-format/tree/v1.4.5#d3-format. And for dates see: https://github.com/d3/d3-time-format/tree/v2.2.3#locale_format. We add two items to d3's date formatter: *%h* for half of the year as a decimal number as well as *%{n}f* for fractional seconds with n digits. For example, *2016-10-13 09:15:23.456* with tickformat *%H~%M~%S.%2f* would display *09~15~23.46*"
    @property
    def tickformatstop(self) -> _plotly_graph_objs_layout_polar_angularaxis.Tickformatstop | Any:
        ...
    @tickformatstop.setter
    def tickformatstop(self, value: Any) -> None: ...
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
    type: Any
    "Sets the angular axis type. If *linear*, set `thetaunit` to determine the unit in which axis value are shown. If *category, use `period` to set the number of integer coordinates around polar axis."
    uirevision: Any
    "Controls persistence of user-driven changes in axis `rotation`. Defaults to `polar<N>.uirevision`."
    visible: bool | Any
    "A single toggle to hide the axis while preserving interaction like dragging. Default is true when a cheater plot is present on the axis, otherwise false"
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        autotypenumbers: Any = ...,
        categoryarray: Any = ...,
        categoryorder: Any = ...,
        color: Any = ...,
        direction: Any = ...,
        dtick: Any = ...,
        exponentformat: Any = ...,
        gridcolor: Any = ...,
        griddash: Any = ...,
        gridwidth: Any = ...,
        hoverformat: Any = ...,
        labelalias: Any = ...,
        layer: Any = ...,
        linecolor: Any = ...,
        linewidth: Any = ...,
        minexponent: Any = ...,
        minorloglabels: Any = ...,
        nticks: Any = ...,
        period: Any = ...,
        rotation: Any = ...,
        separatethousands: Any = ...,
        showexponent: Any = ...,
        showgrid: Any = ...,
        showline: Any = ...,
        showticklabels: Any = ...,
        showtickprefix: Any = ...,
        showticksuffix: Any = ...,
        thetaunit: Any = ...,
        tick0: Any = ...,
        tickangle: Any = ...,
        tickcolor: Any = ...,
        tickfont: Any = ...,
        tickformat: Any = ...,
        tickformatstop: Any = ...,
        ticklabelstep: Any = ...,
        ticklen: Any = ...,
        tickmode: Any = ...,
        tickprefix: Any = ...,
        ticks: Any = ...,
        ticksuffix: Any = ...,
        ticktext: Any = ...,
        tickvals: Any = ...,
        tickwidth: Any = ...,
        type: Any = ...,
        uirevision: Any = ...,
        visible: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'AngularAxis' object\n\nArgs:\n    autotypenumbers: Using *strict* a numeric string in trace data is not converted to a number. Using *convert types* a numeric string in trace data may be treated as a number during automatic axis `type` detection. Defaults to layout.autotypenumbers.\n    categoryarray: Sets the order in which categories on this axis appear. Only has an effect if `categoryorder` is set to *array*. Used with `categoryorder`.\n    categoryorder: Specifies the ordering logic for the case of categorical variables. By default, plotly uses *trace*, which specifies the order that is present in the data supplied. Set `categoryorder` to *category ascending* or *category descending* if order should be determined by the alphanumerical order of the category names. Set `categoryorder` to *array* to derive the ordering from the attribute `categoryarray`. If a category is not found in the `categoryarray` array, the sorting behavior for that attribute will be identical to the *trace* mode. The unspecified categories will follow the categories in `categoryarray`. Set `categoryorder` to *total ascending* or *total descending* if order should be determined by the numerical order of the values. Similarly, the order can be determined by the min, max, sum, mean, geometric mean or median of all the values.\n    color: Sets default for all colors associated with this axis all at once: line, font, tick, and grid colors. Grid color is lightened by blending this with the plot background Individual pieces can override this.\n    direction: Sets the direction corresponding to positive angles.\n    dtick: Sets the step in-between ticks on this axis. Use with `tick0`. Must be a positive number, or special strings available to *log* and *date* axes. If the axis `type` is *log*, then ticks are set every 10^(n*dtick) where n is the tick number. For example, to set a tick mark at 1, 10, 100, 1000, ... set dtick to 1. To set tick marks at 1, 100, 10000, ... set dtick to 2. To set tick marks at 1, 5, 25, 125, 625, 3125, ... set dtick to log_10(5), or 0.69897000433. *log* has several special values; *L<f>*, where `f` is a positive number, gives ticks linearly spaced in value (but not position). For example `tick0` = 0.1, `dtick` = *L0.5* will put ticks at 0.1, 0.6, 1.1, 1.6 etc. To show powers of 10 plus small digits between, use *D1* (all digits) or *D2* (only 2 and 5). `tick0` is ignored for *D1* and *D2*. If the axis `type` is *date*, then you must convert the time to milliseconds. For example, to set the interval between ticks to one day, set `dtick` to 86400000.0. *date* also has special values *M<n>* gives ticks spaced by a number of months. `n` must be a positive integer. To set ticks on the 15th of every third month, set `tick0` to *2000-01-15* and `dtick` to *M3*. To set ticks every 4 years, set `dtick` to *M48*\n    exponentformat: Determines a formatting rule for the tick exponents. For example, consider the number 1,000,000,000. If *none*, it appears as 1,000,000,000. If *e*, 1e+9. If *E*, 1E+9. If *power*, 1x10^9 (with 9 in a super script). If *SI*, 1G. If *B*, 1B. *SI* uses prefixes from \"femto\" f (10^-15) to \"tera\" T (10^12). *SI extended* covers instead the full SI range from \"quecto\" q (10^-30) to \"quetta\" Q (10^30). If *SI* or *SI extended* is used and the exponent is beyond the above ranges, the formatting rule will automatically be switched to the power notation.\n    gridcolor: Sets the color of the grid lines.\n    griddash: Sets the dash style of lines. Set to a dash type string (*solid*, *dot*, *dash*, *longdash*, *dashdot*, or *longdashdot*) or a dash length list in px (eg *5px,10px,2px,2px*).\n    gridwidth: Sets the width (in px) of the grid lines.\n    hoverformat: Sets the hover text formatting rule using d3 formatting mini-languages which are very similar to those in Python. For numbers, see: https://github.com/d3/d3-format/tree/v1.4.5#d3-format. And for dates see: https://github.com/d3/d3-time-format/tree/v2.2.3#locale_format. We add two items to d3's date formatter: *%h* for half of the year as a decimal number as well as *%{n}f* for fractional seconds with n digits. For example, *2016-10-13 09:15:23.456* with tickformat *%H~%M~%S.%2f* would display *09~15~23.46*\n    labelalias: Replacement text for specific tick or hover labels. For example using {US: 'USA', CA: 'Canada'} changes US to USA and CA to Canada. The labels we would have shown must match the keys exactly, after adding any tickprefix or ticksuffix. For negative numbers the minus sign symbol used (U+2212) is wider than the regular ascii dash. That means you need to use −1 instead of -1. labelalias can be used with any axis type, and both keys (if needed) and values (if desired) can include html-like tags or MathJax.\n    layer: Sets the layer on which this axis is displayed. If *above traces*, this axis is displayed above all the subplot's traces If *below traces*, this axis is displayed below all the subplot's traces, but above the grid lines. Useful when used together with scatter-like traces with `cliponaxis` set to *false* to show markers and/or text nodes above this axis.\n    linecolor: Sets the axis line color.\n    linewidth: Sets the width (in px) of the axis line.\n    minexponent: Hide SI prefix for 10^n if |n| is below this number. This only has an effect when `tickformat` is *SI* or *B*.\n    minorloglabels: Determines how minor log labels are displayed. If *small digits*, small digits i.e. 2 or 5 are displayed. If *complete*, complete digits are displayed. If *none*, no labels are displayed.\n    nticks: Specifies the maximum number of ticks for the particular axis. The actual number of ticks will be chosen automatically to be less than or equal to `nticks`. Has an effect only if `tickmode` is set to *auto*.\n    period: Set the angular period. Has an effect only when `angularaxis.type` is *category*.\n    rotation: Sets that start position (in degrees) of the angular axis By default, polar subplots with `direction` set to *counterclockwise* get a `rotation` of *0* which corresponds to due East (like what mathematicians prefer). In turn, polar with `direction` set to *clockwise* get a rotation of *90* which corresponds to due North (like on a compass),\n    separatethousands: If \"true\", even 4-digit integers are separated\n    showexponent: If *all*, all exponents are shown besides their significands. If *first*, only the exponent of the first tick is shown. If *last*, only the exponent of the last tick is shown. If *none*, no exponents appear.\n    showgrid: Determines whether or not grid lines are drawn. If *true*, the grid lines are drawn at every tick mark.\n    showline: Determines whether or not a line bounding this axis is drawn.\n    showticklabels: Determines whether or not the tick labels are drawn.\n    showtickprefix: If *all*, all tick labels are displayed with a prefix. If *first*, only the first tick is displayed with a prefix. If *last*, only the last tick is displayed with a suffix. If *none*, tick prefixes are hidden.\n    showticksuffix: Same as `showtickprefix` but for tick suffixes.\n    thetaunit: Sets the format unit of the formatted *theta* values. Has an effect only when `angularaxis.type` is *linear*.\n    tick0: Sets the placement of the first tick on this axis. Use with `dtick`. If the axis `type` is *log*, then you must take the log of your starting tick (e.g. to set the starting tick to 100, set the `tick0` to 2) except when `dtick`=*L<f>* (see `dtick` for more info). If the axis `type` is *date*, it should be a date string, like date data. If the axis `type` is *category*, it should be a number, using the scale where each category is assigned a serial number from zero in the order it appears.\n    tickangle: Sets the angle of the tick labels with respect to the horizontal. For example, a `tickangle` of -90 draws the tick labels vertically.\n    tickcolor: Sets the tick color.\n    tickfont: Sets the tick font.\n    tickformat: Sets the tick label formatting rule using d3 formatting mini-languages which are very similar to those in Python. For numbers, see: https://github.com/d3/d3-format/tree/v1.4.5#d3-format. And for dates see: https://github.com/d3/d3-time-format/tree/v2.2.3#locale_format. We add two items to d3's date formatter: *%h* for half of the year as a decimal number as well as *%{n}f* for fractional seconds with n digits. For example, *2016-10-13 09:15:23.456* with tickformat *%H~%M~%S.%2f* would display *09~15~23.46*\n    ticklabelstep: Sets the spacing between tick labels as compared to the spacing between ticks. A value of 1 (default) means each tick gets a label. A value of 2 means shows every 2nd label. A larger value n means only every nth tick is labeled. `tick0` determines which labels are shown. Not implemented for axes with `type` *log* or *multicategory*, or when `tickmode` is *array*.\n    ticklen: Sets the tick length (in px).\n    tickmode: Sets the tick mode for this axis. If *auto*, the number of ticks is set via `nticks`. If *linear*, the placement of the ticks is determined by a starting position `tick0` and a tick step `dtick` (*linear* is the default value if `tick0` and `dtick` are provided). If *array*, the placement of the ticks is set via `tickvals` and the tick text is `ticktext`. (*array* is the default value if `tickvals` is provided).\n    tickprefix: Sets a tick label prefix.\n    ticks: Determines whether ticks are drawn or not. If **, this axis' ticks are not drawn. If *outside* (*inside*), this axis' are drawn outside (inside) the axis lines.\n    ticksuffix: Sets a tick label suffix.\n    ticktext: Sets the text displayed at the ticks position via `tickvals`. Only has an effect if `tickmode` is set to *array*. Used with `tickvals`.\n    tickvals: Sets the values at which ticks on this axis appear. Only has an effect if `tickmode` is set to *array*. Used with `ticktext`.\n    tickwidth: Sets the tick width (in px).\n    type: Sets the angular axis type. If *linear*, set `thetaunit` to determine the unit in which axis value are shown. If *category, use `period` to set the number of integer coordinates around polar axis.\n    uirevision: Controls persistence of user-driven changes in axis `rotation`. Defaults to `polar<N>.uirevision`.\n    visible: A single toggle to hide the axis while preserving interaction like dragging. Default is true when a cheater plot is present on the axis, otherwise false"
        ...

class Domain(_PlotlyObject):
    "Create a new 'Domain' object"
    column: int | Any
    "If there is a layout grid, use the domain for this column in the grid for this polar subplot."
    row: int | Any
    "If there is a layout grid, use the domain for this row in the grid for this polar subplot."
    x: Any
    "Sets the horizontal domain of this polar subplot (in plot fraction)."
    y: Any
    "Sets the vertical domain of this polar subplot (in plot fraction)."
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
        "Create a new 'Domain' object\n\nArgs:\n    column: If there is a layout grid, use the domain for this column in the grid for this polar subplot.\n    row: If there is a layout grid, use the domain for this row in the grid for this polar subplot.\n    x: Sets the horizontal domain of this polar subplot (in plot fraction).\n    y: Sets the vertical domain of this polar subplot (in plot fraction)."
        ...

class RadialAxis(_PlotlyObject):
    "Create a new 'RadialAxis' object"
    angle: Any
    "Sets the angle (in degrees) from which the radial axis is drawn. Note that by default, radial axis line on the theta=0 line corresponds to a line pointing right (like what mathematicians prefer). Defaults to the first `polar.sector` angle."
    autorange: Any
    "Determines whether or not the range of this axis is computed in relation to the input data. See `rangemode` for more info. If `range` is provided and it has a value for both the lower and upper bound, `autorange` is set to *false*. Using *min* applies autorange only to set the minimum. Using *max* applies autorange only to set the maximum. Using *min reversed* applies autorange only to set the minimum on a reversed axis. Using *max reversed* applies autorange only to set the maximum on a reversed axis. Using *reversed* applies autorange on both ends and reverses the axis direction."
    @property
    def autorangeoptions(self) -> _plotly_graph_objs_layout_polar_radialaxis.Autorangeoptions | Any:
        ...
    @autorangeoptions.setter
    def autorangeoptions(self, value: Any) -> None: ...
    autotickangles: Any
    "When `tickangle` is set to *auto*, it will be set to the first angle in this array that is large enough to prevent label overlap."
    autotypenumbers: Any
    "Using *strict* a numeric string in trace data is not converted to a number. Using *convert types* a numeric string in trace data may be treated as a number during automatic axis `type` detection. Defaults to layout.autotypenumbers."
    calendar: Any
    "Sets the calendar system to use for `range` and `tick0` if this is a date axis. This does not set the calendar for interpreting data on this axis, that's specified in the trace or via the global `layout.calendar`"
    categoryarray: Any
    "Sets the order in which categories on this axis appear. Only has an effect if `categoryorder` is set to *array*. Used with `categoryorder`."
    categoryorder: Any
    "Specifies the ordering logic for the case of categorical variables. By default, plotly uses *trace*, which specifies the order that is present in the data supplied. Set `categoryorder` to *category ascending* or *category descending* if order should be determined by the alphanumerical order of the category names. Set `categoryorder` to *array* to derive the ordering from the attribute `categoryarray`. If a category is not found in the `categoryarray` array, the sorting behavior for that attribute will be identical to the *trace* mode. The unspecified categories will follow the categories in `categoryarray`. Set `categoryorder` to *total ascending* or *total descending* if order should be determined by the numerical order of the values. Similarly, the order can be determined by the min, max, sum, mean, geometric mean or median of all the values."
    color: Any
    "Sets default for all colors associated with this axis all at once: line, font, tick, and grid colors. Grid color is lightened by blending this with the plot background Individual pieces can override this."
    dtick: Any
    "Sets the step in-between ticks on this axis. Use with `tick0`. Must be a positive number, or special strings available to *log* and *date* axes. If the axis `type` is *log*, then ticks are set every 10^(n*dtick) where n is the tick number. For example, to set a tick mark at 1, 10, 100, 1000, ... set dtick to 1. To set tick marks at 1, 100, 10000, ... set dtick to 2. To set tick marks at 1, 5, 25, 125, 625, 3125, ... set dtick to log_10(5), or 0.69897000433. *log* has several special values; *L<f>*, where `f` is a positive number, gives ticks linearly spaced in value (but not position). For example `tick0` = 0.1, `dtick` = *L0.5* will put ticks at 0.1, 0.6, 1.1, 1.6 etc. To show powers of 10 plus small digits between, use *D1* (all digits) or *D2* (only 2 and 5). `tick0` is ignored for *D1* and *D2*. If the axis `type` is *date*, then you must convert the time to milliseconds. For example, to set the interval between ticks to one day, set `dtick` to 86400000.0. *date* also has special values *M<n>* gives ticks spaced by a number of months. `n` must be a positive integer. To set ticks on the 15th of every third month, set `tick0` to *2000-01-15* and `dtick` to *M3*. To set ticks every 4 years, set `dtick` to *M48*"
    exponentformat: Any
    "Determines a formatting rule for the tick exponents. For example, consider the number 1,000,000,000. If *none*, it appears as 1,000,000,000. If *e*, 1e+9. If *E*, 1E+9. If *power*, 1x10^9 (with 9 in a super script). If *SI*, 1G. If *B*, 1B. *SI* uses prefixes from \"femto\" f (10^-15) to \"tera\" T (10^12). *SI extended* covers instead the full SI range from \"quecto\" q (10^-30) to \"quetta\" Q (10^30). If *SI* or *SI extended* is used and the exponent is beyond the above ranges, the formatting rule will automatically be switched to the power notation."
    gridcolor: Any
    "Sets the color of the grid lines."
    griddash: str | Any
    "Sets the dash style of lines. Set to a dash type string (*solid*, *dot*, *dash*, *longdash*, *dashdot*, or *longdashdot*) or a dash length list in px (eg *5px,10px,2px,2px*)."
    gridwidth: float | Any
    "Sets the width (in px) of the grid lines."
    hoverformat: str | Any
    "Sets the hover text formatting rule using d3 formatting mini-languages which are very similar to those in Python. For numbers, see: https://github.com/d3/d3-format/tree/v1.4.5#d3-format. And for dates see: https://github.com/d3/d3-time-format/tree/v2.2.3#locale_format. We add two items to d3's date formatter: *%h* for half of the year as a decimal number as well as *%{n}f* for fractional seconds with n digits. For example, *2016-10-13 09:15:23.456* with tickformat *%H~%M~%S.%2f* would display *09~15~23.46*"
    labelalias: Any
    "Replacement text for specific tick or hover labels. For example using {US: 'USA', CA: 'Canada'} changes US to USA and CA to Canada. The labels we would have shown must match the keys exactly, after adding any tickprefix or ticksuffix. For negative numbers the minus sign symbol used (U+2212) is wider than the regular ascii dash. That means you need to use −1 instead of -1. labelalias can be used with any axis type, and both keys (if needed) and values (if desired) can include html-like tags or MathJax."
    layer: Any
    "Sets the layer on which this axis is displayed. If *above traces*, this axis is displayed above all the subplot's traces If *below traces*, this axis is displayed below all the subplot's traces, but above the grid lines. Useful when used together with scatter-like traces with `cliponaxis` set to *false* to show markers and/or text nodes above this axis."
    linecolor: Any
    "Sets the axis line color."
    linewidth: float | Any
    "Sets the width (in px) of the axis line."
    maxallowed: Any
    "Determines the maximum range of this axis."
    minallowed: Any
    "Determines the minimum range of this axis."
    minexponent: float | Any
    "Hide SI prefix for 10^n if |n| is below this number. This only has an effect when `tickformat` is *SI* or *B*."
    minorloglabels: Any
    "Determines how minor log labels are displayed. If *small digits*, small digits i.e. 2 or 5 are displayed. If *complete*, complete digits are displayed. If *none*, no labels are displayed."
    nticks: int | Any
    "Specifies the maximum number of ticks for the particular axis. The actual number of ticks will be chosen automatically to be less than or equal to `nticks`. Has an effect only if `tickmode` is set to *auto*."
    range: Any
    "Sets the range of this axis. If the axis `type` is *log*, then you must take the log of your desired range (e.g. to set the range from 1 to 100, set the range from 0 to 2). If the axis `type` is *date*, it should be date strings, like date data, though Date objects and unix milliseconds will be accepted and converted to strings. If the axis `type` is *category*, it should be numbers, using the scale where each category is assigned a serial number from zero in the order it appears. Leaving either or both elements `null` impacts the default `autorange`."
    rangemode: Any
    "If *tozero*, the range extends to 0, regardless of the input data If *nonnegative*, the range is non-negative, regardless of the input data. If *normal*, the range is computed in relation to the extrema of the input data (same behavior as for cartesian axes)."
    separatethousands: bool | Any
    "If \"true\", even 4-digit integers are separated"
    showexponent: Any
    "If *all*, all exponents are shown besides their significands. If *first*, only the exponent of the first tick is shown. If *last*, only the exponent of the last tick is shown. If *none*, no exponents appear."
    showgrid: bool | Any
    "Determines whether or not grid lines are drawn. If *true*, the grid lines are drawn at every tick mark."
    showline: bool | Any
    "Determines whether or not a line bounding this axis is drawn."
    showticklabels: bool | Any
    "Determines whether or not the tick labels are drawn."
    showtickprefix: Any
    "If *all*, all tick labels are displayed with a prefix. If *first*, only the first tick is displayed with a prefix. If *last*, only the last tick is displayed with a suffix. If *none*, tick prefixes are hidden."
    showticksuffix: Any
    "Same as `showtickprefix` but for tick suffixes."
    side: Any
    "Determines on which side of radial axis line the tick and tick labels appear."
    tick0: Any
    "Sets the placement of the first tick on this axis. Use with `dtick`. If the axis `type` is *log*, then you must take the log of your starting tick (e.g. to set the starting tick to 100, set the `tick0` to 2) except when `dtick`=*L<f>* (see `dtick` for more info). If the axis `type` is *date*, it should be a date string, like date data. If the axis `type` is *category*, it should be a number, using the scale where each category is assigned a serial number from zero in the order it appears."
    tickangle: Any
    "Sets the angle of the tick labels with respect to the horizontal. For example, a `tickangle` of -90 draws the tick labels vertically."
    tickcolor: Any
    "Sets the tick color."
    @property
    def tickfont(self) -> _plotly_graph_objs_layout_polar_radialaxis.Tickfont | Any:
        "Sets the tick font."
        ...
    @tickfont.setter
    def tickfont(self, value: Any) -> None: ...
    tickformat: str | Any
    "Sets the tick label formatting rule using d3 formatting mini-languages which are very similar to those in Python. For numbers, see: https://github.com/d3/d3-format/tree/v1.4.5#d3-format. And for dates see: https://github.com/d3/d3-time-format/tree/v2.2.3#locale_format. We add two items to d3's date formatter: *%h* for half of the year as a decimal number as well as *%{n}f* for fractional seconds with n digits. For example, *2016-10-13 09:15:23.456* with tickformat *%H~%M~%S.%2f* would display *09~15~23.46*"
    @property
    def tickformatstop(self) -> _plotly_graph_objs_layout_polar_radialaxis.Tickformatstop | Any:
        ...
    @tickformatstop.setter
    def tickformatstop(self, value: Any) -> None: ...
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
    def title(self) -> _plotly_graph_objs_layout_polar_radialaxis.Title | Any:
        ...
    @title.setter
    def title(self, value: Any) -> None: ...
    type: Any
    "Sets the axis type. By default, plotly attempts to determined the axis type by looking into the data of the traces that referenced the axis in question."
    uirevision: Any
    "Controls persistence of user-driven changes in axis `range`, `autorange`, `angle`, and `title` if in `editable: true` configuration. Defaults to `polar<N>.uirevision`."
    visible: bool | Any
    "A single toggle to hide the axis while preserving interaction like dragging. Default is true when a cheater plot is present on the axis, otherwise false"
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        angle: Any = ...,
        autorange: Any = ...,
        autorangeoptions: Any = ...,
        autotickangles: Any = ...,
        autotypenumbers: Any = ...,
        calendar: Any = ...,
        categoryarray: Any = ...,
        categoryorder: Any = ...,
        color: Any = ...,
        dtick: Any = ...,
        exponentformat: Any = ...,
        gridcolor: Any = ...,
        griddash: Any = ...,
        gridwidth: Any = ...,
        hoverformat: Any = ...,
        labelalias: Any = ...,
        layer: Any = ...,
        linecolor: Any = ...,
        linewidth: Any = ...,
        maxallowed: Any = ...,
        minallowed: Any = ...,
        minexponent: Any = ...,
        minorloglabels: Any = ...,
        nticks: Any = ...,
        range: Any = ...,
        rangemode: Any = ...,
        separatethousands: Any = ...,
        showexponent: Any = ...,
        showgrid: Any = ...,
        showline: Any = ...,
        showticklabels: Any = ...,
        showtickprefix: Any = ...,
        showticksuffix: Any = ...,
        side: Any = ...,
        tick0: Any = ...,
        tickangle: Any = ...,
        tickcolor: Any = ...,
        tickfont: Any = ...,
        tickformat: Any = ...,
        tickformatstop: Any = ...,
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
        type: Any = ...,
        uirevision: Any = ...,
        visible: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'RadialAxis' object\n\nArgs:\n    angle: Sets the angle (in degrees) from which the radial axis is drawn. Note that by default, radial axis line on the theta=0 line corresponds to a line pointing right (like what mathematicians prefer). Defaults to the first `polar.sector` angle.\n    autorange: Determines whether or not the range of this axis is computed in relation to the input data. See `rangemode` for more info. If `range` is provided and it has a value for both the lower and upper bound, `autorange` is set to *false*. Using *min* applies autorange only to set the minimum. Using *max* applies autorange only to set the maximum. Using *min reversed* applies autorange only to set the minimum on a reversed axis. Using *max reversed* applies autorange only to set the maximum on a reversed axis. Using *reversed* applies autorange on both ends and reverses the axis direction.\n    autotickangles: When `tickangle` is set to *auto*, it will be set to the first angle in this array that is large enough to prevent label overlap.\n    autotypenumbers: Using *strict* a numeric string in trace data is not converted to a number. Using *convert types* a numeric string in trace data may be treated as a number during automatic axis `type` detection. Defaults to layout.autotypenumbers.\n    calendar: Sets the calendar system to use for `range` and `tick0` if this is a date axis. This does not set the calendar for interpreting data on this axis, that's specified in the trace or via the global `layout.calendar`\n    categoryarray: Sets the order in which categories on this axis appear. Only has an effect if `categoryorder` is set to *array*. Used with `categoryorder`.\n    categoryorder: Specifies the ordering logic for the case of categorical variables. By default, plotly uses *trace*, which specifies the order that is present in the data supplied. Set `categoryorder` to *category ascending* or *category descending* if order should be determined by the alphanumerical order of the category names. Set `categoryorder` to *array* to derive the ordering from the attribute `categoryarray`. If a category is not found in the `categoryarray` array, the sorting behavior for that attribute will be identical to the *trace* mode. The unspecified categories will follow the categories in `categoryarray`. Set `categoryorder` to *total ascending* or *total descending* if order should be determined by the numerical order of the values. Similarly, the order can be determined by the min, max, sum, mean, geometric mean or median of all the values.\n    color: Sets default for all colors associated with this axis all at once: line, font, tick, and grid colors. Grid color is lightened by blending this with the plot background Individual pieces can override this.\n    dtick: Sets the step in-between ticks on this axis. Use with `tick0`. Must be a positive number, or special strings available to *log* and *date* axes. If the axis `type` is *log*, then ticks are set every 10^(n*dtick) where n is the tick number. For example, to set a tick mark at 1, 10, 100, 1000, ... set dtick to 1. To set tick marks at 1, 100, 10000, ... set dtick to 2. To set tick marks at 1, 5, 25, 125, 625, 3125, ... set dtick to log_10(5), or 0.69897000433. *log* has several special values; *L<f>*, where `f` is a positive number, gives ticks linearly spaced in value (but not position). For example `tick0` = 0.1, `dtick` = *L0.5* will put ticks at 0.1, 0.6, 1.1, 1.6 etc. To show powers of 10 plus small digits between, use *D1* (all digits) or *D2* (only 2 and 5). `tick0` is ignored for *D1* and *D2*. If the axis `type` is *date*, then you must convert the time to milliseconds. For example, to set the interval between ticks to one day, set `dtick` to 86400000.0. *date* also has special values *M<n>* gives ticks spaced by a number of months. `n` must be a positive integer. To set ticks on the 15th of every third month, set `tick0` to *2000-01-15* and `dtick` to *M3*. To set ticks every 4 years, set `dtick` to *M48*\n    exponentformat: Determines a formatting rule for the tick exponents. For example, consider the number 1,000,000,000. If *none*, it appears as 1,000,000,000. If *e*, 1e+9. If *E*, 1E+9. If *power*, 1x10^9 (with 9 in a super script). If *SI*, 1G. If *B*, 1B. *SI* uses prefixes from \"femto\" f (10^-15) to \"tera\" T (10^12). *SI extended* covers instead the full SI range from \"quecto\" q (10^-30) to \"quetta\" Q (10^30). If *SI* or *SI extended* is used and the exponent is beyond the above ranges, the formatting rule will automatically be switched to the power notation.\n    gridcolor: Sets the color of the grid lines.\n    griddash: Sets the dash style of lines. Set to a dash type string (*solid*, *dot*, *dash*, *longdash*, *dashdot*, or *longdashdot*) or a dash length list in px (eg *5px,10px,2px,2px*).\n    gridwidth: Sets the width (in px) of the grid lines.\n    hoverformat: Sets the hover text formatting rule using d3 formatting mini-languages which are very similar to those in Python. For numbers, see: https://github.com/d3/d3-format/tree/v1.4.5#d3-format. And for dates see: https://github.com/d3/d3-time-format/tree/v2.2.3#locale_format. We add two items to d3's date formatter: *%h* for half of the year as a decimal number as well as *%{n}f* for fractional seconds with n digits. For example, *2016-10-13 09:15:23.456* with tickformat *%H~%M~%S.%2f* would display *09~15~23.46*\n    labelalias: Replacement text for specific tick or hover labels. For example using {US: 'USA', CA: 'Canada'} changes US to USA and CA to Canada. The labels we would have shown must match the keys exactly, after adding any tickprefix or ticksuffix. For negative numbers the minus sign symbol used (U+2212) is wider than the regular ascii dash. That means you need to use −1 instead of -1. labelalias can be used with any axis type, and both keys (if needed) and values (if desired) can include html-like tags or MathJax.\n    layer: Sets the layer on which this axis is displayed. If *above traces*, this axis is displayed above all the subplot's traces If *below traces*, this axis is displayed below all the subplot's traces, but above the grid lines. Useful when used together with scatter-like traces with `cliponaxis` set to *false* to show markers and/or text nodes above this axis.\n    linecolor: Sets the axis line color.\n    linewidth: Sets the width (in px) of the axis line.\n    maxallowed: Determines the maximum range of this axis.\n    minallowed: Determines the minimum range of this axis.\n    minexponent: Hide SI prefix for 10^n if |n| is below this number. This only has an effect when `tickformat` is *SI* or *B*.\n    minorloglabels: Determines how minor log labels are displayed. If *small digits*, small digits i.e. 2 or 5 are displayed. If *complete*, complete digits are displayed. If *none*, no labels are displayed.\n    nticks: Specifies the maximum number of ticks for the particular axis. The actual number of ticks will be chosen automatically to be less than or equal to `nticks`. Has an effect only if `tickmode` is set to *auto*.\n    range: Sets the range of this axis. If the axis `type` is *log*, then you must take the log of your desired range (e.g. to set the range from 1 to 100, set the range from 0 to 2). If the axis `type` is *date*, it should be date strings, like date data, though Date objects and unix milliseconds will be accepted and converted to strings. If the axis `type` is *category*, it should be numbers, using the scale where each category is assigned a serial number from zero in the order it appears. Leaving either or both elements `null` impacts the default `autorange`.\n    rangemode: If *tozero*, the range extends to 0, regardless of the input data If *nonnegative*, the range is non-negative, regardless of the input data. If *normal*, the range is computed in relation to the extrema of the input data (same behavior as for cartesian axes).\n    separatethousands: If \"true\", even 4-digit integers are separated\n    showexponent: If *all*, all exponents are shown besides their significands. If *first*, only the exponent of the first tick is shown. If *last*, only the exponent of the last tick is shown. If *none*, no exponents appear.\n    showgrid: Determines whether or not grid lines are drawn. If *true*, the grid lines are drawn at every tick mark.\n    showline: Determines whether or not a line bounding this axis is drawn.\n    showticklabels: Determines whether or not the tick labels are drawn.\n    showtickprefix: If *all*, all tick labels are displayed with a prefix. If *first*, only the first tick is displayed with a prefix. If *last*, only the last tick is displayed with a suffix. If *none*, tick prefixes are hidden.\n    showticksuffix: Same as `showtickprefix` but for tick suffixes.\n    side: Determines on which side of radial axis line the tick and tick labels appear.\n    tick0: Sets the placement of the first tick on this axis. Use with `dtick`. If the axis `type` is *log*, then you must take the log of your starting tick (e.g. to set the starting tick to 100, set the `tick0` to 2) except when `dtick`=*L<f>* (see `dtick` for more info). If the axis `type` is *date*, it should be a date string, like date data. If the axis `type` is *category*, it should be a number, using the scale where each category is assigned a serial number from zero in the order it appears.\n    tickangle: Sets the angle of the tick labels with respect to the horizontal. For example, a `tickangle` of -90 draws the tick labels vertically.\n    tickcolor: Sets the tick color.\n    tickfont: Sets the tick font.\n    tickformat: Sets the tick label formatting rule using d3 formatting mini-languages which are very similar to those in Python. For numbers, see: https://github.com/d3/d3-format/tree/v1.4.5#d3-format. And for dates see: https://github.com/d3/d3-time-format/tree/v2.2.3#locale_format. We add two items to d3's date formatter: *%h* for half of the year as a decimal number as well as *%{n}f* for fractional seconds with n digits. For example, *2016-10-13 09:15:23.456* with tickformat *%H~%M~%S.%2f* would display *09~15~23.46*\n    ticklabelstep: Sets the spacing between tick labels as compared to the spacing between ticks. A value of 1 (default) means each tick gets a label. A value of 2 means shows every 2nd label. A larger value n means only every nth tick is labeled. `tick0` determines which labels are shown. Not implemented for axes with `type` *log* or *multicategory*, or when `tickmode` is *array*.\n    ticklen: Sets the tick length (in px).\n    tickmode: Sets the tick mode for this axis. If *auto*, the number of ticks is set via `nticks`. If *linear*, the placement of the ticks is determined by a starting position `tick0` and a tick step `dtick` (*linear* is the default value if `tick0` and `dtick` are provided). If *array*, the placement of the ticks is set via `tickvals` and the tick text is `ticktext`. (*array* is the default value if `tickvals` is provided).\n    tickprefix: Sets a tick label prefix.\n    ticks: Determines whether ticks are drawn or not. If **, this axis' ticks are not drawn. If *outside* (*inside*), this axis' are drawn outside (inside) the axis lines.\n    ticksuffix: Sets a tick label suffix.\n    ticktext: Sets the text displayed at the ticks position via `tickvals`. Only has an effect if `tickmode` is set to *array*. Used with `tickvals`.\n    tickvals: Sets the values at which ticks on this axis appear. Only has an effect if `tickmode` is set to *array*. Used with `ticktext`.\n    tickwidth: Sets the tick width (in px).\n    type: Sets the axis type. By default, plotly attempts to determined the axis type by looking into the data of the traces that referenced the axis in question.\n    uirevision: Controls persistence of user-driven changes in axis `range`, `autorange`, `angle`, and `title` if in `editable: true` configuration. Defaults to `polar<N>.uirevision`.\n    visible: A single toggle to hide the axis while preserving interaction like dragging. Default is true when a cheater plot is present on the axis, otherwise false"
        ...
