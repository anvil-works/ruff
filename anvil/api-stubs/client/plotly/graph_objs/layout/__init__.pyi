# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the Plotly catalogue generator in doc/anvil-api-stubs/plotly-stubs.mjs instead, then run:
#   pnpm -F docs build
#
from plotly._base import _PlotlyObject
from typing import Any, Mapping
import plotly.graph_objs.layout.annotation as _plotly_graph_objs_layout_annotation
import plotly.graph_objs.layout.annotation as annotation
import plotly.graph_objs.layout.coloraxis as _plotly_graph_objs_layout_coloraxis
import plotly.graph_objs.layout.coloraxis as coloraxis
import plotly.graph_objs.layout.geo as _plotly_graph_objs_layout_geo
import plotly.graph_objs.layout.geo as geo
import plotly.graph_objs.layout.grid as _plotly_graph_objs_layout_grid
import plotly.graph_objs.layout.grid as grid
import plotly.graph_objs.layout.hoverlabel as _plotly_graph_objs_layout_hoverlabel
import plotly.graph_objs.layout.hoverlabel as hoverlabel
import plotly.graph_objs.layout.legend as _plotly_graph_objs_layout_legend
import plotly.graph_objs.layout.legend as legend
import plotly.graph_objs.layout.map as _plotly_graph_objs_layout_map
import plotly.graph_objs.layout.map as map
import plotly.graph_objs.layout.mapbox as _plotly_graph_objs_layout_mapbox
import plotly.graph_objs.layout.mapbox as mapbox
import plotly.graph_objs.layout.newselection as _plotly_graph_objs_layout_newselection
import plotly.graph_objs.layout.newselection as newselection
import plotly.graph_objs.layout.newshape as _plotly_graph_objs_layout_newshape
import plotly.graph_objs.layout.newshape as newshape
import plotly.graph_objs.layout.polar as _plotly_graph_objs_layout_polar
import plotly.graph_objs.layout.polar as polar
import plotly.graph_objs.layout.scene as _plotly_graph_objs_layout_scene
import plotly.graph_objs.layout.scene as scene
import plotly.graph_objs.layout.selection as _plotly_graph_objs_layout_selection
import plotly.graph_objs.layout.selection as selection
import plotly.graph_objs.layout.shape as _plotly_graph_objs_layout_shape
import plotly.graph_objs.layout.shape as shape
import plotly.graph_objs.layout.slider as _plotly_graph_objs_layout_slider
import plotly.graph_objs.layout.slider as slider
import plotly.graph_objs.layout.smith as _plotly_graph_objs_layout_smith
import plotly.graph_objs.layout.smith as smith
import plotly.graph_objs.layout.ternary as _plotly_graph_objs_layout_ternary
import plotly.graph_objs.layout.ternary as ternary
import plotly.graph_objs.layout.title as _plotly_graph_objs_layout_title
import plotly.graph_objs.layout.title as title
import plotly.graph_objs.layout.updatemenu as _plotly_graph_objs_layout_updatemenu
import plotly.graph_objs.layout.updatemenu as updatemenu
import plotly.graph_objs.layout.xaxis as _plotly_graph_objs_layout_xaxis
import plotly.graph_objs.layout.xaxis as xaxis
import plotly.graph_objs.layout.yaxis as _plotly_graph_objs_layout_yaxis
import plotly.graph_objs.layout.yaxis as yaxis

class Activeselection(_PlotlyObject):
    "Create a new 'Activeselection' object"
    fillcolor: Any
    "Sets the color filling the active selection' interior."
    opacity: float | Any
    "Sets the opacity of the active selection."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        fillcolor: Any = ...,
        opacity: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Activeselection' object\n\nArgs:\n    fillcolor: Sets the color filling the active selection' interior.\n    opacity: Sets the opacity of the active selection."
        ...

class Activeshape(_PlotlyObject):
    "Create a new 'Activeshape' object"
    fillcolor: Any
    "Sets the color filling the active shape' interior."
    opacity: float | Any
    "Sets the opacity of the active shape."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        fillcolor: Any = ...,
        opacity: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Activeshape' object\n\nArgs:\n    fillcolor: Sets the color filling the active shape' interior.\n    opacity: Sets the opacity of the active shape."
        ...

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
    ax: Any
    "Sets the x component of the arrow tail about the arrow head. If `axref` is `pixel`, a positive (negative) component corresponds to an arrow pointing from right to left (left to right). If `axref` is not `pixel` and is exactly the same as `xref`, this is an absolute value on that axis, like `x`, specified in the same coordinates as `xref`."
    axref: Any
    "Indicates in what coordinates the tail of the annotation (ax,ay) is specified. If set to a x axis id (e.g. *x* or *x2*), the `x` position refers to a x coordinate. If set to *paper*, the `x` position refers to the distance from the left of the plotting area in normalized coordinates where *0* (*1*) corresponds to the left (right). If set to a x axis ID followed by *domain* (separated by a space), the position behaves like for *paper*, but refers to the distance in fractions of the domain length from the left of the domain of that axis: e.g., *x2 domain* refers to the domain of the second x axis and a x position of 0.5 refers to the point between the left and the right of the domain of the second x axis. In order for absolute positioning of the arrow to work, *axref* must be exactly the same as *xref*, otherwise *axref* will revert to *pixel* (explained next). For relative positioning, *axref* can be set to *pixel*, in which case the *ax* value is specified in pixels relative to *x*. Absolute positioning is useful for trendline annotations which should continue to indicate the correct trend when zoomed. Relative positioning is useful for specifying the text offset for an annotated point."
    ay: Any
    "Sets the y component of the arrow tail about the arrow head. If `ayref` is `pixel`, a positive (negative) component corresponds to an arrow pointing from bottom to top (top to bottom). If `ayref` is not `pixel` and is exactly the same as `yref`, this is an absolute value on that axis, like `y`, specified in the same coordinates as `yref`."
    ayref: Any
    "Indicates in what coordinates the tail of the annotation (ax,ay) is specified. If set to a y axis id (e.g. *y* or *y2*), the `y` position refers to a y coordinate. If set to *paper*, the `y` position refers to the distance from the bottom of the plotting area in normalized coordinates where *0* (*1*) corresponds to the bottom (top). If set to a y axis ID followed by *domain* (separated by a space), the position behaves like for *paper*, but refers to the distance in fractions of the domain length from the bottom of the domain of that axis: e.g., *y2 domain* refers to the domain of the second y axis and a y position of 0.5 refers to the point between the bottom and the top of the domain of the second y axis. In order for absolute positioning of the arrow to work, *ayref* must be exactly the same as *yref*, otherwise *ayref* will revert to *pixel* (explained next). For relative positioning, *ayref* can be set to *pixel*, in which case the *ay* value is specified in pixels relative to *y*. Absolute positioning is useful for trendline annotations which should continue to indicate the correct trend when zoomed. Relative positioning is useful for specifying the text offset for an annotated point."
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
    clicktoshow: Any
    "Makes this annotation respond to clicks on the plot. If you click a data point that exactly matches the `x` and `y` values of this annotation, and it is hidden (visible: false), it will appear. In *onoff* mode, you must click the same point again to make it disappear, so if you click multiple points, you can show multiple annotations. In *onout* mode, a click anywhere else in the plot (on another data point or not) will hide this annotation. If you need to show/hide this annotation in response to different `x` or `y` values, you can set `xclick` and/or `yclick`. This is useful for example to label the side of a bar. To label markers though, `standoff` is preferred over `xclick` and `yclick`."
    @property
    def font(self) -> _plotly_graph_objs_layout_annotation.Font | Any:
        "Sets the annotation text font."
        ...
    @font.setter
    def font(self, value: Any) -> None: ...
    height: float | Any
    "Sets an explicit height for the text box. null (default) lets the text set the box height. Taller text will be clipped."
    @property
    def hoverlabel(self) -> _plotly_graph_objs_layout_annotation.Hoverlabel | Any:
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
    "Sets the annotation's x position. If the axis `type` is *log*, then you must take the log of your desired range. If the axis `type` is *date*, it should be date strings, like date data, though Date objects and unix milliseconds will be accepted and converted to strings. If the axis `type` is *category*, it should be numbers, using the scale where each category is assigned a serial number from zero in the order it appears."
    xanchor: Any
    "Sets the text box's horizontal position anchor This anchor binds the `x` position to the *left*, *center* or *right* of the annotation. For example, if `x` is set to 1, `xref` to *paper* and `xanchor` to *right* then the right-most portion of the annotation lines up with the right-most edge of the plotting area. If *auto*, the anchor is equivalent to *center* for data-referenced annotations or if there is an arrow, whereas for paper-referenced with no arrow, the anchor picked corresponds to the closest side."
    xclick: Any
    "Toggle this annotation when clicking a data point whose `x` value is `xclick` rather than the annotation's `x` value."
    xref: Any
    "Sets the annotation's x coordinate axis. If set to a x axis id (e.g. *x* or *x2*), the `x` position refers to a x coordinate. If set to *paper*, the `x` position refers to the distance from the left of the plotting area in normalized coordinates where *0* (*1*) corresponds to the left (right). If set to a x axis ID followed by *domain* (separated by a space), the position behaves like for *paper*, but refers to the distance in fractions of the domain length from the left of the domain of that axis: e.g., *x2 domain* refers to the domain of the second x axis and a x position of 0.5 refers to the point between the left and the right of the domain of the second x axis."
    xshift: float | Any
    "Shifts the position of the whole annotation and arrow to the right (positive) or left (negative) by this many pixels."
    y: Any
    "Sets the annotation's y position. If the axis `type` is *log*, then you must take the log of your desired range. If the axis `type` is *date*, it should be date strings, like date data, though Date objects and unix milliseconds will be accepted and converted to strings. If the axis `type` is *category*, it should be numbers, using the scale where each category is assigned a serial number from zero in the order it appears."
    yanchor: Any
    "Sets the text box's vertical position anchor This anchor binds the `y` position to the *top*, *middle* or *bottom* of the annotation. For example, if `y` is set to 1, `yref` to *paper* and `yanchor` to *top* then the top-most portion of the annotation lines up with the top-most edge of the plotting area. If *auto*, the anchor is equivalent to *middle* for data-referenced annotations or if there is an arrow, whereas for paper-referenced with no arrow, the anchor picked corresponds to the closest side."
    yclick: Any
    "Toggle this annotation when clicking a data point whose `y` value is `yclick` rather than the annotation's `y` value."
    yref: Any
    "Sets the annotation's y coordinate axis. If set to a y axis id (e.g. *y* or *y2*), the `y` position refers to a y coordinate. If set to *paper*, the `y` position refers to the distance from the bottom of the plotting area in normalized coordinates where *0* (*1*) corresponds to the bottom (top). If set to a y axis ID followed by *domain* (separated by a space), the position behaves like for *paper*, but refers to the distance in fractions of the domain length from the bottom of the domain of that axis: e.g., *y2 domain* refers to the domain of the second y axis and a y position of 0.5 refers to the point between the bottom and the top of the domain of the second y axis."
    yshift: float | Any
    "Shifts the position of the whole annotation and arrow up (positive) or down (negative) by this many pixels."
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
        axref: Any = ...,
        ay: Any = ...,
        ayref: Any = ...,
        bgcolor: Any = ...,
        bordercolor: Any = ...,
        borderpad: Any = ...,
        borderwidth: Any = ...,
        captureevents: Any = ...,
        clicktoshow: Any = ...,
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
        xclick: Any = ...,
        xref: Any = ...,
        xshift: Any = ...,
        y: Any = ...,
        yanchor: Any = ...,
        yclick: Any = ...,
        yref: Any = ...,
        yshift: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Annotation' object\n\nArgs:\n    align: Sets the horizontal alignment of the `text` within the box. Has an effect only if `text` spans two or more lines (i.e. `text` contains one or more <br> HTML tags) or if an explicit width is set to override the text width.\n    arrowcolor: Sets the color of the annotation arrow.\n    arrowhead: Sets the end annotation arrow head style.\n    arrowside: Sets the annotation arrow head position.\n    arrowsize: Sets the size of the end annotation arrow head, relative to `arrowwidth`. A value of 1 (default) gives a head about 3x as wide as the line.\n    arrowwidth: Sets the width (in px) of annotation arrow line.\n    ax: Sets the x component of the arrow tail about the arrow head. If `axref` is `pixel`, a positive (negative) component corresponds to an arrow pointing from right to left (left to right). If `axref` is not `pixel` and is exactly the same as `xref`, this is an absolute value on that axis, like `x`, specified in the same coordinates as `xref`.\n    axref: Indicates in what coordinates the tail of the annotation (ax,ay) is specified. If set to a x axis id (e.g. *x* or *x2*), the `x` position refers to a x coordinate. If set to *paper*, the `x` position refers to the distance from the left of the plotting area in normalized coordinates where *0* (*1*) corresponds to the left (right). If set to a x axis ID followed by *domain* (separated by a space), the position behaves like for *paper*, but refers to the distance in fractions of the domain length from the left of the domain of that axis: e.g., *x2 domain* refers to the domain of the second x axis and a x position of 0.5 refers to the point between the left and the right of the domain of the second x axis. In order for absolute positioning of the arrow to work, *axref* must be exactly the same as *xref*, otherwise *axref* will revert to *pixel* (explained next). For relative positioning, *axref* can be set to *pixel*, in which case the *ax* value is specified in pixels relative to *x*. Absolute positioning is useful for trendline annotations which should continue to indicate the correct trend when zoomed. Relative positioning is useful for specifying the text offset for an annotated point.\n    ay: Sets the y component of the arrow tail about the arrow head. If `ayref` is `pixel`, a positive (negative) component corresponds to an arrow pointing from bottom to top (top to bottom). If `ayref` is not `pixel` and is exactly the same as `yref`, this is an absolute value on that axis, like `y`, specified in the same coordinates as `yref`.\n    ayref: Indicates in what coordinates the tail of the annotation (ax,ay) is specified. If set to a y axis id (e.g. *y* or *y2*), the `y` position refers to a y coordinate. If set to *paper*, the `y` position refers to the distance from the bottom of the plotting area in normalized coordinates where *0* (*1*) corresponds to the bottom (top). If set to a y axis ID followed by *domain* (separated by a space), the position behaves like for *paper*, but refers to the distance in fractions of the domain length from the bottom of the domain of that axis: e.g., *y2 domain* refers to the domain of the second y axis and a y position of 0.5 refers to the point between the bottom and the top of the domain of the second y axis. In order for absolute positioning of the arrow to work, *ayref* must be exactly the same as *yref*, otherwise *ayref* will revert to *pixel* (explained next). For relative positioning, *ayref* can be set to *pixel*, in which case the *ay* value is specified in pixels relative to *y*. Absolute positioning is useful for trendline annotations which should continue to indicate the correct trend when zoomed. Relative positioning is useful for specifying the text offset for an annotated point.\n    bgcolor: Sets the background color of the annotation.\n    bordercolor: Sets the color of the border enclosing the annotation `text`.\n    borderpad: Sets the padding (in px) between the `text` and the enclosing border.\n    borderwidth: Sets the width (in px) of the border enclosing the annotation `text`.\n    captureevents: Determines whether the annotation text box captures mouse move and click events, or allows those events to pass through to data points in the plot that may be behind the annotation. By default `captureevents` is *false* unless `hovertext` is provided. If you use the event `plotly_clickannotation` without `hovertext` you must explicitly enable `captureevents`.\n    clicktoshow: Makes this annotation respond to clicks on the plot. If you click a data point that exactly matches the `x` and `y` values of this annotation, and it is hidden (visible: false), it will appear. In *onoff* mode, you must click the same point again to make it disappear, so if you click multiple points, you can show multiple annotations. In *onout* mode, a click anywhere else in the plot (on another data point or not) will hide this annotation. If you need to show/hide this annotation in response to different `x` or `y` values, you can set `xclick` and/or `yclick`. This is useful for example to label the side of a bar. To label markers though, `standoff` is preferred over `xclick` and `yclick`.\n    font: Sets the annotation text font.\n    height: Sets an explicit height for the text box. null (default) lets the text set the box height. Taller text will be clipped.\n    hovertext: Sets text to appear when hovering over this annotation. If omitted or blank, no hover label will appear.\n    name: When used in a template, named items are created in the output figure in addition to any items the figure already has in this array. You can modify these items in the output figure by making your own item with `templateitemname` matching this `name` alongside your modifications (including `visible: false` or `enabled: false` to hide it). Has no effect outside of a template.\n    opacity: Sets the opacity of the annotation (text + arrow).\n    showarrow: Determines whether or not the annotation is drawn with an arrow. If *true*, `text` is placed near the arrow's tail. If *false*, `text` lines up with the `x` and `y` provided.\n    standoff: Sets a distance, in pixels, to move the end arrowhead away from the position it is pointing at, for example to point at the edge of a marker independent of zoom. Note that this shortens the arrow from the `ax` / `ay` vector, in contrast to `xshift` / `yshift` which moves everything by this amount.\n    startarrowhead: Sets the start annotation arrow head style.\n    startarrowsize: Sets the size of the start annotation arrow head, relative to `arrowwidth`. A value of 1 (default) gives a head about 3x as wide as the line.\n    startstandoff: Sets a distance, in pixels, to move the start arrowhead away from the position it is pointing at, for example to point at the edge of a marker independent of zoom. Note that this shortens the arrow from the `ax` / `ay` vector, in contrast to `xshift` / `yshift` which moves everything by this amount.\n    templateitemname: Used to refer to a named item in this array in the template. Named items from the template will be created even without a matching item in the input figure, but you can modify one by making an item with `templateitemname` matching its `name`, alongside your modifications (including `visible: false` or `enabled: false` to hide it). If there is no template or no matching item, this item will be hidden unless you explicitly show it with `visible: true`.\n    text: Sets the text associated with this annotation. Plotly uses a subset of HTML tags to do things like newline (`<br>`), bold (`<b></b>`), italics (`<i></i>`), hyperlinks (`<a href='...'></a>`). Tags `<em>`, `<sup>`, `<sub>`, `<s>`, `<u>`, and `<span>` are also supported.\n    textangle: Sets the angle at which the `text` is drawn with respect to the horizontal.\n    valign: Sets the vertical alignment of the `text` within the box. Has an effect only if an explicit height is set to override the text height.\n    visible: Determines whether or not this annotation is visible.\n    width: Sets an explicit width for the text box. null (default) lets the text set the box width. Wider text will be clipped. There is no automatic wrapping; use <br> to start a new line.\n    x: Sets the annotation's x position. If the axis `type` is *log*, then you must take the log of your desired range. If the axis `type` is *date*, it should be date strings, like date data, though Date objects and unix milliseconds will be accepted and converted to strings. If the axis `type` is *category*, it should be numbers, using the scale where each category is assigned a serial number from zero in the order it appears.\n    xanchor: Sets the text box's horizontal position anchor This anchor binds the `x` position to the *left*, *center* or *right* of the annotation. For example, if `x` is set to 1, `xref` to *paper* and `xanchor` to *right* then the right-most portion of the annotation lines up with the right-most edge of the plotting area. If *auto*, the anchor is equivalent to *center* for data-referenced annotations or if there is an arrow, whereas for paper-referenced with no arrow, the anchor picked corresponds to the closest side.\n    xclick: Toggle this annotation when clicking a data point whose `x` value is `xclick` rather than the annotation's `x` value.\n    xref: Sets the annotation's x coordinate axis. If set to a x axis id (e.g. *x* or *x2*), the `x` position refers to a x coordinate. If set to *paper*, the `x` position refers to the distance from the left of the plotting area in normalized coordinates where *0* (*1*) corresponds to the left (right). If set to a x axis ID followed by *domain* (separated by a space), the position behaves like for *paper*, but refers to the distance in fractions of the domain length from the left of the domain of that axis: e.g., *x2 domain* refers to the domain of the second x axis and a x position of 0.5 refers to the point between the left and the right of the domain of the second x axis.\n    xshift: Shifts the position of the whole annotation and arrow to the right (positive) or left (negative) by this many pixels.\n    y: Sets the annotation's y position. If the axis `type` is *log*, then you must take the log of your desired range. If the axis `type` is *date*, it should be date strings, like date data, though Date objects and unix milliseconds will be accepted and converted to strings. If the axis `type` is *category*, it should be numbers, using the scale where each category is assigned a serial number from zero in the order it appears.\n    yanchor: Sets the text box's vertical position anchor This anchor binds the `y` position to the *top*, *middle* or *bottom* of the annotation. For example, if `y` is set to 1, `yref` to *paper* and `yanchor` to *top* then the top-most portion of the annotation lines up with the top-most edge of the plotting area. If *auto*, the anchor is equivalent to *middle* for data-referenced annotations or if there is an arrow, whereas for paper-referenced with no arrow, the anchor picked corresponds to the closest side.\n    yclick: Toggle this annotation when clicking a data point whose `y` value is `yclick` rather than the annotation's `y` value.\n    yref: Sets the annotation's y coordinate axis. If set to a y axis id (e.g. *y* or *y2*), the `y` position refers to a y coordinate. If set to *paper*, the `y` position refers to the distance from the bottom of the plotting area in normalized coordinates where *0* (*1*) corresponds to the bottom (top). If set to a y axis ID followed by *domain* (separated by a space), the position behaves like for *paper*, but refers to the distance in fractions of the domain length from the bottom of the domain of that axis: e.g., *y2 domain* refers to the domain of the second y axis and a y position of 0.5 refers to the point between the bottom and the top of the domain of the second y axis.\n    yshift: Shifts the position of the whole annotation and arrow up (positive) or down (negative) by this many pixels."
        ...

class Coloraxis(_PlotlyObject):
    "Create a new 'Coloraxis' object"
    autocolorscale: bool | Any
    "Determines whether the colorscale is a default palette (`autocolorscale: true`) or the palette determined by `colorscale`. In case `colorscale` is unspecified or `autocolorscale` is true, the default palette will be chosen according to whether numbers in the `color` array are all positive, all negative or mixed."
    cauto: bool | Any
    "Determines whether or not the color domain is computed with respect to the input data (here corresponding trace color array(s)) or the bounds set in `cmin` and `cmax` Defaults to `false` when `cmin` and `cmax` are set by the user."
    cmax: float | Any
    "Sets the upper bound of the color domain. Value should have the same units as corresponding trace color array(s) and if set, `cmin` must be set as well."
    cmid: float | Any
    "Sets the mid-point of the color domain by scaling `cmin` and/or `cmax` to be equidistant to this point. Value should have the same units as corresponding trace color array(s). Has no effect when `cauto` is `false`."
    cmin: float | Any
    "Sets the lower bound of the color domain. Value should have the same units as corresponding trace color array(s) and if set, `cmax` must be set as well."
    @property
    def colorbar(self) -> _plotly_graph_objs_layout_coloraxis.ColorBar | Any:
        ...
    @colorbar.setter
    def colorbar(self, value: Any) -> None: ...
    colorscale: Any
    "Sets the colorscale. The colorscale must be an array containing arrays mapping a normalized value to an rgb, rgba, hex, hsl, hsla, hwb, or named color string. At minimum, a mapping for the lowest (0) and highest (1) values are required. For example, `[[0, 'rgb(0,0,255)'], [1, 'rgb(255,0,0)']]`. To control the bounds of the colorscale in color space, use `cmin` and `cmax`. Alternatively, `colorscale` may be a palette name string of the following list: Blackbody,Bluered,Blues,Cividis,Earth,Electric,Greens,Greys,Hot,Jet,Picnic,Portland,Rainbow,RdBu,Reds,Viridis,YlGnBu,YlOrRd."
    reversescale: bool | Any
    "Reverses the color mapping if true. If true, `cmin` will correspond to the last color in the array and `cmax` will correspond to the first color."
    showscale: bool | Any
    "Determines whether or not a colorbar is displayed for this trace."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        autocolorscale: Any = ...,
        cauto: Any = ...,
        cmax: Any = ...,
        cmid: Any = ...,
        cmin: Any = ...,
        colorbar: Any = ...,
        colorscale: Any = ...,
        reversescale: Any = ...,
        showscale: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Coloraxis' object\n\nArgs:\n    autocolorscale: Determines whether the colorscale is a default palette (`autocolorscale: true`) or the palette determined by `colorscale`. In case `colorscale` is unspecified or `autocolorscale` is true, the default palette will be chosen according to whether numbers in the `color` array are all positive, all negative or mixed.\n    cauto: Determines whether or not the color domain is computed with respect to the input data (here corresponding trace color array(s)) or the bounds set in `cmin` and `cmax` Defaults to `false` when `cmin` and `cmax` are set by the user.\n    cmax: Sets the upper bound of the color domain. Value should have the same units as corresponding trace color array(s) and if set, `cmin` must be set as well.\n    cmid: Sets the mid-point of the color domain by scaling `cmin` and/or `cmax` to be equidistant to this point. Value should have the same units as corresponding trace color array(s). Has no effect when `cauto` is `false`.\n    cmin: Sets the lower bound of the color domain. Value should have the same units as corresponding trace color array(s) and if set, `cmax` must be set as well.\n    colorscale: Sets the colorscale. The colorscale must be an array containing arrays mapping a normalized value to an rgb, rgba, hex, hsl, hsla, hwb, or named color string. At minimum, a mapping for the lowest (0) and highest (1) values are required. For example, `[[0, 'rgb(0,0,255)'], [1, 'rgb(255,0,0)']]`. To control the bounds of the colorscale in color space, use `cmin` and `cmax`. Alternatively, `colorscale` may be a palette name string of the following list: Blackbody,Bluered,Blues,Cividis,Earth,Electric,Greens,Greys,Hot,Jet,Picnic,Portland,Rainbow,RdBu,Reds,Viridis,YlGnBu,YlOrRd.\n    reversescale: Reverses the color mapping if true. If true, `cmin` will correspond to the last color in the array and `cmax` will correspond to the first color.\n    showscale: Determines whether or not a colorbar is displayed for this trace."
        ...

class Colorscale(_PlotlyObject):
    "Create a new 'Colorscale' object"
    diverging: Any
    "Sets the default diverging colorscale. Note that `autocolorscale` must be true for this attribute to work."
    sequential: Any
    "Sets the default sequential colorscale for positive values. Note that `autocolorscale` must be true for this attribute to work."
    sequentialminus: Any
    "Sets the default sequential colorscale for negative values. Note that `autocolorscale` must be true for this attribute to work."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        diverging: Any = ...,
        sequential: Any = ...,
        sequentialminus: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Colorscale' object\n\nArgs:\n    diverging: Sets the default diverging colorscale. Note that `autocolorscale` must be true for this attribute to work.\n    sequential: Sets the default sequential colorscale for positive values. Note that `autocolorscale` must be true for this attribute to work.\n    sequentialminus: Sets the default sequential colorscale for negative values. Note that `autocolorscale` must be true for this attribute to work."
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

