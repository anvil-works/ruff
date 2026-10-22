# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the Plotly catalogue generator in doc/anvil-api-stubs/plotly-stubs.mjs instead, then run:
#   pnpm -F docs build
#
from plotly._base import _PlotlyObject
from typing import Any, Mapping
import plotly.graph_objs.carpet.aaxis as _plotly_graph_objs_carpet_aaxis
import plotly.graph_objs.carpet.aaxis as aaxis
import plotly.graph_objs.carpet.baxis as _plotly_graph_objs_carpet_baxis
import plotly.graph_objs.carpet.baxis as baxis
import plotly.graph_objs.carpet.legendgrouptitle as _plotly_graph_objs_carpet_legendgrouptitle
import plotly.graph_objs.carpet.legendgrouptitle as legendgrouptitle

class Aaxis(_PlotlyObject):
    "Create a new 'Aaxis' object"
    arraydtick: int | Any
    "The stride between grid lines along the axis"
    arraytick0: int | Any
    "The starting index of grid lines along the axis"
    autorange: Any
    "Determines whether or not the range of this axis is computed in relation to the input data. See `rangemode` for more info. If `range` is provided, then `autorange` is set to *false*."
    autotypenumbers: Any
    "Using *strict* a numeric string in trace data is not converted to a number. Using *convert types* a numeric string in trace data may be treated as a number during automatic axis `type` detection. Defaults to layout.autotypenumbers."
    categoryarray: Any
    "Sets the order in which categories on this axis appear. Only has an effect if `categoryorder` is set to *array*. Used with `categoryorder`."
    categoryorder: Any
    "Specifies the ordering logic for the case of categorical variables. By default, plotly uses *trace*, which specifies the order that is present in the data supplied. Set `categoryorder` to *category ascending* or *category descending* if order should be determined by the alphanumerical order of the category names. Set `categoryorder` to *array* to derive the ordering from the attribute `categoryarray`. If a category is not found in the `categoryarray` array, the sorting behavior for that attribute will be identical to the *trace* mode. The unspecified categories will follow the categories in `categoryarray`."
    cheatertype: Any
    color: Any
    "Sets default for all colors associated with this axis all at once: line, font, tick, and grid colors. Grid color is lightened by blending this with the plot background Individual pieces can override this."
    dtick: float | Any
    "The stride between grid lines along the axis"
    endline: bool | Any
    "Determines whether or not a line is drawn at along the final value of this axis. If *true*, the end line is drawn on top of the grid lines."
    endlinecolor: Any
    "Sets the line color of the end line."
    endlinewidth: float | Any
    "Sets the width (in px) of the end line."
    exponentformat: Any
    "Determines a formatting rule for the tick exponents. For example, consider the number 1,000,000,000. If *none*, it appears as 1,000,000,000. If *e*, 1e+9. If *E*, 1E+9. If *power*, 1x10^9 (with 9 in a super script). If *SI*, 1G. If *B*, 1B."
    fixedrange: bool | Any
    "Determines whether or not this axis is zoom-able. If true, then zoom is disabled."
    gridcolor: Any
    "Sets the axis line color."
    griddash: str | Any
    "Sets the dash style of lines. Set to a dash type string (*solid*, *dot*, *dash*, *longdash*, *dashdot*, or *longdashdot*) or a dash length list in px (eg *5px,10px,2px,2px*)."
    gridwidth: float | Any
    "Sets the width (in px) of the axis line."
    labelalias: Any
    "Replacement text for specific tick or hover labels. For example using {US: 'USA', CA: 'Canada'} changes US to USA and CA to Canada. The labels we would have shown must match the keys exactly, after adding any tickprefix or ticksuffix. For negative numbers the minus sign symbol used (U+2212) is wider than the regular ascii dash. That means you need to use −1 instead of -1. labelalias can be used with any axis type, and both keys (if needed) and values (if desired) can include html-like tags or MathJax."
    labelpadding: int | Any
    "Extra padding between label and the axis"
    labelprefix: str | Any
    "Sets a axis label prefix."
    labelsuffix: str | Any
    "Sets a axis label suffix."
    linecolor: Any
    "Sets the axis line color."
    linewidth: float | Any
    "Sets the width (in px) of the axis line."
    minexponent: float | Any
    "Hide SI prefix for 10^n if |n| is below this number"
    minorgridcolor: Any
    "Sets the color of the grid lines."
    minorgridcount: int | Any
    "Sets the number of minor grid ticks per major grid tick"
    minorgriddash: str | Any
    "Sets the dash style of lines. Set to a dash type string (*solid*, *dot*, *dash*, *longdash*, *dashdot*, or *longdashdot*) or a dash length list in px (eg *5px,10px,2px,2px*)."
    minorgridwidth: float | Any
    "Sets the width (in px) of the grid lines."
    nticks: int | Any
    "Specifies the maximum number of ticks for the particular axis. The actual number of ticks will be chosen automatically to be less than or equal to `nticks`. Has an effect only if `tickmode` is set to *auto*."
    range: Any
    "Sets the range of this axis. If the axis `type` is *log*, then you must take the log of your desired range (e.g. to set the range from 1 to 100, set the range from 0 to 2). If the axis `type` is *date*, it should be date strings, like date data, though Date objects and unix milliseconds will be accepted and converted to strings. If the axis `type` is *category*, it should be numbers, using the scale where each category is assigned a serial number from zero in the order it appears."
    rangemode: Any
    "If *normal*, the range is computed in relation to the extrema of the input data. If *tozero*, the range extends to 0, regardless of the input data If *nonnegative*, the range is non-negative, regardless of the input data."
    separatethousands: bool | Any
    "If \"true\", even 4-digit integers are separated"
    showexponent: Any
    "If *all*, all exponents are shown besides their significands. If *first*, only the exponent of the first tick is shown. If *last*, only the exponent of the last tick is shown. If *none*, no exponents appear."
    showgrid: bool | Any
    "Determines whether or not grid lines are drawn. If *true*, the grid lines are drawn at every tick mark."
    showline: bool | Any
    "Determines whether or not a line bounding this axis is drawn."
    showticklabels: Any
    "Determines whether axis labels are drawn on the low side, the high side, both, or neither side of the axis."
    showtickprefix: Any
    "If *all*, all tick labels are displayed with a prefix. If *first*, only the first tick is displayed with a prefix. If *last*, only the last tick is displayed with a suffix. If *none*, tick prefixes are hidden."
    showticksuffix: Any
    "Same as `showtickprefix` but for tick suffixes."
    smoothing: float | Any
    startline: bool | Any
    "Determines whether or not a line is drawn at along the starting value of this axis. If *true*, the start line is drawn on top of the grid lines."
    startlinecolor: Any
    "Sets the line color of the start line."
    startlinewidth: float | Any
    "Sets the width (in px) of the start line."
    tick0: float | Any
    "The starting index of grid lines along the axis"
    tickangle: Any
    "Sets the angle of the tick labels with respect to the horizontal. For example, a `tickangle` of -90 draws the tick labels vertically."
    @property
    def tickfont(self) -> _plotly_graph_objs_carpet_aaxis.Tickfont | Any:
        "Sets the tick font."
        ...
    @tickfont.setter
    def tickfont(self, value: Any) -> None: ...
    tickformat: str | Any
    "Sets the tick label formatting rule using d3 formatting mini-languages which are very similar to those in Python. For numbers, see: https://github.com/d3/d3-format/tree/v1.4.5#d3-format. And for dates see: https://github.com/d3/d3-time-format/tree/v2.2.3#locale_format. We add two items to d3's date formatter: *%h* for half of the year as a decimal number as well as *%{n}f* for fractional seconds with n digits. For example, *2016-10-13 09:15:23.456* with tickformat *%H~%M~%S.%2f* would display *09~15~23.46*"
    @property
    def tickformatstop(self) -> _plotly_graph_objs_carpet_aaxis.Tickformatstop | Any:
        ...
    @tickformatstop.setter
    def tickformatstop(self, value: Any) -> None: ...
    tickmode: Any
    tickprefix: str | Any
    "Sets a tick label prefix."
    ticksuffix: str | Any
    "Sets a tick label suffix."
    ticktext: Any
    "Sets the text displayed at the ticks position via `tickvals`. Only has an effect if `tickmode` is set to *array*. Used with `tickvals`."
    tickvals: Any
    "Sets the values at which ticks on this axis appear. Only has an effect if `tickmode` is set to *array*. Used with `ticktext`."
    @property
    def title(self) -> _plotly_graph_objs_carpet_aaxis.Title | Any:
        ...
    @title.setter
    def title(self, value: Any) -> None: ...
    type: Any
    "Sets the axis type. By default, plotly attempts to determined the axis type by looking into the data of the traces that referenced the axis in question."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        arraydtick: Any = ...,
        arraytick0: Any = ...,
        autorange: Any = ...,
        autotypenumbers: Any = ...,
        categoryarray: Any = ...,
        categoryorder: Any = ...,
        cheatertype: Any = ...,
        color: Any = ...,
        dtick: Any = ...,
        endline: Any = ...,
        endlinecolor: Any = ...,
        endlinewidth: Any = ...,
        exponentformat: Any = ...,
        fixedrange: Any = ...,
        gridcolor: Any = ...,
        griddash: Any = ...,
        gridwidth: Any = ...,
        labelalias: Any = ...,
        labelpadding: Any = ...,
        labelprefix: Any = ...,
        labelsuffix: Any = ...,
        linecolor: Any = ...,
        linewidth: Any = ...,
        minexponent: Any = ...,
        minorgridcolor: Any = ...,
        minorgridcount: Any = ...,
        minorgriddash: Any = ...,
        minorgridwidth: Any = ...,
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
        smoothing: Any = ...,
        startline: Any = ...,
        startlinecolor: Any = ...,
        startlinewidth: Any = ...,
        tick0: Any = ...,
        tickangle: Any = ...,
        tickfont: Any = ...,
        tickformat: Any = ...,
        tickformatstop: Any = ...,
        tickmode: Any = ...,
        tickprefix: Any = ...,
        ticksuffix: Any = ...,
        ticktext: Any = ...,
        tickvals: Any = ...,
        title: Any = ...,
        type: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Aaxis' object\n\nArgs:\n    arraydtick: The stride between grid lines along the axis\n    arraytick0: The starting index of grid lines along the axis\n    autorange: Determines whether or not the range of this axis is computed in relation to the input data. See `rangemode` for more info. If `range` is provided, then `autorange` is set to *false*.\n    autotypenumbers: Using *strict* a numeric string in trace data is not converted to a number. Using *convert types* a numeric string in trace data may be treated as a number during automatic axis `type` detection. Defaults to layout.autotypenumbers.\n    categoryarray: Sets the order in which categories on this axis appear. Only has an effect if `categoryorder` is set to *array*. Used with `categoryorder`.\n    categoryorder: Specifies the ordering logic for the case of categorical variables. By default, plotly uses *trace*, which specifies the order that is present in the data supplied. Set `categoryorder` to *category ascending* or *category descending* if order should be determined by the alphanumerical order of the category names. Set `categoryorder` to *array* to derive the ordering from the attribute `categoryarray`. If a category is not found in the `categoryarray` array, the sorting behavior for that attribute will be identical to the *trace* mode. The unspecified categories will follow the categories in `categoryarray`.\n    color: Sets default for all colors associated with this axis all at once: line, font, tick, and grid colors. Grid color is lightened by blending this with the plot background Individual pieces can override this.\n    dtick: The stride between grid lines along the axis\n    endline: Determines whether or not a line is drawn at along the final value of this axis. If *true*, the end line is drawn on top of the grid lines.\n    endlinecolor: Sets the line color of the end line.\n    endlinewidth: Sets the width (in px) of the end line.\n    exponentformat: Determines a formatting rule for the tick exponents. For example, consider the number 1,000,000,000. If *none*, it appears as 1,000,000,000. If *e*, 1e+9. If *E*, 1E+9. If *power*, 1x10^9 (with 9 in a super script). If *SI*, 1G. If *B*, 1B.\n    fixedrange: Determines whether or not this axis is zoom-able. If true, then zoom is disabled.\n    gridcolor: Sets the axis line color.\n    griddash: Sets the dash style of lines. Set to a dash type string (*solid*, *dot*, *dash*, *longdash*, *dashdot*, or *longdashdot*) or a dash length list in px (eg *5px,10px,2px,2px*).\n    gridwidth: Sets the width (in px) of the axis line.\n    labelalias: Replacement text for specific tick or hover labels. For example using {US: 'USA', CA: 'Canada'} changes US to USA and CA to Canada. The labels we would have shown must match the keys exactly, after adding any tickprefix or ticksuffix. For negative numbers the minus sign symbol used (U+2212) is wider than the regular ascii dash. That means you need to use −1 instead of -1. labelalias can be used with any axis type, and both keys (if needed) and values (if desired) can include html-like tags or MathJax.\n    labelpadding: Extra padding between label and the axis\n    labelprefix: Sets a axis label prefix.\n    labelsuffix: Sets a axis label suffix.\n    linecolor: Sets the axis line color.\n    linewidth: Sets the width (in px) of the axis line.\n    minexponent: Hide SI prefix for 10^n if |n| is below this number\n    minorgridcolor: Sets the color of the grid lines.\n    minorgridcount: Sets the number of minor grid ticks per major grid tick\n    minorgriddash: Sets the dash style of lines. Set to a dash type string (*solid*, *dot*, *dash*, *longdash*, *dashdot*, or *longdashdot*) or a dash length list in px (eg *5px,10px,2px,2px*).\n    minorgridwidth: Sets the width (in px) of the grid lines.\n    nticks: Specifies the maximum number of ticks for the particular axis. The actual number of ticks will be chosen automatically to be less than or equal to `nticks`. Has an effect only if `tickmode` is set to *auto*.\n    range: Sets the range of this axis. If the axis `type` is *log*, then you must take the log of your desired range (e.g. to set the range from 1 to 100, set the range from 0 to 2). If the axis `type` is *date*, it should be date strings, like date data, though Date objects and unix milliseconds will be accepted and converted to strings. If the axis `type` is *category*, it should be numbers, using the scale where each category is assigned a serial number from zero in the order it appears.\n    rangemode: If *normal*, the range is computed in relation to the extrema of the input data. If *tozero*, the range extends to 0, regardless of the input data If *nonnegative*, the range is non-negative, regardless of the input data.\n    separatethousands: If \"true\", even 4-digit integers are separated\n    showexponent: If *all*, all exponents are shown besides their significands. If *first*, only the exponent of the first tick is shown. If *last*, only the exponent of the last tick is shown. If *none*, no exponents appear.\n    showgrid: Determines whether or not grid lines are drawn. If *true*, the grid lines are drawn at every tick mark.\n    showline: Determines whether or not a line bounding this axis is drawn.\n    showticklabels: Determines whether axis labels are drawn on the low side, the high side, both, or neither side of the axis.\n    showtickprefix: If *all*, all tick labels are displayed with a prefix. If *first*, only the first tick is displayed with a prefix. If *last*, only the last tick is displayed with a suffix. If *none*, tick prefixes are hidden.\n    showticksuffix: Same as `showtickprefix` but for tick suffixes.\n    startline: Determines whether or not a line is drawn at along the starting value of this axis. If *true*, the start line is drawn on top of the grid lines.\n    startlinecolor: Sets the line color of the start line.\n    startlinewidth: Sets the width (in px) of the start line.\n    tick0: The starting index of grid lines along the axis\n    tickangle: Sets the angle of the tick labels with respect to the horizontal. For example, a `tickangle` of -90 draws the tick labels vertically.\n    tickfont: Sets the tick font.\n    tickformat: Sets the tick label formatting rule using d3 formatting mini-languages which are very similar to those in Python. For numbers, see: https://github.com/d3/d3-format/tree/v1.4.5#d3-format. And for dates see: https://github.com/d3/d3-time-format/tree/v2.2.3#locale_format. We add two items to d3's date formatter: *%h* for half of the year as a decimal number as well as *%{n}f* for fractional seconds with n digits. For example, *2016-10-13 09:15:23.456* with tickformat *%H~%M~%S.%2f* would display *09~15~23.46*\n    tickprefix: Sets a tick label prefix.\n    ticksuffix: Sets a tick label suffix.\n    ticktext: Sets the text displayed at the ticks position via `tickvals`. Only has an effect if `tickmode` is set to *array*. Used with `tickvals`.\n    tickvals: Sets the values at which ticks on this axis appear. Only has an effect if `tickmode` is set to *array*. Used with `ticktext`.\n    type: Sets the axis type. By default, plotly attempts to determined the axis type by looking into the data of the traces that referenced the axis in question."
        ...

