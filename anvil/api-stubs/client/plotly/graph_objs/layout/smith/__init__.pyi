# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the Plotly catalogue generator in doc/anvil-api-stubs/plotly-stubs.mjs instead, then run:
#   pnpm -F docs build
#
from plotly._base import _PlotlyObject
from typing import Any, Mapping
import plotly.graph_objs.layout.smith.imaginaryaxis as _plotly_graph_objs_layout_smith_imaginaryaxis
import plotly.graph_objs.layout.smith.imaginaryaxis as imaginaryaxis
import plotly.graph_objs.layout.smith.realaxis as _plotly_graph_objs_layout_smith_realaxis
import plotly.graph_objs.layout.smith.realaxis as realaxis

class Domain(_PlotlyObject):
    "Create a new 'Domain' object"
    column: int | Any
    "If there is a layout grid, use the domain for this column in the grid for this smith subplot."
    row: int | Any
    "If there is a layout grid, use the domain for this row in the grid for this smith subplot."
    x: Any
    "Sets the horizontal domain of this smith subplot (in plot fraction)."
    y: Any
    "Sets the vertical domain of this smith subplot (in plot fraction)."
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
        "Create a new 'Domain' object\n\nArgs:\n    column: If there is a layout grid, use the domain for this column in the grid for this smith subplot.\n    row: If there is a layout grid, use the domain for this row in the grid for this smith subplot.\n    x: Sets the horizontal domain of this smith subplot (in plot fraction).\n    y: Sets the vertical domain of this smith subplot (in plot fraction)."
        ...

class Imaginaryaxis(_PlotlyObject):
    "Create a new 'Imaginaryaxis' object"
    color: Any
    "Sets default for all colors associated with this axis all at once: line, font, tick, and grid colors. Grid color is lightened by blending this with the plot background Individual pieces can override this."
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
    tickcolor: Any
    "Sets the tick color."
    @property
    def tickfont(self) -> _plotly_graph_objs_layout_smith_imaginaryaxis.Tickfont | Any:
        "Sets the tick font."
        ...
    @tickfont.setter
    def tickfont(self, value: Any) -> None: ...
    tickformat: str | Any
    "Sets the tick label formatting rule using d3 formatting mini-languages which are very similar to those in Python. For numbers, see: https://github.com/d3/d3-format/tree/v1.4.5#d3-format. And for dates see: https://github.com/d3/d3-time-format/tree/v2.2.3#locale_format. We add two items to d3's date formatter: *%h* for half of the year as a decimal number as well as *%{n}f* for fractional seconds with n digits. For example, *2016-10-13 09:15:23.456* with tickformat *%H~%M~%S.%2f* would display *09~15~23.46*"
    ticklen: float | Any
    "Sets the tick length (in px)."
    tickprefix: str | Any
    "Sets a tick label prefix."
    ticks: Any
    "Determines whether ticks are drawn or not. If **, this axis' ticks are not drawn. If *outside* (*inside*), this axis' are drawn outside (inside) the axis lines."
    ticksuffix: str | Any
    "Sets a tick label suffix."
    tickvals: Any
    "Sets the values at which ticks on this axis appear. Defaults to `realaxis.tickvals` plus the same as negatives and zero."
    tickwidth: float | Any
    "Sets the tick width (in px)."
    visible: bool | Any
    "A single toggle to hide the axis while preserving interaction like dragging. Default is true when a cheater plot is present on the axis, otherwise false"
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        color: Any = ...,
        gridcolor: Any = ...,
        griddash: Any = ...,
        gridwidth: Any = ...,
        hoverformat: Any = ...,
        labelalias: Any = ...,
        layer: Any = ...,
        linecolor: Any = ...,
        linewidth: Any = ...,
        showgrid: Any = ...,
        showline: Any = ...,
        showticklabels: Any = ...,
        showtickprefix: Any = ...,
        showticksuffix: Any = ...,
        tickcolor: Any = ...,
        tickfont: Any = ...,
        tickformat: Any = ...,
        ticklen: Any = ...,
        tickprefix: Any = ...,
        ticks: Any = ...,
        ticksuffix: Any = ...,
        tickvals: Any = ...,
        tickwidth: Any = ...,
        visible: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Imaginaryaxis' object\n\nArgs:\n    color: Sets default for all colors associated with this axis all at once: line, font, tick, and grid colors. Grid color is lightened by blending this with the plot background Individual pieces can override this.\n    gridcolor: Sets the color of the grid lines.\n    griddash: Sets the dash style of lines. Set to a dash type string (*solid*, *dot*, *dash*, *longdash*, *dashdot*, or *longdashdot*) or a dash length list in px (eg *5px,10px,2px,2px*).\n    gridwidth: Sets the width (in px) of the grid lines.\n    hoverformat: Sets the hover text formatting rule using d3 formatting mini-languages which are very similar to those in Python. For numbers, see: https://github.com/d3/d3-format/tree/v1.4.5#d3-format. And for dates see: https://github.com/d3/d3-time-format/tree/v2.2.3#locale_format. We add two items to d3's date formatter: *%h* for half of the year as a decimal number as well as *%{n}f* for fractional seconds with n digits. For example, *2016-10-13 09:15:23.456* with tickformat *%H~%M~%S.%2f* would display *09~15~23.46*\n    labelalias: Replacement text for specific tick or hover labels. For example using {US: 'USA', CA: 'Canada'} changes US to USA and CA to Canada. The labels we would have shown must match the keys exactly, after adding any tickprefix or ticksuffix. For negative numbers the minus sign symbol used (U+2212) is wider than the regular ascii dash. That means you need to use −1 instead of -1. labelalias can be used with any axis type, and both keys (if needed) and values (if desired) can include html-like tags or MathJax.\n    layer: Sets the layer on which this axis is displayed. If *above traces*, this axis is displayed above all the subplot's traces If *below traces*, this axis is displayed below all the subplot's traces, but above the grid lines. Useful when used together with scatter-like traces with `cliponaxis` set to *false* to show markers and/or text nodes above this axis.\n    linecolor: Sets the axis line color.\n    linewidth: Sets the width (in px) of the axis line.\n    showgrid: Determines whether or not grid lines are drawn. If *true*, the grid lines are drawn at every tick mark.\n    showline: Determines whether or not a line bounding this axis is drawn.\n    showticklabels: Determines whether or not the tick labels are drawn.\n    showtickprefix: If *all*, all tick labels are displayed with a prefix. If *first*, only the first tick is displayed with a prefix. If *last*, only the last tick is displayed with a suffix. If *none*, tick prefixes are hidden.\n    showticksuffix: Same as `showtickprefix` but for tick suffixes.\n    tickcolor: Sets the tick color.\n    tickfont: Sets the tick font.\n    tickformat: Sets the tick label formatting rule using d3 formatting mini-languages which are very similar to those in Python. For numbers, see: https://github.com/d3/d3-format/tree/v1.4.5#d3-format. And for dates see: https://github.com/d3/d3-time-format/tree/v2.2.3#locale_format. We add two items to d3's date formatter: *%h* for half of the year as a decimal number as well as *%{n}f* for fractional seconds with n digits. For example, *2016-10-13 09:15:23.456* with tickformat *%H~%M~%S.%2f* would display *09~15~23.46*\n    ticklen: Sets the tick length (in px).\n    tickprefix: Sets a tick label prefix.\n    ticks: Determines whether ticks are drawn or not. If **, this axis' ticks are not drawn. If *outside* (*inside*), this axis' are drawn outside (inside) the axis lines.\n    ticksuffix: Sets a tick label suffix.\n    tickvals: Sets the values at which ticks on this axis appear. Defaults to `realaxis.tickvals` plus the same as negatives and zero.\n    tickwidth: Sets the tick width (in px).\n    visible: A single toggle to hide the axis while preserving interaction like dragging. Default is true when a cheater plot is present on the axis, otherwise false"
        ...