class Geo(_PlotlyObject):
    "Create a new 'Geo' object"
    bgcolor: Any
    "Set the background color of the map"
    @property
    def center(self) -> _plotly_graph_objs_layout_geo.Center | Any:
        ...
    @center.setter
    def center(self, value: Any) -> None: ...
    coastlinecolor: Any
    "Sets the coastline color."
    coastlinewidth: float | Any
    "Sets the coastline stroke width (in px)."
    countrycolor: Any
    "Sets line color of the country boundaries."
    countrywidth: float | Any
    "Sets line width (in px) of the country boundaries."
    @property
    def domain(self) -> _plotly_graph_objs_layout_geo.Domain | Any:
        ...
    @domain.setter
    def domain(self, value: Any) -> None: ...
    fitbounds: Any
    "Determines if this subplot's view settings are auto-computed to fit trace data. On scoped maps, setting `fitbounds` leads to `center.lon` and `center.lat` getting auto-filled. On maps with a non-clipped projection, setting `fitbounds` leads to `center.lon`, `center.lat`, and `projection.rotation.lon` getting auto-filled. On maps with a clipped projection, setting `fitbounds` leads to `center.lon`, `center.lat`, `projection.rotation.lon`, `projection.rotation.lat`, `lonaxis.range` and `lataxis.range` getting auto-filled. If *locations* (default), only the trace's visible locations are considered in the `fitbounds` computations. If *geojson*, the entire trace input `geojson` (if provided) is considered in the `fitbounds` computations. If *false*, the view settings are used as-is; set this to opt out of auto-fitting."
    framecolor: Any
    "Sets the color the frame."
    framewidth: float | Any
    "Sets the stroke width (in px) of the frame."
    lakecolor: Any
    "Sets the color of the lakes."
    landcolor: Any
    "Sets the land mass color."
    @property
    def lataxis(self) -> _plotly_graph_objs_layout_geo.Lataxis | Any:
        ...
    @lataxis.setter
    def lataxis(self, value: Any) -> None: ...
    @property
    def lonaxis(self) -> _plotly_graph_objs_layout_geo.Lonaxis | Any:
        ...
    @lonaxis.setter
    def lonaxis(self, value: Any) -> None: ...
    oceancolor: Any
    "Sets the ocean color"
    @property
    def projection(self) -> _plotly_graph_objs_layout_geo.Projection | Any:
        ...
    @projection.setter
    def projection(self, value: Any) -> None: ...
    resolution: Any
    "Sets the resolution of the base layers. The values have units of km/mm e.g. 110 corresponds to a scale ratio of 1:110,000,000."
    rivercolor: Any
    "Sets color of the rivers."
    riverwidth: float | Any
    "Sets the stroke width (in px) of the rivers."
    scope: Any
    "Set the scope of the map."
    showcoastlines: bool | Any
    "Sets whether or not the coastlines are drawn."
    showcountries: bool | Any
    "Sets whether or not country boundaries are drawn."
    showframe: bool | Any
    "Sets whether or not a frame is drawn around the map."
    showlakes: bool | Any
    "Sets whether or not lakes are drawn."
    showland: bool | Any
    "Sets whether or not land masses are filled in color."
    showocean: bool | Any
    "Sets whether or not oceans are filled in color."
    showrivers: bool | Any
    "Sets whether or not rivers are drawn."
    showsubunits: bool | Any
    "Sets whether or not boundaries of subunits within countries (e.g. states, provinces) are drawn."
    subunitcolor: Any
    "Sets the color of the subunits boundaries."
    subunitwidth: float | Any
    "Sets the stroke width (in px) of the subunits boundaries."
    uirevision: Any
    "Controls persistence of user-driven changes in the view (projection and center). Defaults to `layout.uirevision`."
    visible: bool | Any
    "Sets the default visibility of the base layers."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        bgcolor: Any = ...,
        center: Any = ...,
        coastlinecolor: Any = ...,
        coastlinewidth: Any = ...,
        countrycolor: Any = ...,
        countrywidth: Any = ...,
        domain: Any = ...,
        fitbounds: Any = ...,
        framecolor: Any = ...,
        framewidth: Any = ...,
        lakecolor: Any = ...,
        landcolor: Any = ...,
        lataxis: Any = ...,
        lonaxis: Any = ...,
        oceancolor: Any = ...,
        projection: Any = ...,
        resolution: Any = ...,
        rivercolor: Any = ...,
        riverwidth: Any = ...,
        scope: Any = ...,
        showcoastlines: Any = ...,
        showcountries: Any = ...,
        showframe: Any = ...,
        showlakes: Any = ...,
        showland: Any = ...,
        showocean: Any = ...,
        showrivers: Any = ...,
        showsubunits: Any = ...,
        subunitcolor: Any = ...,
        subunitwidth: Any = ...,
        uirevision: Any = ...,
        visible: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Geo' object\n\nArgs:\n    bgcolor: Set the background color of the map\n    coastlinecolor: Sets the coastline color.\n    coastlinewidth: Sets the coastline stroke width (in px).\n    countrycolor: Sets line color of the country boundaries.\n    countrywidth: Sets line width (in px) of the country boundaries.\n    fitbounds: Determines if this subplot's view settings are auto-computed to fit trace data. On scoped maps, setting `fitbounds` leads to `center.lon` and `center.lat` getting auto-filled. On maps with a non-clipped projection, setting `fitbounds` leads to `center.lon`, `center.lat`, and `projection.rotation.lon` getting auto-filled. On maps with a clipped projection, setting `fitbounds` leads to `center.lon`, `center.lat`, `projection.rotation.lon`, `projection.rotation.lat`, `lonaxis.range` and `lataxis.range` getting auto-filled. If *locations* (default), only the trace's visible locations are considered in the `fitbounds` computations. If *geojson*, the entire trace input `geojson` (if provided) is considered in the `fitbounds` computations. If *false*, the view settings are used as-is; set this to opt out of auto-fitting.\n    framecolor: Sets the color the frame.\n    framewidth: Sets the stroke width (in px) of the frame.\n    lakecolor: Sets the color of the lakes.\n    landcolor: Sets the land mass color.\n    oceancolor: Sets the ocean color\n    resolution: Sets the resolution of the base layers. The values have units of km/mm e.g. 110 corresponds to a scale ratio of 1:110,000,000.\n    rivercolor: Sets color of the rivers.\n    riverwidth: Sets the stroke width (in px) of the rivers.\n    scope: Set the scope of the map.\n    showcoastlines: Sets whether or not the coastlines are drawn.\n    showcountries: Sets whether or not country boundaries are drawn.\n    showframe: Sets whether or not a frame is drawn around the map.\n    showlakes: Sets whether or not lakes are drawn.\n    showland: Sets whether or not land masses are filled in color.\n    showocean: Sets whether or not oceans are filled in color.\n    showrivers: Sets whether or not rivers are drawn.\n    showsubunits: Sets whether or not boundaries of subunits within countries (e.g. states, provinces) are drawn.\n    subunitcolor: Sets the color of the subunits boundaries.\n    subunitwidth: Sets the stroke width (in px) of the subunits boundaries.\n    uirevision: Controls persistence of user-driven changes in the view (projection and center). Defaults to `layout.uirevision`.\n    visible: Sets the default visibility of the base layers."
        ...

class Grid(_PlotlyObject):
    "Create a new 'Grid' object"
    columns: int | Any
    "The number of columns in the grid. If you provide a 2D `subplots` array, the length of its longest row is used as the default. If you give an `xaxes` array, its length is used as the default. But it's also possible to have a different length, if you want to leave a row at the end for non-cartesian subplots."
    @property
    def domain(self) -> _plotly_graph_objs_layout_grid.Domain | Any:
        ...
    @domain.setter
    def domain(self, value: Any) -> None: ...
    pattern: Any
    "If no `subplots`, `xaxes`, or `yaxes` are given but we do have `rows` and `columns`, we can generate defaults using consecutive axis IDs, in two ways: *coupled* gives one x axis per column and one y axis per row. *independent* uses a new xy pair for each cell, left-to-right across each row then iterating rows according to `roworder`."
    roworder: Any
    "Is the first row the top or the bottom? Note that columns are always enumerated from left to right."
    rows: int | Any
    "The number of rows in the grid. If you provide a 2D `subplots` array or a `yaxes` array, its length is used as the default. But it's also possible to have a different length, if you want to leave a row at the end for non-cartesian subplots."
    subplots: Any
    "Used for freeform grids, where some axes may be shared across subplots but others are not. Each entry should be a cartesian subplot id, like *xy* or *x3y2*, or ** to leave that cell empty. You may reuse x axes within the same column, and y axes within the same row. Non-cartesian subplots and traces that support `domain` can place themselves in this grid separately using the `gridcell` attribute."
    xaxes: Any
    "Used with `yaxes` when the x and y axes are shared across columns and rows. Each entry should be an x axis id like *x*, *x2*, etc., or ** to not put an x axis in that column. Entries other than ** must be unique. Ignored if `subplots` is present. If missing but `yaxes` is present, will generate consecutive IDs."
    xgap: float | Any
    "Horizontal space between grid cells, expressed as a fraction of the total width available to one cell. Defaults to 0.1 for coupled-axes grids and 0.2 for independent grids."
    xside: Any
    "Sets where the x axis labels and titles go. *bottom* means the very bottom of the grid. *bottom plot* is the lowest plot that each x axis is used in. *top* and *top plot* are similar."
    yaxes: Any
    "Used with `yaxes` when the x and y axes are shared across columns and rows. Each entry should be an y axis id like *y*, *y2*, etc., or ** to not put a y axis in that row. Entries other than ** must be unique. Ignored if `subplots` is present. If missing but `xaxes` is present, will generate consecutive IDs."
    ygap: float | Any
    "Vertical space between grid cells, expressed as a fraction of the total height available to one cell. Defaults to 0.1 for coupled-axes grids and 0.3 for independent grids."
    yside: Any
    "Sets where the y axis labels and titles go. *left* means the very left edge of the grid. *left plot* is the leftmost plot that each y axis is used in. *right* and *right plot* are similar."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        columns: Any = ...,
        domain: Any = ...,
        pattern: Any = ...,
        roworder: Any = ...,
        rows: Any = ...,
        subplots: Any = ...,
        xaxes: Any = ...,
        xgap: Any = ...,
        xside: Any = ...,
        yaxes: Any = ...,
        ygap: Any = ...,
        yside: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Grid' object\n\nArgs:\n    columns: The number of columns in the grid. If you provide a 2D `subplots` array, the length of its longest row is used as the default. If you give an `xaxes` array, its length is used as the default. But it's also possible to have a different length, if you want to leave a row at the end for non-cartesian subplots.\n    pattern: If no `subplots`, `xaxes`, or `yaxes` are given but we do have `rows` and `columns`, we can generate defaults using consecutive axis IDs, in two ways: *coupled* gives one x axis per column and one y axis per row. *independent* uses a new xy pair for each cell, left-to-right across each row then iterating rows according to `roworder`.\n    roworder: Is the first row the top or the bottom? Note that columns are always enumerated from left to right.\n    rows: The number of rows in the grid. If you provide a 2D `subplots` array or a `yaxes` array, its length is used as the default. But it's also possible to have a different length, if you want to leave a row at the end for non-cartesian subplots.\n    subplots: Used for freeform grids, where some axes may be shared across subplots but others are not. Each entry should be a cartesian subplot id, like *xy* or *x3y2*, or ** to leave that cell empty. You may reuse x axes within the same column, and y axes within the same row. Non-cartesian subplots and traces that support `domain` can place themselves in this grid separately using the `gridcell` attribute.\n    xaxes: Used with `yaxes` when the x and y axes are shared across columns and rows. Each entry should be an x axis id like *x*, *x2*, etc., or ** to not put an x axis in that column. Entries other than ** must be unique. Ignored if `subplots` is present. If missing but `yaxes` is present, will generate consecutive IDs.\n    xgap: Horizontal space between grid cells, expressed as a fraction of the total width available to one cell. Defaults to 0.1 for coupled-axes grids and 0.2 for independent grids.\n    xside: Sets where the x axis labels and titles go. *bottom* means the very bottom of the grid. *bottom plot* is the lowest plot that each x axis is used in. *top* and *top plot* are similar.\n    yaxes: Used with `yaxes` when the x and y axes are shared across columns and rows. Each entry should be an y axis id like *y*, *y2*, etc., or ** to not put a y axis in that row. Entries other than ** must be unique. Ignored if `subplots` is present. If missing but `xaxes` is present, will generate consecutive IDs.\n    ygap: Vertical space between grid cells, expressed as a fraction of the total height available to one cell. Defaults to 0.1 for coupled-axes grids and 0.3 for independent grids.\n    yside: Sets where the y axis labels and titles go. *left* means the very left edge of the grid. *left plot* is the leftmost plot that each y axis is used in. *right* and *right plot* are similar."
        ...

class Hoverlabel(_PlotlyObject):
    "Create a new 'Hoverlabel' object"
    align: Any
    "Sets the horizontal alignment of the text content within hover label box. Has an effect only if the hover label text spans more two or more lines"
    bgcolor: Any
    "Sets the background color of all hover labels on graph"
    bordercolor: Any
    "Sets the border color of all hover labels on graph."
    @property
    def font(self) -> _plotly_graph_objs_layout_hoverlabel.Font | Any:
        "Sets the default hover label font used by all traces on the graph."
        ...
    @font.setter
    def font(self, value: Any) -> None: ...
    @property
    def grouptitlefont(self) -> _plotly_graph_objs_layout_hoverlabel.Grouptitlefont | Any:
        "Sets the font for group titles in hover (unified modes). Defaults to `hoverlabel.font`."
        ...
    @grouptitlefont.setter
    def grouptitlefont(self, value: Any) -> None: ...
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
        grouptitlefont: Any = ...,
        namelength: Any = ...,
        showarrow: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Hoverlabel' object\n\nArgs:\n    align: Sets the horizontal alignment of the text content within hover label box. Has an effect only if the hover label text spans more two or more lines\n    bgcolor: Sets the background color of all hover labels on graph\n    bordercolor: Sets the border color of all hover labels on graph.\n    font: Sets the default hover label font used by all traces on the graph.\n    grouptitlefont: Sets the font for group titles in hover (unified modes). Defaults to `hoverlabel.font`.\n    namelength: Sets the default length (in number of characters) of the trace name in the hover labels for all traces. -1 shows the whole name regardless of length. 0-3 shows the first 0-3 characters, and an integer >3 will show the whole name if it is less than that many characters, but if it is longer, will truncate to `namelength - 3` characters and add an ellipsis.\n    showarrow: Sets whether or not to show the hover label arrow/triangle pointing to the data point."
        ...

class Image(_PlotlyObject):
    "Create a new 'Image' object"
    layer: Any
    "Specifies whether images are drawn below or above traces. When `xref` and `yref` are both set to `paper`, image is drawn below the entire plot area."
    name: str | Any
    "When used in a template, named items are created in the output figure in addition to any items the figure already has in this array. You can modify these items in the output figure by making your own item with `templateitemname` matching this `name` alongside your modifications (including `visible: false` or `enabled: false` to hide it). Has no effect outside of a template."
    opacity: float | Any
    "Sets the opacity of the image."
    sizex: float | Any
    "Sets the image container size horizontally. The image will be sized based on the `position` value. When `xref` is set to `paper`, units are sized relative to the plot width. When `xref` ends with ` domain`, units are sized relative to the axis width."
    sizey: float | Any
    "Sets the image container size vertically. The image will be sized based on the `position` value. When `yref` is set to `paper`, units are sized relative to the plot height. When `yref` ends with ` domain`, units are sized relative to the axis height."
    sizing: Any
    "Specifies which dimension of the image to constrain."
    source: str | Any
    "Specifies the URL of the image to be used. The URL must be accessible from the domain where the plot code is run, and can be either relative or absolute."
    templateitemname: str | Any
    "Used to refer to a named item in this array in the template. Named items from the template will be created even without a matching item in the input figure, but you can modify one by making an item with `templateitemname` matching its `name`, alongside your modifications (including `visible: false` or `enabled: false` to hide it). If there is no template or no matching item, this item will be hidden unless you explicitly show it with `visible: true`."
    visible: bool | Any
    "Determines whether or not this image is visible."
    x: Any
    "Sets the image's x position. When `xref` is set to `paper`, units are sized relative to the plot height. See `xref` for more info"
    xanchor: Any
    "Sets the anchor for the x position"
    xref: Any
    "Sets the images's x coordinate axis. If set to a x axis id (e.g. *x* or *x2*), the `x` position refers to a x coordinate. If set to *paper*, the `x` position refers to the distance from the left of the plotting area in normalized coordinates where *0* (*1*) corresponds to the left (right). If set to a x axis ID followed by *domain* (separated by a space), the position behaves like for *paper*, but refers to the distance in fractions of the domain length from the left of the domain of that axis: e.g., *x2 domain* refers to the domain of the second x axis and a x position of 0.5 refers to the point between the left and the right of the domain of the second x axis."
    y: Any
    "Sets the image's y position. When `yref` is set to `paper`, units are sized relative to the plot height. See `yref` for more info"
    yanchor: Any
    "Sets the anchor for the y position."
    yref: Any
    "Sets the images's y coordinate axis. If set to a y axis id (e.g. *y* or *y2*), the `y` position refers to a y coordinate. If set to *paper*, the `y` position refers to the distance from the bottom of the plotting area in normalized coordinates where *0* (*1*) corresponds to the bottom (top). If set to a y axis ID followed by *domain* (separated by a space), the position behaves like for *paper*, but refers to the distance in fractions of the domain length from the bottom of the domain of that axis: e.g., *y2 domain* refers to the domain of the second y axis and a y position of 0.5 refers to the point between the bottom and the top of the domain of the second y axis."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        layer: Any = ...,
        name: Any = ...,
        opacity: Any = ...,
        sizex: Any = ...,
        sizey: Any = ...,
        sizing: Any = ...,
        source: Any = ...,
        templateitemname: Any = ...,
        visible: Any = ...,
        x: Any = ...,
        xanchor: Any = ...,
        xref: Any = ...,
        y: Any = ...,
        yanchor: Any = ...,
        yref: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Image' object\n\nArgs:\n    layer: Specifies whether images are drawn below or above traces. When `xref` and `yref` are both set to `paper`, image is drawn below the entire plot area.\n    name: When used in a template, named items are created in the output figure in addition to any items the figure already has in this array. You can modify these items in the output figure by making your own item with `templateitemname` matching this `name` alongside your modifications (including `visible: false` or `enabled: false` to hide it). Has no effect outside of a template.\n    opacity: Sets the opacity of the image.\n    sizex: Sets the image container size horizontally. The image will be sized based on the `position` value. When `xref` is set to `paper`, units are sized relative to the plot width. When `xref` ends with ` domain`, units are sized relative to the axis width.\n    sizey: Sets the image container size vertically. The image will be sized based on the `position` value. When `yref` is set to `paper`, units are sized relative to the plot height. When `yref` ends with ` domain`, units are sized relative to the axis height.\n    sizing: Specifies which dimension of the image to constrain.\n    source: Specifies the URL of the image to be used. The URL must be accessible from the domain where the plot code is run, and can be either relative or absolute.\n    templateitemname: Used to refer to a named item in this array in the template. Named items from the template will be created even without a matching item in the input figure, but you can modify one by making an item with `templateitemname` matching its `name`, alongside your modifications (including `visible: false` or `enabled: false` to hide it). If there is no template or no matching item, this item will be hidden unless you explicitly show it with `visible: true`.\n    visible: Determines whether or not this image is visible.\n    x: Sets the image's x position. When `xref` is set to `paper`, units are sized relative to the plot height. See `xref` for more info\n    xanchor: Sets the anchor for the x position\n    xref: Sets the images's x coordinate axis. If set to a x axis id (e.g. *x* or *x2*), the `x` position refers to a x coordinate. If set to *paper*, the `x` position refers to the distance from the left of the plotting area in normalized coordinates where *0* (*1*) corresponds to the left (right). If set to a x axis ID followed by *domain* (separated by a space), the position behaves like for *paper*, but refers to the distance in fractions of the domain length from the left of the domain of that axis: e.g., *x2 domain* refers to the domain of the second x axis and a x position of 0.5 refers to the point between the left and the right of the domain of the second x axis.\n    y: Sets the image's y position. When `yref` is set to `paper`, units are sized relative to the plot height. See `yref` for more info\n    yanchor: Sets the anchor for the y position.\n    yref: Sets the images's y coordinate axis. If set to a y axis id (e.g. *y* or *y2*), the `y` position refers to a y coordinate. If set to *paper*, the `y` position refers to the distance from the bottom of the plotting area in normalized coordinates where *0* (*1*) corresponds to the bottom (top). If set to a y axis ID followed by *domain* (separated by a space), the position behaves like for *paper*, but refers to the distance in fractions of the domain length from the bottom of the domain of that axis: e.g., *y2 domain* refers to the domain of the second y axis and a y position of 0.5 refers to the point between the bottom and the top of the domain of the second y axis."
        ...

