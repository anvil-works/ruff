# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the Plotly catalogue generator in doc/anvil-api-stubs/plotly-stubs.mjs instead, then run:
#   pnpm -F docs build
#
from plotly._base import _PlotlyObject
from typing import Any, Mapping
import plotly.graph_objs.layout.scene.annotation as _plotly_graph_objs_layout_scene_annotation
import plotly.graph_objs.layout.scene.annotation as annotation
import plotly.graph_objs.layout.scene.aspectratio as _plotly_graph_objs_layout_scene_aspectratio
import plotly.graph_objs.layout.scene.aspectratio as aspectratio
import plotly.graph_objs.layout.scene.camera as _plotly_graph_objs_layout_scene_camera
import plotly.graph_objs.layout.scene.camera as camera
import plotly.graph_objs.layout.scene.xaxis as _plotly_graph_objs_layout_scene_xaxis
import plotly.graph_objs.layout.scene.xaxis as xaxis
import plotly.graph_objs.layout.scene.yaxis as _plotly_graph_objs_layout_scene_yaxis
import plotly.graph_objs.layout.scene.yaxis as yaxis
import plotly.graph_objs.layout.scene.zaxis as _plotly_graph_objs_layout_scene_zaxis
import plotly.graph_objs.layout.scene.zaxis as zaxis

class Annotation(_PlotlyObject):
    "Create a new 'Annotation' object"
    align: Any
    "Sets the horizontal alignment of the `text` within the box. Has an effect only if `text` spans two or more lines (i.e. `text` contains one or more <br> HTML tags) or if an explicit width is set to override the text width."
    arrowcolor: Any
    "Sets the color of the annotation arrow."
    arrowhead: int | Any
    "Sets the end annotation arrow head style."
    arrowside: str | Any
    "Sets the annotation arrow head position."
    arrowsize: float | Any
    "Sets the size of the end annotation arrow head, relative to `arrowwidth`. A value of 1 (default) gives a head about 3x as wide as the line."
    arrowwidth: float | Any
    "Sets the width (in px) of annotation arrow line."
    ax: float | Any
    "Sets the x component of the arrow tail about the arrow head (in pixels)."
    ay: float | Any
    "Sets the y component of the arrow tail about the arrow head (in pixels)."
    bgcolor: Any
    "Sets the background color of the annotation."
    bordercolor: Any
    "Sets the color of the border enclosing the annotation `text`."
    borderpad: float | Any
    "Sets the padding (in px) between the `text` and the enclosing border."
    borderwidth: float | Any
    "Sets the width (in px) of the border enclosing the annotation `text`."
    captureevents: bool | Any
    "Determines whether the annotation text box captures mouse move and click events, or allows those events to pass through to data points in the plot that may be behind the annotation. By default `captureevents` is *false* unless `hovertext` is provided. If you use the event `plotly_clickannotation` without `hovertext` you must explicitly enable `captureevents`."
    @property
    def font(self) -> _plotly_graph_objs_layout_scene_annotation.Font | Any:
        "Sets the annotation text font."
        ...
    @font.setter
    def font(self, value: Any) -> None: ...
    height: float | Any
    "Sets an explicit height for the text box. null (default) lets the text set the box height. Taller text will be clipped."
    @property
    def hoverlabel(self) -> _plotly_graph_objs_layout_scene_annotation.Hoverlabel | Any:
        ...
    @hoverlabel.setter
    def hoverlabel(self, value: Any) -> None: ...
    hovertext: str | Any
    "Sets text to appear when hovering over this annotation. If omitted or blank, no hover label will appear."
    name: str | Any
    "When used in a template, named items are created in the output figure in addition to any items the figure already has in this array. You can modify these items in the output figure by making your own item with `templateitemname` matching this `name` alongside your modifications (including `visible: false` or `enabled: false` to hide it). Has no effect outside of a template."
    opacity: float | Any
    "Sets the opacity of the annotation (text + arrow)."
    showarrow: bool | Any
    "Determines whether or not the annotation is drawn with an arrow. If *true*, `text` is placed near the arrow's tail. If *false*, `text` lines up with the `x` and `y` provided."
    standoff: float | Any
    "Sets a distance, in pixels, to move the end arrowhead away from the position it is pointing at, for example to point at the edge of a marker independent of zoom. Note that this shortens the arrow from the `ax` / `ay` vector, in contrast to `xshift` / `yshift` which moves everything by this amount."
    startarrowhead: int | Any
    "Sets the start annotation arrow head style."
    startarrowsize: float | Any
    "Sets the size of the start annotation arrow head, relative to `arrowwidth`. A value of 1 (default) gives a head about 3x as wide as the line."
    startstandoff: float | Any
    "Sets a distance, in pixels, to move the start arrowhead away from the position it is pointing at, for example to point at the edge of a marker independent of zoom. Note that this shortens the arrow from the `ax` / `ay` vector, in contrast to `xshift` / `yshift` which moves everything by this amount."
    templateitemname: str | Any
    "Used to refer to a named item in this array in the template. Named items from the template will be created even without a matching item in the input figure, but you can modify one by making an item with `templateitemname` matching its `name`, alongside your modifications (including `visible: false` or `enabled: false` to hide it). If there is no template or no matching item, this item will be hidden unless you explicitly show it with `visible: true`."
    text: str | Any
    "Sets the text associated with this annotation. Plotly uses a subset of HTML tags to do things like newline (`<br>`), bold (`<b></b>`), italics (`<i></i>`), hyperlinks (`<a href='...'></a>`). Tags `<em>`, `<sup>`, `<sub>`, `<s>`, `<u>`, and `<span>` are also supported."
    textangle: Any
    "Sets the angle at which the `text` is drawn with respect to the horizontal."
    valign: Any
    "Sets the vertical alignment of the `text` within the box. Has an effect only if an explicit height is set to override the text height."
    visible: bool | Any
    "Determines whether or not this annotation is visible."
    width: float | Any
    "Sets an explicit width for the text box. null (default) lets the text set the box width. Wider text will be clipped. There is no automatic wrapping; use <br> to start a new line."
    x: Any
    "Sets the annotation's x position."
    xanchor: Any
    "Sets the text box's horizontal position anchor This anchor binds the `x` position to the *left*, *center* or *right* of the annotation. For example, if `x` is set to 1, `xref` to *paper* and `xanchor` to *right* then the right-most portion of the annotation lines up with the right-most edge of the plotting area. If *auto*, the anchor is equivalent to *center* for data-referenced annotations or if there is an arrow, whereas for paper-referenced with no arrow, the anchor picked corresponds to the closest side."
    xshift: float | Any
    "Shifts the position of the whole annotation and arrow to the right (positive) or left (negative) by this many pixels."
    y: Any
    "Sets the annotation's y position."
    yanchor: Any
    "Sets the text box's vertical position anchor This anchor binds the `y` position to the *top*, *middle* or *bottom* of the annotation. For example, if `y` is set to 1, `yref` to *paper* and `yanchor` to *top* then the top-most portion of the annotation lines up with the top-most edge of the plotting area. If *auto*, the anchor is equivalent to *middle* for data-referenced annotations or if there is an arrow, whereas for paper-referenced with no arrow, the anchor picked corresponds to the closest side."
    yshift: float | Any
    "Shifts the position of the whole annotation and arrow up (positive) or down (negative) by this many pixels."
    z: Any
    "Sets the annotation's z position."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        align: Any = ...,
        arrowcolor: Any = ...,
        arrowhead: Any = ...,
        arrowside: Any = ...,
        arrowsize: Any = ...,
        arrowwidth: Any = ...,
        ax: Any = ...,
        ay: Any = ...,
        bgcolor: Any = ...,
        bordercolor: Any = ...,
        borderpad: Any = ...,
        borderwidth: Any = ...,
        captureevents: Any = ...,
        font: Any = ...,
        height: Any = ...,
        hoverlabel: Any = ...,
        hovertext: Any = ...,
        name: Any = ...,
        opacity: Any = ...,
        showarrow: Any = ...,
        standoff: Any = ...,
        startarrowhead: Any = ...,
        startarrowsize: Any = ...,
        startstandoff: Any = ...,
        templateitemname: Any = ...,
        text: Any = ...,
        textangle: Any = ...,
        valign: Any = ...,
        visible: Any = ...,
        width: Any = ...,
        x: Any = ...,
        xanchor: Any = ...,
        xshift: Any = ...,
        y: Any = ...,
        yanchor: Any = ...,
        yshift: Any = ...,
        z: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Annotation' object\n\nArgs:\n    align: Sets the horizontal alignment of the `text` within the box. Has an effect only if `text` spans two or more lines (i.e. `text` contains one or more <br> HTML tags) or if an explicit width is set to override the text width.\n    arrowcolor: Sets the color of the annotation arrow.\n    arrowhead: Sets the end annotation arrow head style.\n    arrowside: Sets the annotation arrow head position.\n    arrowsize: Sets the size of the end annotation arrow head, relative to `arrowwidth`. A value of 1 (default) gives a head about 3x as wide as the line.\n    arrowwidth: Sets the width (in px) of annotation arrow line.\n    ax: Sets the x component of the arrow tail about the arrow head (in pixels).\n    ay: Sets the y component of the arrow tail about the arrow head (in pixels).\n    bgcolor: Sets the background color of the annotation.\n    bordercolor: Sets the color of the border enclosing the annotation `text`.\n    borderpad: Sets the padding (in px) between the `text` and the enclosing border.\n    borderwidth: Sets the width (in px) of the border enclosing the annotation `text`.\n    captureevents: Determines whether the annotation text box captures mouse move and click events, or allows those events to pass through to data points in the plot that may be behind the annotation. By default `captureevents` is *false* unless `hovertext` is provided. If you use the event `plotly_clickannotation` without `hovertext` you must explicitly enable `captureevents`.\n    font: Sets the annotation text font.\n    height: Sets an explicit height for the text box. null (default) lets the text set the box height. Taller text will be clipped.\n    hovertext: Sets text to appear when hovering over this annotation. If omitted or blank, no hover label will appear.\n    name: When used in a template, named items are created in the output figure in addition to any items the figure already has in this array. You can modify these items in the output figure by making your own item with `templateitemname` matching this `name` alongside your modifications (including `visible: false` or `enabled: false` to hide it). Has no effect outside of a template.\n    opacity: Sets the opacity of the annotation (text + arrow).\n    showarrow: Determines whether or not the annotation is drawn with an arrow. If *true*, `text` is placed near the arrow's tail. If *false*, `text` lines up with the `x` and `y` provided.\n    standoff: Sets a distance, in pixels, to move the end arrowhead away from the position it is pointing at, for example to point at the edge of a marker independent of zoom. Note that this shortens the arrow from the `ax` / `ay` vector, in contrast to `xshift` / `yshift` which moves everything by this amount.\n    startarrowhead: Sets the start annotation arrow head style.\n    startarrowsize: Sets the size of the start annotation arrow head, relative to `arrowwidth`. A value of 1 (default) gives a head about 3x as wide as the line.\n    startstandoff: Sets a distance, in pixels, to move the start arrowhead away from the position it is pointing at, for example to point at the edge of a marker independent of zoom. Note that this shortens the arrow from the `ax` / `ay` vector, in contrast to `xshift` / `yshift` which moves everything by this amount.\n    templateitemname: Used to refer to a named item in this array in the template. Named items from the template will be created even without a matching item in the input figure, but you can modify one by making an item with `templateitemname` matching its `name`, alongside your modifications (including `visible: false` or `enabled: false` to hide it). If there is no template or no matching item, this item will be hidden unless you explicitly show it with `visible: true`.\n    text: Sets the text associated with this annotation. Plotly uses a subset of HTML tags to do things like newline (`<br>`), bold (`<b></b>`), italics (`<i></i>`), hyperlinks (`<a href='...'></a>`). Tags `<em>`, `<sup>`, `<sub>`, `<s>`, `<u>`, and `<span>` are also supported.\n    textangle: Sets the angle at which the `text` is drawn with respect to the horizontal.\n    valign: Sets the vertical alignment of the `text` within the box. Has an effect only if an explicit height is set to override the text height.\n    visible: Determines whether or not this annotation is visible.\n    width: Sets an explicit width for the text box. null (default) lets the text set the box width. Wider text will be clipped. There is no automatic wrapping; use <br> to start a new line.\n    x: Sets the annotation's x position.\n    xanchor: Sets the text box's horizontal position anchor This anchor binds the `x` position to the *left*, *center* or *right* of the annotation. For example, if `x` is set to 1, `xref` to *paper* and `xanchor` to *right* then the right-most portion of the annotation lines up with the right-most edge of the plotting area. If *auto*, the anchor is equivalent to *center* for data-referenced annotations or if there is an arrow, whereas for paper-referenced with no arrow, the anchor picked corresponds to the closest side.\n    xshift: Shifts the position of the whole annotation and arrow to the right (positive) or left (negative) by this many pixels.\n    y: Sets the annotation's y position.\n    yanchor: Sets the text box's vertical position anchor This anchor binds the `y` position to the *top*, *middle* or *bottom* of the annotation. For example, if `y` is set to 1, `yref` to *paper* and `yanchor` to *top* then the top-most portion of the annotation lines up with the top-most edge of the plotting area. If *auto*, the anchor is equivalent to *middle* for data-referenced annotations or if there is an arrow, whereas for paper-referenced with no arrow, the anchor picked corresponds to the closest side.\n    yshift: Shifts the position of the whole annotation and arrow up (positive) or down (negative) by this many pixels.\n    z: Sets the annotation's z position."
        ...

