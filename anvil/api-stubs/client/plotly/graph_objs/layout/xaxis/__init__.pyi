# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the Plotly catalogue generator in doc/anvil-api-stubs/plotly-stubs.mjs instead, then run:
#   pnpm -F docs build
#
from plotly._base import _PlotlyObject
from typing import Any, Mapping
import plotly.graph_objs.layout.xaxis.rangeselector as _plotly_graph_objs_layout_xaxis_rangeselector
import plotly.graph_objs.layout.xaxis.rangeselector as rangeselector
import plotly.graph_objs.layout.xaxis.rangeslider as _plotly_graph_objs_layout_xaxis_rangeslider
import plotly.graph_objs.layout.xaxis.rangeslider as rangeslider
import plotly.graph_objs.layout.xaxis.title as _plotly_graph_objs_layout_xaxis_title
import plotly.graph_objs.layout.xaxis.title as title

class Autorangeoptions(_PlotlyObject):
    "Create a new 'Autorangeoptions' object"
    clipmax: Any
    "Clip autorange maximum if it goes beyond this value. Has no effect when `autorangeoptions.maxallowed` is provided."
    clipmin: Any
    "Clip autorange minimum if it goes beyond this value. Has no effect when `autorangeoptions.minallowed` is provided."
    include: Any
    "Extends the autorange to include this value or array of values, even when they fall outside the data range. Has no effect on endpoints set by `autorangeoptions.minallowed` or `autorangeoptions.maxallowed`. Subject to `autorangeoptions.clipmin` and `autorangeoptions.clipmax`."
    maxallowed: Any
    "Use this value exactly as autorange maximum."
    minallowed: Any
    "Use this value exactly as autorange minimum."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        clipmax: Any = ...,
        clipmin: Any = ...,
        include: Any = ...,
        maxallowed: Any = ...,
        minallowed: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Autorangeoptions' object\n\nArgs:\n    clipmax: Clip autorange maximum if it goes beyond this value. Has no effect when `autorangeoptions.maxallowed` is provided.\n    clipmin: Clip autorange minimum if it goes beyond this value. Has no effect when `autorangeoptions.minallowed` is provided.\n    include: Extends the autorange to include this value or array of values, even when they fall outside the data range. Has no effect on endpoints set by `autorangeoptions.minallowed` or `autorangeoptions.maxallowed`. Subject to `autorangeoptions.clipmin` and `autorangeoptions.clipmax`.\n    maxallowed: Use this value exactly as autorange maximum.\n    minallowed: Use this value exactly as autorange minimum."
        ...