class Baxis(_PlotlyObject):
    "Create a new 'Baxis' object"
    arraydtick: int | Any
    "The stride between grid lines along the axis"
    arraytick0: int | Any
    "The starting index of grid lines along the axis"
    autorange: Any
    "Determines whether or not the range of this axis is computed in relation to the input data. See `rangemode` for more info. If `range` is provided, then `autorange` is set to *false*."
    autotypenumbers: Any
    "Using *strict* a numeric string in trace data is not converted to a number. Using *convert types* a numeric string in trace data may be treated as a number during automatic axis `type` detection. Defaults to layout.autotypenumbers."
    categoryarray: Any
    "Sets the order in which categories on this axis appear. Only has an effect if `categoryorder` is set to *array*. Used with `categoryorder`."
    categoryorder: Any
    "Specifies the ordering logic for the case of categorical variables. By default, plotly uses *trace*, which specifies the order that is present in the data supplied. Set `categoryorder` to *category ascending* or *category descending* if order should be determined by the alphanumerical order of the category names. Set `categoryorder` to *array* to derive the ordering from the attribute `categoryarray`. If a category is not found in the `categoryarray` array, the sorting behavior for that attribute will be identical to the *trace* mode. The unspecified categories will follow the categories in `categoryarray`."
    cheatertype: Any
    color: Any
    "Sets default for all colors associated with this axis all at once: line, font, tick, and grid colors. Grid color is lightened by blending this with the plot background Individual pieces can override this."
    dtick: float | Any
    "The stride between grid lines along the axis"
    endline: bool | Any
    "Determines whether or not a line is drawn at along the final value of this axis. If *true*, the end line is drawn on top of the grid lines."
    endlinecolor: Any
    "Sets the line color of the end line."
    endlinewidth: float | Any
    "Sets the width (in px) of the end line."
    exponentformat: Any
    "Determines a formatting rule for the tick exponents. For example, consider the number 1,000,000,000. If *none*, it appears as 1,000,000,000. If *e*, 1e+9. If *E*, 1E+9. If *power*, 1x10^9 (with 9 in a super script). If *SI*, 1G. If *B*, 1B."
    fixedrange: bool | Any
    "Determines whether or not this axis is zoom-able. If true, then zoom is disabled."
    gridcolor: Any
    "Sets the axis line color."
    griddash: str | Any
    "Sets the dash style of lines. Set to a dash type string (*solid*, *dot*, *dash*, *longdash*, *dashdot*, or *longdashdot*) or a dash length list in px (eg *5px,10px,2px,2px*)."
    gridwidth: float | Any
    "Sets the width (in px) of the axis line."
    labelalias: Any
    "Replacement text for specific tick or hover labels. For example using {US: 'USA', CA: 'Canada'} changes US to USA and CA to Canada. The labels we would have shown must match the keys exactly, after adding any tickprefix or ticksuffix. For negative numbers the minus sign symbol used (U+2212) is wider than the regular ascii dash. That means you need to use −1 instead of -1. labelalias can be used with any axis type, and both keys (if needed) and values (if desired) can include html-like tags or MathJax."
    labelpadding: int | Any
    "Extra padding between label and the axis"
    labelprefix: str | Any
    "Sets a axis label prefix."
    labelsuffix: str | Any
    "Sets a axis label suffix."
    linecolor: Any
    "Sets the axis line color."
    linewidth: float | Any
    "Sets the width (in px) of the axis line."
    minexponent: float | Any
    "Hide SI prefix for 10^n if |n| is below this number"
    minorgridcolor: Any
    "Sets the color of the grid lines."
    minorgridcount: int | Any
    "Sets the number of minor grid ticks per major grid tick"
    minorgriddash: str | Any
    "Sets the dash style of lines. Set to a dash type string (*solid*, *dot*, *dash*, *longdash*, *dashdot*, or *longdashdot*) or a dash length list in px (eg *5px,10px,2px,2px*)."
    minorgridwidth: float | Any
    "Sets the width (in px) of the grid lines."
    nticks: int | Any
    "Specifies the maximum number of ticks for the particular axis. The actual number of ticks will be chosen automatically to be less than or equal to `nticks`. Has an effect only if `tickmode` is set to *auto*."
    range: Any
    "Sets the range of this axis. If the axis `type` is *log*, then you must take the log of your desired range (e.g. to set the range from 1 to 100, set the range from 0 to 2). If the axis `type` is *date*, it should be date strings, like date data, though Date objects and unix milliseconds will be accepted and converted to strings. If the axis `type` is *category*, it should be numbers, using the scale where each category is assigned a serial number from zero in the order it appears."
    rangemode: Any
    "If *normal*, the range is computed in relation to the extrema of the input data. If *tozero*, the range extends to 0, regardless of the input data If *nonnegative*, the range is non-negative, regardless of the input data."
    separatethousands: bool | Any
    "If \"true\", even 4-digit integers are separated"
    showexponent: Any
    "If *all*, all exponents are shown besides their significands. If *first*, only the exponent of the first tick is shown. If *last*, only the exponent of the last tick is shown. If *none*, no exponents appear."
    showgrid: bool | Any
    "Determines whether or not grid lines are drawn. If *true*, the grid lines are drawn at every tick mark."
    showline: bool | Any
    "Determines whether or not a line bounding this axis is drawn."
    showticklabels: Any
    "Determines whether axis labels are drawn on the low side, the high side, both, or neither side of the axis."
    showtickprefix: Any
    "If *all*, all tick labels are displayed with a prefix. If *first*, only the first tick is displayed with a prefix. If *last*, only the last tick is displayed with a suffix. If *none*, tick prefixes are hidden."
    showticksuffix: Any
    "Same as `showtickprefix` but for tick suffixes."
    smoothing: float | Any
    startline: bool | Any
    "Determines whether or not a line is drawn at along the starting value of this axis. If *true*, the start line is drawn on top of the grid lines."
    startlinecolor: Any
    "Sets the line color of the start line."
    startlinewidth: float | Any
    "Sets the width (in px) of the start line."
    tick0: float | Any
    "The starting index of grid lines along the axis"
    tickangle: Any
    "Sets the angle of the tick labels with respect to the horizontal. For example, a `tickangle` of -90 draws the tick labels vertically."
    @property
    def tickfont(self) -> _plotly_graph_objs_carpet_baxis.Tickfont | Any:
        "Sets the tick font."
        ...
    @tickfont.setter
    def tickfont(self, value: Any) -> None: ...
    tickformat: str | Any
    "Sets the tick label formatting rule using d3 formatting mini-languages which are very similar to those in Python. For numbers, see: https://github.com/d3/d3-format/tree/v1.4.5#d3-format. And for dates see: https://github.com/d3/d3-time-format/tree/v2.2.3#locale_format. We add two items to d3's date formatter: *%h* for half of the year as a decimal number as well as *%{n}f* for fractional seconds with n digits. For example, *2016-10-13 09:15:23.456* with tickformat *%H~%M~%S.%2f* would display *09~15~23.46*"
    @property
    def tickformatstop(self) -> _plotly_graph_objs_carpet_baxis.Tickformatstop | Any:
        ...
    @tickformatstop.setter
    def tickformatstop(self, value: Any) -> None: ...
    tickmode: Any
    tickprefix: str | Any
    "Sets a tick label prefix."
    ticksuffix: str | Any
    "Sets a tick label suffix."
    ticktext: Any
    "Sets the text displayed at the ticks position via `tickvals`. Only has an effect if `tickmode` is set to *array*. Used with `tickvals`."
    tickvals: Any
    "Sets the values at which ticks on this axis appear. Only has an effect if `tickmode` is set to *array*. Used with `ticktext`."
    @property
    def title(self) -> _plotly_graph_objs_carpet_baxis.Title | Any:
        ...
    @title.setter
    def title(self, value: Any) -> None: ...
    type: Any
    "Sets the axis type. By default, plotly attempts to determined the axis type by looking into the data of the traces that referenced the axis in question."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        arraydtick: Any = ...,
        arraytick0: Any = ...,
        autorange: Any = ...,
        autotypenumbers: Any = ...,
        categoryarray: Any = ...,
        categoryorder: Any = ...,
        cheatertype: Any = ...,
        color: Any = ...,
        dtick: Any = ...,
        endline: Any = ...,
        endlinecolor: Any = ...,
        endlinewidth: Any = ...,
        exponentformat: Any = ...,
        fixedrange: Any = ...,
        gridcolor: Any = ...,
        griddash: Any = ...,
        gridwidth: Any = ...,
        labelalias: Any = ...,
        labelpadding: Any = ...,
        labelprefix: Any = ...,
        labelsuffix: Any = ...,
        linecolor: Any = ...,
        linewidth: Any = ...,
        minexponent: Any = ...,
        minorgridcolor: Any = ...,
        minorgridcount: Any = ...,
        minorgriddash: Any = ...,
        minorgridwidth: Any = ...,
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
        smoothing: Any = ...,
        startline: Any = ...,
        startlinecolor: Any = ...,
        startlinewidth: Any = ...,
        tick0: Any = ...,
        tickangle: Any = ...,
        tickfont: Any = ...,
        tickformat: Any = ...,
        tickformatstop: Any = ...,
        tickmode: Any = ...,
        tickprefix: Any = ...,
        ticksuffix: Any = ...,
        ticktext: Any = ...,
        tickvals: Any = ...,
        title: Any = ...,
        type: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Baxis' object\n\nArgs:\n    arraydtick: The stride between grid lines along the axis\n    arraytick0: The starting index of grid lines along the axis\n    autorange: Determines whether or not the range of this axis is computed in relation to the input data. See `rangemode` for more info. If `range` is provided, then `autorange` is set to *false*.\n    autotypenumbers: Using *strict* a numeric string in trace data is not converted to a number. Using *convert types* a numeric string in trace data may be treated as a number during automatic axis `type` detection. Defaults to layout.autotypenumbers.\n    categoryarray: Sets the order in which categories on this axis appear. Only has an effect if `categoryorder` is set to *array*. Used with `categoryorder`.\n    categoryorder: Specifies the ordering logic for the case of categorical variables. By default, plotly uses *trace*, which specifies the order that is present in the data supplied. Set `categoryorder` to *category ascending* or *category descending* if order should be determined by the alphanumerical order of the category names. Set `categoryorder` to *array* to derive the ordering from the attribute `categoryarray`. If a category is not found in the `categoryarray` array, the sorting behavior for that attribute will be identical to the *trace* mode. The unspecified categories will follow the categories in `categoryarray`.\n    color: Sets default for all colors associated with this axis all at once: line, font, tick, and grid colors. Grid color is lightened by blending this with the plot background Individual pieces can override this.\n    dtick: The stride between grid lines along the axis\n    endline: Determines whether or not a line is drawn at along the final value of this axis. If *true*, the end line is drawn on top of the grid lines.\n    endlinecolor: Sets the line color of the end line.\n    endlinewidth: Sets the width (in px) of the end line.\n    exponentformat: Determines a formatting rule for the tick exponents. For example, consider the number 1,000,000,000. If *none*, it appears as 1,000,000,000. If *e*, 1e+9. If *E*, 1E+9. If *power*, 1x10^9 (with 9 in a super script). If *SI*, 1G. If *B*, 1B.\n    fixedrange: Determines whether or not this axis is zoom-able. If true, then zoom is disabled.\n    gridcolor: Sets the axis line color.\n    griddash: Sets the dash style of lines. Set to a dash type string (*solid*, *dot*, *dash*, *longdash*, *dashdot*, or *longdashdot*) or a dash length list in px (eg *5px,10px,2px,2px*).\n    gridwidth: Sets the width (in px) of the axis line.\n    labelalias: Replacement text for specific tick or hover labels. For example using {US: 'USA', CA: 'Canada'} changes US to USA and CA to Canada. The labels we would have shown must match the keys exactly, after adding any tickprefix or ticksuffix. For negative numbers the minus sign symbol used (U+2212) is wider than the regular ascii dash. That means you need to use −1 instead of -1. labelalias can be used with any axis type, and both keys (if needed) and values (if desired) can include html-like tags or MathJax.\n    labelpadding: Extra padding between label and the axis\n    labelprefix: Sets a axis label prefix.\n    labelsuffix: Sets a axis label suffix.\n    linecolor: Sets the axis line color.\n    linewidth: Sets the width (in px) of the axis line.\n    minexponent: Hide SI prefix for 10^n if |n| is below this number\n    minorgridcolor: Sets the color of the grid lines.\n    minorgridcount: Sets the number of minor grid ticks per major grid tick\n    minorgriddash: Sets the dash style of lines. Set to a dash type string (*solid*, *dot*, *dash*, *longdash*, *dashdot*, or *longdashdot*) or a dash length list in px (eg *5px,10px,2px,2px*).\n    minorgridwidth: Sets the width (in px) of the grid lines.\n    nticks: Specifies the maximum number of ticks for the particular axis. The actual number of ticks will be chosen automatically to be less than or equal to `nticks`. Has an effect only if `tickmode` is set to *auto*.\n    range: Sets the range of this axis. If the axis `type` is *log*, then you must take the log of your desired range (e.g. to set the range from 1 to 100, set the range from 0 to 2). If the axis `type` is *date*, it should be date strings, like date data, though Date objects and unix milliseconds will be accepted and converted to strings. If the axis `type` is *category*, it should be numbers, using the scale where each category is assigned a serial number from zero in the order it appears.\n    rangemode: If *normal*, the range is computed in relation to the extrema of the input data. If *tozero*, the range extends to 0, regardless of the input data If *nonnegative*, the range is non-negative, regardless of the input data.\n    separatethousands: If \"true\", even 4-digit integers are separated\n    showexponent: If *all*, all exponents are shown besides their significands. If *first*, only the exponent of the first tick is shown. If *last*, only the exponent of the last tick is shown. If *none*, no exponents appear.\n    showgrid: Determines whether or not grid lines are drawn. If *true*, the grid lines are drawn at every tick mark.\n    showline: Determines whether or not a line bounding this axis is drawn.\n    showticklabels: Determines whether axis labels are drawn on the low side, the high side, both, or neither side of the axis.\n    showtickprefix: If *all*, all tick labels are displayed with a prefix. If *first*, only the first tick is displayed with a prefix. If *last*, only the last tick is displayed with a suffix. If *none*, tick prefixes are hidden.\n    showticksuffix: Same as `showtickprefix` but for tick suffixes.\n    startline: Determines whether or not a line is drawn at along the starting value of this axis. If *true*, the start line is drawn on top of the grid lines.\n    startlinecolor: Sets the line color of the start line.\n    startlinewidth: Sets the width (in px) of the start line.\n    tick0: The starting index of grid lines along the axis\n    tickangle: Sets the angle of the tick labels with respect to the horizontal. For example, a `tickangle` of -90 draws the tick labels vertically.\n    tickfont: Sets the tick font.\n    tickformat: Sets the tick label formatting rule using d3 formatting mini-languages which are very similar to those in Python. For numbers, see: https://github.com/d3/d3-format/tree/v1.4.5#d3-format. And for dates see: https://github.com/d3/d3-time-format/tree/v2.2.3#locale_format. We add two items to d3's date formatter: *%h* for half of the year as a decimal number as well as *%{n}f* for fractional seconds with n digits. For example, *2016-10-13 09:15:23.456* with tickformat *%H~%M~%S.%2f* would display *09~15~23.46*\n    tickprefix: Sets a tick label prefix.\n    ticksuffix: Sets a tick label suffix.\n    ticktext: Sets the text displayed at the ticks position via `tickvals`. Only has an effect if `tickmode` is set to *array*. Used with `tickvals`.\n    tickvals: Sets the values at which ticks on this axis appear. Only has an effect if `tickmode` is set to *array*. Used with `ticktext`.\n    type: Sets the axis type. By default, plotly attempts to determined the axis type by looking into the data of the traces that referenced the axis in question."
        ...

class Font(_PlotlyObject):
    "Create a new 'Font' object"
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
        "Create a new 'Font' object\n\nArgs:\n    family: HTML font family - the typeface that will be applied by the web browser. The web browser can only apply a font if it is available on the system where it runs. Provide multiple font families, separated by commas, to indicate the order in which to apply fonts if they aren't available.\n    lineposition: Sets the kind of decoration line(s) with text, such as an *under*, *over* or *through* as well as combinations e.g. *under+over*, etc.\n    shadow: Sets the shape and color of the shadow behind text. *auto* places minimal shadow and applies contrast text font color. See https://developer.mozilla.org/en-US/docs/Web/CSS/text-shadow for additional options.\n    style: Sets whether a font should be styled with a normal or italic face from its family.\n    textcase: Sets capitalization of text. It can be used to make text appear in all-uppercase or all-lowercase, or with each word capitalized.\n    variant: Sets the variant of the font.\n    weight: Sets the weight (or boldness) of the font."
        ...

class Legendgrouptitle(_PlotlyObject):
    "Create a new 'Legendgrouptitle' object"
    @property
    def font(self) -> _plotly_graph_objs_carpet_legendgrouptitle.Font | Any:
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
