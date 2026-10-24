# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the Plotly catalogue generator in doc/anvil-api-stubs/plotly-stubs.mjs instead, then run:
#   pnpm -F docs build
#
from plotly._base import _PlotlyObject
from typing import Any, Mapping
import plotly.graph_objs.layout.geo.projection as _plotly_graph_objs_layout_geo_projection
import plotly.graph_objs.layout.geo.projection as projection

class Center(_PlotlyObject):
    "Create a new 'Center' object"
    lat: float | Any
    "Sets the latitude of the map's center. For all projection types, the map's latitude center lies at the middle of the latitude range by default."
    lon: float | Any
    "Sets the longitude of the map's center. By default, the map's longitude center lies at the middle of the longitude range for scoped projection and above `projection.rotation.lon` otherwise."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        lat: Any = ...,
        lon: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Center' object\n\nArgs:\n    lat: Sets the latitude of the map's center. For all projection types, the map's latitude center lies at the middle of the latitude range by default.\n    lon: Sets the longitude of the map's center. By default, the map's longitude center lies at the middle of the longitude range for scoped projection and above `projection.rotation.lon` otherwise."
        ...

class Domain(_PlotlyObject):
    "Create a new 'Domain' object"
    column: int | Any
    "If there is a layout grid, use the domain for this column in the grid for this geo subplot. Note that geo subplots are constrained by domain. In general, when `projection.scale` is set to 1. a map will fit either its x or y domain, but not both."
    row: int | Any
    "If there is a layout grid, use the domain for this row in the grid for this geo subplot. Note that geo subplots are constrained by domain. In general, when `projection.scale` is set to 1. a map will fit either its x or y domain, but not both."
    x: Any
    "Sets the horizontal domain of this geo subplot (in plot fraction). Note that geo subplots are constrained by domain. In general, when `projection.scale` is set to 1. a map will fit either its x or y domain, but not both."
    y: Any
    "Sets the vertical domain of this geo subplot (in plot fraction). Note that geo subplots are constrained by domain. In general, when `projection.scale` is set to 1. a map will fit either its x or y domain, but not both."
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
        "Create a new 'Domain' object\n\nArgs:\n    column: If there is a layout grid, use the domain for this column in the grid for this geo subplot. Note that geo subplots are constrained by domain. In general, when `projection.scale` is set to 1. a map will fit either its x or y domain, but not both.\n    row: If there is a layout grid, use the domain for this row in the grid for this geo subplot. Note that geo subplots are constrained by domain. In general, when `projection.scale` is set to 1. a map will fit either its x or y domain, but not both.\n    x: Sets the horizontal domain of this geo subplot (in plot fraction). Note that geo subplots are constrained by domain. In general, when `projection.scale` is set to 1. a map will fit either its x or y domain, but not both.\n    y: Sets the vertical domain of this geo subplot (in plot fraction). Note that geo subplots are constrained by domain. In general, when `projection.scale` is set to 1. a map will fit either its x or y domain, but not both."
        ...

class Lataxis(_PlotlyObject):
    "Create a new 'Lataxis' object"
    dtick: float | Any
    "Sets the graticule's longitude/latitude tick step."
    gridcolor: Any
    "Sets the graticule's stroke color."
    griddash: str | Any
    "Sets the dash style of lines. Set to a dash type string (*solid*, *dot*, *dash*, *longdash*, *dashdot*, or *longdashdot*) or a dash length list in px (eg *5px,10px,2px,2px*)."
    gridwidth: float | Any
    "Sets the graticule's stroke width (in px)."
    range: Any
    "Sets the range of this axis (in degrees), sets the map's clipped coordinates."
    showgrid: bool | Any
    "Sets whether or not graticule are shown on the map."
    tick0: float | Any
    "Sets the graticule's starting tick longitude/latitude."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        dtick: Any = ...,
        gridcolor: Any = ...,
        griddash: Any = ...,
        gridwidth: Any = ...,
        range: Any = ...,
        showgrid: Any = ...,
        tick0: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Lataxis' object\n\nArgs:\n    dtick: Sets the graticule's longitude/latitude tick step.\n    gridcolor: Sets the graticule's stroke color.\n    griddash: Sets the dash style of lines. Set to a dash type string (*solid*, *dot*, *dash*, *longdash*, *dashdot*, or *longdashdot*) or a dash length list in px (eg *5px,10px,2px,2px*).\n    gridwidth: Sets the graticule's stroke width (in px).\n    range: Sets the range of this axis (in degrees), sets the map's clipped coordinates.\n    showgrid: Sets whether or not graticule are shown on the map.\n    tick0: Sets the graticule's starting tick longitude/latitude."
        ...