class Aspectratio(_PlotlyObject):
    "Create a new 'Aspectratio' object"
    @property
    def impliedEdits(self) -> _plotly_graph_objs_layout_scene_aspectratio.Impliededits | Any:
        ...
    @impliedEdits.setter
    def impliedEdits(self, value: Any) -> None: ...
    x: float | Any
    y: float | Any
    z: float | Any
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        impliedEdits: Any = ...,
        x: Any = ...,
        y: Any = ...,
        z: Any = ...,
        **kwargs: Any,
    ) -> None:
        ...

class Camera(_PlotlyObject):
    "Create a new 'Camera' object"
    @property
    def center(self) -> _plotly_graph_objs_layout_scene_camera.Center | Any:
        "Sets the (x,y,z) components of the 'center' camera vector This vector determines the translation (x,y,z) space about the center of this scene. By default, there is no such translation."
        ...
    @center.setter
    def center(self, value: Any) -> None: ...
    @property
    def eye(self) -> _plotly_graph_objs_layout_scene_camera.Eye | Any:
        "Sets the (x,y,z) components of the 'eye' camera vector. This vector determines the view point about the origin of this scene."
        ...
    @eye.setter
    def eye(self, value: Any) -> None: ...
    @property
    def projection(self) -> _plotly_graph_objs_layout_scene_camera.Projection | Any:
        ...
    @projection.setter
    def projection(self, value: Any) -> None: ...
    @property
    def up(self) -> _plotly_graph_objs_layout_scene_camera.Up | Any:
        "Sets the (x,y,z) components of the 'up' camera vector. This vector determines the up direction of this scene with respect to the page. The default is *{x: 0, y: 0, z: 1}* which means that the z axis points up."
        ...
    @up.setter
    def up(self, value: Any) -> None: ...
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        center: Any = ...,
        eye: Any = ...,
        projection: Any = ...,
        up: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Camera' object\n\nArgs:\n    center: Sets the (x,y,z) components of the 'center' camera vector This vector determines the translation (x,y,z) space about the center of this scene. By default, there is no such translation.\n    eye: Sets the (x,y,z) components of the 'eye' camera vector. This vector determines the view point about the origin of this scene.\n    up: Sets the (x,y,z) components of the 'up' camera vector. This vector determines the up direction of this scene with respect to the page. The default is *{x: 0, y: 0, z: 1}* which means that the z axis points up."
        ...

class Domain(_PlotlyObject):
    "Create a new 'Domain' object"
    column: int | Any
    "If there is a layout grid, use the domain for this column in the grid for this scene subplot."
    row: int | Any
    "If there is a layout grid, use the domain for this row in the grid for this scene subplot."
    x: Any
    "Sets the horizontal domain of this scene subplot (in plot fraction)."
    y: Any
    "Sets the vertical domain of this scene subplot (in plot fraction)."
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
        "Create a new 'Domain' object\n\nArgs:\n    column: If there is a layout grid, use the domain for this column in the grid for this scene subplot.\n    row: If there is a layout grid, use the domain for this row in the grid for this scene subplot.\n    x: Sets the horizontal domain of this scene subplot (in plot fraction).\n    y: Sets the vertical domain of this scene subplot (in plot fraction)."
        ...

