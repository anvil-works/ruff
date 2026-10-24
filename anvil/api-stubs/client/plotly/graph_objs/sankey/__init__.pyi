# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the Plotly catalogue generator in doc/anvil-api-stubs/plotly-stubs.mjs instead, then run:
#   pnpm -F docs build
#
from plotly._base import _PlotlyObject
from typing import Any, Mapping
import plotly.graph_objs.sankey.hoverlabel as _plotly_graph_objs_sankey_hoverlabel
import plotly.graph_objs.sankey.hoverlabel as hoverlabel
import plotly.graph_objs.sankey.legendgrouptitle as _plotly_graph_objs_sankey_legendgrouptitle
import plotly.graph_objs.sankey.legendgrouptitle as legendgrouptitle
import plotly.graph_objs.sankey.link as _plotly_graph_objs_sankey_link
import plotly.graph_objs.sankey.link as link
import plotly.graph_objs.sankey.node as _plotly_graph_objs_sankey_node
import plotly.graph_objs.sankey.node as node

class Domain(_PlotlyObject):
    "Create a new 'Domain' object"
    column: int | Any
    "If there is a layout grid, use the domain for this column in the grid for this sankey trace."
    row: int | Any
    "If there is a layout grid, use the domain for this row in the grid for this sankey trace."
    x: Any
    "Sets the horizontal domain of this sankey trace (in plot fraction)."
    y: Any
    "Sets the vertical domain of this sankey trace (in plot fraction)."
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
        "Create a new 'Domain' object\n\nArgs:\n    column: If there is a layout grid, use the domain for this column in the grid for this sankey trace.\n    row: If there is a layout grid, use the domain for this row in the grid for this sankey trace.\n    x: Sets the horizontal domain of this sankey trace (in plot fraction).\n    y: Sets the vertical domain of this sankey trace (in plot fraction)."
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
    def font(self) -> _plotly_graph_objs_sankey_hoverlabel.Font | Any:
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
    def font(self) -> _plotly_graph_objs_sankey_legendgrouptitle.Font | Any:
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