class Legend(_PlotlyObject):
    "Create a new 'Legend' object"
    bgcolor: Any
    "Sets the legend background color. Defaults to `layout.paper_bgcolor`."
    bordercolor: Any
    "Sets the color of the border enclosing the legend."
    borderwidth: float | Any
    "Sets the width (in px) of the border enclosing the legend."
    entrywidth: float | Any
    "Sets the width (in px or fraction) of the legend. Use 0 to size the entry based on the text width, when `entrywidthmode` is set to *pixels*."
    entrywidthmode: Any
    "Determines what entrywidth means."
    @property
    def font(self) -> _plotly_graph_objs_layout_legend.Font | Any:
        "Sets the font used to text the legend items."
        ...
    @font.setter
    def font(self, value: Any) -> None: ...
    groupclick: Any
    "Determines the behavior on legend group item click. *toggleitem* toggles the visibility of the individual item clicked on the graph. *togglegroup* toggles the visibility of all items in the same legendgroup as the item clicked on the graph."
    groupdoubleclick: Any
    "Determines the behavior on legend group item double-click. *toggleitem* toggles the visibility of the individual item clicked on the graph. *togglegroup* toggles the visibility of all items in the same legendgroup as the item clicked on the graph. Defaults to the value of `groupclick`."
    @property
    def grouptitlefont(self) -> _plotly_graph_objs_layout_legend.Grouptitlefont | Any:
        "Sets the font for group titles in legend. Defaults to `legend.font` with its size increased about 10%."
        ...
    @grouptitlefont.setter
    def grouptitlefont(self, value: Any) -> None: ...
    indentation: float | Any
    "Sets the indentation (in px) of the legend entries."
    itemclick: Any
    "Determines the behavior on legend item click. *toggle* toggles the visibility of the item clicked on the graph. *toggleothers* makes the clicked item the sole visible item on the graph. *false* disables legend item click interactions."
    itemdoubleclick: Any
    "Determines the behavior on legend item double-click. *toggle* toggles the visibility of the item clicked on the graph. *toggleothers* makes the clicked item the sole visible item on the graph. *false* disables legend item double-click interactions."
    itemsizing: Any
    "Determines if the legend items symbols scale with their corresponding *trace* attributes or remain *constant* independent of the symbol size on the graph."
    itemwidth: float | Any
    "Sets the width (in px) of the legend item symbols (the part other than the title.text)."
    maxheight: float | Any
    "Sets the max height (in px) of the legend, or max height ratio (reference height * ratio) if less than or equal to 1. Default value is: 0.5 for horizontal legends; 1 for vertical legends. The minimum allowed height is 30px. For a ratio of 0.5, the legend will take up to 50% of the reference height before displaying a scrollbar. The reference height is the full layout height with the following exception: vertically oriented legends with a `yref` of `\"paper\", located to the side of the plot. In this case, the reference height is the plot height."
    orientation: Any
    "Sets the orientation of the legend."
    @property
    def title(self) -> _plotly_graph_objs_layout_legend.Title | Any:
        ...
    @title.setter
    def title(self, value: Any) -> None: ...
    titleclick: Any
    "Determines the behavior on legend title click. *toggle* toggles the visibility of all items in the legend. *toggleothers* toggles the visibility of all other legends. *false* disables legend title click interactions. Defaults to *toggle* when there are multiple legends, *false* otherwise. Not supported for legends containing pie and pie-like traces."
    titledoubleclick: Any
    "Determines the behavior on legend title double-click. *toggle* toggles the visibility of all items in the legend. *toggleothers* toggles the visibility of all other legends. *false* disables legend title double-click interactions. Defaults to *toggleothers* when there are multiple legends, *false* otherwise. Not supported for legends containing pie and pie-like traces."
    tracegroupgap: float | Any
    "Sets the amount of vertical space (in px) between legend groups."
    traceorder: str | Any
    "Determines the order at which the legend items are displayed. If *normal*, the items are displayed top-to-bottom in the same order as the input data. If *reversed*, the items are displayed in the opposite order as *normal*. If *grouped*, the items are displayed in groups (when a trace `legendgroup` is provided). if *grouped+reversed*, the items are displayed in the opposite order as *grouped*."
    uirevision: Any
    "Controls persistence of legend-driven changes in trace and pie label visibility. Defaults to `layout.uirevision`."
    valign: Any
    "Sets the vertical alignment of the symbols with respect to their associated text."
    visible: bool | Any
    "Determines whether or not this legend is visible."
    x: float | Any
    "Sets the x position with respect to `xref` (in normalized coordinates) of the legend. When `xref` is *paper*, defaults to *1.02* for vertical legends and defaults to *0* for horizontal legends. When `xref` is *container*, defaults to *1* for vertical legends and defaults to *0* for horizontal legends. Must be between *0* and *1* if `xref` is *container*. and between *-2* and *3* if `xref` is *paper*."
    xanchor: Any
    "Sets the legend's horizontal position anchor. This anchor binds the `x` position to the *left*, *center* or *right* of the legend. Value *auto* anchors legends to the right for `x` values greater than or equal to 2/3, anchors legends to the left for `x` values less than or equal to 1/3 and anchors legends with respect to their center otherwise."
    xref: Any
    "Sets the container `x` refers to. *container* spans the entire `width` of the plot. *paper* refers to the width of the plotting area only."
    y: float | Any
    "Sets the y position with respect to `yref` (in normalized coordinates) of the legend. When `yref` is *paper*, defaults to *1* for vertical legends, defaults to *-0.1* for horizontal legends on graphs w/o range sliders and defaults to *1.1* for horizontal legends on graph with one or multiple range sliders. When `yref` is *container*, defaults to *1*. Must be between *0* and *1* if `yref` is *container* and between *-2* and *3* if `yref` is *paper*."
    yanchor: Any
    "Sets the legend's vertical position anchor. This anchor binds the `y` position to the *top*, *middle* or *bottom* of the legend. Value *auto* anchors legends at their bottom for `y` values less than or equal to 1/3, anchors legends to at their top for `y` values greater than or equal to 2/3 and anchors legends with respect to their middle otherwise."
    yref: Any
    "Sets the container `y` refers to. *container* spans the entire `height` of the plot. *paper* refers to the height of the plotting area only."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        bgcolor: Any = ...,
        bordercolor: Any = ...,
        borderwidth: Any = ...,
        entrywidth: Any = ...,
        entrywidthmode: Any = ...,
        font: Any = ...,
        groupclick: Any = ...,
        groupdoubleclick: Any = ...,
        grouptitlefont: Any = ...,
        indentation: Any = ...,
        itemclick: Any = ...,
        itemdoubleclick: Any = ...,
        itemsizing: Any = ...,
        itemwidth: Any = ...,
        maxheight: Any = ...,
        orientation: Any = ...,
        title: Any = ...,
        titleclick: Any = ...,
        titledoubleclick: Any = ...,
        tracegroupgap: Any = ...,
        traceorder: Any = ...,
        uirevision: Any = ...,
        valign: Any = ...,
        visible: Any = ...,
        x: Any = ...,
        xanchor: Any = ...,
        xref: Any = ...,
        y: Any = ...,
        yanchor: Any = ...,
        yref: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Legend' object\n\nArgs:\n    bgcolor: Sets the legend background color. Defaults to `layout.paper_bgcolor`.\n    bordercolor: Sets the color of the border enclosing the legend.\n    borderwidth: Sets the width (in px) of the border enclosing the legend.\n    entrywidth: Sets the width (in px or fraction) of the legend. Use 0 to size the entry based on the text width, when `entrywidthmode` is set to *pixels*.\n    entrywidthmode: Determines what entrywidth means.\n    font: Sets the font used to text the legend items.\n    groupclick: Determines the behavior on legend group item click. *toggleitem* toggles the visibility of the individual item clicked on the graph. *togglegroup* toggles the visibility of all items in the same legendgroup as the item clicked on the graph.\n    groupdoubleclick: Determines the behavior on legend group item double-click. *toggleitem* toggles the visibility of the individual item clicked on the graph. *togglegroup* toggles the visibility of all items in the same legendgroup as the item clicked on the graph. Defaults to the value of `groupclick`.\n    grouptitlefont: Sets the font for group titles in legend. Defaults to `legend.font` with its size increased about 10%.\n    indentation: Sets the indentation (in px) of the legend entries.\n    itemclick: Determines the behavior on legend item click. *toggle* toggles the visibility of the item clicked on the graph. *toggleothers* makes the clicked item the sole visible item on the graph. *false* disables legend item click interactions.\n    itemdoubleclick: Determines the behavior on legend item double-click. *toggle* toggles the visibility of the item clicked on the graph. *toggleothers* makes the clicked item the sole visible item on the graph. *false* disables legend item double-click interactions.\n    itemsizing: Determines if the legend items symbols scale with their corresponding *trace* attributes or remain *constant* independent of the symbol size on the graph.\n    itemwidth: Sets the width (in px) of the legend item symbols (the part other than the title.text).\n    maxheight: Sets the max height (in px) of the legend, or max height ratio (reference height * ratio) if less than or equal to 1. Default value is: 0.5 for horizontal legends; 1 for vertical legends. The minimum allowed height is 30px. For a ratio of 0.5, the legend will take up to 50% of the reference height before displaying a scrollbar. The reference height is the full layout height with the following exception: vertically oriented legends with a `yref` of `\"paper\", located to the side of the plot. In this case, the reference height is the plot height.\n    orientation: Sets the orientation of the legend.\n    titleclick: Determines the behavior on legend title click. *toggle* toggles the visibility of all items in the legend. *toggleothers* toggles the visibility of all other legends. *false* disables legend title click interactions. Defaults to *toggle* when there are multiple legends, *false* otherwise. Not supported for legends containing pie and pie-like traces.\n    titledoubleclick: Determines the behavior on legend title double-click. *toggle* toggles the visibility of all items in the legend. *toggleothers* toggles the visibility of all other legends. *false* disables legend title double-click interactions. Defaults to *toggleothers* when there are multiple legends, *false* otherwise. Not supported for legends containing pie and pie-like traces.\n    tracegroupgap: Sets the amount of vertical space (in px) between legend groups.\n    traceorder: Determines the order at which the legend items are displayed. If *normal*, the items are displayed top-to-bottom in the same order as the input data. If *reversed*, the items are displayed in the opposite order as *normal*. If *grouped*, the items are displayed in groups (when a trace `legendgroup` is provided). if *grouped+reversed*, the items are displayed in the opposite order as *grouped*.\n    uirevision: Controls persistence of legend-driven changes in trace and pie label visibility. Defaults to `layout.uirevision`.\n    valign: Sets the vertical alignment of the symbols with respect to their associated text.\n    visible: Determines whether or not this legend is visible.\n    x: Sets the x position with respect to `xref` (in normalized coordinates) of the legend. When `xref` is *paper*, defaults to *1.02* for vertical legends and defaults to *0* for horizontal legends. When `xref` is *container*, defaults to *1* for vertical legends and defaults to *0* for horizontal legends. Must be between *0* and *1* if `xref` is *container*. and between *-2* and *3* if `xref` is *paper*.\n    xanchor: Sets the legend's horizontal position anchor. This anchor binds the `x` position to the *left*, *center* or *right* of the legend. Value *auto* anchors legends to the right for `x` values greater than or equal to 2/3, anchors legends to the left for `x` values less than or equal to 1/3 and anchors legends with respect to their center otherwise.\n    xref: Sets the container `x` refers to. *container* spans the entire `width` of the plot. *paper* refers to the width of the plotting area only.\n    y: Sets the y position with respect to `yref` (in normalized coordinates) of the legend. When `yref` is *paper*, defaults to *1* for vertical legends, defaults to *-0.1* for horizontal legends on graphs w/o range sliders and defaults to *1.1* for horizontal legends on graph with one or multiple range sliders. When `yref` is *container*, defaults to *1*. Must be between *0* and *1* if `yref` is *container* and between *-2* and *3* if `yref` is *paper*.\n    yanchor: Sets the legend's vertical position anchor. This anchor binds the `y` position to the *top*, *middle* or *bottom* of the legend. Value *auto* anchors legends at their bottom for `y` values less than or equal to 1/3, anchors legends to at their top for `y` values greater than or equal to 2/3 and anchors legends with respect to their middle otherwise.\n    yref: Sets the container `y` refers to. *container* spans the entire `height` of the plot. *paper* refers to the height of the plotting area only."
        ...

class Map(_PlotlyObject):
    "Create a new 'Map' object"
    bearing: float | Any
    "Sets the bearing angle of the map in degrees counter-clockwise from North (map.bearing)."
    @property
    def bounds(self) -> _plotly_graph_objs_layout_map.Bounds | Any:
        ...
    @bounds.setter
    def bounds(self, value: Any) -> None: ...
    @property
    def center(self) -> _plotly_graph_objs_layout_map.Center | Any:
        ...
    @center.setter
    def center(self, value: Any) -> None: ...
    @property
    def domain(self) -> _plotly_graph_objs_layout_map.Domain | Any:
        ...
    @domain.setter
    def domain(self, value: Any) -> None: ...
    fitbounds: Any
    "Determines if this subplot's view settings are auto-computed to fit trace data. If *locations* (default), the view is auto-fit to the lon/lat coordinates of the visible trace data. If *false*, the view settings are used as-is; set this to opt out of auto-fitting. If `fitbounds` is enabled but a user provides `center` or `zoom`, auto-fit will be skipped."
    @property
    def layer(self) -> _plotly_graph_objs_layout_map.Layer | Any:
        ...
    @layer.setter
    def layer(self, value: Any) -> None: ...
    pitch: float | Any
    "Sets the pitch angle of the map (in degrees, where *0* means perpendicular to the surface of the map) (map.pitch)."
    style: Any
    "Defines the map layers that are rendered by default below the trace layers defined in `data`, which are themselves by default rendered below the layers defined in `layout.map.layers`.  These layers can be defined either explicitly as a Map Style object which can contain multiple layer definitions that load data from any public or private Tile Map Service (TMS or XYZ) or Web Map Service (WMS) or implicitly by using one of the built-in style objects which use WMSes or by using a custom style URL  Map Style objects are of the form described in the MapLibre GL JS documentation available at https://maplibre.org/maplibre-style-spec/  The built-in plotly.js styles objects are: basic, carto-darkmatter, carto-darkmatter-nolabels, carto-positron, carto-positron-nolabels, carto-voyager, carto-voyager-nolabels, dark, light, open-street-map, outdoors, satellite, satellite-streets, streets, white-bg."
    uirevision: Any
    "Controls persistence of user-driven changes in the view: `center`, `zoom`, `bearing`, `pitch`. Defaults to `layout.uirevision`."
    zoom: float | Any
    "Sets the zoom level of the map (map.zoom)."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        bearing: Any = ...,
        bounds: Any = ...,
        center: Any = ...,
        domain: Any = ...,
        fitbounds: Any = ...,
        layer: Any = ...,
        pitch: Any = ...,
        style: Any = ...,
        uirevision: Any = ...,
        zoom: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Map' object\n\nArgs:\n    bearing: Sets the bearing angle of the map in degrees counter-clockwise from North (map.bearing).\n    fitbounds: Determines if this subplot's view settings are auto-computed to fit trace data. If *locations* (default), the view is auto-fit to the lon/lat coordinates of the visible trace data. If *false*, the view settings are used as-is; set this to opt out of auto-fitting. If `fitbounds` is enabled but a user provides `center` or `zoom`, auto-fit will be skipped.\n    pitch: Sets the pitch angle of the map (in degrees, where *0* means perpendicular to the surface of the map) (map.pitch).\n    style: Defines the map layers that are rendered by default below the trace layers defined in `data`, which are themselves by default rendered below the layers defined in `layout.map.layers`.  These layers can be defined either explicitly as a Map Style object which can contain multiple layer definitions that load data from any public or private Tile Map Service (TMS or XYZ) or Web Map Service (WMS) or implicitly by using one of the built-in style objects which use WMSes or by using a custom style URL  Map Style objects are of the form described in the MapLibre GL JS documentation available at https://maplibre.org/maplibre-style-spec/  The built-in plotly.js styles objects are: basic, carto-darkmatter, carto-darkmatter-nolabels, carto-positron, carto-positron-nolabels, carto-voyager, carto-voyager-nolabels, dark, light, open-street-map, outdoors, satellite, satellite-streets, streets, white-bg.\n    uirevision: Controls persistence of user-driven changes in the view: `center`, `zoom`, `bearing`, `pitch`. Defaults to `layout.uirevision`.\n    zoom: Sets the zoom level of the map (map.zoom)."
        ...

class Margin(_PlotlyObject):
    "Create a new 'Margin' object"
    autoexpand: bool | Any
    "Turns on/off margin expansion computations. Legends, colorbars, updatemenus, sliders, axis rangeselector and rangeslider are allowed to push the margins by defaults."
    b: float | Any
    "Sets the bottom margin (in px)."
    l: float | Any
    "Sets the left margin (in px)."
    pad: float | Any
    "Sets the amount of padding (in px) between the plotting area and the axis lines"
    r: float | Any
    "Sets the right margin (in px)."
    t: float | Any
    "Sets the top margin (in px)."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        autoexpand: Any = ...,
        b: Any = ...,
        l: Any = ...,
        pad: Any = ...,
        r: Any = ...,
        t: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Margin' object\n\nArgs:\n    autoexpand: Turns on/off margin expansion computations. Legends, colorbars, updatemenus, sliders, axis rangeselector and rangeslider are allowed to push the margins by defaults.\n    b: Sets the bottom margin (in px).\n    l: Sets the left margin (in px).\n    pad: Sets the amount of padding (in px) between the plotting area and the axis lines\n    r: Sets the right margin (in px).\n    t: Sets the top margin (in px)."
        ...

class Modebar(_PlotlyObject):
    "Create a new 'Modebar' object"
    activecolor: Any
    "Sets the color of the active or hovered on icons in the modebar."
    add: str | Any
    "Determines which predefined modebar buttons to add. Please note that these buttons will only be shown if they are compatible with all trace types used in a graph. Similar to `config.modeBarButtonsToAdd` option. This may include *v1hovermode*, *hoverclosest*, *hovercompare*, *togglehover*, *togglespikelines*, *drawline*, *drawopenpath*, *drawclosedpath*, *drawcircle*, *drawrect*, *eraseshape*, *downloadJson*."
    bgcolor: Any
    "Sets the background color of the modebar."
    color: Any
    "Sets the color of the icons in the modebar."
    orientation: Any
    "Sets the orientation of the modebar."
    remove: str | Any
    "Determines which predefined modebar buttons to remove. Similar to `config.modeBarButtonsToRemove` option. This may include *autoScale2d*, *autoscale*, *hoverCompareCartesian*, *hovercompare*, *lasso*, *lasso2d*, *orbitRotation*, *orbitrotation*, *pan*, *pan2d*, *pan3d*, *reset*, *resetCameraDefault3d*, *resetCameraLastSave3d*, *resetGeo*, *resetSankeyGroup*, *resetScale2d*, *resetViewMap*, *resetViews*, *resetcameradefault*, *resetcameralastsave*, *resetsankeygroup*, *resetscale*, *resetview*, *resetviews*, *select*, *select2d*, *sendChartToCloud*, *sendcharttocloud*, *tableRotation*, *tablerotation*, *toImage*, *toggleHover*, *toggleSpikelines*, *togglehover*, *togglespikelines*, *toimage*, *zoom*, *zoom2d*, *zoom3d*, *zoomIn2d*, *zoomInGeo*, *zoomInMap*, *zoomOut2d*, *zoomOutGeo*, *zoomOutMap*, *zoomin*, *zoomout*."
    uirevision: Any
    "Controls persistence of user-driven changes related to the modebar, including `hovermode`, `dragmode`, and `showspikes` at both the root level and inside subplots. Defaults to `layout.uirevision`."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        activecolor: Any = ...,
        add: Any = ...,
        bgcolor: Any = ...,
        color: Any = ...,
        orientation: Any = ...,
        remove: Any = ...,
        uirevision: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Modebar' object\n\nArgs:\n    activecolor: Sets the color of the active or hovered on icons in the modebar.\n    add: Determines which predefined modebar buttons to add. Please note that these buttons will only be shown if they are compatible with all trace types used in a graph. Similar to `config.modeBarButtonsToAdd` option. This may include *v1hovermode*, *hoverclosest*, *hovercompare*, *togglehover*, *togglespikelines*, *drawline*, *drawopenpath*, *drawclosedpath*, *drawcircle*, *drawrect*, *eraseshape*, *downloadJson*.\n    bgcolor: Sets the background color of the modebar.\n    color: Sets the color of the icons in the modebar.\n    orientation: Sets the orientation of the modebar.\n    remove: Determines which predefined modebar buttons to remove. Similar to `config.modeBarButtonsToRemove` option. This may include *autoScale2d*, *autoscale*, *hoverCompareCartesian*, *hovercompare*, *lasso*, *lasso2d*, *orbitRotation*, *orbitrotation*, *pan*, *pan2d*, *pan3d*, *reset*, *resetCameraDefault3d*, *resetCameraLastSave3d*, *resetGeo*, *resetSankeyGroup*, *resetScale2d*, *resetViewMap*, *resetViews*, *resetcameradefault*, *resetcameralastsave*, *resetsankeygroup*, *resetscale*, *resetview*, *resetviews*, *select*, *select2d*, *sendChartToCloud*, *sendcharttocloud*, *tableRotation*, *tablerotation*, *toImage*, *toggleHover*, *toggleSpikelines*, *togglehover*, *togglespikelines*, *toimage*, *zoom*, *zoom2d*, *zoom3d*, *zoomIn2d*, *zoomInGeo*, *zoomInMap*, *zoomOut2d*, *zoomOutGeo*, *zoomOutMap*, *zoomin*, *zoomout*.\n    uirevision: Controls persistence of user-driven changes related to the modebar, including `hovermode`, `dragmode`, and `showspikes` at both the root level and inside subplots. Defaults to `layout.uirevision`."
        ...

class Newselection(_PlotlyObject):
    "Create a new 'Newselection' object"
    @property
    def line(self) -> _plotly_graph_objs_layout_newselection.Line | Any:
        ...
    @line.setter
    def line(self, value: Any) -> None: ...
    mode: Any
    "Describes how a new selection is created. If `immediate`, a new selection is created after first mouse up. If `gradual`, a new selection is not created after first mouse. By adding to and subtracting from the initial selection, this option allows declaring extra outlines of the selection."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        line: Any = ...,
        mode: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Newselection' object\n\nArgs:\n    mode: Describes how a new selection is created. If `immediate`, a new selection is created after first mouse up. If `gradual`, a new selection is not created after first mouse. By adding to and subtracting from the initial selection, this option allows declaring extra outlines of the selection."
        ...

class Newshape(_PlotlyObject):
    "Create a new 'Newshape' object"
    drawdirection: Any
    "When `dragmode` is set to *drawrect*, *drawline* or *drawcircle* this limits the drag to be horizontal, vertical or diagonal. Using *diagonal* there is no limit e.g. in drawing lines in any direction. *ortho* limits the draw to be either horizontal or vertical. *horizontal* allows horizontal extend. *vertical* allows vertical extend."
    fillcolor: Any
    "Sets the color filling new shapes' interior. Please note that if using a fillcolor with alpha greater than half, drag inside the active shape starts moving the shape underneath, otherwise a new shape could be started over."
    fillrule: Any
    "Determines the path's interior. For more info please visit https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/fill-rule"
    @property
    def label(self) -> _plotly_graph_objs_layout_newshape.Label | Any:
        ...
    @label.setter
    def label(self, value: Any) -> None: ...
    layer: Any
    "Specifies whether new shapes are drawn below gridlines (*below*), between gridlines and traces (*between*) or above traces (*above*)."
    legend: str | Any
    "Sets the reference to a legend to show new shape in. References to these legends are *legend*, *legend2*, *legend3*, etc. Settings for these legends are set in the layout, under `layout.legend`, `layout.legend2`, etc."
    legendgroup: str | Any
    "Sets the legend group for new shape. Traces and shapes part of the same legend group hide/show at the same time when toggling legend items."
    @property
    def legendgrouptitle(self) -> _plotly_graph_objs_layout_newshape.Legendgrouptitle | Any:
        ...
    @legendgrouptitle.setter
    def legendgrouptitle(self, value: Any) -> None: ...
    legendrank: float | Any
    "Sets the legend rank for new shape. Items and groups with smaller ranks are presented on top/left side while with *reversed* `legend.traceorder` they are on bottom/right side. The default legendrank is 1000, so that you can use ranks less than 1000 to place certain items before all unranked items, and ranks greater than 1000 to go after all unranked items."
    legendwidth: float | Any
    "Sets the width (in px or fraction) of the legend for new shape."
    @property
    def line(self) -> _plotly_graph_objs_layout_newshape.Line | Any:
        ...
    @line.setter
    def line(self, value: Any) -> None: ...
    name: str | Any
    "Sets new shape name. The name appears as the legend item."
    opacity: float | Any
    "Sets the opacity of new shapes."
    showlegend: bool | Any
    "Determines whether or not new shape is shown in the legend."
    visible: Any
    "Determines whether or not new shape is visible. If *legendonly*, the shape is not drawn, but can appear as a legend item (provided that the legend itself is visible)."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        drawdirection: Any = ...,
        fillcolor: Any = ...,
        fillrule: Any = ...,
        label: Any = ...,
        layer: Any = ...,
        legend: Any = ...,
        legendgroup: Any = ...,
        legendgrouptitle: Any = ...,
        legendrank: Any = ...,
        legendwidth: Any = ...,
        line: Any = ...,
        name: Any = ...,
        opacity: Any = ...,
        showlegend: Any = ...,
        visible: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Newshape' object\n\nArgs:\n    drawdirection: When `dragmode` is set to *drawrect*, *drawline* or *drawcircle* this limits the drag to be horizontal, vertical or diagonal. Using *diagonal* there is no limit e.g. in drawing lines in any direction. *ortho* limits the draw to be either horizontal or vertical. *horizontal* allows horizontal extend. *vertical* allows vertical extend.\n    fillcolor: Sets the color filling new shapes' interior. Please note that if using a fillcolor with alpha greater than half, drag inside the active shape starts moving the shape underneath, otherwise a new shape could be started over.\n    fillrule: Determines the path's interior. For more info please visit https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/fill-rule\n    layer: Specifies whether new shapes are drawn below gridlines (*below*), between gridlines and traces (*between*) or above traces (*above*).\n    legend: Sets the reference to a legend to show new shape in. References to these legends are *legend*, *legend2*, *legend3*, etc. Settings for these legends are set in the layout, under `layout.legend`, `layout.legend2`, etc.\n    legendgroup: Sets the legend group for new shape. Traces and shapes part of the same legend group hide/show at the same time when toggling legend items.\n    legendrank: Sets the legend rank for new shape. Items and groups with smaller ranks are presented on top/left side while with *reversed* `legend.traceorder` they are on bottom/right side. The default legendrank is 1000, so that you can use ranks less than 1000 to place certain items before all unranked items, and ranks greater than 1000 to go after all unranked items.\n    legendwidth: Sets the width (in px or fraction) of the legend for new shape.\n    name: Sets new shape name. The name appears as the legend item.\n    opacity: Sets the opacity of new shapes.\n    showlegend: Determines whether or not new shape is shown in the legend.\n    visible: Determines whether or not new shape is visible. If *legendonly*, the shape is not drawn, but can appear as a legend item (provided that the legend itself is visible)."
        ...

class Polar(_PlotlyObject):
    "Create a new 'Polar' object"
    @property
    def angularaxis(self) -> _plotly_graph_objs_layout_polar.AngularAxis | Any:
        ...
    @angularaxis.setter
    def angularaxis(self, value: Any) -> None: ...
    bgcolor: Any
    "Set the background color of the subplot"
    @property
    def domain(self) -> _plotly_graph_objs_layout_polar.Domain | Any:
        ...
    @domain.setter
    def domain(self, value: Any) -> None: ...
    gridshape: Any
    "Determines if the radial axis grid lines and angular axis line are drawn as *circular* sectors or as *linear* (polygon) sectors. Has an effect only when the angular axis has `type` *category*. Note that `radialaxis.angle` is snapped to the angle of the closest vertex when `gridshape` is *circular* (so that radial axis scale is the same as the data scale)."
    hole: float | Any
    "Sets the fraction of the radius to cut out of the polar subplot."
    @property
    def radialaxis(self) -> _plotly_graph_objs_layout_polar.RadialAxis | Any:
        ...
    @radialaxis.setter
    def radialaxis(self, value: Any) -> None: ...
    sector: Any
    "Sets angular span of this polar subplot with two angles (in degrees). Sector are assumed to be spanned in the counterclockwise direction with *0* corresponding to rightmost limit of the polar subplot."
    uirevision: Any
    "Controls persistence of user-driven changes in axis attributes, if not overridden in the individual axes. Defaults to `layout.uirevision`."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        angularaxis: Any = ...,
        bgcolor: Any = ...,
        domain: Any = ...,
        gridshape: Any = ...,
        hole: Any = ...,
        radialaxis: Any = ...,
        sector: Any = ...,
        uirevision: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Polar' object\n\nArgs:\n    bgcolor: Set the background color of the subplot\n    gridshape: Determines if the radial axis grid lines and angular axis line are drawn as *circular* sectors or as *linear* (polygon) sectors. Has an effect only when the angular axis has `type` *category*. Note that `radialaxis.angle` is snapped to the angle of the closest vertex when `gridshape` is *circular* (so that radial axis scale is the same as the data scale).\n    hole: Sets the fraction of the radius to cut out of the polar subplot.\n    sector: Sets angular span of this polar subplot with two angles (in degrees). Sector are assumed to be spanned in the counterclockwise direction with *0* corresponding to rightmost limit of the polar subplot.\n    uirevision: Controls persistence of user-driven changes in axis attributes, if not overridden in the individual axes. Defaults to `layout.uirevision`."
        ...

class Scene(_PlotlyObject):
    "Create a new 'Scene' object"
    @property
    def annotation(self) -> _plotly_graph_objs_layout_scene.Annotation | Any:
        ...
    @annotation.setter
    def annotation(self, value: Any) -> None: ...
    aspectmode: Any
    "If *cube*, this scene's axes are drawn as a cube, regardless of the axes' ranges. If *data*, this scene's axes are drawn in proportion with the axes' ranges. If *manual*, this scene's axes are drawn in proportion with the input of *aspectratio* (the default behavior if *aspectratio* is provided). If *auto*, this scene's axes are drawn using the results of *data* except when one axis is more than four times the size of the two others, where in that case the results of *cube* are used."
    @property
    def aspectratio(self) -> _plotly_graph_objs_layout_scene.Aspectratio | Any:
        "Sets this scene's axis aspectratio."
        ...
    @aspectratio.setter
    def aspectratio(self, value: Any) -> None: ...
    bgcolor: Any
    @property
    def camera(self) -> _plotly_graph_objs_layout_scene.Camera | Any:
        ...
    @camera.setter
    def camera(self, value: Any) -> None: ...
    @property
    def domain(self) -> _plotly_graph_objs_layout_scene.Domain | Any:
        ...
    @domain.setter
    def domain(self, value: Any) -> None: ...
    dragmode: Any
    "Determines the mode of drag interactions for this scene."
    hovermode: Any
    "Determines the mode of hover interactions for this scene."
    uirevision: Any
    "Controls persistence of user-driven changes in camera attributes. Defaults to `layout.uirevision`."
    @property
    def xaxis(self) -> _plotly_graph_objs_layout_scene.XAxis | Any:
        ...
    @xaxis.setter
    def xaxis(self, value: Any) -> None: ...
    @property
    def yaxis(self) -> _plotly_graph_objs_layout_scene.YAxis | Any:
        ...
    @yaxis.setter
    def yaxis(self, value: Any) -> None: ...
    @property
    def zaxis(self) -> _plotly_graph_objs_layout_scene.ZAxis | Any:
        ...
    @zaxis.setter
    def zaxis(self, value: Any) -> None: ...
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        annotation: Any = ...,
        aspectmode: Any = ...,
        aspectratio: Any = ...,
        bgcolor: Any = ...,
        camera: Any = ...,
        domain: Any = ...,
        dragmode: Any = ...,
        hovermode: Any = ...,
        uirevision: Any = ...,
        xaxis: Any = ...,
        yaxis: Any = ...,
        zaxis: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Scene' object\n\nArgs:\n    aspectmode: If *cube*, this scene's axes are drawn as a cube, regardless of the axes' ranges. If *data*, this scene's axes are drawn in proportion with the axes' ranges. If *manual*, this scene's axes are drawn in proportion with the input of *aspectratio* (the default behavior if *aspectratio* is provided). If *auto*, this scene's axes are drawn using the results of *data* except when one axis is more than four times the size of the two others, where in that case the results of *cube* are used.\n    aspectratio: Sets this scene's axis aspectratio.\n    dragmode: Determines the mode of drag interactions for this scene.\n    hovermode: Determines the mode of hover interactions for this scene.\n    uirevision: Controls persistence of user-driven changes in camera attributes. Defaults to `layout.uirevision`."
        ...