class XAxis(_PlotlyObject):
    "Create a new 'XAxis' object"
    autorange: Any
    "Determines whether or not the range of this axis is computed in relation to the input data. See `rangemode` for more info. If `range` is provided and it has a value for both the lower and upper bound, `autorange` is set to *false*. Using *min* applies autorange only to set the minimum. Using *max* applies autorange only to set the maximum. Using *min reversed* applies autorange only to set the minimum on a reversed axis. Using *max reversed* applies autorange only to set the maximum on a reversed axis. Using *reversed* applies autorange on both ends and reverses the axis direction."
    @property
    def autorangeoptions(self) -> _plotly_graph_objs_layout_scene_xaxis.Autorangeoptions | Any:
        ...
    @autorangeoptions.setter
    def autorangeoptions(self, value: Any) -> None: ...
    autotypenumbers: Any
    "Using *strict* a numeric string in trace data is not converted to a number. Using *convert types* a numeric string in trace data may be treated as a number during automatic axis `type` detection. Defaults to layout.autotypenumbers."
    backgroundcolor: Any
    "Sets the background color of this axis' wall."
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
    gridwidth: float | Any
    "Sets the width (in px) of the grid lines."
    hoverformat: str | Any
    "Sets the hover text formatting rule using d3 formatting mini-languages which are very similar to those in Python. For numbers, see: https://github.com/d3/d3-format/tree/v1.4.5#d3-format. And for dates see: https://github.com/d3/d3-time-format/tree/v2.2.3#locale_format. We add two items to d3's date formatter: *%h* for half of the year as a decimal number as well as *%{n}f* for fractional seconds with n digits. For example, *2016-10-13 09:15:23.456* with tickformat *%H~%M~%S.%2f* would display *09~15~23.46*"
    labelalias: Any
    "Replacement text for specific tick or hover labels. For example using {US: 'USA', CA: 'Canada'} changes US to USA and CA to Canada. The labels we would have shown must match the keys exactly, after adding any tickprefix or ticksuffix. For negative numbers the minus sign symbol used (U+2212) is wider than the regular ascii dash. That means you need to use −1 instead of -1. labelalias can be used with any axis type, and both keys (if needed) and values (if desired) can include html-like tags or MathJax."
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
    mirror: Any
    "Determines if the axis lines or/and ticks are mirrored to the opposite side of the plotting area. If *true*, the axis lines are mirrored. If *ticks*, the axis lines and ticks are mirrored. If *false*, mirroring is disable. If *all*, axis lines are mirrored on all shared-axes subplots. If *allticks*, axis lines and ticks are mirrored on all shared-axes subplots."
    nticks: int | Any
    "Specifies the maximum number of ticks for the particular axis. The actual number of ticks will be chosen automatically to be less than or equal to `nticks`. Has an effect only if `tickmode` is set to *auto*."
    range: Any
    "Sets the range of this axis. If the axis `type` is *log*, then you must take the log of your desired range (e.g. to set the range from 1 to 100, set the range from 0 to 2). If the axis `type` is *date*, it should be date strings, like date data, though Date objects and unix milliseconds will be accepted and converted to strings. If the axis `type` is *category*, it should be numbers, using the scale where each category is assigned a serial number from zero in the order it appears. Leaving either or both elements `null` impacts the default `autorange`."
    rangemode: Any
    "If *normal*, the range is computed in relation to the extrema of the input data. If *tozero*, the range extends to 0, regardless of the input data If *nonnegative*, the range is non-negative, regardless of the input data. Applies only to linear axes."
    separatethousands: bool | Any
    "If \"true\", even 4-digit integers are separated"
    showaxeslabels: bool | Any
    "Sets whether or not this axis is labeled"
    showbackground: bool | Any
    "Sets whether or not this axis' wall has a background color."
    showexponent: Any
    "If *all*, all exponents are shown besides their significands. If *first*, only the exponent of the first tick is shown. If *last*, only the exponent of the last tick is shown. If *none*, no exponents appear."
    showgrid: bool | Any
    "Determines whether or not grid lines are drawn. If *true*, the grid lines are drawn at every tick mark."
    showline: bool | Any
    "Determines whether or not a line bounding this axis is drawn."
    showspikes: bool | Any
    "Sets whether or not spikes starting from data points to this axis' wall are shown on hover."
    showticklabels: bool | Any
    "Determines whether or not the tick labels are drawn."
    showtickprefix: Any
    "If *all*, all tick labels are displayed with a prefix. If *first*, only the first tick is displayed with a prefix. If *last*, only the last tick is displayed with a suffix. If *none*, tick prefixes are hidden."
    showticksuffix: Any
    "Same as `showtickprefix` but for tick suffixes."
    spikecolor: Any
    "Sets the color of the spikes."
    spikesides: bool | Any
    "Sets whether or not spikes extending from the projection data points to this axis' wall boundaries are shown on hover."
    spikethickness: float | Any
    "Sets the thickness (in px) of the spikes."
    tick0: Any
    "Sets the placement of the first tick on this axis. Use with `dtick`. If the axis `type` is *log*, then you must take the log of your starting tick (e.g. to set the starting tick to 100, set the `tick0` to 2) except when `dtick`=*L<f>* (see `dtick` for more info). If the axis `type` is *date*, it should be a date string, like date data. If the axis `type` is *category*, it should be a number, using the scale where each category is assigned a serial number from zero in the order it appears."
    tickangle: Any
    "Sets the angle of the tick labels with respect to the horizontal. For example, a `tickangle` of -90 draws the tick labels vertically."
    tickcolor: Any
    "Sets the tick color."
    @property
    def tickfont(self) -> _plotly_graph_objs_layout_scene_xaxis.Tickfont | Any:
        "Sets the tick font."
        ...
    @tickfont.setter
    def tickfont(self, value: Any) -> None: ...
    tickformat: str | Any
    "Sets the tick label formatting rule using d3 formatting mini-languages which are very similar to those in Python. For numbers, see: https://github.com/d3/d3-format/tree/v1.4.5#d3-format. And for dates see: https://github.com/d3/d3-time-format/tree/v2.2.3#locale_format. We add two items to d3's date formatter: *%h* for half of the year as a decimal number as well as *%{n}f* for fractional seconds with n digits. For example, *2016-10-13 09:15:23.456* with tickformat *%H~%M~%S.%2f* would display *09~15~23.46*"
    @property
    def tickformatstop(self) -> _plotly_graph_objs_layout_scene_xaxis.Tickformatstop | Any:
        ...
    @tickformatstop.setter
    def tickformatstop(self, value: Any) -> None: ...
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
    def title(self) -> _plotly_graph_objs_layout_scene_xaxis.Title | Any:
        ...
    @title.setter
    def title(self, value: Any) -> None: ...
    type: Any
    "Sets the axis type. By default, plotly attempts to determined the axis type by looking into the data of the traces that referenced the axis in question."
    visible: bool | Any
    "A single toggle to hide the axis while preserving interaction like dragging. Default is true when a cheater plot is present on the axis, otherwise false"
    zeroline: bool | Any
    "Determines whether or not a line is drawn at along the 0 value of this axis. If *true*, the zero line is drawn on top of the grid lines."
    zerolinecolor: Any
    "Sets the line color of the zero line."
    zerolinewidth: float | Any
    "Sets the width (in px) of the zero line."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        autorange: Any = ...,
        autorangeoptions: Any = ...,
        autotypenumbers: Any = ...,
        backgroundcolor: Any = ...,
        calendar: Any = ...,
        categoryarray: Any = ...,
        categoryorder: Any = ...,
        color: Any = ...,
        dtick: Any = ...,
        exponentformat: Any = ...,
        gridcolor: Any = ...,
        gridwidth: Any = ...,
        hoverformat: Any = ...,
        labelalias: Any = ...,
        linecolor: Any = ...,
        linewidth: Any = ...,
        maxallowed: Any = ...,
        minallowed: Any = ...,
        minexponent: Any = ...,
        mirror: Any = ...,
        nticks: Any = ...,
        range: Any = ...,
        rangemode: Any = ...,
        separatethousands: Any = ...,
        showaxeslabels: Any = ...,
        showbackground: Any = ...,
        showexponent: Any = ...,
        showgrid: Any = ...,
        showline: Any = ...,
        showspikes: Any = ...,
        showticklabels: Any = ...,
        showtickprefix: Any = ...,
        showticksuffix: Any = ...,
        spikecolor: Any = ...,
        spikesides: Any = ...,
        spikethickness: Any = ...,
        tick0: Any = ...,
        tickangle: Any = ...,
        tickcolor: Any = ...,
        tickfont: Any = ...,
        tickformat: Any = ...,
        tickformatstop: Any = ...,
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
        visible: Any = ...,
        zeroline: Any = ...,
        zerolinecolor: Any = ...,
        zerolinewidth: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'XAxis' object\n\nArgs:\n    autorange: Determines whether or not the range of this axis is computed in relation to the input data. See `rangemode` for more info. If `range` is provided and it has a value for both the lower and upper bound, `autorange` is set to *false*. Using *min* applies autorange only to set the minimum. Using *max* applies autorange only to set the maximum. Using *min reversed* applies autorange only to set the minimum on a reversed axis. Using *max reversed* applies autorange only to set the maximum on a reversed axis. Using *reversed* applies autorange on both ends and reverses the axis direction.\n    autotypenumbers: Using *strict* a numeric string in trace data is not converted to a number. Using *convert types* a numeric string in trace data may be treated as a number during automatic axis `type` detection. Defaults to layout.autotypenumbers.\n    backgroundcolor: Sets the background color of this axis' wall.\n    calendar: Sets the calendar system to use for `range` and `tick0` if this is a date axis. This does not set the calendar for interpreting data on this axis, that's specified in the trace or via the global `layout.calendar`\n    categoryarray: Sets the order in which categories on this axis appear. Only has an effect if `categoryorder` is set to *array*. Used with `categoryorder`.\n    categoryorder: Specifies the ordering logic for the case of categorical variables. By default, plotly uses *trace*, which specifies the order that is present in the data supplied. Set `categoryorder` to *category ascending* or *category descending* if order should be determined by the alphanumerical order of the category names. Set `categoryorder` to *array* to derive the ordering from the attribute `categoryarray`. If a category is not found in the `categoryarray` array, the sorting behavior for that attribute will be identical to the *trace* mode. The unspecified categories will follow the categories in `categoryarray`. Set `categoryorder` to *total ascending* or *total descending* if order should be determined by the numerical order of the values. Similarly, the order can be determined by the min, max, sum, mean, geometric mean or median of all the values.\n    color: Sets default for all colors associated with this axis all at once: line, font, tick, and grid colors. Grid color is lightened by blending this with the plot background Individual pieces can override this.\n    dtick: Sets the step in-between ticks on this axis. Use with `tick0`. Must be a positive number, or special strings available to *log* and *date* axes. If the axis `type` is *log*, then ticks are set every 10^(n*dtick) where n is the tick number. For example, to set a tick mark at 1, 10, 100, 1000, ... set dtick to 1. To set tick marks at 1, 100, 10000, ... set dtick to 2. To set tick marks at 1, 5, 25, 125, 625, 3125, ... set dtick to log_10(5), or 0.69897000433. *log* has several special values; *L<f>*, where `f` is a positive number, gives ticks linearly spaced in value (but not position). For example `tick0` = 0.1, `dtick` = *L0.5* will put ticks at 0.1, 0.6, 1.1, 1.6 etc. To show powers of 10 plus small digits between, use *D1* (all digits) or *D2* (only 2 and 5). `tick0` is ignored for *D1* and *D2*. If the axis `type` is *date*, then you must convert the time to milliseconds. For example, to set the interval between ticks to one day, set `dtick` to 86400000.0. *date* also has special values *M<n>* gives ticks spaced by a number of months. `n` must be a positive integer. To set ticks on the 15th of every third month, set `tick0` to *2000-01-15* and `dtick` to *M3*. To set ticks every 4 years, set `dtick` to *M48*\n    exponentformat: Determines a formatting rule for the tick exponents. For example, consider the number 1,000,000,000. If *none*, it appears as 1,000,000,000. If *e*, 1e+9. If *E*, 1E+9. If *power*, 1x10^9 (with 9 in a super script). If *SI*, 1G. If *B*, 1B. *SI* uses prefixes from \"femto\" f (10^-15) to \"tera\" T (10^12). *SI extended* covers instead the full SI range from \"quecto\" q (10^-30) to \"quetta\" Q (10^30). If *SI* or *SI extended* is used and the exponent is beyond the above ranges, the formatting rule will automatically be switched to the power notation.\n    gridcolor: Sets the color of the grid lines.\n    gridwidth: Sets the width (in px) of the grid lines.\n    hoverformat: Sets the hover text formatting rule using d3 formatting mini-languages which are very similar to those in Python. For numbers, see: https://github.com/d3/d3-format/tree/v1.4.5#d3-format. And for dates see: https://github.com/d3/d3-time-format/tree/v2.2.3#locale_format. We add two items to d3's date formatter: *%h* for half of the year as a decimal number as well as *%{n}f* for fractional seconds with n digits. For example, *2016-10-13 09:15:23.456* with tickformat *%H~%M~%S.%2f* would display *09~15~23.46*\n    labelalias: Replacement text for specific tick or hover labels. For example using {US: 'USA', CA: 'Canada'} changes US to USA and CA to Canada. The labels we would have shown must match the keys exactly, after adding any tickprefix or ticksuffix. For negative numbers the minus sign symbol used (U+2212) is wider than the regular ascii dash. That means you need to use −1 instead of -1. labelalias can be used with any axis type, and both keys (if needed) and values (if desired) can include html-like tags or MathJax.\n    linecolor: Sets the axis line color.\n    linewidth: Sets the width (in px) of the axis line.\n    maxallowed: Determines the maximum range of this axis.\n    minallowed: Determines the minimum range of this axis.\n    minexponent: Hide SI prefix for 10^n if |n| is below this number. This only has an effect when `tickformat` is *SI* or *B*.\n    mirror: Determines if the axis lines or/and ticks are mirrored to the opposite side of the plotting area. If *true*, the axis lines are mirrored. If *ticks*, the axis lines and ticks are mirrored. If *false*, mirroring is disable. If *all*, axis lines are mirrored on all shared-axes subplots. If *allticks*, axis lines and ticks are mirrored on all shared-axes subplots.\n    nticks: Specifies the maximum number of ticks for the particular axis. The actual number of ticks will be chosen automatically to be less than or equal to `nticks`. Has an effect only if `tickmode` is set to *auto*.\n    range: Sets the range of this axis. If the axis `type` is *log*, then you must take the log of your desired range (e.g. to set the range from 1 to 100, set the range from 0 to 2). If the axis `type` is *date*, it should be date strings, like date data, though Date objects and unix milliseconds will be accepted and converted to strings. If the axis `type` is *category*, it should be numbers, using the scale where each category is assigned a serial number from zero in the order it appears. Leaving either or both elements `null` impacts the default `autorange`.\n    rangemode: If *normal*, the range is computed in relation to the extrema of the input data. If *tozero*, the range extends to 0, regardless of the input data If *nonnegative*, the range is non-negative, regardless of the input data. Applies only to linear axes.\n    separatethousands: If \"true\", even 4-digit integers are separated\n    showaxeslabels: Sets whether or not this axis is labeled\n    showbackground: Sets whether or not this axis' wall has a background color.\n    showexponent: If *all*, all exponents are shown besides their significands. If *first*, only the exponent of the first tick is shown. If *last*, only the exponent of the last tick is shown. If *none*, no exponents appear.\n    showgrid: Determines whether or not grid lines are drawn. If *true*, the grid lines are drawn at every tick mark.\n    showline: Determines whether or not a line bounding this axis is drawn.\n    showspikes: Sets whether or not spikes starting from data points to this axis' wall are shown on hover.\n    showticklabels: Determines whether or not the tick labels are drawn.\n    showtickprefix: If *all*, all tick labels are displayed with a prefix. If *first*, only the first tick is displayed with a prefix. If *last*, only the last tick is displayed with a suffix. If *none*, tick prefixes are hidden.\n    showticksuffix: Same as `showtickprefix` but for tick suffixes.\n    spikecolor: Sets the color of the spikes.\n    spikesides: Sets whether or not spikes extending from the projection data points to this axis' wall boundaries are shown on hover.\n    spikethickness: Sets the thickness (in px) of the spikes.\n    tick0: Sets the placement of the first tick on this axis. Use with `dtick`. If the axis `type` is *log*, then you must take the log of your starting tick (e.g. to set the starting tick to 100, set the `tick0` to 2) except when `dtick`=*L<f>* (see `dtick` for more info). If the axis `type` is *date*, it should be a date string, like date data. If the axis `type` is *category*, it should be a number, using the scale where each category is assigned a serial number from zero in the order it appears.\n    tickangle: Sets the angle of the tick labels with respect to the horizontal. For example, a `tickangle` of -90 draws the tick labels vertically.\n    tickcolor: Sets the tick color.\n    tickfont: Sets the tick font.\n    tickformat: Sets the tick label formatting rule using d3 formatting mini-languages which are very similar to those in Python. For numbers, see: https://github.com/d3/d3-format/tree/v1.4.5#d3-format. And for dates see: https://github.com/d3/d3-time-format/tree/v2.2.3#locale_format. We add two items to d3's date formatter: *%h* for half of the year as a decimal number as well as *%{n}f* for fractional seconds with n digits. For example, *2016-10-13 09:15:23.456* with tickformat *%H~%M~%S.%2f* would display *09~15~23.46*\n    ticklen: Sets the tick length (in px).\n    tickmode: Sets the tick mode for this axis. If *auto*, the number of ticks is set via `nticks`. If *linear*, the placement of the ticks is determined by a starting position `tick0` and a tick step `dtick` (*linear* is the default value if `tick0` and `dtick` are provided). If *array*, the placement of the ticks is set via `tickvals` and the tick text is `ticktext`. (*array* is the default value if `tickvals` is provided).\n    tickprefix: Sets a tick label prefix.\n    ticks: Determines whether ticks are drawn or not. If **, this axis' ticks are not drawn. If *outside* (*inside*), this axis' are drawn outside (inside) the axis lines.\n    ticksuffix: Sets a tick label suffix.\n    ticktext: Sets the text displayed at the ticks position via `tickvals`. Only has an effect if `tickmode` is set to *array*. Used with `tickvals`.\n    tickvals: Sets the values at which ticks on this axis appear. Only has an effect if `tickmode` is set to *array*. Used with `ticktext`.\n    tickwidth: Sets the tick width (in px).\n    type: Sets the axis type. By default, plotly attempts to determined the axis type by looking into the data of the traces that referenced the axis in question.\n    visible: A single toggle to hide the axis while preserving interaction like dragging. Default is true when a cheater plot is present on the axis, otherwise false\n    zeroline: Determines whether or not a line is drawn at along the 0 value of this axis. If *true*, the zero line is drawn on top of the grid lines.\n    zerolinecolor: Sets the line color of the zero line.\n    zerolinewidth: Sets the width (in px) of the zero line."
        ...

