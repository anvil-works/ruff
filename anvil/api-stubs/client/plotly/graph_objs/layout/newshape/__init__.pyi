# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the Plotly catalogue generator in doc/anvil-api-stubs/plotly-stubs.mjs instead, then run:
#   pnpm -F docs build
#
from plotly._base import _PlotlyObject
from typing import Any, Mapping
import plotly.graph_objs.layout.newshape.label as _plotly_graph_objs_layout_newshape_label
import plotly.graph_objs.layout.newshape.label as label
import plotly.graph_objs.layout.newshape.legendgrouptitle as _plotly_graph_objs_layout_newshape_legendgrouptitle
import plotly.graph_objs.layout.newshape.legendgrouptitle as legendgrouptitle

class Label(_PlotlyObject):
    "Create a new 'Label' object"
    @property
    def font(self) -> _plotly_graph_objs_layout_newshape_label.Font | Any:
        "Sets the new shape label text font."
        ...
    @font.setter
    def font(self, value: Any) -> None: ...
    padding: float | Any
    "Sets padding (in px) between edge of label and edge of new shape."
    text: str | Any
    "Sets the text to display with the new shape. It is also used for legend item if `name` is not provided."
    textangle: Any
    "Sets the angle at which the label text is drawn with respect to the horizontal. For lines, angle *auto* is the same angle as the line. For all other shapes, angle *auto* is horizontal."
    textposition: Any
    "Sets the position of the label text relative to the new shape. Supported values for rectangles, circles and paths are *top left*, *top center*, *top right*, *middle left*, *middle center*, *middle right*, *bottom left*, *bottom center*, and *bottom right*. Supported values for lines are *start*, *middle*, and *end*. Default: *middle center* for rectangles, circles, and paths; *middle* for lines."
    texttemplate: str | Any
    "Template string used for rendering the new shape's label. Note that this will override `text`. Variables are inserted using %{variable}, for example \"x0: %{x0}\". Numbers are formatted using d3-format's syntax %{variable:d3-format}, for example \"Price: %{x0:$.2f}\". See https://github.com/d3/d3-format/tree/v1.4.5#d3-format for details on the formatting syntax. Dates are formatted using d3-time-format's syntax %{variable|d3-time-format}, for example \"Day: %{x0|%m %b %Y}\". See https://github.com/d3/d3-time-format/tree/v2.2.3#locale_format for details on the date formatting syntax. A single multiplication or division operation may be applied to numeric variables, and combined with d3 number formatting, for example \"Length in cm: %{x0*2.54}\", \"%{slope*60:.1f} meters per second.\" For log axes, variable values are given in log units. For date axes, x/y coordinate variables and center variables use datetimes, while all other variable values use values in ms. Finally, the template string has access to variables `x0`, `x1`, `y0`, `y1`, `slope`, `dx`, `dy`, `width`, `height`, `length`, `xcenter`, `ycenter`, `simpleXVariables` and `simpleYVariables`. Variables that can't be found will be replaced with the specifier. For example, a template of \"data: %{x}, %{y}\" will result in a value of \"data: 1, %{y}\" if x is 1 and y is missing. Variables with an undefined value will be replaced with the fallback value."
    texttemplatefallback: Any
    "Fallback string that's displayed when a variable referenced in a template is missing. If the boolean value 'false' is passed in, the specifier with the missing variable will be displayed."
    xanchor: Any
    "Sets the label's horizontal position anchor This anchor binds the specified `textposition` to the *left*, *center* or *right* of the label text. For example, if `textposition` is set to *top right* and `xanchor` to *right* then the right-most portion of the label text lines up with the right-most edge of the new shape."
    yanchor: Any
    "Sets the label's vertical position anchor This anchor binds the specified `textposition` to the *top*, *middle* or *bottom* of the label text. For example, if `textposition` is set to *top right* and `yanchor` to *top* then the top-most portion of the label text lines up with the top-most edge of the new shape."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        font: Any = ...,
        padding: Any = ...,
        text: Any = ...,
        textangle: Any = ...,
        textposition: Any = ...,
        texttemplate: Any = ...,
        texttemplatefallback: Any = ...,
        xanchor: Any = ...,
        yanchor: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Label' object\n\nArgs:\n    font: Sets the new shape label text font.\n    padding: Sets padding (in px) between edge of label and edge of new shape.\n    text: Sets the text to display with the new shape. It is also used for legend item if `name` is not provided.\n    textangle: Sets the angle at which the label text is drawn with respect to the horizontal. For lines, angle *auto* is the same angle as the line. For all other shapes, angle *auto* is horizontal.\n    textposition: Sets the position of the label text relative to the new shape. Supported values for rectangles, circles and paths are *top left*, *top center*, *top right*, *middle left*, *middle center*, *middle right*, *bottom left*, *bottom center*, and *bottom right*. Supported values for lines are *start*, *middle*, and *end*. Default: *middle center* for rectangles, circles, and paths; *middle* for lines.\n    texttemplate: Template string used for rendering the new shape's label. Note that this will override `text`. Variables are inserted using %{variable}, for example \"x0: %{x0}\". Numbers are formatted using d3-format's syntax %{variable:d3-format}, for example \"Price: %{x0:$.2f}\". See https://github.com/d3/d3-format/tree/v1.4.5#d3-format for details on the formatting syntax. Dates are formatted using d3-time-format's syntax %{variable|d3-time-format}, for example \"Day: %{x0|%m %b %Y}\". See https://github.com/d3/d3-time-format/tree/v2.2.3#locale_format for details on the date formatting syntax. A single multiplication or division operation may be applied to numeric variables, and combined with d3 number formatting, for example \"Length in cm: %{x0*2.54}\", \"%{slope*60:.1f} meters per second.\" For log axes, variable values are given in log units. For date axes, x/y coordinate variables and center variables use datetimes, while all other variable values use values in ms. Finally, the template string has access to variables `x0`, `x1`, `y0`, `y1`, `slope`, `dx`, `dy`, `width`, `height`, `length`, `xcenter`, `ycenter`, `simpleXVariables` and `simpleYVariables`. Variables that can't be found will be replaced with the specifier. For example, a template of \"data: %{x}, %{y}\" will result in a value of \"data: 1, %{y}\" if x is 1 and y is missing. Variables with an undefined value will be replaced with the fallback value.\n    texttemplatefallback: Fallback string that's displayed when a variable referenced in a template is missing. If the boolean value 'false' is passed in, the specifier with the missing variable will be displayed.\n    xanchor: Sets the label's horizontal position anchor This anchor binds the specified `textposition` to the *left*, *center* or *right* of the label text. For example, if `textposition` is set to *top right* and `xanchor` to *right* then the right-most portion of the label text lines up with the right-most edge of the new shape.\n    yanchor: Sets the label's vertical position anchor This anchor binds the specified `textposition` to the *top*, *middle* or *bottom* of the label text. For example, if `textposition` is set to *top right* and `yanchor` to *top* then the top-most portion of the label text lines up with the top-most edge of the new shape."
        ...

class Legendgrouptitle(_PlotlyObject):
    "Create a new 'Legendgrouptitle' object"
    @property
    def font(self) -> _plotly_graph_objs_layout_newshape_legendgrouptitle.Font | Any:
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
    "Sets the line color. By default uses either dark grey or white to increase contrast with background color."
    dash: str | Any
    "Sets the dash style of lines. Set to a dash type string (*solid*, *dot*, *dash*, *longdash*, *dashdot*, or *longdashdot*) or a dash length list in px (eg *5px,10px,2px,2px*)."
    width: float | Any
    "Sets the line width (in px)."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        color: Any = ...,
        dash: Any = ...,
        width: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Line' object\n\nArgs:\n    color: Sets the line color. By default uses either dark grey or white to increase contrast with background color.\n    dash: Sets the dash style of lines. Set to a dash type string (*solid*, *dot*, *dash*, *longdash*, *dashdot*, or *longdashdot*) or a dash length list in px (eg *5px,10px,2px,2px*).\n    width: Sets the line width (in px)."
        ...