class Selection(_PlotlyObject):
    "Create a new 'Selection' object"
    @property
    def line(self) -> _plotly_graph_objs_layout_selection.Line | Any:
        ...
    @line.setter
    def line(self, value: Any) -> None: ...
    name: str | Any
    "When used in a template, named items are created in the output figure in addition to any items the figure already has in this array. You can modify these items in the output figure by making your own item with `templateitemname` matching this `name` alongside your modifications (including `visible: false` or `enabled: false` to hide it). Has no effect outside of a template."
    opacity: float | Any
    "Sets the opacity of the selection."
    path: str | Any
    "For `type` *path* - a valid SVG path similar to `shapes.path` in data coordinates. Allowed segments are: M, L and Z."
    templateitemname: str | Any
    "Used to refer to a named item in this array in the template. Named items from the template will be created even without a matching item in the input figure, but you can modify one by making an item with `templateitemname` matching its `name`, alongside your modifications (including `visible: false` or `enabled: false` to hide it). If there is no template or no matching item, this item will be hidden unless you explicitly show it with `visible: true`."
    type: Any
    "Specifies the selection type to be drawn. If *rect*, a rectangle is drawn linking (`x0`,`y0`), (`x1`,`y0`), (`x1`,`y1`) and (`x0`,`y1`). If *path*, draw a custom SVG path using `path`."
    x0: Any
    "Sets the selection's starting x position."
    x1: Any
    "Sets the selection's end x position."
    xref: Any
    "Sets the selection's x coordinate axis. If set to a x axis id (e.g. *x* or *x2*), the `x` position refers to a x coordinate. If set to *paper*, the `x` position refers to the distance from the left of the plotting area in normalized coordinates where *0* (*1*) corresponds to the left (right). If set to a x axis ID followed by *domain* (separated by a space), the position behaves like for *paper*, but refers to the distance in fractions of the domain length from the left of the domain of that axis: e.g., *x2 domain* refers to the domain of the second x axis and a x position of 0.5 refers to the point between the left and the right of the domain of the second x axis."
    y0: Any
    "Sets the selection's starting y position."
    y1: Any
    "Sets the selection's end y position."
    yref: Any
    "Sets the selection's x coordinate axis. If set to a y axis id (e.g. *y* or *y2*), the `y` position refers to a y coordinate. If set to *paper*, the `y` position refers to the distance from the bottom of the plotting area in normalized coordinates where *0* (*1*) corresponds to the bottom (top). If set to a y axis ID followed by *domain* (separated by a space), the position behaves like for *paper*, but refers to the distance in fractions of the domain length from the bottom of the domain of that axis: e.g., *y2 domain* refers to the domain of the second y axis and a y position of 0.5 refers to the point between the bottom and the top of the domain of the second y axis."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        line: Any = ...,
        name: Any = ...,
        opacity: Any = ...,
        path: Any = ...,
        templateitemname: Any = ...,
        type: Any = ...,
        x0: Any = ...,
        x1: Any = ...,
        xref: Any = ...,
        y0: Any = ...,
        y1: Any = ...,
        yref: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Selection' object\n\nArgs:\n    name: When used in a template, named items are created in the output figure in addition to any items the figure already has in this array. You can modify these items in the output figure by making your own item with `templateitemname` matching this `name` alongside your modifications (including `visible: false` or `enabled: false` to hide it). Has no effect outside of a template.\n    opacity: Sets the opacity of the selection.\n    path: For `type` *path* - a valid SVG path similar to `shapes.path` in data coordinates. Allowed segments are: M, L and Z.\n    templateitemname: Used to refer to a named item in this array in the template. Named items from the template will be created even without a matching item in the input figure, but you can modify one by making an item with `templateitemname` matching its `name`, alongside your modifications (including `visible: false` or `enabled: false` to hide it). If there is no template or no matching item, this item will be hidden unless you explicitly show it with `visible: true`.\n    type: Specifies the selection type to be drawn. If *rect*, a rectangle is drawn linking (`x0`,`y0`), (`x1`,`y0`), (`x1`,`y1`) and (`x0`,`y1`). If *path*, draw a custom SVG path using `path`.\n    x0: Sets the selection's starting x position.\n    x1: Sets the selection's end x position.\n    xref: Sets the selection's x coordinate axis. If set to a x axis id (e.g. *x* or *x2*), the `x` position refers to a x coordinate. If set to *paper*, the `x` position refers to the distance from the left of the plotting area in normalized coordinates where *0* (*1*) corresponds to the left (right). If set to a x axis ID followed by *domain* (separated by a space), the position behaves like for *paper*, but refers to the distance in fractions of the domain length from the left of the domain of that axis: e.g., *x2 domain* refers to the domain of the second x axis and a x position of 0.5 refers to the point between the left and the right of the domain of the second x axis.\n    y0: Sets the selection's starting y position.\n    y1: Sets the selection's end y position.\n    yref: Sets the selection's x coordinate axis. If set to a y axis id (e.g. *y* or *y2*), the `y` position refers to a y coordinate. If set to *paper*, the `y` position refers to the distance from the bottom of the plotting area in normalized coordinates where *0* (*1*) corresponds to the bottom (top). If set to a y axis ID followed by *domain* (separated by a space), the position behaves like for *paper*, but refers to the distance in fractions of the domain length from the bottom of the domain of that axis: e.g., *y2 domain* refers to the domain of the second y axis and a y position of 0.5 refers to the point between the bottom and the top of the domain of the second y axis."
        ...

class Shape(_PlotlyObject):
    "Create a new 'Shape' object"
    editable: bool | Any
    "Determines whether the shape could be activated for edit or not. Has no effect when the older editable shapes mode is enabled via `config.editable` or `config.edits.shapePosition`."
    fillcolor: Any
    "Sets the color filling the shape's interior. Only applies to closed shapes."
    fillrule: Any
    "Determines which regions of complex paths constitute the interior. For more info please visit https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/fill-rule"
    @property
    def label(self) -> _plotly_graph_objs_layout_shape.Label | Any:
        ...
    @label.setter
    def label(self, value: Any) -> None: ...
    layer: Any
    "Specifies whether shapes are drawn below gridlines (*below*), between gridlines and traces (*between*) or above traces (*above*)."
    legend: str | Any
    "Sets the reference to a legend to show this shape in. References to these legends are *legend*, *legend2*, *legend3*, etc. Settings for these legends are set in the layout, under `layout.legend`, `layout.legend2`, etc."
    legendgroup: str | Any
    "Sets the legend group for this shape. Traces and shapes part of the same legend group hide/show at the same time when toggling legend items."
    @property
    def legendgrouptitle(self) -> _plotly_graph_objs_layout_shape.Legendgrouptitle | Any:
        ...
    @legendgrouptitle.setter
    def legendgrouptitle(self, value: Any) -> None: ...
    legendrank: float | Any
    "Sets the legend rank for this shape. Items and groups with smaller ranks are presented on top/left side while with *reversed* `legend.traceorder` they are on bottom/right side. The default legendrank is 1000, so that you can use ranks less than 1000 to place certain items before all unranked items, and ranks greater than 1000 to go after all unranked items. When having unranked or equal rank items shapes would be displayed after traces i.e. according to their order in data and layout."
    legendwidth: float | Any
    "Sets the width (in px or fraction) of the legend for this shape."
    @property
    def line(self) -> _plotly_graph_objs_layout_shape.Line | Any:
        ...
    @line.setter
    def line(self, value: Any) -> None: ...
    name: str | Any
    "When used in a template, named items are created in the output figure in addition to any items the figure already has in this array. You can modify these items in the output figure by making your own item with `templateitemname` matching this `name` alongside your modifications (including `visible: false` or `enabled: false` to hide it). Has no effect outside of a template."
    opacity: float | Any
    "Sets the opacity of the shape."
    path: str | Any
    "For `type` *path* - a valid SVG path with the pixel values replaced by data values in `xsizemode`/`ysizemode` being *scaled* and taken unmodified as pixels relative to `xanchor` and `yanchor` in case of *pixel* size mode. There are a few restrictions / quirks only absolute instructions, not relative. So the allowed segments are: M, L, H, V, Q, C, T, S, and Z arcs (A) are not allowed because radius rx and ry are relative. In the future we could consider supporting relative commands, but we would have to decide on how to handle date and log axes. Note that even as is, Q and C Bezier paths that are smooth on linear axes may not be smooth on log, and vice versa. no chained \"polybezier\" commands - specify the segment type for each one. On category axes, values are numbers scaled to the serial numbers of categories because using the categories themselves there would be no way to describe fractional positions On data axes: because space and T are both normal components of path strings, we can't use either to separate date from time parts. Therefore we'll use underscore for this purpose: 2015-02-21_13:45:56.789"
    showlegend: bool | Any
    "Determines whether or not this shape is shown in the legend."
    templateitemname: str | Any
    "Used to refer to a named item in this array in the template. Named items from the template will be created even without a matching item in the input figure, but you can modify one by making an item with `templateitemname` matching its `name`, alongside your modifications (including `visible: false` or `enabled: false` to hide it). If there is no template or no matching item, this item will be hidden unless you explicitly show it with `visible: true`."
    type: Any
    "Specifies the shape type to be drawn. If *line*, a line is drawn from (`x0`,`y0`) to (`x1`,`y1`) with respect to the axes' sizing mode. If *circle*, a circle is drawn from ((`x0`+`x1`)/2, (`y0`+`y1`)/2)) with radius (|(`x0`+`x1`)/2 - `x0`|, |(`y0`+`y1`)/2 -`y0`)|) with respect to the axes' sizing mode. If *rect*, a rectangle is drawn linking (`x0`,`y0`), (`x1`,`y0`), (`x1`,`y1`), (`x0`,`y1`), (`x0`,`y0`) with respect to the axes' sizing mode. If *path*, draw a custom SVG path using `path`. with respect to the axes' sizing mode."
    visible: Any
    "Determines whether or not this shape is visible. If *legendonly*, the shape is not drawn, but can appear as a legend item (provided that the legend itself is visible)."
    x0: Any
    "Sets the shape's starting x position. See `type` and `xsizemode` for more info."
    x0shift: float | Any
    "Shifts `x0` away from the center of the category when `xref` is a *category* or *multicategory* axis. -0.5 corresponds to the start of the category and 0.5 corresponds to the end of the category."
    x1: Any
    "Sets the shape's end x position. See `type` and `xsizemode` for more info."
    x1shift: float | Any
    "Shifts `x1` away from the center of the category when `xref` is a *category* or *multicategory* axis. -0.5 corresponds to the start of the category and 0.5 corresponds to the end of the category."
    xanchor: Any
    "Only relevant in conjunction with `xsizemode` set to *pixel*. Specifies the anchor point on the x axis to which `x0`, `x1` and x coordinates within `path` are relative to. E.g. useful to attach a pixel sized shape to a certain data value. No effect when `xsizemode` not set to *pixel*."
    xref: Any
    "Sets the shape's x coordinate axis. If set to a x axis id (e.g. *x* or *x2*), the `x` position refers to a x coordinate. If set to *paper*, the `x` position refers to the distance from the left of the plotting area in normalized coordinates where *0* (*1*) corresponds to the left (right). If set to a x axis ID followed by *domain* (separated by a space), the position behaves like for *paper*, but refers to the distance in fractions of the domain length from the left of the domain of that axis: e.g., *x2 domain* refers to the domain of the second x axis and a x position of 0.5 refers to the point between the left and the right of the domain of the second x axis. If an array of axis IDs is provided, each `x` value will refer to the corresponding axis, e.g., ['x', 'x2'] for a rectangle, line, or circle means `x0` uses the `x` axis and `x1` uses the `x2` axis. Path shapes using an array should have one entry for each x coordinate in the string."
    xsizemode: Any
    "Sets the shapes's sizing mode along the x axis. If set to *scaled*, `x0`, `x1` and x coordinates within `path` refer to data values on the x axis or a fraction of the plot area's width (`xref` set to *paper*). If set to *pixel*, `xanchor` specifies the x position in terms of data or plot fraction but `x0`, `x1` and x coordinates within `path` are pixels relative to `xanchor`. This way, the shape can have a fixed width while maintaining a position relative to data or plot fraction. Note: `xsizemode` *pixel* is not supported when `xref` is an array."
    y0: Any
    "Sets the shape's starting y position. See `type` and `ysizemode` for more info."
    y0shift: float | Any
    "Shifts `y0` away from the center of the category when `yref` is a *category* or *multicategory* axis. -0.5 corresponds to the start of the category and 0.5 corresponds to the end of the category."
    y1: Any
    "Sets the shape's end y position. See `type` and `ysizemode` for more info."
    y1shift: float | Any
    "Shifts `y1` away from the center of the category when `yref` is a *category* or *multicategory* axis. -0.5 corresponds to the start of the category and 0.5 corresponds to the end of the category."
    yanchor: Any
    "Only relevant in conjunction with `ysizemode` set to *pixel*. Specifies the anchor point on the y axis to which `y0`, `y1` and y coordinates within `path` are relative to. E.g. useful to attach a pixel sized shape to a certain data value. No effect when `ysizemode` not set to *pixel*."
    yref: Any
    "Sets the shape's y coordinate axis. If set to a y axis id (e.g. *y* or *y2*), the `y` position refers to a y coordinate. If set to *paper*, the `y` position refers to the distance from the bottom of the plotting area in normalized coordinates where *0* (*1*) corresponds to the bottom (top). If set to a y axis ID followed by *domain* (separated by a space), the position behaves like for *paper*, but refers to the distance in fractions of the domain length from the bottom of the domain of that axis: e.g., *y2 domain* refers to the domain of the second y axis and a y position of 0.5 refers to the point between the bottom and the top of the domain of the second y axis. If an array of axis IDs is provided, each `y` value will refer to the corresponding axis, e.g., ['y', 'y2'] for a rectangle, line, or circle means `y0` uses the `y` axis and `y1` uses the `y2` axis. Path shapes using an array should have one entry for each y coordinate in the string."
    ysizemode: Any
    "Sets the shapes's sizing mode along the y axis. If set to *scaled*, `y0`, `y1` and y coordinates within `path` refer to data values on the y axis or a fraction of the plot area's height (`yref` set to *paper*). If set to *pixel*, `yanchor` specifies the y position in terms of data or plot fraction but `y0`, `y1` and y coordinates within `path` are pixels relative to `yanchor`. This way, the shape can have a fixed height while maintaining a position relative to data or plot fraction. Note: `ysizemode` *pixel* is not supported when `yref` is an array."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        editable: Any = ...,
        fillcolor: Any = ...,
        fillrule: Any = ...,
        label: Any = ...,
        layer: Any = ...,
        legend: Any = ...,
        legendgroup: Any = ...,
        legendgrouptitle: Any = ...,
        legendrank: Any = ...,
        legendwidth: Any = ...,
        line: Any = ...,
        name: Any = ...,
        opacity: Any = ...,
        path: Any = ...,
        showlegend: Any = ...,
        templateitemname: Any = ...,
        type: Any = ...,
        visible: Any = ...,
        x0: Any = ...,
        x0shift: Any = ...,
        x1: Any = ...,
        x1shift: Any = ...,
        xanchor: Any = ...,
        xref: Any = ...,
        xsizemode: Any = ...,
        y0: Any = ...,
        y0shift: Any = ...,
        y1: Any = ...,
        y1shift: Any = ...,
        yanchor: Any = ...,
        yref: Any = ...,
        ysizemode: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Shape' object\n\nArgs:\n    editable: Determines whether the shape could be activated for edit or not. Has no effect when the older editable shapes mode is enabled via `config.editable` or `config.edits.shapePosition`.\n    fillcolor: Sets the color filling the shape's interior. Only applies to closed shapes.\n    fillrule: Determines which regions of complex paths constitute the interior. For more info please visit https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/fill-rule\n    layer: Specifies whether shapes are drawn below gridlines (*below*), between gridlines and traces (*between*) or above traces (*above*).\n    legend: Sets the reference to a legend to show this shape in. References to these legends are *legend*, *legend2*, *legend3*, etc. Settings for these legends are set in the layout, under `layout.legend`, `layout.legend2`, etc.\n    legendgroup: Sets the legend group for this shape. Traces and shapes part of the same legend group hide/show at the same time when toggling legend items.\n    legendrank: Sets the legend rank for this shape. Items and groups with smaller ranks are presented on top/left side while with *reversed* `legend.traceorder` they are on bottom/right side. The default legendrank is 1000, so that you can use ranks less than 1000 to place certain items before all unranked items, and ranks greater than 1000 to go after all unranked items. When having unranked or equal rank items shapes would be displayed after traces i.e. according to their order in data and layout.\n    legendwidth: Sets the width (in px or fraction) of the legend for this shape.\n    name: When used in a template, named items are created in the output figure in addition to any items the figure already has in this array. You can modify these items in the output figure by making your own item with `templateitemname` matching this `name` alongside your modifications (including `visible: false` or `enabled: false` to hide it). Has no effect outside of a template.\n    opacity: Sets the opacity of the shape.\n    path: For `type` *path* - a valid SVG path with the pixel values replaced by data values in `xsizemode`/`ysizemode` being *scaled* and taken unmodified as pixels relative to `xanchor` and `yanchor` in case of *pixel* size mode. There are a few restrictions / quirks only absolute instructions, not relative. So the allowed segments are: M, L, H, V, Q, C, T, S, and Z arcs (A) are not allowed because radius rx and ry are relative. In the future we could consider supporting relative commands, but we would have to decide on how to handle date and log axes. Note that even as is, Q and C Bezier paths that are smooth on linear axes may not be smooth on log, and vice versa. no chained \"polybezier\" commands - specify the segment type for each one. On category axes, values are numbers scaled to the serial numbers of categories because using the categories themselves there would be no way to describe fractional positions On data axes: because space and T are both normal components of path strings, we can't use either to separate date from time parts. Therefore we'll use underscore for this purpose: 2015-02-21_13:45:56.789\n    showlegend: Determines whether or not this shape is shown in the legend.\n    templateitemname: Used to refer to a named item in this array in the template. Named items from the template will be created even without a matching item in the input figure, but you can modify one by making an item with `templateitemname` matching its `name`, alongside your modifications (including `visible: false` or `enabled: false` to hide it). If there is no template or no matching item, this item will be hidden unless you explicitly show it with `visible: true`.\n    type: Specifies the shape type to be drawn. If *line*, a line is drawn from (`x0`,`y0`) to (`x1`,`y1`) with respect to the axes' sizing mode. If *circle*, a circle is drawn from ((`x0`+`x1`)/2, (`y0`+`y1`)/2)) with radius (|(`x0`+`x1`)/2 - `x0`|, |(`y0`+`y1`)/2 -`y0`)|) with respect to the axes' sizing mode. If *rect*, a rectangle is drawn linking (`x0`,`y0`), (`x1`,`y0`), (`x1`,`y1`), (`x0`,`y1`), (`x0`,`y0`) with respect to the axes' sizing mode. If *path*, draw a custom SVG path using `path`. with respect to the axes' sizing mode.\n    visible: Determines whether or not this shape is visible. If *legendonly*, the shape is not drawn, but can appear as a legend item (provided that the legend itself is visible).\n    x0: Sets the shape's starting x position. See `type` and `xsizemode` for more info.\n    x0shift: Shifts `x0` away from the center of the category when `xref` is a *category* or *multicategory* axis. -0.5 corresponds to the start of the category and 0.5 corresponds to the end of the category.\n    x1: Sets the shape's end x position. See `type` and `xsizemode` for more info.\n    x1shift: Shifts `x1` away from the center of the category when `xref` is a *category* or *multicategory* axis. -0.5 corresponds to the start of the category and 0.5 corresponds to the end of the category.\n    xanchor: Only relevant in conjunction with `xsizemode` set to *pixel*. Specifies the anchor point on the x axis to which `x0`, `x1` and x coordinates within `path` are relative to. E.g. useful to attach a pixel sized shape to a certain data value. No effect when `xsizemode` not set to *pixel*.\n    xref: Sets the shape's x coordinate axis. If set to a x axis id (e.g. *x* or *x2*), the `x` position refers to a x coordinate. If set to *paper*, the `x` position refers to the distance from the left of the plotting area in normalized coordinates where *0* (*1*) corresponds to the left (right). If set to a x axis ID followed by *domain* (separated by a space), the position behaves like for *paper*, but refers to the distance in fractions of the domain length from the left of the domain of that axis: e.g., *x2 domain* refers to the domain of the second x axis and a x position of 0.5 refers to the point between the left and the right of the domain of the second x axis. If an array of axis IDs is provided, each `x` value will refer to the corresponding axis, e.g., ['x', 'x2'] for a rectangle, line, or circle means `x0` uses the `x` axis and `x1` uses the `x2` axis. Path shapes using an array should have one entry for each x coordinate in the string.\n    xsizemode: Sets the shapes's sizing mode along the x axis. If set to *scaled*, `x0`, `x1` and x coordinates within `path` refer to data values on the x axis or a fraction of the plot area's width (`xref` set to *paper*). If set to *pixel*, `xanchor` specifies the x position in terms of data or plot fraction but `x0`, `x1` and x coordinates within `path` are pixels relative to `xanchor`. This way, the shape can have a fixed width while maintaining a position relative to data or plot fraction. Note: `xsizemode` *pixel* is not supported when `xref` is an array.\n    y0: Sets the shape's starting y position. See `type` and `ysizemode` for more info.\n    y0shift: Shifts `y0` away from the center of the category when `yref` is a *category* or *multicategory* axis. -0.5 corresponds to the start of the category and 0.5 corresponds to the end of the category.\n    y1: Sets the shape's end y position. See `type` and `ysizemode` for more info.\n    y1shift: Shifts `y1` away from the center of the category when `yref` is a *category* or *multicategory* axis. -0.5 corresponds to the start of the category and 0.5 corresponds to the end of the category.\n    yanchor: Only relevant in conjunction with `ysizemode` set to *pixel*. Specifies the anchor point on the y axis to which `y0`, `y1` and y coordinates within `path` are relative to. E.g. useful to attach a pixel sized shape to a certain data value. No effect when `ysizemode` not set to *pixel*.\n    yref: Sets the shape's y coordinate axis. If set to a y axis id (e.g. *y* or *y2*), the `y` position refers to a y coordinate. If set to *paper*, the `y` position refers to the distance from the bottom of the plotting area in normalized coordinates where *0* (*1*) corresponds to the bottom (top). If set to a y axis ID followed by *domain* (separated by a space), the position behaves like for *paper*, but refers to the distance in fractions of the domain length from the bottom of the domain of that axis: e.g., *y2 domain* refers to the domain of the second y axis and a y position of 0.5 refers to the point between the bottom and the top of the domain of the second y axis. If an array of axis IDs is provided, each `y` value will refer to the corresponding axis, e.g., ['y', 'y2'] for a rectangle, line, or circle means `y0` uses the `y` axis and `y1` uses the `y2` axis. Path shapes using an array should have one entry for each y coordinate in the string.\n    ysizemode: Sets the shapes's sizing mode along the y axis. If set to *scaled*, `y0`, `y1` and y coordinates within `path` refer to data values on the y axis or a fraction of the plot area's height (`yref` set to *paper*). If set to *pixel*, `yanchor` specifies the y position in terms of data or plot fraction but `y0`, `y1` and y coordinates within `path` are pixels relative to `yanchor`. This way, the shape can have a fixed height while maintaining a position relative to data or plot fraction. Note: `ysizemode` *pixel* is not supported when `yref` is an array."
        ...