class YAxis(_PlotlyObject):
    "Create a new 'YAxis' object"
    autorange: Any
    "Determines whether or not the range of this axis is computed in relation to the input data. See `rangemode` for more info. If `range` is provided and it has a value for both the lower and upper bound, `autorange` is set to *false*. Using *min* applies autorange only to set the minimum. Using *max* applies autorange only to set the maximum. Using *min reversed* applies autorange only to set the minimum on a reversed axis. Using *max reversed* applies autorange only to set the maximum on a reversed axis. Using *reversed* applies autorange on both ends and reverses the axis direction."
    @property
    def autorangeoptions(self) -> _plotly_graph_objs_layout_scene_yaxis.Autorangeoptions | Any:
        ...
    @autorangeoptions.setter
    def autorangeoptions(self, value: Any) -> None: ...
    autotypenumbers: Any
    "Using *strict* a numeric string in trace data is not converted to a number. Using *convert types* a numeric string in trace data may be treated as a number during automatic axis `type` detection. Defaults to layout.autotypenumbers."
    backgroundcolor: Any
    "Sets the background color of this axis' wall."
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
    gridwidth: float | Any
    "Sets the width (in px) of the grid lines."
    hoverformat: str | Any
    "Sets the hover text formatting rule using d3 formatting mini-languages which are very similar to those in Python. For numbers, see: https://github.com/d3/d3-format/tree/v1.4.5#d3-format. And for dates see: https://github.com/d3/d3-time-format/tree/v2.2.3#locale_format. We add two items to d3's date formatter: *%h* for half of the year as a decimal number as well as *%{n}f* for fractional seconds with n digits. For example, *2016-10-13 09:15:23.456* with tickformat *%H~%M~%S.%2f* would display *09~15~23.46*"
    labelalias: Any
    "Replacement text for specific tick or hover labels. For example using {US: 'USA', CA: 'Canada'} changes US to USA and CA to Canada. The labels we would have shown must match the keys exactly, after adding any tickprefix or ticksuffix. For negative numbers the minus sign symbol used (U+2212) is wider than the regular ascii dash. That means you need to use −1 instead of -1. labelalias can be used with any axis type, and both keys (if needed) and values (if desired) can include html-like tags or MathJax."
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
    mirror: Any
    "Determines if the axis lines or/and ticks are mirrored to the opposite side of the plotting area. If *true*, the axis lines are mirrored. If *ticks*, the axis lines and ticks are mirrored. If *false*, mirroring is disable. If *all*, axis lines are mirrored on all shared-axes subplots. If *allticks*, axis lines and ticks are mirrored on all shared-axes subplots."
    nticks: int | Any
    "Specifies the maximum number of ticks for the particular axis. The actual number of ticks will be chosen automatically to be less than or equal to `nticks`. Has an effect only if `tickmode` is set to *auto*."
    range: Any
    "Sets the range of this axis. If the axis `type` is *log*, then you must take the log of your desired range (e.g. to set the range from 1 to 100, set the range from 0 to 2). If the axis `type` is *date*, it should be date strings, like date data, though Date objects and unix milliseconds will be accepted and converted to strings. If the axis `type` is *category*, it should be numbers, using the scale where each category is assigned a serial number from zero in the order it appears. Leaving either or both elements `null` impacts the default `autorange`."
    rangemode: Any
    "If *normal*, the range is computed in relation to the extrema of the input data. If *tozero*, the range extends to 0, regardless of the input data If *nonnegative*, the range is non-negative, regardless of the input data. Applies only to linear axes."
    separatethousands: bool | Any
    "If \"true\", even 4-digit integers are separated"
    showaxeslabels: bool | Any
    "Sets whether or not this axis is labeled"
    showbackground: bool | Any
    "Sets whether or not this axis' wall has a background color."
    showexponent: Any
    "If *all*, all exponents are shown besides their significands. If *first*, only the exponent of the first tick is shown. If *last*, only the exponent of the last tick is shown. If *none*, no exponents appear."
    showgrid: bool | Any
    "Determines whether or not grid lines are drawn. If *true*, the grid lines are drawn at every tick mark."
    showline: bool | Any
    "Determines whether or not a line bounding this axis is drawn."
    showspikes: bool | Any
    "Sets whether or not spikes starting from data points to this axis' wall are shown on hover."
    showticklabels: bool | Any
    "Determines whether or not the tick labels are drawn."
    showtickprefix: Any
    "If *all*, all tick labels are displayed with a prefix. If *first*, only the first tick is displayed with a prefix. If *last*, only the last tick is displayed with a suffix. If *none*, tick prefixes are hidden."
    showticksuffix: Any
    "Same as `showtickprefix` but for tick suffixes."
    spikecolor: Any
    "Sets the color of the spikes."
    spikesides: bool | Any
    "Sets whether or not spikes extending from the projection data points to this axis' wall boundaries are shown on hover."
    spikethickness: float | Any
    "Sets the thickness (in px) of the spikes."
    tick0: Any
    "Sets the placement of the first tick on this axis. Use with `dtick`. If the axis `type` is *log*, then you must take the log of your starting tick (e.g. to set the starting tick to 100, set the `tick0` to 2) except when `dtick`=*L<f>* (see `dtick` for more info). If the axis `type` is *date*, it should be a date string, like date data. If the axis `type` is *category*, it should be a number, using the scale where each category is assigned a serial number from zero in the order it appears."
    tickangle: Any
    "Sets the angle of the tick labels with respect to the horizontal. For example, a `tickangle` of -90 draws the tick labels vertically."
    tickcolor: Any
    "Sets the tick color."
    @property
    def tickfont(self) -> _plotly_graph_objs_layout_scene_yaxis.Tickfont | Any:
        "Sets the tick font."
        ...
    @tickfont.setter
    def tickfont(self, value: Any) -> None: ...
    tickformat: str | Any
    "Sets the tick label formatting rule using d3 formatting mini-languages which are very similar to those in Python. For numbers, see: https://github.com/d3/d3-format/tree/v1.4.5#d3-format. And for dates see: https://github.com/d3/d3-time-format/tree/v2.2.3#locale_format. We add two items to d3's date formatter: *%h* for half of the year as a decimal number as well as *%{n}f* for fractional seconds with n digits. For example, *2016-10-13 09:15:23.456* with tickformat *%H~%M~%S.%2f* would display *09~15~23.46*"
    @property
    def tickformatstop(self) -> _plotly_graph_objs_layout_scene_yaxis.Tickformatstop | Any:
        ...
    @tickformatstop.setter
    def tickformatstop(self, value: Any) -> None: ...
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
    def title(self) -> _plotly_graph_objs_layout_scene_yaxis.Title | Any:
        ...
    @title.setter
    def title(self, value: Any) -> None: ...
    type: Any
    "Sets the axis type. By default, plotly attempts to determined the axis type by looking into the data of the traces that referenced the axis in question."
    visible: bool | Any
    "A single toggle to hide the axis while preserving interaction like dragging. Default is true when a cheater plot is present on the axis, otherwise false"
    zeroline: bool | Any
    "Determines whether or not a line is drawn at along the 0 value of this axis. If *true*, the zero line is drawn on top of the grid lines."
    zerolinecolor: Any
    "Sets the line color of the zero line."
    zerolinewidth: float | Any
    "Sets the width (in px) of the zero line."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        autorange: Any = ...,
        autorangeoptions: Any = ...,
        autotypenumbers: Any = ...,
        backgroundcolor: Any = ...,
        calendar: Any = ...,
        categoryarray: Any = ...,
        categoryorder: Any = ...,
        color: Any = ...,
        dtick: Any = ...,
        exponentformat: Any = ...,
        gridcolor: Any = ...,
        gridwidth: Any = ...,
        hoverformat: Any = ...,
        labelalias: Any = ...,
        linecolor: Any = ...,
        linewidth: Any = ...,
        maxallowed: Any = ...,
        minallowed: Any = ...,
        minexponent: Any = ...,
        mirror: Any = ...,
        nticks: Any = ...,
        range: Any = ...,
        rangemode: Any = ...,
        separatethousands: Any = ...,
        showaxeslabels: Any = ...,
        showbackground: Any = ...,
        showexponent: Any = ...,
        showgrid: Any = ...,
        showline: Any = ...,
        showspikes: Any = ...,
        showticklabels: Any = ...,
        showtickprefix: Any = ...,
        showticksuffix: Any = ...,
        spikecolor: Any = ...,
        spikesides: Any = ...,
        spikethickness: Any = ...,
        tick0: Any = ...,
        tickangle: Any = ...,
        tickcolor: Any = ...,
        tickfont: Any = ...,
        tickformat: Any = ...,
        tickformatstop: Any = ...,
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
        visible: Any = ...,
        zeroline: Any = ...,
        zerolinecolor: Any = ...,
        zerolinewidth: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'YAxis' object\n\nArgs:\n    autorange: Determines whether or not the range of this axis is computed in relation to the input data. See `rangemode` for more info. If `range` is provided and it has a value for both the lower and upper bound, `autorange` is set to *false*. Using *min* applies autorange only to set the minimum. Using *max* applies autorange only to set the maximum. Using *min reversed* applies autorange only to set the minimum on a reversed axis. Using *max reversed* applies autorange only to set the maximum on a reversed axis. Using *reversed* applies autorange on both ends and reverses the axis direction.\n    autotypenumbers: Using *strict* a numeric string in trace data is not converted to a number. Using *convert types* a numeric string in trace data may be treated as a number during automatic axis `type` detection. Defaults to layout.autotypenumbers.\n    backgroundcolor: Sets the background color of this axis' wall.\n    calendar: Sets the calendar system to use for `range` and `tick0` if this is a date axis. This does not set the calendar for interpreting data on this axis, that's specified in the trace or via the global `layout.calendar`\n    categoryarray: Sets the order in which categories on this axis appear. Only has an effect if `categoryorder` is set to *array*. Used with `categoryorder`.\n    categoryorder: Specifies the ordering logic for the case of categorical variables. By default, plotly uses *trace*, which specifies the order that is present in the data supplied. Set `categoryorder` to *category ascending* or *category descending* if order should be determined by the alphanumerical order of the category names. Set `categoryorder` to *array* to derive the ordering from the attribute `categoryarray`. If a category is not found in the `categoryarray` array, the sorting behavior for that attribute will be identical to the *trace* mode. The unspecified categories will follow the categories in `categoryarray`. Set `categoryorder` to *total ascending* or *total descending* if order should be determined by the numerical order of the values. Similarly, the order can be determined by the min, max, sum, mean, geometric mean or median of all the values.\n    color: Sets default for all colors associated with this axis all at once: line, font, tick, and grid colors. Grid color is lightened by blending this with the plot background Individual pieces can override this.\n    dtick: Sets the step in-between ticks on this axis. Use with `tick0`. Must be a positive number, or special strings available to *log* and *date* axes. If the axis `type` is *log*, then ticks are set every 10^(n*dtick) where n is the tick number. For example, to set a tick mark at 1, 10, 100, 1000, ... set dtick to 1. To set tick marks at 1, 100, 10000, ... set dtick to 2. To set tick marks at 1, 5, 25, 125, 625, 3125, ... set dtick to log_10(5), or 0.69897000433. *log* has several special values; *L<f>*, where `f` is a positive number, gives ticks linearly spaced in value (but not position). For example `tick0` = 0.1, `dtick` = *L0.5* will put ticks at 0.1, 0.6, 1.1, 1.6 etc. To show powers of 10 plus small digits between, use *D1* (all digits) or *D2* (only 2 and 5). `tick0` is ignored for *D1* and *D2*. If the axis `type` is *date*, then you must convert the time to milliseconds. For example, to set the interval between ticks to one day, set `dtick` to 86400000.0. *date* also has special values *M<n>* gives ticks spaced by a number of months. `n` must be a positive integer. To set ticks on the 15th of every third month, set `tick0` to *2000-01-15* and `dtick` to *M3*. To set ticks every 4 years, set `dtick` to *M48*\n    exponentformat: Determines a formatting rule for the tick exponents. For example, consider the number 1,000,000,000. If *none*, it appears as 1,000,000,000. If *e*, 1e+9. If *E*, 1E+9. If *power*, 1x10^9 (with 9 in a super script). If *SI*, 1G. If *B*, 1B. *SI* uses prefixes from \"femto\" f (10^-15) to \"tera\" T (10^12). *SI extended* covers instead the full SI range from \"quecto\" q (10^-30) to \"quetta\" Q (10^30). If *SI* or *SI extended* is used and the exponent is beyond the above ranges, the formatting rule will automatically be switched to the power notation.\n    gridcolor: Sets the color of the grid lines.\n    gridwidth: Sets the width (in px) of the grid lines.\n    hoverformat: Sets the hover text formatting rule using d3 formatting mini-languages which are very similar to those in Python. For numbers, see: https://github.com/d3/d3-format/tree/v1.4.5#d3-format. And for dates see: https://github.com/d3/d3-time-format/tree/v2.2.3#locale_format. We add two items to d3's date formatter: *%h* for half of the year as a decimal number as well as *%{n}f* for fractional seconds with n digits. For example, *2016-10-13 09:15:23.456* with tickformat *%H~%M~%S.%2f* would display *09~15~23.46*\n    labelalias: Replacement text for specific tick or hover labels. For example using {US: 'USA', CA: 'Canada'} changes US to USA and CA to Canada. The labels we would have shown must match the keys exactly, after adding any tickprefix or ticksuffix. For negative numbers the minus sign symbol used (U+2212) is wider than the regular ascii dash. That means you need to use −1 instead of -1. labelalias can be used with any axis type, and both keys (if needed) and values (if desired) can include html-like tags or MathJax.\n    linecolor: Sets the axis line color.\n    linewidth: Sets the width (in px) of the axis line.\n    maxallowed: Determines the maximum range of this axis.\n    minallowed: Determines the minimum range of this axis.\n    minexponent: Hide SI prefix for 10^n if |n| is below this number. This only has an effect when `tickformat` is *SI* or *B*.\n    mirror: Determines if the axis lines or/and ticks are mirrored to the opposite side of the plotting area. If *true*, the axis lines are mirrored. If *ticks*, the axis lines and ticks are mirrored. If *false*, mirroring is disable. If *all*, axis lines are mirrored on all shared-axes subplots. If *allticks*, axis lines and ticks are mirrored on all shared-axes subplots.\n    nticks: Specifies the maximum number of ticks for the particular axis. The actual number of ticks will be chosen automatically to be less than or equal to `nticks`. Has an effect only if `tickmode` is set to *auto*.\n    range: Sets the range of this axis. If the axis `type` is *log*, then you must take the log of your desired range (e.g. to set the range from 1 to 100, set the range from 0 to 2). If the axis `type` is *date*, it should be date strings, like date data, though Date objects and unix milliseconds will be accepted and converted to strings. If the axis `type` is *category*, it should be numbers, using the scale where each category is assigned a serial number from zero in the order it appears. Leaving either or both elements `null` impacts the default `autorange`.\n    rangemode: If *normal*, the range is computed in relation to the extrema of the input data. If *tozero*, the range extends to 0, regardless of the input data If *nonnegative*, the range is non-negative, regardless of the input data. Applies only to linear axes.\n    separatethousands: If \"true\", even 4-digit integers are separated\n    showaxeslabels: Sets whether or not this axis is labeled\n    showbackground: Sets whether or not this axis' wall has a background color.\n    showexponent: If *all*, all exponents are shown besides their significands. If *first*, only the exponent of the first tick is shown. If *last*, only the exponent of the last tick is shown. If *none*, no exponents appear.\n    showgrid: Determines whether or not grid lines are drawn. If *true*, the grid lines are drawn at every tick mark.\n    showline: Determines whether or not a line bounding this axis is drawn.\n    showspikes: Sets whether or not spikes starting from data points to this axis' wall are shown on hover.\n    showticklabels: Determines whether or not the tick labels are drawn.\n    showtickprefix: If *all*, all tick labels are displayed with a prefix. If *first*, only the first tick is displayed with a prefix. If *last*, only the last tick is displayed with a suffix. If *none*, tick prefixes are hidden.\n    showticksuffix: Same as `showtickprefix` but for tick suffixes.\n    spikecolor: Sets the color of the spikes.\n    spikesides: Sets whether or not spikes extending from the projection data points to this axis' wall boundaries are shown on hover.\n    spikethickness: Sets the thickness (in px) of the spikes.\n    tick0: Sets the placement of the first tick on this axis. Use with `dtick`. If the axis `type` is *log*, then you must take the log of your starting tick (e.g. to set the starting tick to 100, set the `tick0` to 2) except when `dtick`=*L<f>* (see `dtick` for more info). If the axis `type` is *date*, it should be a date string, like date data. If the axis `type` is *category*, it should be a number, using the scale where each category is assigned a serial number from zero in the order it appears.\n    tickangle: Sets the angle of the tick labels with respect to the horizontal. For example, a `tickangle` of -90 draws the tick labels vertically.\n    tickcolor: Sets the tick color.\n    tickfont: Sets the tick font.\n    tickformat: Sets the tick label formatting rule using d3 formatting mini-languages which are very similar to those in Python. For numbers, see: https://github.com/d3/d3-format/tree/v1.4.5#d3-format. And for dates see: https://github.com/d3/d3-time-format/tree/v2.2.3#locale_format. We add two items to d3's date formatter: *%h* for half of the year as a decimal number as well as *%{n}f* for fractional seconds with n digits. For example, *2016-10-13 09:15:23.456* with tickformat *%H~%M~%S.%2f* would display *09~15~23.46*\n    ticklen: Sets the tick length (in px).\n    tickmode: Sets the tick mode for this axis. If *auto*, the number of ticks is set via `nticks`. If *linear*, the placement of the ticks is determined by a starting position `tick0` and a tick step `dtick` (*linear* is the default value if `tick0` and `dtick` are provided). If *array*, the placement of the ticks is set via `tickvals` and the tick text is `ticktext`. (*array* is the default value if `tickvals` is provided).\n    tickprefix: Sets a tick label prefix.\n    ticks: Determines whether ticks are drawn or not. If **, this axis' ticks are not drawn. If *outside* (*inside*), this axis' are drawn outside (inside) the axis lines.\n    ticksuffix: Sets a tick label suffix.\n    ticktext: Sets the text displayed at the ticks position via `tickvals`. Only has an effect if `tickmode` is set to *array*. Used with `tickvals`.\n    tickvals: Sets the values at which ticks on this axis appear. Only has an effect if `tickmode` is set to *array*. Used with `ticktext`.\n    tickwidth: Sets the tick width (in px).\n    type: Sets the axis type. By default, plotly attempts to determined the axis type by looking into the data of the traces that referenced the axis in question.\n    visible: A single toggle to hide the axis while preserving interaction like dragging. Default is true when a cheater plot is present on the axis, otherwise false\n    zeroline: Determines whether or not a line is drawn at along the 0 value of this axis. If *true*, the zero line is drawn on top of the grid lines.\n    zerolinecolor: Sets the line color of the zero line.\n    zerolinewidth: Sets the width (in px) of the zero line."
        ...