class Minor(_PlotlyObject):
    "Create a new 'Minor' object"
    dtick: Any
    "Sets the step in-between ticks on this axis. Use with `tick0`. Must be a positive number, or special strings available to *log* and *date* axes. If the axis `type` is *log*, then ticks are set every 10^(n*dtick) where n is the tick number. For example, to set a tick mark at 1, 10, 100, 1000, ... set dtick to 1. To set tick marks at 1, 100, 10000, ... set dtick to 2. To set tick marks at 1, 5, 25, 125, 625, 3125, ... set dtick to log_10(5), or 0.69897000433. *log* has several special values; *L<f>*, where `f` is a positive number, gives ticks linearly spaced in value (but not position). For example `tick0` = 0.1, `dtick` = *L0.5* will put ticks at 0.1, 0.6, 1.1, 1.6 etc. To show powers of 10 plus small digits between, use *D1* (all digits) or *D2* (only 2 and 5). `tick0` is ignored for *D1* and *D2*. If the axis `type` is *date*, then you must convert the time to milliseconds. For example, to set the interval between ticks to one day, set `dtick` to 86400000.0. *date* also has special values *M<n>* gives ticks spaced by a number of months. `n` must be a positive integer. To set ticks on the 15th of every third month, set `tick0` to *2000-01-15* and `dtick` to *M3*. To set ticks every 4 years, set `dtick` to *M48*"
    gridcolor: Any
    "Sets the color of the grid lines."
    griddash: str | Any
    "Sets the dash style of lines. Set to a dash type string (*solid*, *dot*, *dash*, *longdash*, *dashdot*, or *longdashdot*) or a dash length list in px (eg *5px,10px,2px,2px*)."
    gridwidth: float | Any
    "Sets the width (in px) of the grid lines."
    nticks: int | Any
    "Specifies the maximum number of ticks for the particular axis. The actual number of ticks will be chosen automatically to be less than or equal to `nticks`. Has an effect only if `tickmode` is set to *auto*."
    showgrid: bool | Any
    "Determines whether or not grid lines are drawn. If *true*, the grid lines are drawn at every tick mark."
    tick0: Any
    "Sets the placement of the first tick on this axis. Use with `dtick`. If the axis `type` is *log*, then you must take the log of your starting tick (e.g. to set the starting tick to 100, set the `tick0` to 2) except when `dtick`=*L<f>* (see `dtick` for more info). If the axis `type` is *date*, it should be a date string, like date data. If the axis `type` is *category*, it should be a number, using the scale where each category is assigned a serial number from zero in the order it appears."
    tickcolor: Any
    "Sets the tick color."
    ticklen: float | Any
    "Sets the tick length (in px)."
    tickmode: Any
    "Sets the tick mode for this axis. If *auto*, the number of ticks is set via `nticks`. If *linear*, the placement of the ticks is determined by a starting position `tick0` and a tick step `dtick` (*linear* is the default value if `tick0` and `dtick` are provided). If *array*, the placement of the ticks is set via `tickvals` and the tick text is `ticktext`. (*array* is the default value if `tickvals` is provided)."
    ticks: Any
    "Determines whether ticks are drawn or not. If **, this axis' ticks are not drawn. If *outside* (*inside*), this axis' are drawn outside (inside) the axis lines."
    tickvals: Any
    "Sets the values at which ticks on this axis appear. Only has an effect if `tickmode` is set to *array*. Used with `ticktext`."
    tickwidth: float | Any
    "Sets the tick width (in px)."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        dtick: Any = ...,
        gridcolor: Any = ...,
        griddash: Any = ...,
        gridwidth: Any = ...,
        nticks: Any = ...,
        showgrid: Any = ...,
        tick0: Any = ...,
        tickcolor: Any = ...,
        ticklen: Any = ...,
        tickmode: Any = ...,
        ticks: Any = ...,
        tickvals: Any = ...,
        tickwidth: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Minor' object\n\nArgs:\n    dtick: Sets the step in-between ticks on this axis. Use with `tick0`. Must be a positive number, or special strings available to *log* and *date* axes. If the axis `type` is *log*, then ticks are set every 10^(n*dtick) where n is the tick number. For example, to set a tick mark at 1, 10, 100, 1000, ... set dtick to 1. To set tick marks at 1, 100, 10000, ... set dtick to 2. To set tick marks at 1, 5, 25, 125, 625, 3125, ... set dtick to log_10(5), or 0.69897000433. *log* has several special values; *L<f>*, where `f` is a positive number, gives ticks linearly spaced in value (but not position). For example `tick0` = 0.1, `dtick` = *L0.5* will put ticks at 0.1, 0.6, 1.1, 1.6 etc. To show powers of 10 plus small digits between, use *D1* (all digits) or *D2* (only 2 and 5). `tick0` is ignored for *D1* and *D2*. If the axis `type` is *date*, then you must convert the time to milliseconds. For example, to set the interval between ticks to one day, set `dtick` to 86400000.0. *date* also has special values *M<n>* gives ticks spaced by a number of months. `n` must be a positive integer. To set ticks on the 15th of every third month, set `tick0` to *2000-01-15* and `dtick` to *M3*. To set ticks every 4 years, set `dtick` to *M48*\n    gridcolor: Sets the color of the grid lines.\n    griddash: Sets the dash style of lines. Set to a dash type string (*solid*, *dot*, *dash*, *longdash*, *dashdot*, or *longdashdot*) or a dash length list in px (eg *5px,10px,2px,2px*).\n    gridwidth: Sets the width (in px) of the grid lines.\n    nticks: Specifies the maximum number of ticks for the particular axis. The actual number of ticks will be chosen automatically to be less than or equal to `nticks`. Has an effect only if `tickmode` is set to *auto*.\n    showgrid: Determines whether or not grid lines are drawn. If *true*, the grid lines are drawn at every tick mark.\n    tick0: Sets the placement of the first tick on this axis. Use with `dtick`. If the axis `type` is *log*, then you must take the log of your starting tick (e.g. to set the starting tick to 100, set the `tick0` to 2) except when `dtick`=*L<f>* (see `dtick` for more info). If the axis `type` is *date*, it should be a date string, like date data. If the axis `type` is *category*, it should be a number, using the scale where each category is assigned a serial number from zero in the order it appears.\n    tickcolor: Sets the tick color.\n    ticklen: Sets the tick length (in px).\n    tickmode: Sets the tick mode for this axis. If *auto*, the number of ticks is set via `nticks`. If *linear*, the placement of the ticks is determined by a starting position `tick0` and a tick step `dtick` (*linear* is the default value if `tick0` and `dtick` are provided). If *array*, the placement of the ticks is set via `tickvals` and the tick text is `ticktext`. (*array* is the default value if `tickvals` is provided).\n    ticks: Determines whether ticks are drawn or not. If **, this axis' ticks are not drawn. If *outside* (*inside*), this axis' are drawn outside (inside) the axis lines.\n    tickvals: Sets the values at which ticks on this axis appear. Only has an effect if `tickmode` is set to *array*. Used with `ticktext`.\n    tickwidth: Sets the tick width (in px)."
        ...