class Link(_PlotlyObject):
    "Create a new 'Link' object"
    arrowlen: float | Any
    "Sets the length (in px) of the links arrow, if 0 no arrow will be drawn."
    color: Any
    "Sets the `link` color. It can be a single value, or an array for specifying color for each `link`. If `link.color` is omitted, then by default, a translucent grey link will be used."
    @property
    def concentrationscales(self) -> _plotly_graph_objs_sankey_link.Concentrationscales | Any:
        ...
    @concentrationscales.setter
    def concentrationscales(self, value: Any) -> None: ...
    customdata: Any
    "Assigns extra data to each link."
    hovercolor: Any
    "Sets the `link` hover color. It can be a single value, or an array for specifying hover colors for each `link`. If `link.hovercolor` is omitted, then by default, links will become slightly more opaque when hovered over."
    hoverinfo: Any
    "Determines what trace information appears when hovering links. If `none` or `skip` are set, no information is displayed upon hovering. But, if `none` is set, click and hover events are still fired."
    @property
    def hoverlabel(self) -> _plotly_graph_objs_sankey_link.Hoverlabel | Any:
        ...
    @hoverlabel.setter
    def hoverlabel(self, value: Any) -> None: ...
    hovertemplate: str | Any
    "Template string used for rendering the information that appear on hover box. Note that this will override `hoverinfo`. Variables are inserted using %{variable}, for example \"y: %{y}\" as well as %{xother}, {%_xother}, {%_xother_}, {%xother_}. When showing info for several points, *xother* will be added to those with different x positions from the first point. An underscore before or after *(x|y)other* will add a space on that side, only when this field is shown. Numbers are formatted using d3-format's syntax %{variable:d3-format}, for example \"Price: %{y:$.2f}\". https://github.com/d3/d3-format/tree/v1.4.5#d3-format for details on the formatting syntax. Dates are formatted using d3-time-format's syntax %{variable|d3-time-format}, for example \"Day: %{2019-01-01|%A}\". https://github.com/d3/d3-time-format/tree/v2.2.3#locale_format for details on the date formatting syntax. Variables that can't be found will be replaced with the specifier. For example, a template of \"data: %{x}, %{y}\" will result in a value of \"data: 1, %{y}\" if x is 1 and y is missing. Variables with an undefined value will be replaced with the fallback value. The variables available in `hovertemplate` are the ones emitted as event data described at this link https://plotly.com/javascript/plotlyjs-events/#event-data. Additionally, all attributes that can be specified per-point (the ones that are `arrayOk: true`) are available.  Finally, the template string has access to variables `value` and `label`. Anything contained in tag `<extra>` is displayed in the secondary box, for example `<extra>%{fullData.name}</extra>`. To hide the secondary box completely, use an empty tag `<extra></extra>`."
    hovertemplatefallback: Any
    "Fallback string that's displayed when a variable referenced in a template is missing. If the boolean value 'false' is passed in, the specifier with the missing variable will be displayed."
    label: Any
    "The shown name of the link."
    @property
    def line(self) -> _plotly_graph_objs_sankey_link.Line | Any:
        ...
    @line.setter
    def line(self, value: Any) -> None: ...
    sort: Any
    "For `auto` (the default), the order of links attached to each node is determined automatically by the layout. For `input`, the order of links at each node is kept the same as the order in the input array."
    source: Any
    "An integer number `[0..nodes.length - 1]` that represents the source node."
    target: Any
    "An integer number `[0..nodes.length - 1]` that represents the target node."
    value: Any
    "A numeric value representing the flow volume value."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        arrowlen: Any = ...,
        color: Any = ...,
        concentrationscales: Any = ...,
        customdata: Any = ...,
        hovercolor: Any = ...,
        hoverinfo: Any = ...,
        hoverlabel: Any = ...,
        hovertemplate: Any = ...,
        hovertemplatefallback: Any = ...,
        label: Any = ...,
        line: Any = ...,
        sort: Any = ...,
        source: Any = ...,
        target: Any = ...,
        value: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Link' object\n\nArgs:\n    arrowlen: Sets the length (in px) of the links arrow, if 0 no arrow will be drawn.\n    color: Sets the `link` color. It can be a single value, or an array for specifying color for each `link`. If `link.color` is omitted, then by default, a translucent grey link will be used.\n    customdata: Assigns extra data to each link.\n    hovercolor: Sets the `link` hover color. It can be a single value, or an array for specifying hover colors for each `link`. If `link.hovercolor` is omitted, then by default, links will become slightly more opaque when hovered over.\n    hoverinfo: Determines what trace information appears when hovering links. If `none` or `skip` are set, no information is displayed upon hovering. But, if `none` is set, click and hover events are still fired.\n    hovertemplate: Template string used for rendering the information that appear on hover box. Note that this will override `hoverinfo`. Variables are inserted using %{variable}, for example \"y: %{y}\" as well as %{xother}, {%_xother}, {%_xother_}, {%xother_}. When showing info for several points, *xother* will be added to those with different x positions from the first point. An underscore before or after *(x|y)other* will add a space on that side, only when this field is shown. Numbers are formatted using d3-format's syntax %{variable:d3-format}, for example \"Price: %{y:$.2f}\". https://github.com/d3/d3-format/tree/v1.4.5#d3-format for details on the formatting syntax. Dates are formatted using d3-time-format's syntax %{variable|d3-time-format}, for example \"Day: %{2019-01-01|%A}\". https://github.com/d3/d3-time-format/tree/v2.2.3#locale_format for details on the date formatting syntax. Variables that can't be found will be replaced with the specifier. For example, a template of \"data: %{x}, %{y}\" will result in a value of \"data: 1, %{y}\" if x is 1 and y is missing. Variables with an undefined value will be replaced with the fallback value. The variables available in `hovertemplate` are the ones emitted as event data described at this link https://plotly.com/javascript/plotlyjs-events/#event-data. Additionally, all attributes that can be specified per-point (the ones that are `arrayOk: true`) are available.  Finally, the template string has access to variables `value` and `label`. Anything contained in tag `<extra>` is displayed in the secondary box, for example `<extra>%{fullData.name}</extra>`. To hide the secondary box completely, use an empty tag `<extra></extra>`.\n    hovertemplatefallback: Fallback string that's displayed when a variable referenced in a template is missing. If the boolean value 'false' is passed in, the specifier with the missing variable will be displayed.\n    label: The shown name of the link.\n    sort: For `auto` (the default), the order of links attached to each node is determined automatically by the layout. For `input`, the order of links at each node is kept the same as the order in the input array.\n    source: An integer number `[0..nodes.length - 1]` that represents the source node.\n    target: An integer number `[0..nodes.length - 1]` that represents the target node.\n    value: A numeric value representing the flow volume value."
        ...