class ZAxis(_PlotlyObject):
    "Create a new 'ZAxis' object"
    autorange: Any
    "Determines whether or not the range of this axis is computed in relation to the input data. See `rangemode` for more info. If `range` is provided and it has a value for both the lower and upper bound, `autorange` is set to *false*. Using *min* applies autorange only to set the minimum. Using *max* applies autorange only to set the maximum. Using *min reversed* applies autorange only to set the minimum on a reversed axis. Using *max reversed* applies autorange only to set the maximum on a reversed axis. Using *reversed* applies autorange on both ends and reverses the axis direction."
    @property
    def autorangeoptions(self) -> _plotly_graph_objs_layout_scene_zaxis.Autorangeoptions | Any:
        ...
    @autorangeoptions.setter
    def autorangeoptions(self, value: Any) -> None: ...
    autotypenumbers: Any
    "Using *strict* a numeric string in trace data is not converted to a number. Using *convert types* a numeric string in trace data may be treated as a number during automatic axis `type` detection. Defaults to layout.autotypenumbers."
    backgroundcolor: Any
    "Sets the background color of this axis' wall."
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
    gridwidth: float | Any
    "Sets the width (in px) of the grid lines."
    hoverformat: str | Any
    "Sets the hover text formatting rule using d3 formatting mini-languages which are very similar to those in Python. For numbers, see: https://github.com/d3/d3-format/tree/v1.4.5#d3-format. And for dates see: https://github.com/d3/d3-time-format/tree/v2.2.3#locale_format. We add two items to d3's date formatter: *%h* for half of the year as a decimal number as well as *%{n}f* for fractional seconds with n digits. For example, *2016-10-13 09:15:23.456* with tickformat *%H~%M~%S.%2f* would display *09~15~23.46*"
    labelalias: Any
    "Replacement text for specific tick or hover labels. For example using {US: 'USA', CA: 'Canada'} changes US to USA and CA to Canada. The labels we would have shown must match the keys exactly, after adding any tickprefix or ticksuffix. For negative numbers the minus sign symbol used (U+2212) is wider than the regular ascii dash. That means you need to use −1 instead of -1. labelalias can be used with any axis type, and both keys (if needed) and values (if desired) can include html-like tags or MathJax."
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
    mirror: Any
    "Determines if the axis lines or/and ticks are mirrored to the opposite side of the plotting area. If *true*, the axis lines are mirrored. If *ticks*, the axis lines and ticks are mirrored. If *false*, mirroring is disable. If *all*, axis lines are mirrored on all shared-axes subplots. If *allticks*, axis lines and ticks are mirrored on all shared-axes subplots."
    nticks: int | Any
    "Specifies the maximum number of ticks for the particular axis. The actual number of ticks will be chosen automatically to be less than or equal to `nticks`. Has an effect only if `tickmode` is set to *auto*."
    range: Any
    "Sets the range of this axis. If the axis `type` is *log*, then you must take the log of your desired range (e.g. to set the range from 1 to 100, set the range from 0 to 2). If the axis `type` is *date*, it should be date strings, like date data, though Date objects and unix milliseconds will be accepted and converted to strings. If the axis `type` is *category*, it should be numbers, using the scale where each category is assigned a serial number from zero in the order it appears. Leaving either or both elements `null` impacts the default `autorange`."
    rangemode: Any
    "If *normal*, the range is computed in relation to the extrema of the input data. If *tozero*, the range extends to 0, regardless of the input data If *nonnegative*, the range is non-negative, regardless of the input data. Applies only to linear axes."
    separatethousands: bool | Any
    "If \"true\", even 4-digit integers are separated"
    showaxeslabels: bool | Any
    "Sets whether or not this axis is labeled"
    showbackground: bool | Any
    "Sets whether or not this axis' wall has a background color."
    showexponent: Any
    "If *all*, all exponents are shown besides their significands. If *first*, only the exponent of the first tick is shown. If *last*, only the exponent of the last tick is shown. If *none*, no exponents appear."
    showgrid: bool | Any
    "Determines whether or not grid lines are drawn. If *true*, the grid lines are drawn at every tick mark."
    showline: bool | Any
    "Determines whether or not a line bounding this axis is drawn."
    showspikes: bool | Any
    "Sets whether or not spikes starting from data points to this axis' wall are shown on hover."
    showticklabels: bool | Any
    "Determines whether or not the tick labels are drawn."
    showtickprefix: Any
    "If *all*, all tick labels are displayed with a prefix. If *first*, only the first tick is displayed with a prefix. If *last*, only the last tick is displayed with a suffix. If *none*, tick prefixes are hidden."
    showticksuffix: Any
    "Same as `showtickprefix` but for tick suffixes."
    spikecolor: Any
    "Sets the color of the spikes."
    spikesides: bool | Any
    "Sets whether or not spikes extending from the projection data points to this axis' wall boundaries are shown on hover."
    spikethickness: float | Any
    "Sets the thickness (in px) of the spikes."
    tick0: Any
    "Sets the placement of the first tick on this axis. Use with `dtick`. If the axis `type` is *log*, then you must take the log of your starting tick (e.g. to set the starting tick to 100, set the `tick0` to 2) except when `dtick`=*L<f>* (see `dtick` for more info). If the axis `type` is *date*, it should be a date string, like date data. If the axis `type` is *category*, it should be a number, using the scale where each category is assigned a serial number from zero in the order it appears."
    tickangle: Any
    "Sets the angle of the tick labels with respect to the horizontal. For example, a `tickangle` of -90 draws the tick labels vertically."
    tickcolor: Any
    "Sets the tick color."
    @property
    def tickfont(self) -> _plotly_graph_objs_layout_scene_zaxis.Tickfont | Any:
        "Sets the tick font."
        ...
    @tickfont.setter
    def tickfont(self, value: Any) -> None: ...
    tickformat: str | Any
    "Sets the tick label formatting rule using d3 formatting mini-languages which are very similar to those in Python. For numbers, see: https://github.com/d3/d3-format/tree/v1.4.5#d3-format. And for dates see: https://github.com/d3/d3-time-format/tree/v2.2.3#locale_format. We add two items to d3's date formatter: *%h* for half of the year as a decimal number as well as *%{n}f* for fractional seconds with n digits. For example, *2016-10-13 09:15:23.456* with tickformat *%H~%M~%S.%2f* would display *09~15~23.46*"
    @property
    def tickformatstop(self) -> _plotly_graph_objs_layout_scene_zaxis.Tickformatstop | Any:
        ...
    @tickformatstop.setter
    def tickformatstop(self, value: Any) -> None: ...
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
    def title(self) -> _plotly_graph_objs_layout_scene_zaxis.Title | Any:
        ...
    @title.setter
    def title(self, value: Any) -> None: ...
    type: Any
    "Sets the axis type. By default, plotly attempts to determined the axis type by looking into the data of the traces that referenced the axis in question."
    visible: bool | Any
    "A single toggle to hide the axis while preserving interaction like dragging. Default is true when a cheater plot is present on the axis, otherwise false"
    zeroline: bool | Any
    "Determines whether or not a line is drawn at along the 0 value of this axis. If *true*, the zero line is drawn on top of the grid lines."
    zerolinecolor: Any
    "Sets the line color of the zero line."
    zerolinewidth: float | Any
    "Sets the width (in px) of the zero line."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        autorange: Any = ...,
        autorangeoptions: Any = ...,
        autotypenumbers: Any = ...,
        backgroundcolor: Any = ...,
        calendar: Any = ...,
        categoryarray: Any = ...,
        categoryorder: Any = ...,
        color: Any = ...,
        dtick: Any = ...,
        exponentformat: Any = ...,
        gridcolor: Any = ...,
        gridwidth: Any = ...,
        hoverformat: Any = ...,
        labelalias: Any = ...,
        linecolor: Any = ...,
        linewidth: Any = ...,
        maxallowed: Any = ...,
        minallowed: Any = ...,
        minexponent: Any = ...,
        mirror: Any = ...,
        nticks: Any = ...,
        range: Any = ...,
        rangemode: Any = ...,
        separatethousands: Any = ...,
        showaxeslabels: Any = ...,
        showbackground: Any = ...,
        showexponent: Any = ...,
        showgrid: Any = ...,
        showline: Any = ...,
        showspikes: Any = ...,
        showticklabels: Any = ...,
        showtickprefix: Any = ...,
        showticksuffix: Any = ...,
        spikecolor: Any = ...,
        spikesides: Any = ...,
        spikethickness: Any = ...,
        tick0: Any = ...,
        tickangle: Any = ...,
        tickcolor: Any = ...,
        tickfont: Any = ...,
        tickformat: Any = ...,
        tickformatstop: Any = ...,
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
        visible: Any = ...,
        zeroline: Any = ...,
        zerolinecolor: Any = ...,
        zerolinewidth: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'ZAxis' object\n\nArgs:\n    autorange: Determines whether or not the range of this axis is computed in relation to the input data. See `rangemode` for more info. If `range` is provided and it has a value for both the lower and upper bound, `autorange` is set to *false*. Using *min* applies autorange only to set the minimum. Using *max* applies autorange only to set the maximum. Using *min reversed* applies autorange only to set the minimum on a reversed axis. Using *max reversed* applies autorange only to set the maximum on a reversed axis. Using *reversed* applies autorange on both ends and reverses the axis direction.\n    autotypenumbers: Using *strict* a numeric string in trace data is not converted to a number. Using *convert types* a numeric string in trace data may be treated as a number during automatic axis `type` detection. Defaults to layout.autotypenumbers.\n    backgroundcolor: Sets the background color of this axis' wall.\n    calendar: Sets the calendar system to use for `range` and `tick0` if this is a date axis. This does not set the calendar for interpreting data on this axis, that's specified in the trace or via the global `layout.calendar`\n    categoryarray: Sets the order in which categories on this axis appear. Only has an effect if `categoryorder` is set to *array*. Used with `categoryorder`.\n    categoryorder: Specifies the ordering logic for the case of categorical variables. By default, plotly uses *trace*, which specifies the order that is present in the data supplied. Set `categoryorder` to *category ascending* or *category descending* if order should be determined by the alphanumerical order of the category names. Set `categoryorder` to *array* to derive the ordering from the attribute `categoryarray`. If a category is not found in the `categoryarray` array, the sorting behavior for that attribute will be identical to the *trace* mode. The unspecified categories will follow the categories in `categoryarray`. Set `categoryorder` to *total ascending* or *total descending* if order should be determined by the numerical order of the values. Similarly, the order can be determined by the min, max, sum, mean, geometric mean or median of all the values.\n    color: Sets default for all colors associated with this axis all at once: line, font, tick, and grid colors. Grid color is lightened by blending this with the plot background Individual pieces can override this.\n    dtick: Sets the step in-between ticks on this axis. Use with `tick0`. Must be a positive number, or special strings available to *log* and *date* axes. If the axis `type` is *log*, then ticks are set every 10^(n*dtick) where n is the tick number. For example, to set a tick mark at 1, 10, 100, 1000, ... set dtick to 1. To set tick marks at 1, 100, 10000, ... set dtick to 2. To set tick marks at 1, 5, 25, 125, 625, 3125, ... set dtick to log_10(5), or 0.69897000433. *log* has several special values; *L<f>*, where `f` is a positive number, gives ticks linearly spaced in value (but not position). For example `tick0` = 0.1, `dtick` = *L0.5* will put ticks at 0.1, 0.6, 1.1, 1.6 etc. To show powers of 10 plus small digits between, use *D1* (all digits) or *D2* (only 2 and 5). `tick0` is ignored for *D1* and *D2*. If the axis `type` is *date*, then you must convert the time to milliseconds. For example, to set the interval between ticks to one day, set `dtick` to 86400000.0. *date* also has special values *M<n>* gives ticks spaced by a number of months. `n` must be a positive integer. To set ticks on the 15th of every third month, set `tick0` to *2000-01-15* and `dtick` to *M3*. To set ticks every 4 years, set `dtick` to *M48*\n    exponentformat: Determines a formatting rule for the tick exponents. For example, consider the number 1,000,000,000. If *none*, it appears as 1,000,000,000. If *e*, 1e+9. If *E*, 1E+9. If *power*, 1x10^9 (with 9 in a super script). If *SI*, 1G. If *B*, 1B. *SI* uses prefixes from \"femto\" f (10^-15) to \"tera\" T (10^12). *SI extended* covers instead the full SI range from \"quecto\" q (10^-30) to \"quetta\" Q (10^30). If *SI* or *SI extended* is used and the exponent is beyond the above ranges, the formatting rule will automatically be switched to the power notation.\n    gridcolor: Sets the color of the grid lines.\n    gridwidth: Sets the width (in px) of the grid lines.\n    hoverformat: Sets the hover text formatting rule using d3 formatting mini-languages which are very similar to those in Python. For numbers, see: https://github.com/d3/d3-format/tree/v1.4.5#d3-format. And for dates see: https://github.com/d3/d3-time-format/tree/v2.2.3#locale_format. We add two items to d3's date formatter: *%h* for half of the year as a decimal number as well as *%{n}f* for fractional seconds with n digits. For example, *2016-10-13 09:15:23.456* with tickformat *%H~%M~%S.%2f* would display *09~15~23.46*\n    labelalias: Replacement text for specific tick or hover labels. For example using {US: 'USA', CA: 'Canada'} changes US to USA and CA to Canada. The labels we would have shown must match the keys exactly, after adding any tickprefix or ticksuffix. For negative numbers the minus sign symbol used (U+2212) is wider than the regular ascii dash. That means you need to use −1 instead of -1. labelalias can be used with any axis type, and both keys (if needed) and values (if desired) can include html-like tags or MathJax.\n    linecolor: Sets the axis line color.\n    linewidth: Sets the width (in px) of the axis line.\n    maxallowed: Determines the maximum range of this axis.\n    minallowed: Determines the minimum range of this axis.\n    minexponent: Hide SI prefix for 10^n if |n| is below this number. This only has an effect when `tickformat` is *SI* or *B*.\n    mirror: Determines if the axis lines or/and ticks are mirrored to the opposite side of the plotting area. If *true*, the axis lines are mirrored. If *ticks*, the axis lines and ticks are mirrored. If *false*, mirroring is disable. If *all*, axis lines are mirrored on all shared-axes subplots. If *allticks*, axis lines and ticks are mirrored on all shared-axes subplots.\n    nticks: Specifies the maximum number of ticks for the particular axis. The actual number of ticks will be chosen automatically to be less than or equal to `nticks`. Has an effect only if `tickmode` is set to *auto*.\n    range: Sets the range of this axis. If the axis `type` is *log*, then you must take the log of your desired range (e.g. to set the range from 1 to 100, set the range from 0 to 2). If the axis `type` is *date*, it should be date strings, like date data, though Date objects and unix milliseconds will be accepted and converted to strings. If the axis `type` is *category*, it should be numbers, using the scale where each category is assigned a serial number from zero in the order it appears. Leaving either or both elements `null` impacts the default `autorange`.\n    rangemode: If *normal*, the range is computed in relation to the extrema of the input data. If *tozero*, the range extends to 0, regardless of the input data If *nonnegative*, the range is non-negative, regardless of the input data. Applies only to linear axes.\n    separatethousands: If \"true\", even 4-digit integers are separated\n    showaxeslabels: Sets whether or not this axis is labeled\n    showbackground: Sets whether or not this axis' wall has a background color.\n    showexponent: If *all*, all exponents are shown besides their significands. If *first*, only the exponent of the first tick is shown. If *last*, only the exponent of the last tick is shown. If *none*, no exponents appear.\n    showgrid: Determines whether or not grid lines are drawn. If *true*, the grid lines are drawn at every tick mark.\n    showline: Determines whether or not a line bounding this axis is drawn.\n    showspikes: Sets whether or not spikes starting from data points to this axis' wall are shown on hover.\n    showticklabels: Determines whether or not the tick labels are drawn.\n    showtickprefix: If *all*, all tick labels are displayed with a prefix. If *first*, only the first tick is displayed with a prefix. If *last*, only the last tick is displayed with a suffix. If *none*, tick prefixes are hidden.\n    showticksuffix: Same as `showtickprefix` but for tick suffixes.\n    spikecolor: Sets the color of the spikes.\n    spikesides: Sets whether or not spikes extending from the projection data points to this axis' wall boundaries are shown on hover.\n    spikethickness: Sets the thickness (in px) of the spikes.\n    tick0: Sets the placement of the first tick on this axis. Use with `dtick`. If the axis `type` is *log*, then you must take the log of your starting tick (e.g. to set the starting tick to 100, set the `tick0` to 2) except when `dtick`=*L<f>* (see `dtick` for more info). If the axis `type` is *date*, it should be a date string, like date data. If the axis `type` is *category*, it should be a number, using the scale where each category is assigned a serial number from zero in the order it appears.\n    tickangle: Sets the angle of the tick labels with respect to the horizontal. For example, a `tickangle` of -90 draws the tick labels vertically.\n    tickcolor: Sets the tick color.\n    tickfont: Sets the tick font.\n    tickformat: Sets the tick label formatting rule using d3 formatting mini-languages which are very similar to those in Python. For numbers, see: https://github.com/d3/d3-format/tree/v1.4.5#d3-format. And for dates see: https://github.com/d3/d3-time-format/tree/v2.2.3#locale_format. We add two items to d3's date formatter: *%h* for half of the year as a decimal number as well as *%{n}f* for fractional seconds with n digits. For example, *2016-10-13 09:15:23.456* with tickformat *%H~%M~%S.%2f* would display *09~15~23.46*\n    ticklen: Sets the tick length (in px).\n    tickmode: Sets the tick mode for this axis. If *auto*, the number of ticks is set via `nticks`. If *linear*, the placement of the ticks is determined by a starting position `tick0` and a tick step `dtick` (*linear* is the default value if `tick0` and `dtick` are provided). If *array*, the placement of the ticks is set via `tickvals` and the tick text is `ticktext`. (*array* is the default value if `tickvals` is provided).\n    tickprefix: Sets a tick label prefix.\n    ticks: Determines whether ticks are drawn or not. If **, this axis' ticks are not drawn. If *outside* (*inside*), this axis' are drawn outside (inside) the axis lines.\n    ticksuffix: Sets a tick label suffix.\n    ticktext: Sets the text displayed at the ticks position via `tickvals`. Only has an effect if `tickmode` is set to *array*. Used with `tickvals`.\n    tickvals: Sets the values at which ticks on this axis appear. Only has an effect if `tickmode` is set to *array*. Used with `ticktext`.\n    tickwidth: Sets the tick width (in px).\n    type: Sets the axis type. By default, plotly attempts to determined the axis type by looking into the data of the traces that referenced the axis in question.\n    visible: A single toggle to hide the axis while preserving interaction like dragging. Default is true when a cheater plot is present on the axis, otherwise false\n    zeroline: Determines whether or not a line is drawn at along the 0 value of this axis. If *true*, the zero line is drawn on top of the grid lines.\n    zerolinecolor: Sets the line color of the zero line.\n    zerolinewidth: Sets the width (in px) of the zero line."
        ...
