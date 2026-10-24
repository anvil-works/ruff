# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the Plotly catalogue generator in doc/anvil-api-stubs/plotly-stubs.mjs instead, then run:
#   pnpm -F docs build
#
from plotly._base import _PlotlyObject
from typing import Any, Mapping

class Button(_PlotlyObject):
    "Create a new 'Button' object"
    args: Any
    "Sets the arguments values to be passed to the Plotly method set in `method` on click."
    args2: Any
    "Sets a 2nd set of `args`, these arguments values are passed to the Plotly method set in `method` when clicking this button while in the active state. Use this to create toggle buttons."
    execute: bool | Any
    "When true, the API method is executed. When false, all other behaviors are the same and command execution is skipped. This may be useful when hooking into, for example, the `plotly_buttonclicked` method and executing the API command manually without losing the benefit of the updatemenu automatically binding to the state of the plot through the specification of `method` and `args`."
    label: str | Any
    "Sets the text label to appear on the button."
    method: Any
    "Sets the Plotly method to be called on click. If the `skip` method is used, the API updatemenu will function as normal but will perform no API calls and will not bind automatically to state updates. This may be used to create a component interface and attach to updatemenu events manually via JavaScript."
    name: str | Any
    "When used in a template, named items are created in the output figure in addition to any items the figure already has in this array. You can modify these items in the output figure by making your own item with `templateitemname` matching this `name` alongside your modifications (including `visible: false` or `enabled: false` to hide it). Has no effect outside of a template."
    templateitemname: str | Any
    "Used to refer to a named item in this array in the template. Named items from the template will be created even without a matching item in the input figure, but you can modify one by making an item with `templateitemname` matching its `name`, alongside your modifications (including `visible: false` or `enabled: false` to hide it). If there is no template or no matching item, this item will be hidden unless you explicitly show it with `visible: true`."
    visible: bool | Any
    "Determines whether or not this button is visible."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        args: Any = ...,
        args2: Any = ...,
        execute: Any = ...,
        label: Any = ...,
        method: Any = ...,
        name: Any = ...,
        templateitemname: Any = ...,
        visible: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Button' object\n\nArgs:\n    args: Sets the arguments values to be passed to the Plotly method set in `method` on click.\n    args2: Sets a 2nd set of `args`, these arguments values are passed to the Plotly method set in `method` when clicking this button while in the active state. Use this to create toggle buttons.\n    execute: When true, the API method is executed. When false, all other behaviors are the same and command execution is skipped. This may be useful when hooking into, for example, the `plotly_buttonclicked` method and executing the API command manually without losing the benefit of the updatemenu automatically binding to the state of the plot through the specification of `method` and `args`.\n    label: Sets the text label to appear on the button.\n    method: Sets the Plotly method to be called on click. If the `skip` method is used, the API updatemenu will function as normal but will perform no API calls and will not bind automatically to state updates. This may be used to create a component interface and attach to updatemenu events manually via JavaScript.\n    name: When used in a template, named items are created in the output figure in addition to any items the figure already has in this array. You can modify these items in the output figure by making your own item with `templateitemname` matching this `name` alongside your modifications (including `visible: false` or `enabled: false` to hide it). Has no effect outside of a template.\n    templateitemname: Used to refer to a named item in this array in the template. Named items from the template will be created even without a matching item in the input figure, but you can modify one by making an item with `templateitemname` matching its `name`, alongside your modifications (including `visible: false` or `enabled: false` to hide it). If there is no template or no matching item, this item will be hidden unless you explicitly show it with `visible: true`.\n    visible: Determines whether or not this button is visible."
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