class Slider(_PlotlyObject):
    "Create a new 'Slider' object"
    active: float | Any
    "Determines which button (by index starting from 0) is considered active."
    activebgcolor: Any
    "Sets the background color of the slider grip while dragging."
    bgcolor: Any
    "Sets the background color of the slider."
    bordercolor: Any
    "Sets the color of the border enclosing the slider."
    borderwidth: float | Any
    "Sets the width (in px) of the border enclosing the slider."
    @property
    def currentvalue(self) -> _plotly_graph_objs_layout_slider.Currentvalue | Any:
        ...
    @currentvalue.setter
    def currentvalue(self, value: Any) -> None: ...
    @property
    def font(self) -> _plotly_graph_objs_layout_slider.Font | Any:
        "Sets the font of the slider step labels."
        ...
    @font.setter
    def font(self, value: Any) -> None: ...
    len: float | Any
    "Sets the length of the slider This measure excludes the padding of both ends. That is, the slider's length is this length minus the padding on both ends."
    lenmode: Any
    "Determines whether this slider length is set in units of plot *fraction* or in *pixels. Use `len` to set the value."
    minorticklen: float | Any
    "Sets the length in pixels of minor step tick marks"
    name: str | Any
    "When used in a template, named items are created in the output figure in addition to any items the figure already has in this array. You can modify these items in the output figure by making your own item with `templateitemname` matching this `name` alongside your modifications (including `visible: false` or `enabled: false` to hide it). Has no effect outside of a template."
    @property
    def pad(self) -> _plotly_graph_objs_layout_slider.Pad | Any:
        "Set the padding of the slider component along each side."
        ...
    @pad.setter
    def pad(self, value: Any) -> None: ...
    @property
    def step(self) -> _plotly_graph_objs_layout_slider.Step | Any:
        ...
    @step.setter
    def step(self, value: Any) -> None: ...
    templateitemname: str | Any
    "Used to refer to a named item in this array in the template. Named items from the template will be created even without a matching item in the input figure, but you can modify one by making an item with `templateitemname` matching its `name`, alongside your modifications (including `visible: false` or `enabled: false` to hide it). If there is no template or no matching item, this item will be hidden unless you explicitly show it with `visible: true`."
    tickcolor: Any
    "Sets the color of the border enclosing the slider."
    ticklen: float | Any
    "Sets the length in pixels of step tick marks"
    tickwidth: float | Any
    "Sets the tick width (in px)."
    @property
    def transition(self) -> _plotly_graph_objs_layout_slider.Transition | Any:
        ...
    @transition.setter
    def transition(self, value: Any) -> None: ...
    visible: bool | Any
    "Determines whether or not the slider is visible."
    x: float | Any
    "Sets the x position (in normalized coordinates) of the slider."
    xanchor: Any
    "Sets the slider's horizontal position anchor. This anchor binds the `x` position to the *left*, *center* or *right* of the range selector."
    y: float | Any
    "Sets the y position (in normalized coordinates) of the slider."
    yanchor: Any
    "Sets the slider's vertical position anchor This anchor binds the `y` position to the *top*, *middle* or *bottom* of the range selector."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        active: Any = ...,
        activebgcolor: Any = ...,
        bgcolor: Any = ...,
        bordercolor: Any = ...,
        borderwidth: Any = ...,
        currentvalue: Any = ...,
        font: Any = ...,
        len: Any = ...,
        lenmode: Any = ...,
        minorticklen: Any = ...,
        name: Any = ...,
        pad: Any = ...,
        step: Any = ...,
        templateitemname: Any = ...,
        tickcolor: Any = ...,
        ticklen: Any = ...,
        tickwidth: Any = ...,
        transition: Any = ...,
        visible: Any = ...,
        x: Any = ...,
        xanchor: Any = ...,
        y: Any = ...,
        yanchor: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Slider' object\n\nArgs:\n    active: Determines which button (by index starting from 0) is considered active.\n    activebgcolor: Sets the background color of the slider grip while dragging.\n    bgcolor: Sets the background color of the slider.\n    bordercolor: Sets the color of the border enclosing the slider.\n    borderwidth: Sets the width (in px) of the border enclosing the slider.\n    font: Sets the font of the slider step labels.\n    len: Sets the length of the slider This measure excludes the padding of both ends. That is, the slider's length is this length minus the padding on both ends.\n    lenmode: Determines whether this slider length is set in units of plot *fraction* or in *pixels. Use `len` to set the value.\n    minorticklen: Sets the length in pixels of minor step tick marks\n    name: When used in a template, named items are created in the output figure in addition to any items the figure already has in this array. You can modify these items in the output figure by making your own item with `templateitemname` matching this `name` alongside your modifications (including `visible: false` or `enabled: false` to hide it). Has no effect outside of a template.\n    pad: Set the padding of the slider component along each side.\n    templateitemname: Used to refer to a named item in this array in the template. Named items from the template will be created even without a matching item in the input figure, but you can modify one by making an item with `templateitemname` matching its `name`, alongside your modifications (including `visible: false` or `enabled: false` to hide it). If there is no template or no matching item, this item will be hidden unless you explicitly show it with `visible: true`.\n    tickcolor: Sets the color of the border enclosing the slider.\n    ticklen: Sets the length in pixels of step tick marks\n    tickwidth: Sets the tick width (in px).\n    visible: Determines whether or not the slider is visible.\n    x: Sets the x position (in normalized coordinates) of the slider.\n    xanchor: Sets the slider's horizontal position anchor. This anchor binds the `x` position to the *left*, *center* or *right* of the range selector.\n    y: Sets the y position (in normalized coordinates) of the slider.\n    yanchor: Sets the slider's vertical position anchor This anchor binds the `y` position to the *top*, *middle* or *bottom* of the range selector."
        ...

class Smith(_PlotlyObject):
    "Create a new 'Smith' object"
    bgcolor: Any
    "Set the background color of the subplot"
    @property
    def domain(self) -> _plotly_graph_objs_layout_smith.Domain | Any:
        ...
    @domain.setter
    def domain(self, value: Any) -> None: ...
    @property
    def imaginaryaxis(self) -> _plotly_graph_objs_layout_smith.Imaginaryaxis | Any:
        ...
    @imaginaryaxis.setter
    def imaginaryaxis(self, value: Any) -> None: ...
    @property
    def realaxis(self) -> _plotly_graph_objs_layout_smith.Realaxis | Any:
        ...
    @realaxis.setter
    def realaxis(self, value: Any) -> None: ...
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        bgcolor: Any = ...,
        domain: Any = ...,
        imaginaryaxis: Any = ...,
        realaxis: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Smith' object\n\nArgs:\n    bgcolor: Set the background color of the subplot"
        ...

class Template(_PlotlyObject):
    "Create a new 'Template' object"
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        **kwargs: Any,
    ) -> None:
        ...

class Ternary(_PlotlyObject):
    "Create a new 'Ternary' object"
    @property
    def aaxis(self) -> _plotly_graph_objs_layout_ternary.Aaxis | Any:
        ...
    @aaxis.setter
    def aaxis(self, value: Any) -> None: ...
    @property
    def baxis(self) -> _plotly_graph_objs_layout_ternary.Baxis | Any:
        ...
    @baxis.setter
    def baxis(self, value: Any) -> None: ...
    bgcolor: Any
    "Set the background color of the subplot"
    @property
    def caxis(self) -> _plotly_graph_objs_layout_ternary.Caxis | Any:
        ...
    @caxis.setter
    def caxis(self, value: Any) -> None: ...
    @property
    def domain(self) -> _plotly_graph_objs_layout_ternary.Domain | Any:
        ...
    @domain.setter
    def domain(self, value: Any) -> None: ...
    sum: float | Any
    "The number each triplet should sum to, and the maximum range of each axis"
    uirevision: Any
    "Controls persistence of user-driven changes in axis `min` and `title`, if not overridden in the individual axes. Defaults to `layout.uirevision`."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        aaxis: Any = ...,
        baxis: Any = ...,
        bgcolor: Any = ...,
        caxis: Any = ...,
        domain: Any = ...,
        sum: Any = ...,
        uirevision: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Ternary' object\n\nArgs:\n    bgcolor: Set the background color of the subplot\n    sum: The number each triplet should sum to, and the maximum range of each axis\n    uirevision: Controls persistence of user-driven changes in axis `min` and `title`, if not overridden in the individual axes. Defaults to `layout.uirevision`."
        ...

class Title(_PlotlyObject):
    "Create a new 'Title' object"
    automargin: bool | Any
    "Determines whether the title can automatically push the figure margins. If `yref='paper'` then the margin will expand to ensure that the title doesn’t overlap with the edges of the container. If `yref='container'` then the margins will ensure that the title doesn’t overlap with the plot area, tick labels, and axis titles. If `automargin=true` and the margins need to be expanded, then y will be set to a default 1 and yanchor will be set to an appropriate default to ensure that minimal margin space is needed. Note that when `yref='paper'`, only 1 or 0 are allowed y values. Invalid values will be reset to the default 1."
    @property
    def font(self) -> _plotly_graph_objs_layout_title.Font | Any:
        "Sets the title font."
        ...
    @font.setter
    def font(self, value: Any) -> None: ...
    @property
    def pad(self) -> _plotly_graph_objs_layout_title.Pad | Any:
        "Sets the padding of the title. Each padding value only applies when the corresponding `xanchor`/`yanchor` value is set accordingly. E.g. for left padding to take effect, `xanchor` must be set to *left*. The same rule applies if `xanchor`/`yanchor` is determined automatically. Padding is muted if the respective anchor value is *middle*/*center*."
        ...
    @pad.setter
    def pad(self, value: Any) -> None: ...
    @property
    def subtitle(self) -> _plotly_graph_objs_layout_title.Subtitle | Any:
        ...
    @subtitle.setter
    def subtitle(self, value: Any) -> None: ...
    text: str | Any
    "Sets the plot's title."
    x: float | Any
    "Sets the x position with respect to `xref` in normalized coordinates from *0* (left) to *1* (right)."
    xanchor: Any
    "Sets the title's horizontal alignment with respect to its x position. *left* means that the title starts at x, *right* means that the title ends at x and *center* means that the title's center is at x. *auto* divides `xref` by three and calculates the `xanchor` value automatically based on the value of `x`."
    xref: Any
    "Sets the container `x` refers to. *container* spans the entire `width` of the plot. *paper* refers to the width of the plotting area only."
    y: float | Any
    "Sets the y position with respect to `yref` in normalized coordinates from *0* (bottom) to *1* (top). *auto* places the baseline of the title onto the vertical center of the top margin."
    yanchor: Any
    "Sets the title's vertical alignment with respect to its y position. *top* means that the title's cap line is at y, *bottom* means that the title's baseline is at y and *middle* means that the title's midline is at y. *auto* divides `yref` by three and calculates the `yanchor` value automatically based on the value of `y`."
    yref: Any
    "Sets the container `y` refers to. *container* spans the entire `height` of the plot. *paper* refers to the height of the plotting area only."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        automargin: Any = ...,
        font: Any = ...,
        pad: Any = ...,
        subtitle: Any = ...,
        text: Any = ...,
        x: Any = ...,
        xanchor: Any = ...,
        xref: Any = ...,
        y: Any = ...,
        yanchor: Any = ...,
        yref: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Title' object\n\nArgs:\n    automargin: Determines whether the title can automatically push the figure margins. If `yref='paper'` then the margin will expand to ensure that the title doesn’t overlap with the edges of the container. If `yref='container'` then the margins will ensure that the title doesn’t overlap with the plot area, tick labels, and axis titles. If `automargin=true` and the margins need to be expanded, then y will be set to a default 1 and yanchor will be set to an appropriate default to ensure that minimal margin space is needed. Note that when `yref='paper'`, only 1 or 0 are allowed y values. Invalid values will be reset to the default 1.\n    font: Sets the title font.\n    pad: Sets the padding of the title. Each padding value only applies when the corresponding `xanchor`/`yanchor` value is set accordingly. E.g. for left padding to take effect, `xanchor` must be set to *left*. The same rule applies if `xanchor`/`yanchor` is determined automatically. Padding is muted if the respective anchor value is *middle*/*center*.\n    text: Sets the plot's title.\n    x: Sets the x position with respect to `xref` in normalized coordinates from *0* (left) to *1* (right).\n    xanchor: Sets the title's horizontal alignment with respect to its x position. *left* means that the title starts at x, *right* means that the title ends at x and *center* means that the title's center is at x. *auto* divides `xref` by three and calculates the `xanchor` value automatically based on the value of `x`.\n    xref: Sets the container `x` refers to. *container* spans the entire `width` of the plot. *paper* refers to the width of the plotting area only.\n    y: Sets the y position with respect to `yref` in normalized coordinates from *0* (bottom) to *1* (top). *auto* places the baseline of the title onto the vertical center of the top margin.\n    yanchor: Sets the title's vertical alignment with respect to its y position. *top* means that the title's cap line is at y, *bottom* means that the title's baseline is at y and *middle* means that the title's midline is at y. *auto* divides `yref` by three and calculates the `yanchor` value automatically based on the value of `y`.\n    yref: Sets the container `y` refers to. *container* spans the entire `height` of the plot. *paper* refers to the height of the plotting area only."
        ...

class Transition(_PlotlyObject):
    "Create a new 'Transition' object"
    duration: float | Any
    "The duration of the transition, in milliseconds. If equal to zero, updates are synchronous."
    easing: Any
    "The easing function used for the transition"
    ordering: Any
    "Determines whether the figure's layout or traces smoothly transitions during updates that make both traces and layout change."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        duration: Any = ...,
        easing: Any = ...,
        ordering: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Transition' object\n\nArgs:\n    duration: The duration of the transition, in milliseconds. If equal to zero, updates are synchronous.\n    easing: The easing function used for the transition\n    ordering: Determines whether the figure's layout or traces smoothly transitions during updates that make both traces and layout change."
        ...

class Uniformtext(_PlotlyObject):
    "Create a new 'Uniformtext' object"
    minsize: float | Any
    "Sets the minimum text size between traces of the same type."
    mode: Any
    "Determines how the font size for various text elements are uniformed between each trace type. If the computed text sizes were smaller than the minimum size defined by `uniformtext.minsize` using *hide* option hides the text; and using *show* option shows the text without further downscaling. Please note that if the size defined by `minsize` is greater than the font size defined by trace, then the `minsize` is used."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        minsize: Any = ...,
        mode: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Uniformtext' object\n\nArgs:\n    minsize: Sets the minimum text size between traces of the same type.\n    mode: Determines how the font size for various text elements are uniformed between each trace type. If the computed text sizes were smaller than the minimum size defined by `uniformtext.minsize` using *hide* option hides the text; and using *show* option shows the text without further downscaling. Please note that if the size defined by `minsize` is greater than the font size defined by trace, then the `minsize` is used."
        ...

class Updatemenu(_PlotlyObject):
    "Create a new 'Updatemenu' object"
    active: int | Any
    "Determines which button (by index starting from 0) is considered active."
    bgcolor: Any
    "Sets the background color of the update menu buttons."
    bordercolor: Any
    "Sets the color of the border enclosing the update menu."
    borderwidth: float | Any
    "Sets the width (in px) of the border enclosing the update menu."
    @property
    def button(self) -> _plotly_graph_objs_layout_updatemenu.Button | Any:
        ...
    @button.setter
    def button(self, value: Any) -> None: ...
    direction: Any
    "Determines the direction in which the buttons are laid out, whether in a dropdown menu or a row/column of buttons. For `left` and `up`, the buttons will still appear in left-to-right or top-to-bottom order respectively."
    @property
    def font(self) -> _plotly_graph_objs_layout_updatemenu.Font | Any:
        "Sets the font of the update menu button text."
        ...
    @font.setter
    def font(self, value: Any) -> None: ...
    name: str | Any
    "When used in a template, named items are created in the output figure in addition to any items the figure already has in this array. You can modify these items in the output figure by making your own item with `templateitemname` matching this `name` alongside your modifications (including `visible: false` or `enabled: false` to hide it). Has no effect outside of a template."
    @property
    def pad(self) -> _plotly_graph_objs_layout_updatemenu.Pad | Any:
        "Sets the padding around the buttons or dropdown menu."
        ...
    @pad.setter
    def pad(self, value: Any) -> None: ...
    showactive: bool | Any
    "Highlights active dropdown item or active button if true."
    templateitemname: str | Any
    "Used to refer to a named item in this array in the template. Named items from the template will be created even without a matching item in the input figure, but you can modify one by making an item with `templateitemname` matching its `name`, alongside your modifications (including `visible: false` or `enabled: false` to hide it). If there is no template or no matching item, this item will be hidden unless you explicitly show it with `visible: true`."
    type: Any
    "Determines whether the buttons are accessible via a dropdown menu or whether the buttons are stacked horizontally or vertically"
    visible: bool | Any
    "Determines whether or not the update menu is visible."
    x: float | Any
    "Sets the x position (in normalized coordinates) of the update menu."
    xanchor: Any
    "Sets the update menu's horizontal position anchor. This anchor binds the `x` position to the *left*, *center* or *right* of the range selector."
    y: float | Any
    "Sets the y position (in normalized coordinates) of the update menu."
    yanchor: Any
    "Sets the update menu's vertical position anchor This anchor binds the `y` position to the *top*, *middle* or *bottom* of the range selector."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        active: Any = ...,
        bgcolor: Any = ...,
        bordercolor: Any = ...,
        borderwidth: Any = ...,
        button: Any = ...,
        direction: Any = ...,
        font: Any = ...,
        name: Any = ...,
        pad: Any = ...,
        showactive: Any = ...,
        templateitemname: Any = ...,
        type: Any = ...,
        visible: Any = ...,
        x: Any = ...,
        xanchor: Any = ...,
        y: Any = ...,
        yanchor: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Updatemenu' object\n\nArgs:\n    active: Determines which button (by index starting from 0) is considered active.\n    bgcolor: Sets the background color of the update menu buttons.\n    bordercolor: Sets the color of the border enclosing the update menu.\n    borderwidth: Sets the width (in px) of the border enclosing the update menu.\n    direction: Determines the direction in which the buttons are laid out, whether in a dropdown menu or a row/column of buttons. For `left` and `up`, the buttons will still appear in left-to-right or top-to-bottom order respectively.\n    font: Sets the font of the update menu button text.\n    name: When used in a template, named items are created in the output figure in addition to any items the figure already has in this array. You can modify these items in the output figure by making your own item with `templateitemname` matching this `name` alongside your modifications (including `visible: false` or `enabled: false` to hide it). Has no effect outside of a template.\n    pad: Sets the padding around the buttons or dropdown menu.\n    showactive: Highlights active dropdown item or active button if true.\n    templateitemname: Used to refer to a named item in this array in the template. Named items from the template will be created even without a matching item in the input figure, but you can modify one by making an item with `templateitemname` matching its `name`, alongside your modifications (including `visible: false` or `enabled: false` to hide it). If there is no template or no matching item, this item will be hidden unless you explicitly show it with `visible: true`.\n    type: Determines whether the buttons are accessible via a dropdown menu or whether the buttons are stacked horizontally or vertically\n    visible: Determines whether or not the update menu is visible.\n    x: Sets the x position (in normalized coordinates) of the update menu.\n    xanchor: Sets the update menu's horizontal position anchor. This anchor binds the `x` position to the *left*, *center* or *right* of the range selector.\n    y: Sets the y position (in normalized coordinates) of the update menu.\n    yanchor: Sets the update menu's vertical position anchor This anchor binds the `y` position to the *top*, *middle* or *bottom* of the range selector."
        ...