class Node(_PlotlyObject):
    "Create a new 'Node' object"
    align: Any
    "Sets the alignment method used to position the nodes along the horizontal axis."
    color: Any
    "Sets the `node` color. It can be a single value, or an array for specifying color for each `node`. If `node.color` is omitted, then the default `Plotly` color palette will be cycled through to have a variety of colors. These defaults are not fully opaque, to allow some visibility of what is beneath the node."
    customdata: Any
    "Assigns extra data to each node."
    groups: Any
    "Groups of nodes. Each group is defined by an array with the indices of the nodes it contains. Multiple groups can be specified."
    hoverinfo: Any
    "Determines what trace information appears when hovering nodes. If `none` or `skip` are set, no information is displayed upon hovering. But, if `none` is set, click and hover events are still fired."
    @property
    def hoverlabel(self) -> _plotly_graph_objs_sankey_node.Hoverlabel | Any:
        ...
    @hoverlabel.setter
    def hoverlabel(self, value: Any) -> None: ...
    hovertemplate: str | Any
    "Template string used for rendering the information that appear on hover box. Note that this will override `hoverinfo`. Variables are inserted using %{variable}, for example \"y: %{y}\" as well as %{xother}, {%_xother}, {%_xother_}, {%xother_}. When showing info for several points, *xother* will be added to those with different x positions from the first point. An underscore before or after *(x|y)other* will add a space on that side, only when this field is shown. Numbers are formatted using d3-format's syntax %{variable:d3-format}, for example \"Price: %{y:$.2f}\". https://github.com/d3/d3-format/tree/v1.4.5#d3-format for details on the formatting syntax. Dates are formatted using d3-time-format's syntax %{variable|d3-time-format}, for example \"Day: %{2019-01-01|%A}\". https://github.com/d3/d3-time-format/tree/v2.2.3#locale_format for details on the date formatting syntax. Variables that can't be found will be replaced with the specifier. For example, a template of \"data: %{x}, %{y}\" will result in a value of \"data: 1, %{y}\" if x is 1 and y is missing. Variables with an undefined value will be replaced with the fallback value. The variables available in `hovertemplate` are the ones emitted as event data described at this link https://plotly.com/javascript/plotlyjs-events/#event-data. Additionally, all attributes that can be specified per-point (the ones that are `arrayOk: true`) are available.  Finally, the template string has access to variables `value` and `label`. Anything contained in tag `<extra>` is displayed in the secondary box, for example `<extra>%{fullData.name}</extra>`. To hide the secondary box completely, use an empty tag `<extra></extra>`."
    hovertemplatefallback: Any
    "Fallback string that's displayed when a variable referenced in a template is missing. If the boolean value 'false' is passed in, the specifier with the missing variable will be displayed."
    label: Any
    "The shown name of the node."
    @property
    def line(self) -> _plotly_graph_objs_sankey_node.Line | Any:
        ...
    @line.setter
    def line(self, value: Any) -> None: ...
    pad: float | Any
    "Sets the padding (in px) between the `nodes`."
    sort: Any
    "For `auto` (the default), the vertical order of nodes will be determined automatically by the layout. For `input`, the vertical order of nodes is kept the same as the order in the input array."
    thickness: float | Any
    "Sets the thickness (in px) of the `nodes`."
    x: Any
    "The normalized horizontal position of the node."
    y: Any
    "The normalized vertical position of the node."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        align: Any = ...,
        color: Any = ...,
        customdata: Any = ...,
        groups: Any = ...,
        hoverinfo: Any = ...,
        hoverlabel: Any = ...,
        hovertemplate: Any = ...,
        hovertemplatefallback: Any = ...,
        label: Any = ...,
        line: Any = ...,
        pad: Any = ...,
        sort: Any = ...,
        thickness: Any = ...,
        x: Any = ...,
        y: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Node' object\n\nArgs:\n    align: Sets the alignment method used to position the nodes along the horizontal axis.\n    color: Sets the `node` color. It can be a single value, or an array for specifying color for each `node`. If `node.color` is omitted, then the default `Plotly` color palette will be cycled through to have a variety of colors. These defaults are not fully opaque, to allow some visibility of what is beneath the node.\n    customdata: Assigns extra data to each node.\n    groups: Groups of nodes. Each group is defined by an array with the indices of the nodes it contains. Multiple groups can be specified.\n    hoverinfo: Determines what trace information appears when hovering nodes. If `none` or `skip` are set, no information is displayed upon hovering. But, if `none` is set, click and hover events are still fired.\n    hovertemplate: Template string used for rendering the information that appear on hover box. Note that this will override `hoverinfo`. Variables are inserted using %{variable}, for example \"y: %{y}\" as well as %{xother}, {%_xother}, {%_xother_}, {%xother_}. When showing info for several points, *xother* will be added to those with different x positions from the first point. An underscore before or after *(x|y)other* will add a space on that side, only when this field is shown. Numbers are formatted using d3-format's syntax %{variable:d3-format}, for example \"Price: %{y:$.2f}\". https://github.com/d3/d3-format/tree/v1.4.5#d3-format for details on the formatting syntax. Dates are formatted using d3-time-format's syntax %{variable|d3-time-format}, for example \"Day: %{2019-01-01|%A}\". https://github.com/d3/d3-time-format/tree/v2.2.3#locale_format for details on the date formatting syntax. Variables that can't be found will be replaced with the specifier. For example, a template of \"data: %{x}, %{y}\" will result in a value of \"data: 1, %{y}\" if x is 1 and y is missing. Variables with an undefined value will be replaced with the fallback value. The variables available in `hovertemplate` are the ones emitted as event data described at this link https://plotly.com/javascript/plotlyjs-events/#event-data. Additionally, all attributes that can be specified per-point (the ones that are `arrayOk: true`) are available.  Finally, the template string has access to variables `value` and `label`. Anything contained in tag `<extra>` is displayed in the secondary box, for example `<extra>%{fullData.name}</extra>`. To hide the secondary box completely, use an empty tag `<extra></extra>`.\n    hovertemplatefallback: Fallback string that's displayed when a variable referenced in a template is missing. If the boolean value 'false' is passed in, the specifier with the missing variable will be displayed.\n    label: The shown name of the node.\n    pad: Sets the padding (in px) between the `nodes`.\n    sort: For `auto` (the default), the vertical order of nodes will be determined automatically by the layout. For `input`, the vertical order of nodes is kept the same as the order in the input array.\n    thickness: Sets the thickness (in px) of the `nodes`.\n    x: The normalized horizontal position of the node.\n    y: The normalized vertical position of the node."
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