class Rangebreak(_PlotlyObject):
    "Create a new 'Rangebreak' object"
    bounds: Any
    "Sets the lower and upper bounds of this axis rangebreak. Can be used with `pattern`."
    dvalue: float | Any
    "Sets the size of each `values` item. The default is one day in milliseconds."
    enabled: bool | Any
    "Determines whether this axis rangebreak is enabled or disabled. Please note that `rangebreaks` only work for *date* axis type."
    name: str | Any
    "When used in a template, named items are created in the output figure in addition to any items the figure already has in this array. You can modify these items in the output figure by making your own item with `templateitemname` matching this `name` alongside your modifications (including `visible: false` or `enabled: false` to hide it). Has no effect outside of a template."
    pattern: Any
    "Determines a pattern on the time line that generates breaks. If *day of week* - days of the week in English e.g. 'Sunday' or `sun` (matching is case-insensitive and considers only the first three characters), as well as Sunday-based integers between 0 and 6. If *hour* - hour (24-hour clock) as decimal numbers between 0 and 24. for more info. Examples: - { pattern: 'day of week', bounds: [6, 1] }  or simply { bounds: ['sat', 'mon'] }   breaks from Saturday to Monday (i.e. skips the weekends). - { pattern: 'hour', bounds: [17, 8] }   breaks from 5pm to 8am (i.e. skips non-work hours)."
    templateitemname: str | Any
    "Used to refer to a named item in this array in the template. Named items from the template will be created even without a matching item in the input figure, but you can modify one by making an item with `templateitemname` matching its `name`, alongside your modifications (including `visible: false` or `enabled: false` to hide it). If there is no template or no matching item, this item will be hidden unless you explicitly show it with `visible: true`."
    values: Any
    "Sets the coordinate values corresponding to the rangebreaks. An alternative to `bounds`. Use `dvalue` to set the size of the values along the axis."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        bounds: Any = ...,
        dvalue: Any = ...,
        enabled: Any = ...,
        name: Any = ...,
        pattern: Any = ...,
        templateitemname: Any = ...,
        values: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Rangebreak' object\n\nArgs:\n    bounds: Sets the lower and upper bounds of this axis rangebreak. Can be used with `pattern`.\n    dvalue: Sets the size of each `values` item. The default is one day in milliseconds.\n    enabled: Determines whether this axis rangebreak is enabled or disabled. Please note that `rangebreaks` only work for *date* axis type.\n    name: When used in a template, named items are created in the output figure in addition to any items the figure already has in this array. You can modify these items in the output figure by making your own item with `templateitemname` matching this `name` alongside your modifications (including `visible: false` or `enabled: false` to hide it). Has no effect outside of a template.\n    pattern: Determines a pattern on the time line that generates breaks. If *day of week* - days of the week in English e.g. 'Sunday' or `sun` (matching is case-insensitive and considers only the first three characters), as well as Sunday-based integers between 0 and 6. If *hour* - hour (24-hour clock) as decimal numbers between 0 and 24. for more info. Examples: - { pattern: 'day of week', bounds: [6, 1] }  or simply { bounds: ['sat', 'mon'] }   breaks from Saturday to Monday (i.e. skips the weekends). - { pattern: 'hour', bounds: [17, 8] }   breaks from 5pm to 8am (i.e. skips non-work hours).\n    templateitemname: Used to refer to a named item in this array in the template. Named items from the template will be created even without a matching item in the input figure, but you can modify one by making an item with `templateitemname` matching its `name`, alongside your modifications (including `visible: false` or `enabled: false` to hide it). If there is no template or no matching item, this item will be hidden unless you explicitly show it with `visible: true`.\n    values: Sets the coordinate values corresponding to the rangebreaks. An alternative to `bounds`. Use `dvalue` to set the size of the values along the axis."
        ...