class XAxis(_PlotlyObject):
    "Create a new 'XAxis' object"
    anchor: Any
    "If set to an opposite-letter axis id (e.g. `x2`, `y`), this axis is bound to the corresponding opposite-letter axis. If set to *free*, this axis' position is determined by `position`."
    automargin: str | Any
    "Determines whether long tick labels automatically grow the figure margins."
    autorange: Any
    "Determines whether or not the range of this axis is computed in relation to the input data. See `rangemode` for more info. If `range` is provided and it has a value for both the lower and upper bound, `autorange` is set to *false*. Using *min* applies autorange only to set the minimum. Using *max* applies autorange only to set the maximum. Using *min reversed* applies autorange only to set the minimum on a reversed axis. Using *max reversed* applies autorange only to set the maximum on a reversed axis. Using *reversed* applies autorange on both ends and reverses the axis direction."
    @property
    def autorangeoptions(self) -> _plotly_graph_objs_layout_xaxis.Autorangeoptions | Any:
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
    constrain: Any
    "If this axis needs to be compressed (either due to its own `scaleanchor` and `scaleratio` or those of the other axis), determines how that happens: by increasing the *range*, or by decreasing the *domain*. Default is *domain* for axes containing image traces, *range* otherwise."
    constraintoward: Any
    "If this axis needs to be compressed (either due to its own `scaleanchor` and `scaleratio` or those of the other axis), determines which direction we push the originally specified plot area. Options are *left*, *center* (default), and *right* for x axes, and *top*, *middle* (default), and *bottom* for y axes."
    dividercolor: Any
    "Sets the color of the dividers Only has an effect on *multicategory* axes."
    dividerwidth: float | Any
    "Sets the width (in px) of the dividers Only has an effect on *multicategory* axes."
    domain: Any
    "Sets the domain of this axis (in plot fraction)."
    dtick: Any
    "Sets the step in-between ticks on this axis. Use with `tick0`. Must be a positive number, or special strings available to *log* and *date* axes. If the axis `type` is *log*, then ticks are set every 10^(n*dtick) where n is the tick number. For example, to set a tick mark at 1, 10, 100, 1000, ... set dtick to 1. To set tick marks at 1, 100, 10000, ... set dtick to 2. To set tick marks at 1, 5, 25, 125, 625, 3125, ... set dtick to log_10(5), or 0.69897000433. *log* has several special values; *L<f>*, where `f` is a positive number, gives ticks linearly spaced in value (but not position). For example `tick0` = 0.1, `dtick` = *L0.5* will put ticks at 0.1, 0.6, 1.1, 1.6 etc. To show powers of 10 plus small digits between, use *D1* (all digits) or *D2* (only 2 and 5). `tick0` is ignored for *D1* and *D2*. If the axis `type` is *date*, then you must convert the time to milliseconds. For example, to set the interval between ticks to one day, set `dtick` to 86400000.0. *date* also has special values *M<n>* gives ticks spaced by a number of months. `n` must be a positive integer. To set ticks on the 15th of every third month, set `tick0` to *2000-01-15* and `dtick` to *M3*. To set ticks every 4 years, set `dtick` to *M48*"
    exponentformat: Any
    "Determines a formatting rule for the tick exponents. For example, consider the number 1,000,000,000. If *none*, it appears as 1,000,000,000. If *e*, 1e+9. If *E*, 1E+9. If *power*, 1x10^9 (with 9 in a super script). If *SI*, 1G. If *B*, 1B. *SI* uses prefixes from \"femto\" f (10^-15) to \"tera\" T (10^12). *SI extended* covers instead the full SI range from \"quecto\" q (10^-30) to \"quetta\" Q (10^30). If *SI* or *SI extended* is used and the exponent is beyond the above ranges, the formatting rule will automatically be switched to the power notation."
    fixedrange: bool | Any
    "Determines whether or not this axis is zoom-able. If true, then zoom is disabled."
    gridcolor: Any
    "Sets the color of the grid lines."
    griddash: str | Any
    "Sets the dash style of lines. Set to a dash type string (*solid*, *dot*, *dash*, *longdash*, *dashdot*, or *longdashdot*) or a dash length list in px (eg *5px,10px,2px,2px*)."
    gridwidth: float | Any
    "Sets the width (in px) of the grid lines."
    hoverformat: str | Any
    "Sets the hover text formatting rule using d3 formatting mini-languages which are very similar to those in Python. For numbers, see: https://github.com/d3/d3-format/tree/v1.4.5#d3-format. And for dates see: https://github.com/d3/d3-time-format/tree/v2.2.3#locale_format. We add two items to d3's date formatter: *%h* for half of the year as a decimal number as well as *%{n}f* for fractional seconds with n digits. For example, *2016-10-13 09:15:23.456* with tickformat *%H~%M~%S.%2f* would display *09~15~23.46*"
    insiderange: Any
    "Could be used to set the desired inside range of this axis (excluding the labels) when `ticklabelposition` of the anchored axis has *inside*. Not implemented for axes with `type` *log*. This would be ignored when `range` is provided."
    labelalias: Any
    "Replacement text for specific tick or hover labels. For example using {US: 'USA', CA: 'Canada'} changes US to USA and CA to Canada. The labels we would have shown must match the keys exactly, after adding any tickprefix or ticksuffix. For negative numbers the minus sign symbol used (U+2212) is wider than the regular ascii dash. That means you need to use −1 instead of -1. labelalias can be used with any axis type, and both keys (if needed) and values (if desired) can include html-like tags or MathJax."
    layer: Any
    "Sets the layer on which this axis is displayed. If *above traces*, this axis is displayed above all the subplot's traces If *below traces*, this axis is displayed below all the subplot's traces, but above the grid lines. Useful when used together with scatter-like traces with `cliponaxis` set to *false* to show markers and/or text nodes above this axis."
    linecolor: Any
    "Sets the axis line color."
    linewidth: float | Any
    "Sets the width (in px) of the axis line."
    matches: Any
    "If set to another axis id (e.g. `x2`, `y`), the range of this axis will match the range of the corresponding axis in data-coordinates space. Moreover, matching axes share auto-range values, category lists and histogram auto-bins. Note that setting axes simultaneously in both a `scaleanchor` and a `matches` constraint is currently forbidden. Moreover, note that matching axes must have the same `type`."
    maxallowed: Any
    "Determines the maximum range of this axis."
    minallowed: Any
    "Determines the minimum range of this axis."
    minexponent: float | Any
    "Hide SI prefix for 10^n if |n| is below this number. This only has an effect when `tickformat` is *SI* or *B*."
    @property
    def minor(self) -> _plotly_graph_objs_layout_xaxis.Minor | Any:
        ...
    @minor.setter
    def minor(self, value: Any) -> None: ...
    minorloglabels: Any
    "Determines how minor log labels are displayed. If *small digits*, small digits i.e. 2 or 5 are displayed. If *complete*, complete digits are displayed. If *none*, no labels are displayed."
    mirror: Any
    "Determines if the axis lines or/and ticks are mirrored to the opposite side of the plotting area. If *true*, the axis lines are mirrored. If *ticks*, the axis lines and ticks are mirrored. If *false*, mirroring is disable. If *all*, axis lines are mirrored on all shared-axes subplots. If *allticks*, axis lines and ticks are mirrored on all shared-axes subplots."
    modebardisable: str | Any
    "Disables certain modebar buttons for this axis. *autoscale* disables the autoscale buttons, *zoominout* disables the zoom-in and zoom-out buttons."
    nticks: int | Any
    "Specifies the maximum number of ticks for the particular axis. The actual number of ticks will be chosen automatically to be less than or equal to `nticks`. Has an effect only if `tickmode` is set to *auto*."
    overlaying: Any
    "If set a same-letter axis id, this axis is overlaid on top of the corresponding same-letter axis, with traces and axes visible for both axes. If *false*, this axis does not overlay any same-letter axes. In this case, for axes with overlapping domains only the highest-numbered axis will be visible."
    position: float | Any
    "Sets the position of this axis in the plotting space (in normalized coordinates). Only has an effect if `anchor` is set to *free*."
    range: Any
    "Sets the range of this axis. If the axis `type` is *log*, then you must take the log of your desired range (e.g. to set the range from 1 to 100, set the range from 0 to 2). If the axis `type` is *date*, it should be date strings, like date data, though Date objects and unix milliseconds will be accepted and converted to strings. If the axis `type` is *category*, it should be numbers, using the scale where each category is assigned a serial number from zero in the order it appears. Leaving either or both elements `null` impacts the default `autorange`."
    @property
    def rangebreak(self) -> _plotly_graph_objs_layout_xaxis.Rangebreak | Any:
        ...
    @rangebreak.setter
    def rangebreak(self, value: Any) -> None: ...
    rangemode: Any
    "If *normal*, the range is computed in relation to the extrema of the input data. If *tozero*, the range extends to 0, regardless of the input data If *nonnegative*, the range is non-negative, regardless of the input data. Applies only to linear axes."
    @property
    def rangeselector(self) -> _plotly_graph_objs_layout_xaxis.Rangeselector | Any:
        ...
    @rangeselector.setter
    def rangeselector(self, value: Any) -> None: ...
    @property
    def rangeslider(self) -> _plotly_graph_objs_layout_xaxis.Rangeslider | Any:
        ...
    @rangeslider.setter
    def rangeslider(self, value: Any) -> None: ...
    scaleanchor: Any
    "If set to another axis id (e.g. `x2`, `y`), the range of this axis changes together with the range of the corresponding axis such that the scale of pixels per unit is in a constant ratio. Both axes are still zoomable, but when you zoom one, the other will zoom the same amount, keeping a fixed midpoint. `constrain` and `constraintoward` determine how we enforce the constraint. You can chain these, ie `yaxis: {scaleanchor: *x*}, xaxis2: {scaleanchor: *y*}` but you can only link axes of the same `type`. The linked axis can have the opposite letter (to constrain the aspect ratio) or the same letter (to match scales across subplots). Loops (`yaxis: {scaleanchor: *x*}, xaxis: {scaleanchor: *y*}` or longer) are redundant and the last constraint encountered will be ignored to avoid possible inconsistent constraints via `scaleratio`. Note that setting axes simultaneously in both a `scaleanchor` and a `matches` constraint is currently forbidden. Setting `false` allows to remove a default constraint (occasionally, you may need to prevent a default `scaleanchor` constraint from being applied, eg. when having an image trace `yaxis: {scaleanchor: \"x\"}` is set automatically in order for pixels to be rendered as squares, setting `yaxis: {scaleanchor: false}` allows to remove the constraint)."
    scaleratio: float | Any
    "If this axis is linked to another by `scaleanchor`, this determines the pixel to unit scale ratio. For example, if this value is 10, then every unit on this axis spans 10 times the number of pixels as a unit on the linked axis. Use this for example to create an elevation profile where the vertical scale is exaggerated a fixed amount with respect to the horizontal."
    separatethousands: bool | Any
    "If \"true\", even 4-digit integers are separated"
    showdividers: bool | Any
    "Determines whether or not a dividers are drawn between the category levels of this axis. Only has an effect on *multicategory* axes."
    showexponent: Any
    "If *all*, all exponents are shown besides their significands. If *first*, only the exponent of the first tick is shown. If *last*, only the exponent of the last tick is shown. If *none*, no exponents appear."
    showgrid: bool | Any
    "Determines whether or not grid lines are drawn. If *true*, the grid lines are drawn at every tick mark."
    showline: bool | Any
    "Determines whether or not a line bounding this axis is drawn."
    showspikes: bool | Any
    "Determines whether or not spikes (aka droplines) are drawn for this axis. Note that spikes will never be drawn when `hovermode` is *false*."
    showticklabels: bool | Any
    "Determines whether or not the tick labels are drawn."
    showtickprefix: Any
    "If *all*, all tick labels are displayed with a prefix. If *first*, only the first tick is displayed with a prefix. If *last*, only the last tick is displayed with a suffix. If *none*, tick prefixes are hidden."
    showticksuffix: Any
    "Same as `showtickprefix` but for tick suffixes."
    side: Any
    "Determines whether a x (y) axis is positioned at the *bottom* (*left*) or *top* (*right*) of the plotting area."
    spikecolor: Any
    "Sets the spike color. If undefined, will use the series color"
    spikedash: str | Any
    "Sets the dash style of lines. Set to a dash type string (*solid*, *dot*, *dash*, *longdash*, *dashdot*, or *longdashdot*) or a dash length list in px (eg *5px,10px,2px,2px*)."
    spikemode: str | Any
    "Determines the drawing mode for the spike line If *toaxis*, the line is drawn from the data point to the axis the series is plotted on. If *across*, the line is drawn across the entire plot area, and supercedes *toaxis*. If *marker*, then a marker dot is drawn on the axis the series is plotted on"
    spikesnap: Any
    "Determines whether spikelines are stuck to the cursor or to the closest datapoints."
    spikethickness: float | Any
    "Sets the spike line width in pixels."
    tick0: Any
    "Sets the placement of the first tick on this axis. Use with `dtick`. If the axis `type` is *log*, then you must take the log of your starting tick (e.g. to set the starting tick to 100, set the `tick0` to 2) except when `dtick`=*L<f>* (see `dtick` for more info). If the axis `type` is *date*, it should be a date string, like date data. If the axis `type` is *category*, it should be a number, using the scale where each category is assigned a serial number from zero in the order it appears."
    tickangle: Any
    "Sets the angle of the tick labels with respect to the horizontal. For example, a `tickangle` of -90 draws the tick labels vertically."
    tickcolor: Any
    "Sets the tick color."
    @property
    def tickfont(self) -> _plotly_graph_objs_layout_xaxis.Tickfont | Any:
        "Sets the tick font."
        ...
    @tickfont.setter
    def tickfont(self, value: Any) -> None: ...
    tickformat: str | Any
    "Sets the tick label formatting rule using d3 formatting mini-languages which are very similar to those in Python. For numbers, see: https://github.com/d3/d3-format/tree/v1.4.5#d3-format. And for dates see: https://github.com/d3/d3-time-format/tree/v2.2.3#locale_format. We add two items to d3's date formatter: *%h* for half of the year as a decimal number as well as *%{n}f* for fractional seconds with n digits. For example, *2016-10-13 09:15:23.456* with tickformat *%H~%M~%S.%2f* would display *09~15~23.46*"
    @property
    def tickformatstop(self) -> _plotly_graph_objs_layout_xaxis.Tickformatstop | Any:
        ...
    @tickformatstop.setter
    def tickformatstop(self, value: Any) -> None: ...
    ticklabelindex: int | Any
    "Only for axes with `type` *date* or *linear*. Instead of drawing the major tick label, draw the label for the minor tick that is n positions away from the major tick. E.g. to always draw the label for the minor tick before each major tick, choose `ticklabelindex` -1. This is useful for date axes with `ticklabelmode` *period* if you want to label the period that ends with each major tick instead of the period that begins there."
    ticklabelmode: Any
    "Determines where tick labels are drawn with respect to their corresponding ticks and grid lines. Only has an effect for axes of `type` *date* When set to *period*, tick labels are drawn in the middle of the period between ticks."
    ticklabeloverflow: Any
    "Determines how we handle tick labels that would overflow either the graph div or the domain of the axis. The default value for inside tick labels is *hide past domain*. Otherwise on *category* and *multicategory* axes the default is *allow*. In other cases the default is *hide past div*."
    ticklabelposition: Any
    "Determines where tick labels are drawn with respect to the axis. Please note that top or bottom has no effect on x axes or when `ticklabelmode` is set to *period* or when `tickson` is set to *boundaries*. Similarly, left or right has no effect on y axes or when `ticklabelmode` is set to *period* or when `tickson` is set to *boundaries*. Has no effect on *multicategory* axes. When used on axes linked by `matches` or `scaleanchor`, no extra padding for inside labels would be added by autorange, so that the scales could match."
    ticklabelshift: int | Any
    "Shifts the tick labels by the specified number of pixels in parallel to the axis. Positive values move the labels in the positive direction of the axis."
    ticklabelstandoff: int | Any
    "Sets the standoff distance (in px) between the axis tick labels and their default position. A positive `ticklabelstandoff` moves the labels farther away from the plot area if `ticklabelposition` is *outside*, and deeper into the plot area if `ticklabelposition` is *inside*. A negative `ticklabelstandoff` works in the opposite direction, moving outside ticks towards the plot area and inside ticks towards the outside. If the negative value is large enough, inside ticks can even end up outside and vice versa."
    ticklabelstep: int | Any
    "Sets the spacing between tick labels as compared to the spacing between ticks. A value of 1 (default) means each tick gets a label. A value of 2 means shows every 2nd label. A larger value n means only every nth tick is labeled. `tick0` determines which labels are shown. Not implemented for axes with `type` *log* or *multicategory*, or when `tickmode` is *array*."
    ticklen: float | Any
    "Sets the tick length (in px)."
    tickmode: Any
    "Sets the tick mode for this axis. If *auto*, the number of ticks is set via `nticks`. If *linear*, the placement of the ticks is determined by a starting position `tick0` and a tick step `dtick` (*linear* is the default value if `tick0` and `dtick` are provided). If *array*, the placement of the ticks is set via `tickvals` and the tick text is `ticktext`. (*array* is the default value if `tickvals` is provided). If *sync*, the number of ticks will sync with the overlayed axis set by `overlaying` property. When no other tick info is provided, overlaying (non-categorical) axes default to *sync*, while other axes default to *auto*."
    tickprefix: str | Any
    "Sets a tick label prefix."
    ticks: Any
    "Determines whether ticks are drawn or not. If **, this axis' ticks are not drawn. If *outside* (*inside*), this axis' are drawn outside (inside) the axis lines."
    tickson: Any
    "Determines where ticks and grid lines are drawn with respect to their corresponding tick labels. Only has an effect for axes of `type` *category* or *multicategory*. When set to *boundaries*, ticks and grid lines are drawn half a category to the left/bottom of labels."
    ticksuffix: str | Any
    "Sets a tick label suffix."
    ticktext: Any
    "Sets the text displayed at the ticks position via `tickvals`. Only has an effect if `tickmode` is set to *array*. Used with `tickvals`."
    tickvals: Any
    "Sets the values at which ticks on this axis appear. Only has an effect if `tickmode` is set to *array*. Used with `ticktext`."
    tickwidth: float | Any
    "Sets the tick width (in px)."
    @property
    def title(self) -> _plotly_graph_objs_layout_xaxis.Title | Any:
        ...
    @title.setter
    def title(self, value: Any) -> None: ...
    type: Any
    "Sets the axis type. By default, plotly attempts to determined the axis type by looking into the data of the traces that referenced the axis in question."
    uirevision: Any
    "Controls persistence of user-driven changes in axis `range`, `autorange`, and `title` if in `editable: true` configuration. Defaults to `layout.uirevision`."
    @property
    def unifiedhovertitle(self) -> _plotly_graph_objs_layout_xaxis.Unifiedhovertitle | Any:
        ...
    @unifiedhovertitle.setter
    def unifiedhovertitle(self, value: Any) -> None: ...
    visible: bool | Any
    "A single toggle to hide the axis while preserving interaction like dragging. Default is true when a cheater plot is present on the axis, otherwise false"
    zeroline: bool | Any
    "Determines whether or not a line is drawn at along the 0 value of this axis. If *true*, the zero line is drawn on top of the grid lines."
    zerolinecolor: Any
    "Sets the line color of the zero line."
    zerolinelayer: Any
    "Sets the layer on which this zeroline is displayed. If *above traces*, this zeroline is displayed above all the subplot's traces If *below traces*, this zeroline is displayed below all the subplot's traces, but above the grid lines. Limitation: *zerolinelayer* currently has no effect if the *zorder* property is set on any trace."
    zerolinewidth: float | Any
    "Sets the width (in px) of the zero line."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        anchor: Any = ...,
        automargin: Any = ...,
        autorange: Any = ...,
        autorangeoptions: Any = ...,
        autotickangles: Any = ...,
        autotypenumbers: Any = ...,
        calendar: Any = ...,
        categoryarray: Any = ...,
        categoryorder: Any = ...,
        color: Any = ...,
        constrain: Any = ...,
        constraintoward: Any = ...,
        dividercolor: Any = ...,
        dividerwidth: Any = ...,
        domain: Any = ...,
        dtick: Any = ...,
        exponentformat: Any = ...,
        fixedrange: Any = ...,
        gridcolor: Any = ...,
        griddash: Any = ...,
        gridwidth: Any = ...,
        hoverformat: Any = ...,
        insiderange: Any = ...,
        labelalias: Any = ...,
        layer: Any = ...,
        linecolor: Any = ...,
        linewidth: Any = ...,
        matches: Any = ...,
        maxallowed: Any = ...,
        minallowed: Any = ...,
        minexponent: Any = ...,
        minor: Any = ...,
        minorloglabels: Any = ...,
        mirror: Any = ...,
        modebardisable: Any = ...,
        nticks: Any = ...,
        overlaying: Any = ...,
        position: Any = ...,
        range: Any = ...,
        rangebreak: Any = ...,
        rangemode: Any = ...,
        rangeselector: Any = ...,
        rangeslider: Any = ...,
        scaleanchor: Any = ...,
        scaleratio: Any = ...,
        separatethousands: Any = ...,
        showdividers: Any = ...,
        showexponent: Any = ...,
        showgrid: Any = ...,
        showline: Any = ...,
        showspikes: Any = ...,
        showticklabels: Any = ...,
        showtickprefix: Any = ...,
        showticksuffix: Any = ...,
        side: Any = ...,
        spikecolor: Any = ...,
        spikedash: Any = ...,
        spikemode: Any = ...,
        spikesnap: Any = ...,
        spikethickness: Any = ...,
        tick0: Any = ...,
        tickangle: Any = ...,
        tickcolor: Any = ...,
        tickfont: Any = ...,
        tickformat: Any = ...,
        tickformatstop: Any = ...,
        ticklabelindex: Any = ...,
        ticklabelmode: Any = ...,
        ticklabeloverflow: Any = ...,
        ticklabelposition: Any = ...,
        ticklabelshift: Any = ...,
        ticklabelstandoff: Any = ...,
        ticklabelstep: Any = ...,
        ticklen: Any = ...,
        tickmode: Any = ...,
        tickprefix: Any = ...,
        ticks: Any = ...,
        tickson: Any = ...,
        ticksuffix: Any = ...,
        ticktext: Any = ...,
        tickvals: Any = ...,
        tickwidth: Any = ...,
        title: Any = ...,
        type: Any = ...,
        uirevision: Any = ...,
        unifiedhovertitle: Any = ...,
        visible: Any = ...,
        zeroline: Any = ...,
        zerolinecolor: Any = ...,
        zerolinelayer: Any = ...,
        zerolinewidth: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'XAxis' object\n\nArgs:\n    anchor: If set to an opposite-letter axis id (e.g. `x2`, `y`), this axis is bound to the corresponding opposite-letter axis. If set to *free*, this axis' position is determined by `position`.\n    automargin: Determines whether long tick labels automatically grow the figure margins.\n    autorange: Determines whether or not the range of this axis is computed in relation to the input data. See `rangemode` for more info. If `range` is provided and it has a value for both the lower and upper bound, `autorange` is set to *false*. Using *min* applies autorange only to set the minimum. Using *max* applies autorange only to set the maximum. Using *min reversed* applies autorange only to set the minimum on a reversed axis. Using *max reversed* applies autorange only to set the maximum on a reversed axis. Using *reversed* applies autorange on both ends and reverses the axis direction.\n    autotickangles: When `tickangle` is set to *auto*, it will be set to the first angle in this array that is large enough to prevent label overlap.\n    autotypenumbers: Using *strict* a numeric string in trace data is not converted to a number. Using *convert types* a numeric string in trace data may be treated as a number during automatic axis `type` detection. Defaults to layout.autotypenumbers.\n    calendar: Sets the calendar system to use for `range` and `tick0` if this is a date axis. This does not set the calendar for interpreting data on this axis, that's specified in the trace or via the global `layout.calendar`\n    categoryarray: Sets the order in which categories on this axis appear. Only has an effect if `categoryorder` is set to *array*. Used with `categoryorder`.\n    categoryorder: Specifies the ordering logic for the case of categorical variables. By default, plotly uses *trace*, which specifies the order that is present in the data supplied. Set `categoryorder` to *category ascending* or *category descending* if order should be determined by the alphanumerical order of the category names. Set `categoryorder` to *array* to derive the ordering from the attribute `categoryarray`. If a category is not found in the `categoryarray` array, the sorting behavior for that attribute will be identical to the *trace* mode. The unspecified categories will follow the categories in `categoryarray`. Set `categoryorder` to *total ascending* or *total descending* if order should be determined by the numerical order of the values. Similarly, the order can be determined by the min, max, sum, mean, geometric mean or median of all the values.\n    color: Sets default for all colors associated with this axis all at once: line, font, tick, and grid colors. Grid color is lightened by blending this with the plot background Individual pieces can override this.\n    constrain: If this axis needs to be compressed (either due to its own `scaleanchor` and `scaleratio` or those of the other axis), determines how that happens: by increasing the *range*, or by decreasing the *domain*. Default is *domain* for axes containing image traces, *range* otherwise.\n    constraintoward: If this axis needs to be compressed (either due to its own `scaleanchor` and `scaleratio` or those of the other axis), determines which direction we push the originally specified plot area. Options are *left*, *center* (default), and *right* for x axes, and *top*, *middle* (default), and *bottom* for y axes.\n    dividercolor: Sets the color of the dividers Only has an effect on *multicategory* axes.\n    dividerwidth: Sets the width (in px) of the dividers Only has an effect on *multicategory* axes.\n    domain: Sets the domain of this axis (in plot fraction).\n    dtick: Sets the step in-between ticks on this axis. Use with `tick0`. Must be a positive number, or special strings available to *log* and *date* axes. If the axis `type` is *log*, then ticks are set every 10^(n*dtick) where n is the tick number. For example, to set a tick mark at 1, 10, 100, 1000, ... set dtick to 1. To set tick marks at 1, 100, 10000, ... set dtick to 2. To set tick marks at 1, 5, 25, 125, 625, 3125, ... set dtick to log_10(5), or 0.69897000433. *log* has several special values; *L<f>*, where `f` is a positive number, gives ticks linearly spaced in value (but not position). For example `tick0` = 0.1, `dtick` = *L0.5* will put ticks at 0.1, 0.6, 1.1, 1.6 etc. To show powers of 10 plus small digits between, use *D1* (all digits) or *D2* (only 2 and 5). `tick0` is ignored for *D1* and *D2*. If the axis `type` is *date*, then you must convert the time to milliseconds. For example, to set the interval between ticks to one day, set `dtick` to 86400000.0. *date* also has special values *M<n>* gives ticks spaced by a number of months. `n` must be a positive integer. To set ticks on the 15th of every third month, set `tick0` to *2000-01-15* and `dtick` to *M3*. To set ticks every 4 years, set `dtick` to *M48*\n    exponentformat: Determines a formatting rule for the tick exponents. For example, consider the number 1,000,000,000. If *none*, it appears as 1,000,000,000. If *e*, 1e+9. If *E*, 1E+9. If *power*, 1x10^9 (with 9 in a super script). If *SI*, 1G. If *B*, 1B. *SI* uses prefixes from \"femto\" f (10^-15) to \"tera\" T (10^12). *SI extended* covers instead the full SI range from \"quecto\" q (10^-30) to \"quetta\" Q (10^30). If *SI* or *SI extended* is used and the exponent is beyond the above ranges, the formatting rule will automatically be switched to the power notation.\n    fixedrange: Determines whether or not this axis is zoom-able. If true, then zoom is disabled.\n    gridcolor: Sets the color of the grid lines.\n    griddash: Sets the dash style of lines. Set to a dash type string (*solid*, *dot*, *dash*, *longdash*, *dashdot*, or *longdashdot*) or a dash length list in px (eg *5px,10px,2px,2px*).\n    gridwidth: Sets the width (in px) of the grid lines.\n    hoverformat: Sets the hover text formatting rule using d3 formatting mini-languages which are very similar to those in Python. For numbers, see: https://github.com/d3/d3-format/tree/v1.4.5#d3-format. And for dates see: https://github.com/d3/d3-time-format/tree/v2.2.3#locale_format. We add two items to d3's date formatter: *%h* for half of the year as a decimal number as well as *%{n}f* for fractional seconds with n digits. For example, *2016-10-13 09:15:23.456* with tickformat *%H~%M~%S.%2f* would display *09~15~23.46*\n    insiderange: Could be used to set the desired inside range of this axis (excluding the labels) when `ticklabelposition` of the anchored axis has *inside*. Not implemented for axes with `type` *log*. This would be ignored when `range` is provided.\n    labelalias: Replacement text for specific tick or hover labels. For example using {US: 'USA', CA: 'Canada'} changes US to USA and CA to Canada. The labels we would have shown must match the keys exactly, after adding any tickprefix or ticksuffix. For negative numbers the minus sign symbol used (U+2212) is wider than the regular ascii dash. That means you need to use −1 instead of -1. labelalias can be used with any axis type, and both keys (if needed) and values (if desired) can include html-like tags or MathJax.\n    layer: Sets the layer on which this axis is displayed. If *above traces*, this axis is displayed above all the subplot's traces If *below traces*, this axis is displayed below all the subplot's traces, but above the grid lines. Useful when used together with scatter-like traces with `cliponaxis` set to *false* to show markers and/or text nodes above this axis.\n    linecolor: Sets the axis line color.\n    linewidth: Sets the width (in px) of the axis line.\n    matches: If set to another axis id (e.g. `x2`, `y`), the range of this axis will match the range of the corresponding axis in data-coordinates space. Moreover, matching axes share auto-range values, category lists and histogram auto-bins. Note that setting axes simultaneously in both a `scaleanchor` and a `matches` constraint is currently forbidden. Moreover, note that matching axes must have the same `type`.\n    maxallowed: Determines the maximum range of this axis.\n    minallowed: Determines the minimum range of this axis.\n    minexponent: Hide SI prefix for 10^n if |n| is below this number. This only has an effect when `tickformat` is *SI* or *B*.\n    minorloglabels: Determines how minor log labels are displayed. If *small digits*, small digits i.e. 2 or 5 are displayed. If *complete*, complete digits are displayed. If *none*, no labels are displayed.\n    mirror: Determines if the axis lines or/and ticks are mirrored to the opposite side of the plotting area. If *true*, the axis lines are mirrored. If *ticks*, the axis lines and ticks are mirrored. If *false*, mirroring is disable. If *all*, axis lines are mirrored on all shared-axes subplots. If *allticks*, axis lines and ticks are mirrored on all shared-axes subplots.\n    modebardisable: Disables certain modebar buttons for this axis. *autoscale* disables the autoscale buttons, *zoominout* disables the zoom-in and zoom-out buttons.\n    nticks: Specifies the maximum number of ticks for the particular axis. The actual number of ticks will be chosen automatically to be less than or equal to `nticks`. Has an effect only if `tickmode` is set to *auto*.\n    overlaying: If set a same-letter axis id, this axis is overlaid on top of the corresponding same-letter axis, with traces and axes visible for both axes. If *false*, this axis does not overlay any same-letter axes. In this case, for axes with overlapping domains only the highest-numbered axis will be visible.\n    position: Sets the position of this axis in the plotting space (in normalized coordinates). Only has an effect if `anchor` is set to *free*.\n    range: Sets the range of this axis. If the axis `type` is *log*, then you must take the log of your desired range (e.g. to set the range from 1 to 100, set the range from 0 to 2). If the axis `type` is *date*, it should be date strings, like date data, though Date objects and unix milliseconds will be accepted and converted to strings. If the axis `type` is *category*, it should be numbers, using the scale where each category is assigned a serial number from zero in the order it appears. Leaving either or both elements `null` impacts the default `autorange`.\n    rangemode: If *normal*, the range is computed in relation to the extrema of the input data. If *tozero*, the range extends to 0, regardless of the input data If *nonnegative*, the range is non-negative, regardless of the input data. Applies only to linear axes.\n    scaleanchor: If set to another axis id (e.g. `x2`, `y`), the range of this axis changes together with the range of the corresponding axis such that the scale of pixels per unit is in a constant ratio. Both axes are still zoomable, but when you zoom one, the other will zoom the same amount, keeping a fixed midpoint. `constrain` and `constraintoward` determine how we enforce the constraint. You can chain these, ie `yaxis: {scaleanchor: *x*}, xaxis2: {scaleanchor: *y*}` but you can only link axes of the same `type`. The linked axis can have the opposite letter (to constrain the aspect ratio) or the same letter (to match scales across subplots). Loops (`yaxis: {scaleanchor: *x*}, xaxis: {scaleanchor: *y*}` or longer) are redundant and the last constraint encountered will be ignored to avoid possible inconsistent constraints via `scaleratio`. Note that setting axes simultaneously in both a `scaleanchor` and a `matches` constraint is currently forbidden. Setting `false` allows to remove a default constraint (occasionally, you may need to prevent a default `scaleanchor` constraint from being applied, eg. when having an image trace `yaxis: {scaleanchor: \"x\"}` is set automatically in order for pixels to be rendered as squares, setting `yaxis: {scaleanchor: false}` allows to remove the constraint).\n    scaleratio: If this axis is linked to another by `scaleanchor`, this determines the pixel to unit scale ratio. For example, if this value is 10, then every unit on this axis spans 10 times the number of pixels as a unit on the linked axis. Use this for example to create an elevation profile where the vertical scale is exaggerated a fixed amount with respect to the horizontal.\n    separatethousands: If \"true\", even 4-digit integers are separated\n    showdividers: Determines whether or not a dividers are drawn between the category levels of this axis. Only has an effect on *multicategory* axes.\n    showexponent: If *all*, all exponents are shown besides their significands. If *first*, only the exponent of the first tick is shown. If *last*, only the exponent of the last tick is shown. If *none*, no exponents appear.\n    showgrid: Determines whether or not grid lines are drawn. If *true*, the grid lines are drawn at every tick mark.\n    showline: Determines whether or not a line bounding this axis is drawn.\n    showspikes: Determines whether or not spikes (aka droplines) are drawn for this axis. Note that spikes will never be drawn when `hovermode` is *false*.\n    showticklabels: Determines whether or not the tick labels are drawn.\n    showtickprefix: If *all*, all tick labels are displayed with a prefix. If *first*, only the first tick is displayed with a prefix. If *last*, only the last tick is displayed with a suffix. If *none*, tick prefixes are hidden.\n    showticksuffix: Same as `showtickprefix` but for tick suffixes.\n    side: Determines whether a x (y) axis is positioned at the *bottom* (*left*) or *top* (*right*) of the plotting area.\n    spikecolor: Sets the spike color. If undefined, will use the series color\n    spikedash: Sets the dash style of lines. Set to a dash type string (*solid*, *dot*, *dash*, *longdash*, *dashdot*, or *longdashdot*) or a dash length list in px (eg *5px,10px,2px,2px*).\n    spikemode: Determines the drawing mode for the spike line If *toaxis*, the line is drawn from the data point to the axis the series is plotted on. If *across*, the line is drawn across the entire plot area, and supercedes *toaxis*. If *marker*, then a marker dot is drawn on the axis the series is plotted on\n    spikesnap: Determines whether spikelines are stuck to the cursor or to the closest datapoints.\n    spikethickness: Sets the spike line width in pixels.\n    tick0: Sets the placement of the first tick on this axis. Use with `dtick`. If the axis `type` is *log*, then you must take the log of your starting tick (e.g. to set the starting tick to 100, set the `tick0` to 2) except when `dtick`=*L<f>* (see `dtick` for more info). If the axis `type` is *date*, it should be a date string, like date data. If the axis `type` is *category*, it should be a number, using the scale where each category is assigned a serial number from zero in the order it appears.\n    tickangle: Sets the angle of the tick labels with respect to the horizontal. For example, a `tickangle` of -90 draws the tick labels vertically.\n    tickcolor: Sets the tick color.\n    tickfont: Sets the tick font.\n    tickformat: Sets the tick label formatting rule using d3 formatting mini-languages which are very similar to those in Python. For numbers, see: https://github.com/d3/d3-format/tree/v1.4.5#d3-format. And for dates see: https://github.com/d3/d3-time-format/tree/v2.2.3#locale_format. We add two items to d3's date formatter: *%h* for half of the year as a decimal number as well as *%{n}f* for fractional seconds with n digits. For example, *2016-10-13 09:15:23.456* with tickformat *%H~%M~%S.%2f* would display *09~15~23.46*\n    ticklabelindex: Only for axes with `type` *date* or *linear*. Instead of drawing the major tick label, draw the label for the minor tick that is n positions away from the major tick. E.g. to always draw the label for the minor tick before each major tick, choose `ticklabelindex` -1. This is useful for date axes with `ticklabelmode` *period* if you want to label the period that ends with each major tick instead of the period that begins there.\n    ticklabelmode: Determines where tick labels are drawn with respect to their corresponding ticks and grid lines. Only has an effect for axes of `type` *date* When set to *period*, tick labels are drawn in the middle of the period between ticks.\n    ticklabeloverflow: Determines how we handle tick labels that would overflow either the graph div or the domain of the axis. The default value for inside tick labels is *hide past domain*. Otherwise on *category* and *multicategory* axes the default is *allow*. In other cases the default is *hide past div*.\n    ticklabelposition: Determines where tick labels are drawn with respect to the axis. Please note that top or bottom has no effect on x axes or when `ticklabelmode` is set to *period* or when `tickson` is set to *boundaries*. Similarly, left or right has no effect on y axes or when `ticklabelmode` is set to *period* or when `tickson` is set to *boundaries*. Has no effect on *multicategory* axes. When used on axes linked by `matches` or `scaleanchor`, no extra padding for inside labels would be added by autorange, so that the scales could match.\n    ticklabelshift: Shifts the tick labels by the specified number of pixels in parallel to the axis. Positive values move the labels in the positive direction of the axis.\n    ticklabelstandoff: Sets the standoff distance (in px) between the axis tick labels and their default position. A positive `ticklabelstandoff` moves the labels farther away from the plot area if `ticklabelposition` is *outside*, and deeper into the plot area if `ticklabelposition` is *inside*. A negative `ticklabelstandoff` works in the opposite direction, moving outside ticks towards the plot area and inside ticks towards the outside. If the negative value is large enough, inside ticks can even end up outside and vice versa.\n    ticklabelstep: Sets the spacing between tick labels as compared to the spacing between ticks. A value of 1 (default) means each tick gets a label. A value of 2 means shows every 2nd label. A larger value n means only every nth tick is labeled. `tick0` determines which labels are shown. Not implemented for axes with `type` *log* or *multicategory*, or when `tickmode` is *array*.\n    ticklen: Sets the tick length (in px).\n    tickmode: Sets the tick mode for this axis. If *auto*, the number of ticks is set via `nticks`. If *linear*, the placement of the ticks is determined by a starting position `tick0` and a tick step `dtick` (*linear* is the default value if `tick0` and `dtick` are provided). If *array*, the placement of the ticks is set via `tickvals` and the tick text is `ticktext`. (*array* is the default value if `tickvals` is provided). If *sync*, the number of ticks will sync with the overlayed axis set by `overlaying` property. When no other tick info is provided, overlaying (non-categorical) axes default to *sync*, while other axes default to *auto*.\n    tickprefix: Sets a tick label prefix.\n    ticks: Determines whether ticks are drawn or not. If **, this axis' ticks are not drawn. If *outside* (*inside*), this axis' are drawn outside (inside) the axis lines.\n    tickson: Determines where ticks and grid lines are drawn with respect to their corresponding tick labels. Only has an effect for axes of `type` *category* or *multicategory*. When set to *boundaries*, ticks and grid lines are drawn half a category to the left/bottom of labels.\n    ticksuffix: Sets a tick label suffix.\n    ticktext: Sets the text displayed at the ticks position via `tickvals`. Only has an effect if `tickmode` is set to *array*. Used with `tickvals`.\n    tickvals: Sets the values at which ticks on this axis appear. Only has an effect if `tickmode` is set to *array*. Used with `ticktext`.\n    tickwidth: Sets the tick width (in px).\n    type: Sets the axis type. By default, plotly attempts to determined the axis type by looking into the data of the traces that referenced the axis in question.\n    uirevision: Controls persistence of user-driven changes in axis `range`, `autorange`, and `title` if in `editable: true` configuration. Defaults to `layout.uirevision`.\n    visible: A single toggle to hide the axis while preserving interaction like dragging. Default is true when a cheater plot is present on the axis, otherwise false\n    zeroline: Determines whether or not a line is drawn at along the 0 value of this axis. If *true*, the zero line is drawn on top of the grid lines.\n    zerolinecolor: Sets the line color of the zero line.\n    zerolinelayer: Sets the layer on which this zeroline is displayed. If *above traces*, this zeroline is displayed above all the subplot's traces If *below traces*, this zeroline is displayed below all the subplot's traces, but above the grid lines. Limitation: *zerolinelayer* currently has no effect if the *zorder* property is set on any trace.\n    zerolinewidth: Sets the width (in px) of the zero line."
        ...