class Realaxis(_PlotlyObject):
    "Create a new 'Realaxis' object"
    color: Any
    "Sets default for all colors associated with this axis all at once: line, font, tick, and grid colors. Grid color is lightened by blending this with the plot background Individual pieces can override this."
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
    "Determines on which side of real axis line the tick and tick labels appear."
    tickangle: Any
    "Sets the angle of the tick labels with respect to the horizontal. For example, a `tickangle` of -90 draws the tick labels vertically."
    tickcolor: Any
    "Sets the tick color."
    @property
    def tickfont(self) -> _plotly_graph_objs_layout_smith_realaxis.Tickfont | Any:
        "Sets the tick font."
        ...
    @tickfont.setter
    def tickfont(self, value: Any) -> None: ...
    tickformat: str | Any
    "Sets the tick label formatting rule using d3 formatting mini-languages which are very similar to those in Python. For numbers, see: https://github.com/d3/d3-format/tree/v1.4.5#d3-format. And for dates see: https://github.com/d3/d3-time-format/tree/v2.2.3#locale_format. We add two items to d3's date formatter: *%h* for half of the year as a decimal number as well as *%{n}f* for fractional seconds with n digits. For example, *2016-10-13 09:15:23.456* with tickformat *%H~%M~%S.%2f* would display *09~15~23.46*"
    ticklen: float | Any
    "Sets the tick length (in px)."
    tickprefix: str | Any
    "Sets a tick label prefix."
    ticks: Any
    "Determines whether ticks are drawn or not. If **, this axis' ticks are not drawn. If *top* (*bottom*), this axis' are drawn above (below) the axis line."
    ticksuffix: str | Any
    "Sets a tick label suffix."
    tickvals: Any
    "Sets the values at which ticks on this axis appear."
    tickwidth: float | Any
    "Sets the tick width (in px)."
    visible: bool | Any
    "A single toggle to hide the axis while preserving interaction like dragging. Default is true when a cheater plot is present on the axis, otherwise false"
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        color: Any = ...,
        gridcolor: Any = ...,
        griddash: Any = ...,
        gridwidth: Any = ...,
        hoverformat: Any = ...,
        labelalias: Any = ...,
        layer: Any = ...,
        linecolor: Any = ...,
        linewidth: Any = ...,
        showgrid: Any = ...,
        showline: Any = ...,
        showticklabels: Any = ...,
        showtickprefix: Any = ...,
        showticksuffix: Any = ...,
        side: Any = ...,
        tickangle: Any = ...,
        tickcolor: Any = ...,
        tickfont: Any = ...,
        tickformat: Any = ...,
        ticklen: Any = ...,
        tickprefix: Any = ...,
        ticks: Any = ...,
        ticksuffix: Any = ...,
        tickvals: Any = ...,
        tickwidth: Any = ...,
        visible: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Realaxis' object\n\nArgs:\n    color: Sets default for all colors associated with this axis all at once: line, font, tick, and grid colors. Grid color is lightened by blending this with the plot background Individual pieces can override this.\n    gridcolor: Sets the color of the grid lines.\n    griddash: Sets the dash style of lines. Set to a dash type string (*solid*, *dot*, *dash*, *longdash*, *dashdot*, or *longdashdot*) or a dash length list in px (eg *5px,10px,2px,2px*).\n    gridwidth: Sets the width (in px) of the grid lines.\n    hoverformat: Sets the hover text formatting rule using d3 formatting mini-languages which are very similar to those in Python. For numbers, see: https://github.com/d3/d3-format/tree/v1.4.5#d3-format. And for dates see: https://github.com/d3/d3-time-format/tree/v2.2.3#locale_format. We add two items to d3's date formatter: *%h* for half of the year as a decimal number as well as *%{n}f* for fractional seconds with n digits. For example, *2016-10-13 09:15:23.456* with tickformat *%H~%M~%S.%2f* would display *09~15~23.46*\n    labelalias: Replacement text for specific tick or hover labels. For example using {US: 'USA', CA: 'Canada'} changes US to USA and CA to Canada. The labels we would have shown must match the keys exactly, after adding any tickprefix or ticksuffix. For negative numbers the minus sign symbol used (U+2212) is wider than the regular ascii dash. That means you need to use −1 instead of -1. labelalias can be used with any axis type, and both keys (if needed) and values (if desired) can include html-like tags or MathJax.\n    layer: Sets the layer on which this axis is displayed. If *above traces*, this axis is displayed above all the subplot's traces If *below traces*, this axis is displayed below all the subplot's traces, but above the grid lines. Useful when used together with scatter-like traces with `cliponaxis` set to *false* to show markers and/or text nodes above this axis.\n    linecolor: Sets the axis line color.\n    linewidth: Sets the width (in px) of the axis line.\n    showgrid: Determines whether or not grid lines are drawn. If *true*, the grid lines are drawn at every tick mark.\n    showline: Determines whether or not a line bounding this axis is drawn.\n    showticklabels: Determines whether or not the tick labels are drawn.\n    showtickprefix: If *all*, all tick labels are displayed with a prefix. If *first*, only the first tick is displayed with a prefix. If *last*, only the last tick is displayed with a suffix. If *none*, tick prefixes are hidden.\n    showticksuffix: Same as `showtickprefix` but for tick suffixes.\n    side: Determines on which side of real axis line the tick and tick labels appear.\n    tickangle: Sets the angle of the tick labels with respect to the horizontal. For example, a `tickangle` of -90 draws the tick labels vertically.\n    tickcolor: Sets the tick color.\n    tickfont: Sets the tick font.\n    tickformat: Sets the tick label formatting rule using d3 formatting mini-languages which are very similar to those in Python. For numbers, see: https://github.com/d3/d3-format/tree/v1.4.5#d3-format. And for dates see: https://github.com/d3/d3-time-format/tree/v2.2.3#locale_format. We add two items to d3's date formatter: *%h* for half of the year as a decimal number as well as *%{n}f* for fractional seconds with n digits. For example, *2016-10-13 09:15:23.456* with tickformat *%H~%M~%S.%2f* would display *09~15~23.46*\n    ticklen: Sets the tick length (in px).\n    tickprefix: Sets a tick label prefix.\n    ticks: Determines whether ticks are drawn or not. If **, this axis' ticks are not drawn. If *top* (*bottom*), this axis' are drawn above (below) the axis line.\n    ticksuffix: Sets a tick label suffix.\n    tickvals: Sets the values at which ticks on this axis appear.\n    tickwidth: Sets the tick width (in px).\n    visible: A single toggle to hide the axis while preserving interaction like dragging. Default is true when a cheater plot is present on the axis, otherwise false"
        ...