class Rangeselector(_PlotlyObject):
    "Create a new 'Rangeselector' object"
    activecolor: Any
    "Sets the background color of the active range selector button."
    bgcolor: Any
    "Sets the background color of the range selector buttons."
    bordercolor: Any
    "Sets the color of the border enclosing the range selector."
    borderwidth: float | Any
    "Sets the width (in px) of the border enclosing the range selector."
    @property
    def button(self) -> _plotly_graph_objs_layout_xaxis_rangeselector.Button | Any:
        "Sets the specifications for each buttons. By default, a range selector comes with no buttons."
        ...
    @button.setter
    def button(self, value: Any) -> None: ...
    @property
    def font(self) -> _plotly_graph_objs_layout_xaxis_rangeselector.Font | Any:
        "Sets the font of the range selector button text."
        ...
    @font.setter
    def font(self, value: Any) -> None: ...
    visible: bool | Any
    "Determines whether or not this range selector is visible. Note that range selectors are only available for x axes of `type` set to or auto-typed to *date*."
    x: float | Any
    "Sets the x position (in normalized coordinates) of the range selector."
    xanchor: Any
    "Sets the range selector's horizontal position anchor. This anchor binds the `x` position to the *left*, *center* or *right* of the range selector."
    y: float | Any
    "Sets the y position (in normalized coordinates) of the range selector."
    yanchor: Any
    "Sets the range selector's vertical position anchor This anchor binds the `y` position to the *top*, *middle* or *bottom* of the range selector."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        activecolor: Any = ...,
        bgcolor: Any = ...,
        bordercolor: Any = ...,
        borderwidth: Any = ...,
        button: Any = ...,
        font: Any = ...,
        visible: Any = ...,
        x: Any = ...,
        xanchor: Any = ...,
        y: Any = ...,
        yanchor: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Rangeselector' object\n\nArgs:\n    activecolor: Sets the background color of the active range selector button.\n    bgcolor: Sets the background color of the range selector buttons.\n    bordercolor: Sets the color of the border enclosing the range selector.\n    borderwidth: Sets the width (in px) of the border enclosing the range selector.\n    button: Sets the specifications for each buttons. By default, a range selector comes with no buttons.\n    font: Sets the font of the range selector button text.\n    visible: Determines whether or not this range selector is visible. Note that range selectors are only available for x axes of `type` set to or auto-typed to *date*.\n    x: Sets the x position (in normalized coordinates) of the range selector.\n    xanchor: Sets the range selector's horizontal position anchor. This anchor binds the `x` position to the *left*, *center* or *right* of the range selector.\n    y: Sets the y position (in normalized coordinates) of the range selector.\n    yanchor: Sets the range selector's vertical position anchor This anchor binds the `y` position to the *top*, *middle* or *bottom* of the range selector."
        ...

