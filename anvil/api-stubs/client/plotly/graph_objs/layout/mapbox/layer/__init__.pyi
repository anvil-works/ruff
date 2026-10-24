# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the Plotly catalogue generator in doc/anvil-api-stubs/plotly-stubs.mjs instead, then run:
#   pnpm -F docs build
#
from plotly._base import _PlotlyObject
from typing import Any, Mapping
import plotly.graph_objs.layout.mapbox.layer.symbol as _plotly_graph_objs_layout_mapbox_layer_symbol
import plotly.graph_objs.layout.mapbox.layer.symbol as symbol

class Circle(_PlotlyObject):
    "Create a new 'Circle' object"
    radius: float | Any
    "Sets the circle radius (mapbox.layer.paint.circle-radius). Has an effect only when `type` is set to *circle*."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        radius: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Circle' object\n\nArgs:\n    radius: Sets the circle radius (mapbox.layer.paint.circle-radius). Has an effect only when `type` is set to *circle*."
        ...

class Fill(_PlotlyObject):
    "Create a new 'Fill' object"
    outlinecolor: Any
    "Sets the fill outline color (mapbox.layer.paint.fill-outline-color). Has an effect only when `type` is set to *fill*."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        outlinecolor: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Fill' object\n\nArgs:\n    outlinecolor: Sets the fill outline color (mapbox.layer.paint.fill-outline-color). Has an effect only when `type` is set to *fill*."
        ...

class Line(_PlotlyObject):
    "Create a new 'Line' object"
    dash: Any
    "Sets the length of dashes and gaps (mapbox.layer.paint.line-dasharray). Has an effect only when `type` is set to *line*."
    dashsrc: str | Any
    "Sets the source reference on Chart Studio Cloud for `dash`."
    width: float | Any
    "Sets the line width (mapbox.layer.paint.line-width). Has an effect only when `type` is set to *line*."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        dash: Any = ...,
        dashsrc: Any = ...,
        width: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Line' object\n\nArgs:\n    dash: Sets the length of dashes and gaps (mapbox.layer.paint.line-dasharray). Has an effect only when `type` is set to *line*.\n    dashsrc: Sets the source reference on Chart Studio Cloud for `dash`.\n    width: Sets the line width (mapbox.layer.paint.line-width). Has an effect only when `type` is set to *line*."
        ...

class Symbol(_PlotlyObject):
    "Create a new 'Symbol' object"
    icon: str | Any
    "Sets the symbol icon image (mapbox.layer.layout.icon-image). Full list: https://www.mapbox.com/maki-icons/"
    iconsize: float | Any
    "Sets the symbol icon size (mapbox.layer.layout.icon-size). Has an effect only when `type` is set to *symbol*."
    placement: Any
    "Sets the symbol and/or text placement (mapbox.layer.layout.symbol-placement). If `placement` is *point*, the label is placed where the geometry is located If `placement` is *line*, the label is placed along the line of the geometry If `placement` is *line-center*, the label is placed on the center of the geometry"
    text: str | Any
    "Sets the symbol text (mapbox.layer.layout.text-field)."
    @property
    def textfont(self) -> _plotly_graph_objs_layout_mapbox_layer_symbol.Textfont | Any:
        "Sets the icon text font (color=mapbox.layer.paint.text-color, size=mapbox.layer.layout.text-size). Has an effect only when `type` is set to *symbol*."
        ...
    @textfont.setter
    def textfont(self, value: Any) -> None: ...
    textposition: Any
    "Sets the positions of the `text` elements with respects to the (x,y) coordinates."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        icon: Any = ...,
        iconsize: Any = ...,
        placement: Any = ...,
        text: Any = ...,
        textfont: Any = ...,
        textposition: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Symbol' object\n\nArgs:\n    icon: Sets the symbol icon image (mapbox.layer.layout.icon-image). Full list: https://www.mapbox.com/maki-icons/\n    iconsize: Sets the symbol icon size (mapbox.layer.layout.icon-size). Has an effect only when `type` is set to *symbol*.\n    placement: Sets the symbol and/or text placement (mapbox.layer.layout.symbol-placement). If `placement` is *point*, the label is placed where the geometry is located If `placement` is *line*, the label is placed along the line of the geometry If `placement` is *line-center*, the label is placed on the center of the geometry\n    text: Sets the symbol text (mapbox.layer.layout.text-field).\n    textfont: Sets the icon text font (color=mapbox.layer.paint.text-color, size=mapbox.layer.layout.text-size). Has an effect only when `type` is set to *symbol*.\n    textposition: Sets the positions of the `text` elements with respects to the (x,y) coordinates."
        ...