class Lonaxis(_PlotlyObject):
    "Create a new 'Lonaxis' object"
    dtick: float | Any
    "Sets the graticule's longitude/latitude tick step."
    gridcolor: Any
    "Sets the graticule's stroke color."
    griddash: str | Any
    "Sets the dash style of lines. Set to a dash type string (*solid*, *dot*, *dash*, *longdash*, *dashdot*, or *longdashdot*) or a dash length list in px (eg *5px,10px,2px,2px*)."
    gridwidth: float | Any
    "Sets the graticule's stroke width (in px)."
    range: Any
    "Sets the range of this axis (in degrees), sets the map's clipped coordinates."
    showgrid: bool | Any
    "Sets whether or not graticule are shown on the map."
    tick0: float | Any
    "Sets the graticule's starting tick longitude/latitude."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        dtick: Any = ...,
        gridcolor: Any = ...,
        griddash: Any = ...,
        gridwidth: Any = ...,
        range: Any = ...,
        showgrid: Any = ...,
        tick0: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Lonaxis' object\n\nArgs:\n    dtick: Sets the graticule's longitude/latitude tick step.\n    gridcolor: Sets the graticule's stroke color.\n    griddash: Sets the dash style of lines. Set to a dash type string (*solid*, *dot*, *dash*, *longdash*, *dashdot*, or *longdashdot*) or a dash length list in px (eg *5px,10px,2px,2px*).\n    gridwidth: Sets the graticule's stroke width (in px).\n    range: Sets the range of this axis (in degrees), sets the map's clipped coordinates.\n    showgrid: Sets whether or not graticule are shown on the map.\n    tick0: Sets the graticule's starting tick longitude/latitude."
        ...

class Projection(_PlotlyObject):
    "Create a new 'Projection' object"
    distance: float | Any
    "For satellite projection type only. Sets the distance from the center of the sphere to the point of view as a proportion of the sphere’s radius."
    maxscale: float | Any
    "Sets the maximum zoom level of the map view, relative to `projection.scale`. A `maxscale` of *2* (200%) prevents the user from zooming in beyond twice the base zoom level. Must be greater than or equal to *0*; has no upper bound. Defaults to *null* for no upper bound on zoom."
    minscale: float | Any
    "Sets the minimum zoom level of the map view, relative to `projection.scale`. A `minscale` of *0.5* (50%) prevents the user from zooming out beyond half the base zoom level. Must be greater than or equal to *0*; has no upper bound. The default of *0* imposes no lower bound on zoom."
    parallels: Any
    "For conic projection types only. Sets the parallels (tangent, secant) where the cone intersects the sphere."
    @property
    def rotation(self) -> _plotly_graph_objs_layout_geo_projection.Rotation | Any:
        ...
    @rotation.setter
    def rotation(self, value: Any) -> None: ...
    scale: float | Any
    "Zooms in or out on the map view. A scale of *1* corresponds to the largest zoom level that fits the map's lon and lat ranges. "
    tilt: float | Any
    "For satellite projection type only. Sets the tilt angle of perspective projection."
    type: Any
    "Sets the projection type."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        distance: Any = ...,
        maxscale: Any = ...,
        minscale: Any = ...,
        parallels: Any = ...,
        rotation: Any = ...,
        scale: Any = ...,
        tilt: Any = ...,
        type: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Projection' object\n\nArgs:\n    distance: For satellite projection type only. Sets the distance from the center of the sphere to the point of view as a proportion of the sphere’s radius.\n    maxscale: Sets the maximum zoom level of the map view, relative to `projection.scale`. A `maxscale` of *2* (200%) prevents the user from zooming in beyond twice the base zoom level. Must be greater than or equal to *0*; has no upper bound. Defaults to *null* for no upper bound on zoom.\n    minscale: Sets the minimum zoom level of the map view, relative to `projection.scale`. A `minscale` of *0.5* (50%) prevents the user from zooming out beyond half the base zoom level. Must be greater than or equal to *0*; has no upper bound. The default of *0* imposes no lower bound on zoom.\n    parallels: For conic projection types only. Sets the parallels (tangent, secant) where the cone intersects the sphere.\n    scale: Zooms in or out on the map view. A scale of *1* corresponds to the largest zoom level that fits the map's lon and lat ranges. \n    tilt: For satellite projection type only. Sets the tilt angle of perspective projection.\n    type: Sets the projection type."
        ...