class Rangeslider(_PlotlyObject):
    "Create a new 'Rangeslider' object"
    autorange: bool | Any
    "Determines whether or not the range slider range is computed in relation to the input data. If `range` is provided, then `autorange` is set to *false*."
    bgcolor: Any
    "Sets the background color of the range slider."
    bordercolor: Any
    "Sets the border color of the range slider."
    borderwidth: int | Any
    "Sets the border width of the range slider."
    range: Any
    "Sets the range of the range slider. If not set, defaults to the full xaxis range. If the axis `type` is *log*, then you must take the log of your desired range. If the axis `type` is *date*, it should be date strings, like date data, though Date objects and unix milliseconds will be accepted and converted to strings. If the axis `type` is *category*, it should be numbers, using the scale where each category is assigned a serial number from zero in the order it appears."
    thickness: float | Any
    "The height of the range slider as a fraction of the total plot area height."
    visible: bool | Any
    "Determines whether or not the range slider will be visible. If visible, perpendicular axes will be set to `fixedrange`"
    @property
    def yaxis(self) -> _plotly_graph_objs_layout_xaxis_rangeslider.YAxis | Any:
        ...
    @yaxis.setter
    def yaxis(self, value: Any) -> None: ...
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        autorange: Any = ...,
        bgcolor: Any = ...,
        bordercolor: Any = ...,
        borderwidth: Any = ...,
        range: Any = ...,
        thickness: Any = ...,
        visible: Any = ...,
        yaxis: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Rangeslider' object\n\nArgs:\n    autorange: Determines whether or not the range slider range is computed in relation to the input data. If `range` is provided, then `autorange` is set to *false*.\n    bgcolor: Sets the background color of the range slider.\n    bordercolor: Sets the border color of the range slider.\n    borderwidth: Sets the border width of the range slider.\n    range: Sets the range of the range slider. If not set, defaults to the full xaxis range. If the axis `type` is *log*, then you must take the log of your desired range. If the axis `type` is *date*, it should be date strings, like date data, though Date objects and unix milliseconds will be accepted and converted to strings. If the axis `type` is *category*, it should be numbers, using the scale where each category is assigned a serial number from zero in the order it appears.\n    thickness: The height of the range slider as a fraction of the total plot area height.\n    visible: Determines whether or not the range slider will be visible. If visible, perpendicular axes will be set to `fixedrange`"
        ...

class Tickfont(_PlotlyObject):
    "Create a new 'Tickfont' object"
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
        "Create a new 'Tickfont' object\n\nArgs:\n    family: HTML font family - the typeface that will be applied by the web browser. The web browser can only apply a font if it is available on the system where it runs. Provide multiple font families, separated by commas, to indicate the order in which to apply fonts if they aren't available.\n    lineposition: Sets the kind of decoration line(s) with text, such as an *under*, *over* or *through* as well as combinations e.g. *under+over*, etc.\n    shadow: Sets the shape and color of the shadow behind text. *auto* places minimal shadow and applies contrast text font color. See https://developer.mozilla.org/en-US/docs/Web/CSS/text-shadow for additional options.\n    style: Sets whether a font should be styled with a normal or italic face from its family.\n    textcase: Sets capitalization of text. It can be used to make text appear in all-uppercase or all-lowercase, or with each word capitalized.\n    variant: Sets the variant of the font.\n    weight: Sets the weight (or boldness) of the font."
        ...

class Tickformatstop(_PlotlyObject):
    "Create a new 'Tickformatstop' object"
    dtickrange: Any
    "range [*min*, *max*], where *min*, *max* - dtick values which describe some zoom level, it is possible to omit *min* or *max* value by passing *null*"
    enabled: bool | Any
    "Determines whether or not this stop is used. If `false`, this stop is ignored even within its `dtickrange`."
    name: str | Any
    "When used in a template, named items are created in the output figure in addition to any items the figure already has in this array. You can modify these items in the output figure by making your own item with `templateitemname` matching this `name` alongside your modifications (including `visible: false` or `enabled: false` to hide it). Has no effect outside of a template."
    templateitemname: str | Any
    "Used to refer to a named item in this array in the template. Named items from the template will be created even without a matching item in the input figure, but you can modify one by making an item with `templateitemname` matching its `name`, alongside your modifications (including `visible: false` or `enabled: false` to hide it). If there is no template or no matching item, this item will be hidden unless you explicitly show it with `visible: true`."
    value: str | Any
    "string - dtickformat for described zoom level, the same as *tickformat*"
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        dtickrange: Any = ...,
        enabled: Any = ...,
        name: Any = ...,
        templateitemname: Any = ...,
        value: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Tickformatstop' object\n\nArgs:\n    dtickrange: range [*min*, *max*], where *min*, *max* - dtick values which describe some zoom level, it is possible to omit *min* or *max* value by passing *null*\n    enabled: Determines whether or not this stop is used. If `false`, this stop is ignored even within its `dtickrange`.\n    name: When used in a template, named items are created in the output figure in addition to any items the figure already has in this array. You can modify these items in the output figure by making your own item with `templateitemname` matching this `name` alongside your modifications (including `visible: false` or `enabled: false` to hide it). Has no effect outside of a template.\n    templateitemname: Used to refer to a named item in this array in the template. Named items from the template will be created even without a matching item in the input figure, but you can modify one by making an item with `templateitemname` matching its `name`, alongside your modifications (including `visible: false` or `enabled: false` to hide it). If there is no template or no matching item, this item will be hidden unless you explicitly show it with `visible: true`.\n    value: string - dtickformat for described zoom level, the same as *tickformat*"
        ...

