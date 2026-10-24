# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the Plotly catalogue generator in doc/anvil-api-stubs/plotly-stubs.mjs instead, then run:
#   pnpm -F docs build
#
from plotly._base import _PlotlyObject
from typing import Any, Mapping
import plotly.graph_objs.layout.title.subtitle as _plotly_graph_objs_layout_title_subtitle
import plotly.graph_objs.layout.title.subtitle as subtitle

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

class Pad(_PlotlyObject):
    "Create a new 'Pad' object"
    b: float | Any
    "The amount of padding (in px) along the bottom of the component."
    l: float | Any
    "The amount of padding (in px) on the left side of the component."
    r: float | Any
    "The amount of padding (in px) on the right side of the component."
    t: float | Any
    "The amount of padding (in px) along the top of the component."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        b: Any = ...,
        l: Any = ...,
        r: Any = ...,
        t: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Pad' object\n\nArgs:\n    b: The amount of padding (in px) along the bottom of the component.\n    l: The amount of padding (in px) on the left side of the component.\n    r: The amount of padding (in px) on the right side of the component.\n    t: The amount of padding (in px) along the top of the component."
        ...

class Subtitle(_PlotlyObject):
    "Create a new 'Subtitle' object"
    @property
    def font(self) -> _plotly_graph_objs_layout_title_subtitle.Font | Any:
        "Sets the subtitle font."
        ...
    @font.setter
    def font(self, value: Any) -> None: ...
    text: str | Any
    "Sets the plot's subtitle."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        font: Any = ...,
        text: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Subtitle' object\n\nArgs:\n    font: Sets the subtitle font.\n    text: Sets the plot's subtitle."
        ...
