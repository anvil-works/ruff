# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the Plotly catalogue generator in doc/anvil-api-stubs/plotly-stubs.mjs instead, then run:
#   pnpm -F docs build
#
from plotly._base import _PlotlyObject
from typing import Any, Mapping
import plotly.graph_objs.scattercarpet.marker.colorbar.title as _plotly_graph_objs_scattercarpet_marker_colorbar_title
import plotly.graph_objs.scattercarpet.marker.colorbar.title as title

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
    def font(self) -> _plotly_graph_objs_scattercarpet_marker_colorbar_title.Font | Any:
        "Sets this color bar's title font."
        ...
    @font.setter
    def font(self, value: Any) -> None: ...
    side: Any
    "Determines the location of color bar's title with respect to the color bar. Defaults to *top* when `orientation` is *v* and defaults to *right* when `orientation` is *h*."
    text: str | Any
    "Sets the title of the color bar."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        font: Any = ...,
        side: Any = ...,
        text: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Title' object\n\nArgs:\n    font: Sets this color bar's title font.\n    side: Determines the location of color bar's title with respect to the color bar. Defaults to *top* when `orientation` is *v* and defaults to *right* when `orientation` is *h*.\n    text: Sets the title of the color bar."
        ...