class Title(_PlotlyObject):
    "Create a new 'Title' object"
    @property
    def font(self) -> _plotly_graph_objs_layout_xaxis_title.Font | Any:
        "Sets this axis' title font."
        ...
    @font.setter
    def font(self, value: Any) -> None: ...
    standoff: float | Any
    "Sets the standoff distance (in px) between the axis labels and the title text The default value is a function of the axis tick labels, the title `font.size` and the axis `linewidth`. Note that the axis title position is always constrained within the margins, so the actual standoff distance is always less than the set or default value. By setting `standoff` and turning on `automargin`, plotly.js will push the margins to fit the axis title at given standoff distance."
    text: str | Any
    "Sets the title of this axis."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        font: Any = ...,
        standoff: Any = ...,
        text: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Title' object\n\nArgs:\n    font: Sets this axis' title font.\n    standoff: Sets the standoff distance (in px) between the axis labels and the title text The default value is a function of the axis tick labels, the title `font.size` and the axis `linewidth`. Note that the axis title position is always constrained within the margins, so the actual standoff distance is always less than the set or default value. By setting `standoff` and turning on `automargin`, plotly.js will push the margins to fit the axis title at given standoff distance.\n    text: Sets the title of this axis."
        ...

class Unifiedhovertitle(_PlotlyObject):
    "Create a new 'Unifiedhovertitle' object"
    text: str | Any
    "Template string used for rendering the title that appear on x or y unified hover box. Variables are inserted using %{variable}, for example \"y: %{y}\". Numbers are formatted using d3-format's syntax %{variable:d3-format}, for example \"Price: %{y:$.2f}\". https://github.com/d3/d3-format/tree/v1.4.5#d3-format for details on the formatting syntax. Dates are formatted using d3-time-format's syntax %{variable|d3-time-format}, for example \"Day: %{2019-01-01|%A}\". https://github.com/d3/d3-time-format/tree/v2.2.3#locale_format for details on the date formatting syntax. Variables that can't be found will be replaced with the specifier. For example, a template of \"data: %{x}, %{y}\" will result in a value of \"data: 1, %{y}\" if x is 1 and y is missing. Variables with an undefined value will be replaced with the fallback value."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        text: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Unifiedhovertitle' object\n\nArgs:\n    text: Template string used for rendering the title that appear on x or y unified hover box. Variables are inserted using %{variable}, for example \"y: %{y}\". Numbers are formatted using d3-format's syntax %{variable:d3-format}, for example \"Price: %{y:$.2f}\". https://github.com/d3/d3-format/tree/v1.4.5#d3-format for details on the formatting syntax. Dates are formatted using d3-time-format's syntax %{variable|d3-time-format}, for example \"Day: %{2019-01-01|%A}\". https://github.com/d3/d3-time-format/tree/v2.2.3#locale_format for details on the date formatting syntax. Variables that can't be found will be replaced with the specifier. For example, a template of \"data: %{x}, %{y}\" will result in a value of \"data: 1, %{y}\" if x is 1 and y is missing. Variables with an undefined value will be replaced with the fallback value."
        ...
