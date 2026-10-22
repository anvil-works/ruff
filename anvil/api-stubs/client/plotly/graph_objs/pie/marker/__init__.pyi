# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the Plotly catalogue generator in doc/anvil-api-stubs/plotly-stubs.mjs instead, then run:
#   pnpm -F docs build
#
from plotly._base import _PlotlyObject
from typing import Any, Mapping

class Line(_PlotlyObject):
    "Create a new 'Line' object"
    color: Any
    "Sets the color of the line enclosing each sector."
    width: float | Any
    "Sets the width (in px) of the line enclosing each sector."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        color: Any = ...,
        width: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Line' object\n\nArgs:\n    color: Sets the color of the line enclosing each sector.\n    width: Sets the width (in px) of the line enclosing each sector."
        ...

class Pattern(_PlotlyObject):
    "Create a new 'Pattern' object"
    bgcolor: Any
    "When there is no colorscale sets the color of background pattern fill. Defaults to a `marker.color` background when `fillmode` is *overlay*. Otherwise, defaults to a transparent background."
    fgcolor: Any
    "When there is no colorscale sets the color of foreground pattern fill. Defaults to a `marker.color` background when `fillmode` is *replace*. Otherwise, defaults to dark grey or white to increase contrast with the `bgcolor`."
    fgopacity: float | Any
    "Sets the opacity of the foreground pattern fill. Defaults to a 0.5 when `fillmode` is *overlay*. Otherwise, defaults to 1."
    fillmode: Any
    "Determines whether `marker.color` should be used as a default to `bgcolor` or a `fgcolor`."
    path: str | Any
    "Sets a custom path for pattern fill. Use with no `shape` or `solidity`, provide an SVG path string for the regions of the square from (0,0) to (`size`,`size`) to color."
    shape: Any
    "Sets the shape of the pattern fill. By default, no pattern is used for filling the area."
    size: float | Any
    "Sets the size of unit squares of the pattern fill in pixels, which corresponds to the interval of repetition of the pattern."
    solidity: float | Any
    "Sets the solidity of the pattern fill. Solidity is roughly the fraction of the area filled by the pattern. Solidity of 0 shows only the background color without pattern and solidty of 1 shows only the foreground color without pattern."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        bgcolor: Any = ...,
        fgcolor: Any = ...,
        fgopacity: Any = ...,
        fillmode: Any = ...,
        path: Any = ...,
        shape: Any = ...,
        size: Any = ...,
        solidity: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Pattern' object\n\nArgs:\n    bgcolor: When there is no colorscale sets the color of background pattern fill. Defaults to a `marker.color` background when `fillmode` is *overlay*. Otherwise, defaults to a transparent background.\n    fgcolor: When there is no colorscale sets the color of foreground pattern fill. Defaults to a `marker.color` background when `fillmode` is *replace*. Otherwise, defaults to dark grey or white to increase contrast with the `bgcolor`.\n    fgopacity: Sets the opacity of the foreground pattern fill. Defaults to a 0.5 when `fillmode` is *overlay*. Otherwise, defaults to 1.\n    fillmode: Determines whether `marker.color` should be used as a default to `bgcolor` or a `fgcolor`.\n    path: Sets a custom path for pattern fill. Use with no `shape` or `solidity`, provide an SVG path string for the regions of the square from (0,0) to (`size`,`size`) to color.\n    shape: Sets the shape of the pattern fill. By default, no pattern is used for filling the area.\n    size: Sets the size of unit squares of the pattern fill in pixels, which corresponds to the interval of repetition of the pattern.\n    solidity: Sets the solidity of the pattern fill. Solidity is roughly the fraction of the area filled by the pattern. Solidity of 0 shows only the background color without pattern and solidty of 1 shows only the foreground color without pattern."
        ...
