# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the Plotly catalogue generator in doc/anvil-api-stubs/plotly-stubs.mjs instead, then run:
#   pnpm -F docs build
#
from plotly._base import _PlotlyObject
from typing import Any, Mapping

class Font(_PlotlyObject):
    "Create a new 'Font' object"
    color: Any
    colorsrc: str | Any
    "Sets the source reference on Chart Studio Cloud for `color`."
    family: str | Any
    "HTML font family - the typeface that will be applied by the web browser. The web browser will only be able to apply a font if it is available on the system which it operates. Provide multiple font families, separated by commas, to indicate the preference in which to apply fonts if they aren't available on the system. The Chart Studio Cloud (at https://chart-studio.plotly.com or on-premise) generates images on a server, where only a select number of fonts are installed and supported. These include *Arial*, *Balto*, *Courier New*, *Droid Sans*, *Droid Serif*, *Droid Sans Mono*, *Gravitas One*, *Old Standard TT*, *Open Sans*, *Overpass*, *PT Sans Narrow*, *Raleway*, *Times New Roman*."
    familysrc: str | Any
    "Sets the source reference on Chart Studio Cloud for `family`."
    lineposition: str | Any
    "Sets the kind of decoration line(s) with text, such as an *under*, *over* or *through* as well as combinations e.g. *under+over*, etc."
    linepositionsrc: str | Any
    "Sets the source reference on Chart Studio Cloud for `lineposition`."
    shadow: str | Any
    "Sets the shape and color of the shadow behind text. *auto* places minimal shadow and applies contrast text font color. See https://developer.mozilla.org/en-US/docs/Web/CSS/text-shadow for additional options."
    shadowsrc: str | Any
    "Sets the source reference on Chart Studio Cloud for `shadow`."
    size: float | Any
    sizesrc: str | Any
    "Sets the source reference on Chart Studio Cloud for `size`."
    style: Any
    "Sets whether a font should be styled with a normal or italic face from its family."
    stylesrc: str | Any
    "Sets the source reference on Chart Studio Cloud for `style`."
    textcase: Any
    "Sets capitalization of text. It can be used to make text appear in all-uppercase or all-lowercase, or with each word capitalized."
    textcasesrc: str | Any
    "Sets the source reference on Chart Studio Cloud for `textcase`."
    variant: Any
    "Sets the variant of the font."
    variantsrc: str | Any
    "Sets the source reference on Chart Studio Cloud for `variant`."
    weight: int | Any
    "Sets the weight (or boldness) of the font."
    weightsrc: str | Any
    "Sets the source reference on Chart Studio Cloud for `weight`."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        color: Any = ...,
        colorsrc: Any = ...,
        family: Any = ...,
        familysrc: Any = ...,
        lineposition: Any = ...,
        linepositionsrc: Any = ...,
        shadow: Any = ...,
        shadowsrc: Any = ...,
        size: Any = ...,
        sizesrc: Any = ...,
        style: Any = ...,
        stylesrc: Any = ...,
        textcase: Any = ...,
        textcasesrc: Any = ...,
        variant: Any = ...,
        variantsrc: Any = ...,
        weight: Any = ...,
        weightsrc: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Font' object\n\nArgs:\n    colorsrc: Sets the source reference on Chart Studio Cloud for `color`.\n    family: HTML font family - the typeface that will be applied by the web browser. The web browser will only be able to apply a font if it is available on the system which it operates. Provide multiple font families, separated by commas, to indicate the preference in which to apply fonts if they aren't available on the system. The Chart Studio Cloud (at https://chart-studio.plotly.com or on-premise) generates images on a server, where only a select number of fonts are installed and supported. These include *Arial*, *Balto*, *Courier New*, *Droid Sans*, *Droid Serif*, *Droid Sans Mono*, *Gravitas One*, *Old Standard TT*, *Open Sans*, *Overpass*, *PT Sans Narrow*, *Raleway*, *Times New Roman*.\n    familysrc: Sets the source reference on Chart Studio Cloud for `family`.\n    lineposition: Sets the kind of decoration line(s) with text, such as an *under*, *over* or *through* as well as combinations e.g. *under+over*, etc.\n    linepositionsrc: Sets the source reference on Chart Studio Cloud for `lineposition`.\n    shadow: Sets the shape and color of the shadow behind text. *auto* places minimal shadow and applies contrast text font color. See https://developer.mozilla.org/en-US/docs/Web/CSS/text-shadow for additional options.\n    shadowsrc: Sets the source reference on Chart Studio Cloud for `shadow`.\n    sizesrc: Sets the source reference on Chart Studio Cloud for `size`.\n    style: Sets whether a font should be styled with a normal or italic face from its family.\n    stylesrc: Sets the source reference on Chart Studio Cloud for `style`.\n    textcase: Sets capitalization of text. It can be used to make text appear in all-uppercase or all-lowercase, or with each word capitalized.\n    textcasesrc: Sets the source reference on Chart Studio Cloud for `textcase`.\n    variant: Sets the variant of the font.\n    variantsrc: Sets the source reference on Chart Studio Cloud for `variant`.\n    weight: Sets the weight (or boldness) of the font.\n    weightsrc: Sets the source reference on Chart Studio Cloud for `weight`."
        ...