class YAxis(_PlotlyObject):
    "Create a new 'YAxis' object"
    anchor: Any
    "If set to an opposite-letter axis id (e.g. `x2`, `y`), this axis is bound to the corresponding opposite-letter axis. If set to *free*, this axis' position is determined by `position`."
    automargin: str | Any
    "Determines whether long tick labels automatically grow the figure margins."
    autorange: Any
    "Determines whether or not the range of this axis is computed in relation to the input data. See `rangemode` for more info. If `range` is provided and it has a value for both the lower and upper bound, `autorange` is set to *false*. Using *min* applies autorange only to set the minimum. Using *max* applies autorange only to set the maximum. Using *min reversed* applies autorange only to set the minimum on a reversed axis. Using *max reversed* applies autorange only to set the maximum on a reversed axis. Using *reversed* applies autorange on both ends and reverses the axis direction."
    @property
    def autorangeoptions(self) -> _plotly_graph_objs_layout_yaxis.Autorangeoptions | Any:
        ...
    @autorangeoptions.setter
    def autorangeoptions(self, value: Any) -> None: ...
    autoshift: bool | Any
    "Automatically reposition the axis to avoid overlap with other axes with the same `overlaying` value. This repositioning will account for any `shift` amount applied to other axes on the same side with `autoshift` is set to true. Only has an effect if `anchor` is set to *free*."
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
    constrain: Any
    "If this axis needs to be compressed (either due to its own `scaleanchor` and `scaleratio` or those of the other axis), determines how that happens: by increasing the *range*, or by decreasing the *domain*. Default is *domain* for axes containing image traces, *range* otherwise."
    constraintoward: Any
    "If this axis needs to be compressed (either due to its own `scaleanchor` and `scaleratio` or those of the other axis), determines which direction we push the originally specified plot area. Options are *left*, *center* (default), and *right* for x axes, and *top*, *middle* (default), and *bottom* for y axes."
    dividercolor: Any
    "Sets the color of the dividers Only has an effect on *multicategory* axes."
    dividerwidth: float | Any
    "Sets the width (in px) of the dividers Only has an effect on *multicategory* axes."
    domain: Any
    "Sets the domain of this axis (in plot fraction)."
    dtick: Any
    "Sets the step in-between ticks on this axis. Use with `tick0`. Must be a positive number, or special strings available to *log* and *date* axes. If the axis `type` is *log*, then ticks are set every 10^(n*dtick) where n is the tick number. For example, to set a tick mark at 1, 10, 100, 1000, ... set dtick to 1. To set tick marks at 1, 100, 10000, ... set dtick to 2. To set tick marks at 1, 5, 25, 125, 625, 3125, ... set dtick to log_10(5), or 0.69897000433. *log* has several special values; *L<f>*, where `f` is a positive number, gives ticks linearly spaced in value (but not position). For example `tick0` = 0.1, `dtick` = *L0.5* will put ticks at 0.1, 0.6, 1.1, 1.6 etc. To show powers of 10 plus small digits between, use *D1* (all digits) or *D2* (only 2 and 5). `tick0` is ignored for *D1* and *D2*. If the axis `type` is *date*, then you must convert the time to milliseconds. For example, to set the interval between ticks to one day, set `dtick` to 86400000.0. *date* also has special values *M<n>* gives ticks spaced by a number of months. `n` must be a positive integer. To set ticks on the 15th of every third month, set `tick0` to *2000-01-15* and `dtick` to *M3*. To set ticks every 4 years, set `dtick` to *M48*"
    exponentformat: Any
    "Determines a formatting rule for the tick exponents. For example, consider the number 1,000,000,000. If *none*, it appears as 1,000,000,000. If *e*, 1e+9. If *E*, 1E+9. If *power*, 1x10^9 (with 9 in a super script). If *SI*, 1G. If *B*, 1B. *SI* uses prefixes from \"femto\" f (10^-15) to \"tera\" T (10^12). *SI extended* covers instead the full SI range from \"quecto\" q (10^-30) to \"quetta\" Q (10^30). If *SI* or *SI extended* is used and the exponent is beyond the above ranges, the formatting rule will automatically be switched to the power notation."
    fixedrange: bool | Any
    "Determines whether or not this axis is zoom-able. If true, then zoom is disabled."
    gridcolor: Any
    "Sets the color of the grid lines."
    griddash: str | Any
    "Sets the dash style of lines. Set to a dash type string (*solid*, *dot*, *dash*, *longdash*, *dashdot*, or *longdashdot*) or a dash length list in px (eg *5px,10px,2px,2px*)."
    gridwidth: float | Any
    "Sets the width (in px) of the grid lines."
    hoverformat: str | Any
    "Sets the hover text formatting rule using d3 formatting mini-languages which are very similar to those in Python. For numbers, see: https://github.com/d3/d3-format/tree/v1.4.5#d3-format. And for dates see: https://github.com/d3/d3-time-format/tree/v2.2.3#locale_format. We add two items to d3's date formatter: *%h* for half of the year as a decimal number as well as *%{n}f* for fractional seconds with n digits. For example, *2016-10-13 09:15:23.456* with tickformat *%H~%M~%S.%2f* would display *09~15~23.46*"
    insiderange: Any
    "Could be used to set the desired inside range of this axis (excluding the labels) when `ticklabelposition` of the anchored axis has *inside*. Not implemented for axes with `type` *log*. This would be ignored when `range` is provided."
    labelalias: Any
    "Replacement text for specific tick or hover labels. For example using {US: 'USA', CA: 'Canada'} changes US to USA and CA to Canada. The labels we would have shown must match the keys exactly, after adding any tickprefix or ticksuffix. For negative numbers the minus sign symbol used (U+2212) is wider than the regular ascii dash. That means you need to use −1 instead of -1. labelalias can be used with any axis type, and both keys (if needed) and values (if desired) can include html-like tags or MathJax."
    layer: Any
    "Sets the layer on which this axis is displayed. If *above traces*, this axis is displayed above all the subplot's traces If *below traces*, this axis is displayed below all the subplot's traces, but above the grid lines. Useful when used together with scatter-like traces with `cliponaxis` set to *false* to show markers and/or text nodes above this axis."
    linecolor: Any
    "Sets the axis line color."
    linewidth: float | Any
    "Sets the width (in px) of the axis line."
    matches: Any
    "If set to another axis id (e.g. `x2`, `y`), the range of this axis will match the range of the corresponding axis in data-coordinates space. Moreover, matching axes share auto-range values, category lists and histogram auto-bins. Note that setting axes simultaneously in both a `scaleanchor` and a `matches` constraint is currently forbidden. Moreover, note that matching axes must have the same `type`."
    maxallowed: Any
    "Determines the maximum range of this axis."
    minallowed: Any
    "Determines the minimum range of this axis."
    minexponent: float | Any
    "Hide SI prefix for 10^n if |n| is below this number. This only has an effect when `tickformat` is *SI* or *B*."
    @property
    def minor(self) -> _plotly_graph_objs_layout_yaxis.Minor | Any:
        ...
    @minor.setter
    def minor(self, value: Any) -> None: ...
    minorloglabels: Any
    "Determines how minor log labels are displayed. If *small digits*, small digits i.e. 2 or 5 are displayed. If *complete*, complete digits are displayed. If *none*, no labels are displayed."
    mirror: Any
    "Determines if the axis lines or/and ticks are mirrored to the opposite side of the plotting area. If *true*, the axis lines are mirrored. If *ticks*, the axis lines and ticks are mirrored. If *false*, mirroring is disable. If *all*, axis lines are mirrored on all shared-axes subplots. If *allticks*, axis lines and ticks are mirrored on all shared-axes subplots."
    modebardisable: str | Any
    "Disables certain modebar buttons for this axis. *autoscale* disables the autoscale buttons, *zoominout* disables the zoom-in and zoom-out buttons."
    nticks: int | Any
    "Specifies the maximum number of ticks for the particular axis. The actual number of ticks will be chosen automatically to be less than or equal to `nticks`. Has an effect only if `tickmode` is set to *auto*."
    overlaying: Any
    "If set a same-letter axis id, this axis is overlaid on top of the corresponding same-letter axis, with traces and axes visible for both axes. If *false*, this axis does not overlay any same-letter axes. In this case, for axes with overlapping domains only the highest-numbered axis will be visible."
    position: float | Any
    "Sets the position of this axis in the plotting space (in normalized coordinates). Only has an effect if `anchor` is set to *free*."
    range: Any
    "Sets the range of this axis. If the axis `type` is *log*, then you must take the log of your desired range (e.g. to set the range from 1 to 100, set the range from 0 to 2). If the axis `type` is *date*, it should be date strings, like date data, though Date objects and unix milliseconds will be accepted and converted to strings. If the axis `type` is *category*, it should be numbers, using the scale where each category is assigned a serial number from zero in the order it appears. Leaving either or both elements `null` impacts the default `autorange`."
    @property
    def rangebreak(self) -> _plotly_graph_objs_layout_yaxis.Rangebreak | Any:
        ...
    @rangebreak.setter
    def rangebreak(self, value: Any) -> None: ...
    rangemode: Any
    "If *normal*, the range is computed in relation to the extrema of the input data. If *tozero*, the range extends to 0, regardless of the input data If *nonnegative*, the range is non-negative, regardless of the input data. Applies only to linear axes."
    scaleanchor: Any
    "If set to another axis id (e.g. `x2`, `y`), the range of this axis changes together with the range of the corresponding axis such that the scale of pixels per unit is in a constant ratio. Both axes are still zoomable, but when you zoom one, the other will zoom the same amount, keeping a fixed midpoint. `constrain` and `constraintoward` determine how we enforce the constraint. You can chain these, ie `yaxis: {scaleanchor: *x*}, xaxis2: {scaleanchor: *y*}` but you can only link axes of the same `type`. The linked axis can have the opposite letter (to constrain the aspect ratio) or the same letter (to match scales across subplots). Loops (`yaxis: {scaleanchor: *x*}, xaxis: {scaleanchor: *y*}` or longer) are redundant and the last constraint encountered will be ignored to avoid possible inconsistent constraints via `scaleratio`. Note that setting axes simultaneously in both a `scaleanchor` and a `matches` constraint is currently forbidden. Setting `false` allows to remove a default constraint (occasionally, you may need to prevent a default `scaleanchor` constraint from being applied, eg. when having an image trace `yaxis: {scaleanchor: \"x\"}` is set automatically in order for pixels to be rendered as squares, setting `yaxis: {scaleanchor: false}` allows to remove the constraint)."
    scaleratio: float | Any
    "If this axis is linked to another by `scaleanchor`, this determines the pixel to unit scale ratio. For example, if this value is 10, then every unit on this axis spans 10 times the number of pixels as a unit on the linked axis. Use this for example to create an elevation profile where the vertical scale is exaggerated a fixed amount with respect to the horizontal."
    separatethousands: bool | Any
    "If \"true\", even 4-digit integers are separated"
    shift: float | Any
    "Moves the axis a given number of pixels from where it would have been otherwise. Accepts both positive and negative values, which will shift the axis either right or left, respectively. If `autoshift` is set to true, then this defaults to a padding of -3 if `side` is set to *left*. and defaults to +3 if `side` is set to *right*. Defaults to 0 if `autoshift` is set to false. Only has an effect if `anchor` is set to *free*."
    showdividers: bool | Any
    "Determines whether or not a dividers are drawn between the category levels of this axis. Only has an effect on *multicategory* axes."
    showexponent: Any
    "If *all*, all exponents are shown besides their significands. If *first*, only the exponent of the first tick is shown. If *last*, only the exponent of the last tick is shown. If *none*, no exponents appear."
    showgrid: bool | Any
    "Determines whether or not grid lines are drawn. If *true*, the grid lines are drawn at every tick mark."
    showline: bool | Any
    "Determines whether or not a line bounding this axis is drawn."
    showspikes: bool | Any
    "Determines whether or not spikes (aka droplines) are drawn for this axis. Note that spikes will never be drawn when `hovermode` is *false*."
    showticklabels: bool | Any
    "Determines whether or not the tick labels are drawn."
    showtickprefix: Any
    "If *all*, all tick labels are displayed with a prefix. If *first*, only the first tick is displayed with a prefix. If *last*, only the last tick is displayed with a suffix. If *none*, tick prefixes are hidden."
    showticksuffix: Any
    "Same as `showtickprefix` but for tick suffixes."
    side: Any
    "Determines whether a x (y) axis is positioned at the *bottom* (*left*) or *top* (*right*) of the plotting area."
    spikecolor: Any
    "Sets the spike color. If undefined, will use the series color"
    spikedash: str | Any
    "Sets the dash style of lines. Set to a dash type string (*solid*, *dot*, *dash*, *longdash*, *dashdot*, or *longdashdot*) or a dash length list in px (eg *5px,10px,2px,2px*)."
    spikemode: str | Any
    "Determines the drawing mode for the spike line If *toaxis*, the line is drawn from the data point to the axis the series is plotted on. If *across*, the line is drawn across the entire plot area, and supercedes *toaxis*. If *marker*, then a marker dot is drawn on the axis the series is plotted on"
    spikesnap: Any
    "Determines whether spikelines are stuck to the cursor or to the closest datapoints."
    spikethickness: float | Any
    "Sets the spike line width in pixels."
    tick0: Any
    "Sets the placement of the first tick on this axis. Use with `dtick`. If the axis `type` is *log*, then you must take the log of your starting tick (e.g. to set the starting tick to 100, set the `tick0` to 2) except when `dtick`=*L<f>* (see `dtick` for more info). If the axis `type` is *date*, it should be a date string, like date data. If the axis `type` is *category*, it should be a number, using the scale where each category is assigned a serial number from zero in the order it appears."
    tickangle: Any
    "Sets the angle of the tick labels with respect to the horizontal. For example, a `tickangle` of -90 draws the tick labels vertically."
    tickcolor: Any
    "Sets the tick color."
    @property
    def tickfont(self) -> _plotly_graph_objs_layout_yaxis.Tickfont | Any:
        "Sets the tick font."
        ...
    @tickfont.setter
    def tickfont(self, value: Any) -> None: ...
    tickformat: str | Any
    "Sets the tick label formatting rule using d3 formatting mini-languages which are very similar to those in Python. For numbers, see: https://github.com/d3/d3-format/tree/v1.4.5#d3-format. And for dates see: https://github.com/d3/d3-time-format/tree/v2.2.3#locale_format. We add two items to d3's date formatter: *%h* for half of the year as a decimal number as well as *%{n}f* for fractional seconds with n digits. For example, *2016-10-13 09:15:23.456* with tickformat *%H~%M~%S.%2f* would display *09~15~23.46*"
    @property
    def tickformatstop(self) -> _plotly_graph_objs_layout_yaxis.Tickformatstop | Any:
        ...
    @tickformatstop.setter
    def tickformatstop(self, value: Any) -> None: ...
    ticklabelindex: int | Any
    "Only for axes with `type` *date* or *linear*. Instead of drawing the major tick label, draw the label for the minor tick that is n positions away from the major tick. E.g. to always draw the label for the minor tick before each major tick, choose `ticklabelindex` -1. This is useful for date axes with `ticklabelmode` *period* if you want to label the period that ends with each major tick instead of the period that begins there."
    ticklabelmode: Any
    "Determines where tick labels are drawn with respect to their corresponding ticks and grid lines. Only has an effect for axes of `type` *date* When set to *period*, tick labels are drawn in the middle of the period between ticks."
    ticklabeloverflow: Any
    "Determines how we handle tick labels that would overflow either the graph div or the domain of the axis. The default value for inside tick labels is *hide past domain*. Otherwise on *category* and *multicategory* axes the default is *allow*. In other cases the default is *hide past div*."
    ticklabelposition: Any
    "Determines where tick labels are drawn with respect to the axis. Please note that top or bottom has no effect on x axes or when `ticklabelmode` is set to *period* or when `tickson` is set to *boundaries*. Similarly, left or right has no effect on y axes or when `ticklabelmode` is set to *period* or when `tickson` is set to *boundaries*. Has no effect on *multicategory* axes. When used on axes linked by `matches` or `scaleanchor`, no extra padding for inside labels would be added by autorange, so that the scales could match."
    ticklabelshift: int | Any
    "Shifts the tick labels by the specified number of pixels in parallel to the axis. Positive values move the labels in the positive direction of the axis."
    ticklabelstandoff: int | Any
    "Sets the standoff distance (in px) between the axis tick labels and their default position. A positive `ticklabelstandoff` moves the labels farther away from the plot area if `ticklabelposition` is *outside*, and deeper into the plot area if `ticklabelposition` is *inside*. A negative `ticklabelstandoff` works in the opposite direction, moving outside ticks towards the plot area and inside ticks towards the outside. If the negative value is large enough, inside ticks can even end up outside and vice versa."
    ticklabelstep: int | Any
    "Sets the spacing between tick labels as compared to the spacing between ticks. A value of 1 (default) means each tick gets a label. A value of 2 means shows every 2nd label. A larger value n means only every nth tick is labeled. `tick0` determines which labels are shown. Not implemented for axes with `type` *log* or *multicategory*, or when `tickmode` is *array*."
    ticklen: float | Any
    "Sets the tick length (in px)."
    tickmode: Any
    "Sets the tick mode for this axis. If *auto*, the number of ticks is set via `nticks`. If *linear*, the placement of the ticks is determined by a starting position `tick0` and a tick step `dtick` (*linear* is the default value if `tick0` and `dtick` are provided). If *array*, the placement of the ticks is set via `tickvals` and the tick text is `ticktext`. (*array* is the default value if `tickvals` is provided). If *sync*, the number of ticks will sync with the overlayed axis set by `overlaying` property. When no other tick info is provided, overlaying (non-categorical) axes default to *sync*, while other axes default to *auto*."
    tickprefix: str | Any
    "Sets a tick label prefix."
    ticks: Any
    "Determines whether ticks are drawn or not. If **, this axis' ticks are not drawn. If *outside* (*inside*), this axis' are drawn outside (inside) the axis lines."
    tickson: Any
    "Determines where ticks and grid lines are drawn with respect to their corresponding tick labels. Only has an effect for axes of `type` *category* or *multicategory*. When set to *boundaries*, ticks and grid lines are drawn half a category to the left/bottom of labels."
    ticksuffix: str | Any
    "Sets a tick label suffix."
    ticktext: Any
    "Sets the text displayed at the ticks position via `tickvals`. Only has an effect if `tickmode` is set to *array*. Used with `tickvals`."
    tickvals: Any
    "Sets the values at which ticks on this axis appear. Only has an effect if `tickmode` is set to *array*. Used with `ticktext`."
    tickwidth: float | Any
    "Sets the tick width (in px)."
    @property
    def title(self) -> _plotly_graph_objs_layout_yaxis.Title | Any:
        ...
    @title.setter
    def title(self, value: Any) -> None: ...
    type: Any
    "Sets the axis type. By default, plotly attempts to determined the axis type by looking into the data of the traces that referenced the axis in question."
    uirevision: Any
    "Controls persistence of user-driven changes in axis `range`, `autorange`, and `title` if in `editable: true` configuration. Defaults to `layout.uirevision`."
    @property
    def unifiedhovertitle(self) -> _plotly_graph_objs_layout_yaxis.Unifiedhovertitle | Any:
        ...
    @unifiedhovertitle.setter
    def unifiedhovertitle(self, value: Any) -> None: ...
    visible: bool | Any
    "A single toggle to hide the axis while preserving interaction like dragging. Default is true when a cheater plot is present on the axis, otherwise false"
    zeroline: bool | Any
    "Determines whether or not a line is drawn at along the 0 value of this axis. If *true*, the zero line is drawn on top of the grid lines."
    zerolinecolor: Any
    "Sets the line color of the zero line."
    zerolinelayer: Any
    "Sets the layer on which this zeroline is displayed. If *above traces*, this zeroline is displayed above all the subplot's traces If *below traces*, this zeroline is displayed below all the subplot's traces, but above the grid lines. Limitation: *zerolinelayer* currently has no effect if the *zorder* property is set on any trace."
    zerolinewidth: float | Any
    "Sets the width (in px) of the zero line."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        anchor: Any = ...,
        automargin: Any = ...,
        autorange: Any = ...,
        autorangeoptions: Any = ...,
        autoshift: Any = ...,
        autotickangles: Any = ...,
        autotypenumbers: Any = ...,
        calendar: Any = ...,
        categoryarray: Any = ...,
        categoryorder: Any = ...,
        color: Any = ...,
        constrain: Any = ...,
        constraintoward: Any = ...,
        dividercolor: Any = ...,
        dividerwidth: Any = ...,
        domain: Any = ...,
        dtick: Any = ...,
        exponentformat: Any = ...,
        fixedrange: Any = ...,
        gridcolor: Any = ...,
        griddash: Any = ...,
        gridwidth: Any = ...,
        hoverformat: Any = ...,
        insiderange: Any = ...,
        labelalias: Any = ...,
        layer: Any = ...,
        linecolor: Any = ...,
        linewidth: Any = ...,
        matches: Any = ...,
        maxallowed: Any = ...,
        minallowed: Any = ...,
        minexponent: Any = ...,
        minor: Any = ...,
        minorloglabels: Any = ...,
        mirror: Any = ...,
        modebardisable: Any = ...,
        nticks: Any = ...,
        overlaying: Any = ...,
        position: Any = ...,
        range: Any = ...,
        rangebreak: Any = ...,
        rangemode: Any = ...,
        scaleanchor: Any = ...,
        scaleratio: Any = ...,
        separatethousands: Any = ...,
        shift: Any = ...,
        showdividers: Any = ...,
        showexponent: Any = ...,
        showgrid: Any = ...,
        showline: Any = ...,
        showspikes: Any = ...,
        showticklabels: Any = ...,
        showtickprefix: Any = ...,
        showticksuffix: Any = ...,
        side: Any = ...,
        spikecolor: Any = ...,
        spikedash: Any = ...,
        spikemode: Any = ...,
        spikesnap: Any = ...,
        spikethickness: Any = ...,
        tick0: Any = ...,
        tickangle: Any = ...,
        tickcolor: Any = ...,
        tickfont: Any = ...,
        tickformat: Any = ...,
        tickformatstop: Any = ...,
        ticklabelindex: Any = ...,
        ticklabelmode: Any = ...,
        ticklabeloverflow: Any = ...,
        ticklabelposition: Any = ...,
        ticklabelshift: Any = ...,
        ticklabelstandoff: Any = ...,
        ticklabelstep: Any = ...,
        ticklen: Any = ...,
        tickmode: Any = ...,
        tickprefix: Any = ...,
        ticks: Any = ...,
        tickson: Any = ...,
        ticksuffix: Any = ...,
        ticktext: Any = ...,
        tickvals: Any = ...,
        tickwidth: Any = ...,
        title: Any = ...,
        type: Any = ...,
        uirevision: Any = ...,
        unifiedhovertitle: Any = ...,
        visible: Any = ...,
        zeroline: Any = ...,
        zerolinecolor: Any = ...,
        zerolinelayer: Any = ...,
        zerolinewidth: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'YAxis' object\n\nArgs:\n    anchor: If set to an opposite-letter axis id (e.g. `x2`, `y`), this axis is bound to the corresponding opposite-letter axis. If set to *free*, this axis' position is determined by `position`.\n    automargin: Determines whether long tick labels automatically grow the figure margins.\n    autorange: Determines whether or not the range of this axis is computed in relation to the input data. See `rangemode` for more info. If `range` is provided and it has a value for both the lower and upper bound, `autorange` is set to *false*. Using *min* applies autorange only to set the minimum. Using *max* applies autorange only to set the maximum. Using *min reversed* applies autorange only to set the minimum on a reversed axis. Using *max reversed* applies autorange only to set the maximum on a reversed axis. Using *reversed* applies autorange on both ends and reverses the axis direction.\n    autoshift: Automatically reposition the axis to avoid overlap with other axes with the same `overlaying` value. This repositioning will account for any `shift` amount applied to other axes on the same side with `autoshift` is set to true. Only has an effect if `anchor` is set to *free*.\n    autotickangles: When `tickangle` is set to *auto*, it will be set to the first angle in this array that is large enough to prevent label overlap.\n    autotypenumbers: Using *strict* a numeric string in trace data is not converted to a number. Using *convert types* a numeric string in trace data may be treated as a number during automatic axis `type` detection. Defaults to layout.autotypenumbers.\n    calendar: Sets the calendar system to use for `range` and `tick0` if this is a date axis. This does not set the calendar for interpreting data on this axis, that's specified in the trace or via the global `layout.calendar`\n    categoryarray: Sets the order in which categories on this axis appear. Only has an effect if `categoryorder` is set to *array*. Used with `categoryorder`.\n    categoryorder: Specifies the ordering logic for the case of categorical variables. By default, plotly uses *trace*, which specifies the order that is present in the data supplied. Set `categoryorder` to *category ascending* or *category descending* if order should be determined by the alphanumerical order of the category names. Set `categoryorder` to *array* to derive the ordering from the attribute `categoryarray`. If a category is not found in the `categoryarray` array, the sorting behavior for that attribute will be identical to the *trace* mode. The unspecified categories will follow the categories in `categoryarray`. Set `categoryorder` to *total ascending* or *total descending* if order should be determined by the numerical order of the values. Similarly, the order can be determined by the min, max, sum, mean, geometric mean or median of all the values.\n    color: Sets default for all colors associated with this axis all at once: line, font, tick, and grid colors. Grid color is lightened by blending this with the plot background Individual pieces can override this.\n    constrain: If this axis needs to be compressed (either due to its own `scaleanchor` and `scaleratio` or those of the other axis), determines how that happens: by increasing the *range*, or by decreasing the *domain*. Default is *domain* for axes containing image traces, *range* otherwise.\n    constraintoward: If this axis needs to be compressed (either due to its own `scaleanchor` and `scaleratio` or those of the other axis), determines which direction we push the originally specified plot area. Options are *left*, *center* (default), and *right* for x axes, and *top*, *middle* (default), and *bottom* for y axes.\n    dividercolor: Sets the color of the dividers Only has an effect on *multicategory* axes.\n    dividerwidth: Sets the width (in px) of the dividers Only has an effect on *multicategory* axes.\n    domain: Sets the domain of this axis (in plot fraction).\n    dtick: Sets the step in-between ticks on this axis. Use with `tick0`. Must be a positive number, or special strings available to *log* and *date* axes. If the axis `type` is *log*, then ticks are set every 10^(n*dtick) where n is the tick number. For example, to set a tick mark at 1, 10, 100, 1000, ... set dtick to 1. To set tick marks at 1, 100, 10000, ... set dtick to 2. To set tick marks at 1, 5, 25, 125, 625, 3125, ... set dtick to log_10(5), or 0.69897000433. *log* has several special values; *L<f>*, where `f` is a positive number, gives ticks linearly spaced in value (but not position). For example `tick0` = 0.1, `dtick` = *L0.5* will put ticks at 0.1, 0.6, 1.1, 1.6 etc. To show powers of 10 plus small digits between, use *D1* (all digits) or *D2* (only 2 and 5). `tick0` is ignored for *D1* and *D2*. If the axis `type` is *date*, then you must convert the time to milliseconds. For example, to set the interval between ticks to one day, set `dtick` to 86400000.0. *date* also has special values *M<n>* gives ticks spaced by a number of months. `n` must be a positive integer. To set ticks on the 15th of every third month, set `tick0` to *2000-01-15* and `dtick` to *M3*. To set ticks every 4 years, set `dtick` to *M48*\n    exponentformat: Determines a formatting rule for the tick exponents. For example, consider the number 1,000,000,000. If *none*, it appears as 1,000,000,000. If *e*, 1e+9. If *E*, 1E+9. If *power*, 1x10^9 (with 9 in a super script). If *SI*, 1G. If *B*, 1B. *SI* uses prefixes from \"femto\" f (10^-15) to \"tera\" T (10^12). *SI extended* covers instead the full SI range from \"quecto\" q (10^-30) to \"quetta\" Q (10^30). If *SI* or *SI extended* is used and the exponent is beyond the above ranges, the formatting rule will automatically be switched to the power notation.\n    fixedrange: Determines whether or not this axis is zoom-able. If true, then zoom is disabled.\n    gridcolor: Sets the color of the grid lines.\n    griddash: Sets the dash style of lines. Set to a dash type string (*solid*, *dot*, *dash*, *longdash*, *dashdot*, or *longdashdot*) or a dash length list in px (eg *5px,10px,2px,2px*).\n    gridwidth: Sets the width (in px) of the grid lines.\n    hoverformat: Sets the hover text formatting rule using d3 formatting mini-languages which are very similar to those in Python. For numbers, see: https://github.com/d3/d3-format/tree/v1.4.5#d3-format. And for dates see: https://github.com/d3/d3-time-format/tree/v2.2.3#locale_format. We add two items to d3's date formatter: *%h* for half of the year as a decimal number as well as *%{n}f* for fractional seconds with n digits. For example, *2016-10-13 09:15:23.456* with tickformat *%H~%M~%S.%2f* would display *09~15~23.46*\n    insiderange: Could be used to set the desired inside range of this axis (excluding the labels) when `ticklabelposition` of the anchored axis has *inside*. Not implemented for axes with `type` *log*. This would be ignored when `range` is provided.\n    labelalias: Replacement text for specific tick or hover labels. For example using {US: 'USA', CA: 'Canada'} changes US to USA and CA to Canada. The labels we would have shown must match the keys exactly, after adding any tickprefix or ticksuffix. For negative numbers the minus sign symbol used (U+2212) is wider than the regular ascii dash. That means you need to use −1 instead of -1. labelalias can be used with any axis type, and both keys (if needed) and values (if desired) can include html-like tags or MathJax.\n    layer: Sets the layer on which this axis is displayed. If *above traces*, this axis is displayed above all the subplot's traces If *below traces*, this axis is displayed below all the subplot's traces, but above the grid lines. Useful when used together with scatter-like traces with `cliponaxis` set to *false* to show markers and/or text nodes above this axis.\n    linecolor: Sets the axis line color.\n    linewidth: Sets the width (in px) of the axis line.\n    matches: If set to another axis id (e.g. `x2`, `y`), the range of this axis will match the range of the corresponding axis in data-coordinates space. Moreover, matching axes share auto-range values, category lists and histogram auto-bins. Note that setting axes simultaneously in both a `scaleanchor` and a `matches` constraint is currently forbidden. Moreover, note that matching axes must have the same `type`.\n    maxallowed: Determines the maximum range of this axis.\n    minallowed: Determines the minimum range of this axis.\n    minexponent: Hide SI prefix for 10^n if |n| is below this number. This only has an effect when `tickformat` is *SI* or *B*.\n    minorloglabels: Determines how minor log labels are displayed. If *small digits*, small digits i.e. 2 or 5 are displayed. If *complete*, complete digits are displayed. If *none*, no labels are displayed.\n    mirror: Determines if the axis lines or/and ticks are mirrored to the opposite side of the plotting area. If *true*, the axis lines are mirrored. If *ticks*, the axis lines and ticks are mirrored. If *false*, mirroring is disable. If *all*, axis lines are mirrored on all shared-axes subplots. If *allticks*, axis lines and ticks are mirrored on all shared-axes subplots.\n    modebardisable: Disables certain modebar buttons for this axis. *autoscale* disables the autoscale buttons, *zoominout* disables the zoom-in and zoom-out buttons.\n    nticks: Specifies the maximum number of ticks for the particular axis. The actual number of ticks will be chosen automatically to be less than or equal to `nticks`. Has an effect only if `tickmode` is set to *auto*.\n    overlaying: If set a same-letter axis id, this axis is overlaid on top of the corresponding same-letter axis, with traces and axes visible for both axes. If *false*, this axis does not overlay any same-letter axes. In this case, for axes with overlapping domains only the highest-numbered axis will be visible.\n    position: Sets the position of this axis in the plotting space (in normalized coordinates). Only has an effect if `anchor` is set to *free*.\n    range: Sets the range of this axis. If the axis `type` is *log*, then you must take the log of your desired range (e.g. to set the range from 1 to 100, set the range from 0 to 2). If the axis `type` is *date*, it should be date strings, like date data, though Date objects and unix milliseconds will be accepted and converted to strings. If the axis `type` is *category*, it should be numbers, using the scale where each category is assigned a serial number from zero in the order it appears. Leaving either or both elements `null` impacts the default `autorange`.\n    rangemode: If *normal*, the range is computed in relation to the extrema of the input data. If *tozero*, the range extends to 0, regardless of the input data If *nonnegative*, the range is non-negative, regardless of the input data. Applies only to linear axes.\n    scaleanchor: If set to another axis id (e.g. `x2`, `y`), the range of this axis changes together with the range of the corresponding axis such that the scale of pixels per unit is in a constant ratio. Both axes are still zoomable, but when you zoom one, the other will zoom the same amount, keeping a fixed midpoint. `constrain` and `constraintoward` determine how we enforce the constraint. You can chain these, ie `yaxis: {scaleanchor: *x*}, xaxis2: {scaleanchor: *y*}` but you can only link axes of the same `type`. The linked axis can have the opposite letter (to constrain the aspect ratio) or the same letter (to match scales across subplots). Loops (`yaxis: {scaleanchor: *x*}, xaxis: {scaleanchor: *y*}` or longer) are redundant and the last constraint encountered will be ignored to avoid possible inconsistent constraints via `scaleratio`. Note that setting axes simultaneously in both a `scaleanchor` and a `matches` constraint is currently forbidden. Setting `false` allows to remove a default constraint (occasionally, you may need to prevent a default `scaleanchor` constraint from being applied, eg. when having an image trace `yaxis: {scaleanchor: \"x\"}` is set automatically in order for pixels to be rendered as squares, setting `yaxis: {scaleanchor: false}` allows to remove the constraint).\n    scaleratio: If this axis is linked to another by `scaleanchor`, this determines the pixel to unit scale ratio. For example, if this value is 10, then every unit on this axis spans 10 times the number of pixels as a unit on the linked axis. Use this for example to create an elevation profile where the vertical scale is exaggerated a fixed amount with respect to the horizontal.\n    separatethousands: If \"true\", even 4-digit integers are separated\n    shift: Moves the axis a given number of pixels from where it would have been otherwise. Accepts both positive and negative values, which will shift the axis either right or left, respectively. If `autoshift` is set to true, then this defaults to a padding of -3 if `side` is set to *left*. and defaults to +3 if `side` is set to *right*. Defaults to 0 if `autoshift` is set to false. Only has an effect if `anchor` is set to *free*.\n    showdividers: Determines whether or not a dividers are drawn between the category levels of this axis. Only has an effect on *multicategory* axes.\n    showexponent: If *all*, all exponents are shown besides their significands. If *first*, only the exponent of the first tick is shown. If *last*, only the exponent of the last tick is shown. If *none*, no exponents appear.\n    showgrid: Determines whether or not grid lines are drawn. If *true*, the grid lines are drawn at every tick mark.\n    showline: Determines whether or not a line bounding this axis is drawn.\n    showspikes: Determines whether or not spikes (aka droplines) are drawn for this axis. Note that spikes will never be drawn when `hovermode` is *false*.\n    showticklabels: Determines whether or not the tick labels are drawn.\n    showtickprefix: If *all*, all tick labels are displayed with a prefix. If *first*, only the first tick is displayed with a prefix. If *last*, only the last tick is displayed with a suffix. If *none*, tick prefixes are hidden.\n    showticksuffix: Same as `showtickprefix` but for tick suffixes.\n    side: Determines whether a x (y) axis is positioned at the *bottom* (*left*) or *top* (*right*) of the plotting area.\n    spikecolor: Sets the spike color. If undefined, will use the series color\n    spikedash: Sets the dash style of lines. Set to a dash type string (*solid*, *dot*, *dash*, *longdash*, *dashdot*, or *longdashdot*) or a dash length list in px (eg *5px,10px,2px,2px*).\n    spikemode: Determines the drawing mode for the spike line If *toaxis*, the line is drawn from the data point to the axis the series is plotted on. If *across*, the line is drawn across the entire plot area, and supercedes *toaxis*. If *marker*, then a marker dot is drawn on the axis the series is plotted on\n    spikesnap: Determines whether spikelines are stuck to the cursor or to the closest datapoints.\n    spikethickness: Sets the spike line width in pixels.\n    tick0: Sets the placement of the first tick on this axis. Use with `dtick`. If the axis `type` is *log*, then you must take the log of your starting tick (e.g. to set the starting tick to 100, set the `tick0` to 2) except when `dtick`=*L<f>* (see `dtick` for more info). If the axis `type` is *date*, it should be a date string, like date data. If the axis `type` is *category*, it should be a number, using the scale where each category is assigned a serial number from zero in the order it appears.\n    tickangle: Sets the angle of the tick labels with respect to the horizontal. For example, a `tickangle` of -90 draws the tick labels vertically.\n    tickcolor: Sets the tick color.\n    tickfont: Sets the tick font.\n    tickformat: Sets the tick label formatting rule using d3 formatting mini-languages which are very similar to those in Python. For numbers, see: https://github.com/d3/d3-format/tree/v1.4.5#d3-format. And for dates see: https://github.com/d3/d3-time-format/tree/v2.2.3#locale_format. We add two items to d3's date formatter: *%h* for half of the year as a decimal number as well as *%{n}f* for fractional seconds with n digits. For example, *2016-10-13 09:15:23.456* with tickformat *%H~%M~%S.%2f* would display *09~15~23.46*\n    ticklabelindex: Only for axes with `type` *date* or *linear*. Instead of drawing the major tick label, draw the label for the minor tick that is n positions away from the major tick. E.g. to always draw the label for the minor tick before each major tick, choose `ticklabelindex` -1. This is useful for date axes with `ticklabelmode` *period* if you want to label the period that ends with each major tick instead of the period that begins there.\n    ticklabelmode: Determines where tick labels are drawn with respect to their corresponding ticks and grid lines. Only has an effect for axes of `type` *date* When set to *period*, tick labels are drawn in the middle of the period between ticks.\n    ticklabeloverflow: Determines how we handle tick labels that would overflow either the graph div or the domain of the axis. The default value for inside tick labels is *hide past domain*. Otherwise on *category* and *multicategory* axes the default is *allow*. In other cases the default is *hide past div*.\n    ticklabelposition: Determines where tick labels are drawn with respect to the axis. Please note that top or bottom has no effect on x axes or when `ticklabelmode` is set to *period* or when `tickson` is set to *boundaries*. Similarly, left or right has no effect on y axes or when `ticklabelmode` is set to *period* or when `tickson` is set to *boundaries*. Has no effect on *multicategory* axes. When used on axes linked by `matches` or `scaleanchor`, no extra padding for inside labels would be added by autorange, so that the scales could match.\n    ticklabelshift: Shifts the tick labels by the specified number of pixels in parallel to the axis. Positive values move the labels in the positive direction of the axis.\n    ticklabelstandoff: Sets the standoff distance (in px) between the axis tick labels and their default position. A positive `ticklabelstandoff` moves the labels farther away from the plot area if `ticklabelposition` is *outside*, and deeper into the plot area if `ticklabelposition` is *inside*. A negative `ticklabelstandoff` works in the opposite direction, moving outside ticks towards the plot area and inside ticks towards the outside. If the negative value is large enough, inside ticks can even end up outside and vice versa.\n    ticklabelstep: Sets the spacing between tick labels as compared to the spacing between ticks. A value of 1 (default) means each tick gets a label. A value of 2 means shows every 2nd label. A larger value n means only every nth tick is labeled. `tick0` determines which labels are shown. Not implemented for axes with `type` *log* or *multicategory*, or when `tickmode` is *array*.\n    ticklen: Sets the tick length (in px).\n    tickmode: Sets the tick mode for this axis. If *auto*, the number of ticks is set via `nticks`. If *linear*, the placement of the ticks is determined by a starting position `tick0` and a tick step `dtick` (*linear* is the default value if `tick0` and `dtick` are provided). If *array*, the placement of the ticks is set via `tickvals` and the tick text is `ticktext`. (*array* is the default value if `tickvals` is provided). If *sync*, the number of ticks will sync with the overlayed axis set by `overlaying` property. When no other tick info is provided, overlaying (non-categorical) axes default to *sync*, while other axes default to *auto*.\n    tickprefix: Sets a tick label prefix.\n    ticks: Determines whether ticks are drawn or not. If **, this axis' ticks are not drawn. If *outside* (*inside*), this axis' are drawn outside (inside) the axis lines.\n    tickson: Determines where ticks and grid lines are drawn with respect to their corresponding tick labels. Only has an effect for axes of `type` *category* or *multicategory*. When set to *boundaries*, ticks and grid lines are drawn half a category to the left/bottom of labels.\n    ticksuffix: Sets a tick label suffix.\n    ticktext: Sets the text displayed at the ticks position via `tickvals`. Only has an effect if `tickmode` is set to *array*. Used with `tickvals`.\n    tickvals: Sets the values at which ticks on this axis appear. Only has an effect if `tickmode` is set to *array*. Used with `ticktext`.\n    tickwidth: Sets the tick width (in px).\n    type: Sets the axis type. By default, plotly attempts to determined the axis type by looking into the data of the traces that referenced the axis in question.\n    uirevision: Controls persistence of user-driven changes in axis `range`, `autorange`, and `title` if in `editable: true` configuration. Defaults to `layout.uirevision`.\n    visible: A single toggle to hide the axis while preserving interaction like dragging. Default is true when a cheater plot is present on the axis, otherwise false\n    zeroline: Determines whether or not a line is drawn at along the 0 value of this axis. If *true*, the zero line is drawn on top of the grid lines.\n    zerolinecolor: Sets the line color of the zero line.\n    zerolinelayer: Sets the layer on which this zeroline is displayed. If *above traces*, this zeroline is displayed above all the subplot's traces If *below traces*, this zeroline is displayed below all the subplot's traces, but above the grid lines. Limitation: *zerolinelayer* currently has no effect if the *zorder* property is set on any trace.\n    zerolinewidth: Sets the width (in px) of the zero line."
        ...

class Mapbox(_PlotlyObject):
    "Create a new 'Mapbox' object"
    accesstoken: str | Any
    "Sets the mapbox access token to be used for this mapbox map. Alternatively, the mapbox access token can be set in the configuration options under `mapboxAccessToken`. Note that accessToken are only required when `style` (e.g with values : basic, streets, outdoors, light, dark, satellite, satellite-streets ) and/or a layout layer references the Mapbox server."
    bearing: float | Any
    "Sets the bearing angle of the map in degrees counter-clockwise from North (mapbox.bearing)."
    @property
    def bounds(self) -> _plotly_graph_objs_layout_mapbox.Bounds | Any:
        ...
    @bounds.setter
    def bounds(self, value: Any) -> None: ...
    @property
    def center(self) -> _plotly_graph_objs_layout_mapbox.Center | Any:
        ...
    @center.setter
    def center(self, value: Any) -> None: ...
    @property
    def domain(self) -> _plotly_graph_objs_layout_mapbox.Domain | Any:
        ...
    @domain.setter
    def domain(self, value: Any) -> None: ...
    @property
    def layer(self) -> _plotly_graph_objs_layout_mapbox.Layer | Any:
        ...
    @layer.setter
    def layer(self, value: Any) -> None: ...
    pitch: float | Any
    "Sets the pitch angle of the map (in degrees, where *0* means perpendicular to the surface of the map) (mapbox.pitch)."
    style: Any
    "Defines the map layers that are rendered by default below the trace layers defined in `data`, which are themselves by default rendered below the layers defined in `layout.mapbox.layers`.  These layers can be defined either explicitly as a Mapbox Style object which can contain multiple layer definitions that load data from any public or private Tile Map Service (TMS or XYZ) or Web Map Service (WMS) or implicitly by using one of the built-in style objects which use WMSes which do not require any access tokens, or by using a default Mapbox style or custom Mapbox style URL, both of which require a Mapbox access token  Note that Mapbox access token can be set in the `accesstoken` attribute or in the `mapboxAccessToken` config option.  Mapbox Style objects are of the form described in the Mapbox GL JS documentation available at https://docs.mapbox.com/mapbox-gl-js/style-spec  The built-in plotly.js styles objects are: carto-darkmatter, carto-positron, open-street-map, stamen-terrain, stamen-toner, stamen-watercolor, white-bg  The built-in Mapbox styles are: basic, streets, outdoors, light, dark, satellite, satellite-streets  Mapbox style URLs are of the form: mapbox://mapbox.mapbox-<name>-<version>"
    uirevision: Any
    "Controls persistence of user-driven changes in the view: `center`, `zoom`, `bearing`, `pitch`. Defaults to `layout.uirevision`."
    zoom: float | Any
    "Sets the zoom level of the map (mapbox.zoom)."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        accesstoken: Any = ...,
        bearing: Any = ...,
        bounds: Any = ...,
        center: Any = ...,
        domain: Any = ...,
        layer: Any = ...,
        pitch: Any = ...,
        style: Any = ...,
        uirevision: Any = ...,
        zoom: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Mapbox' object\n\nArgs:\n    accesstoken: Sets the mapbox access token to be used for this mapbox map. Alternatively, the mapbox access token can be set in the configuration options under `mapboxAccessToken`. Note that accessToken are only required when `style` (e.g with values : basic, streets, outdoors, light, dark, satellite, satellite-streets ) and/or a layout layer references the Mapbox server.\n    bearing: Sets the bearing angle of the map in degrees counter-clockwise from North (mapbox.bearing).\n    pitch: Sets the pitch angle of the map (in degrees, where *0* means perpendicular to the surface of the map) (mapbox.pitch).\n    style: Defines the map layers that are rendered by default below the trace layers defined in `data`, which are themselves by default rendered below the layers defined in `layout.mapbox.layers`.  These layers can be defined either explicitly as a Mapbox Style object which can contain multiple layer definitions that load data from any public or private Tile Map Service (TMS or XYZ) or Web Map Service (WMS) or implicitly by using one of the built-in style objects which use WMSes which do not require any access tokens, or by using a default Mapbox style or custom Mapbox style URL, both of which require a Mapbox access token  Note that Mapbox access token can be set in the `accesstoken` attribute or in the `mapboxAccessToken` config option.  Mapbox Style objects are of the form described in the Mapbox GL JS documentation available at https://docs.mapbox.com/mapbox-gl-js/style-spec  The built-in plotly.js styles objects are: carto-darkmatter, carto-positron, open-street-map, stamen-terrain, stamen-toner, stamen-watercolor, white-bg  The built-in Mapbox styles are: basic, streets, outdoors, light, dark, satellite, satellite-streets  Mapbox style URLs are of the form: mapbox://mapbox.mapbox-<name>-<version>\n    uirevision: Controls persistence of user-driven changes in the view: `center`, `zoom`, `bearing`, `pitch`. Defaults to `layout.uirevision`.\n    zoom: Sets the zoom level of the map (mapbox.zoom)."
        ...
