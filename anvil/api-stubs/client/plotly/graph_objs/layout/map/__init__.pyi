# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the Plotly catalogue generator in doc/anvil-api-stubs/plotly-stubs.mjs instead, then run:
#   pnpm -F docs build
#
from plotly._base import _PlotlyObject
from typing import Any, Mapping
import plotly.graph_objs.layout.map.layer as _plotly_graph_objs_layout_map_layer
import plotly.graph_objs.layout.map.layer as layer

class Bounds(_PlotlyObject):
    "Create a new 'Bounds' object"
    east: float | Any
    "Sets the maximum longitude of the map (in degrees East) if `west`, `south` and `north` are declared."
    north: float | Any
    "Sets the maximum latitude of the map (in degrees North) if `east`, `west` and `south` are declared."
    south: float | Any
    "Sets the minimum latitude of the map (in degrees North) if `east`, `west` and `north` are declared."
    west: float | Any
    "Sets the minimum longitude of the map (in degrees East) if `east`, `south` and `north` are declared."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        east: Any = ...,
        north: Any = ...,
        south: Any = ...,
        west: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Bounds' object\n\nArgs:\n    east: Sets the maximum longitude of the map (in degrees East) if `west`, `south` and `north` are declared.\n    north: Sets the maximum latitude of the map (in degrees North) if `east`, `west` and `south` are declared.\n    south: Sets the minimum latitude of the map (in degrees North) if `east`, `west` and `north` are declared.\n    west: Sets the minimum longitude of the map (in degrees East) if `east`, `south` and `north` are declared."
        ...

class Center(_PlotlyObject):
    "Create a new 'Center' object"
    lat: float | Any
    "Sets the latitude of the center of the map (in degrees North)."
    lon: float | Any
    "Sets the longitude of the center of the map (in degrees East)."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        lat: Any = ...,
        lon: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Center' object\n\nArgs:\n    lat: Sets the latitude of the center of the map (in degrees North).\n    lon: Sets the longitude of the center of the map (in degrees East)."
        ...

class Domain(_PlotlyObject):
    "Create a new 'Domain' object"
    column: int | Any
    "If there is a layout grid, use the domain for this column in the grid for this map subplot."
    row: int | Any
    "If there is a layout grid, use the domain for this row in the grid for this map subplot."
    x: Any
    "Sets the horizontal domain of this map subplot (in plot fraction)."
    y: Any
    "Sets the vertical domain of this map subplot (in plot fraction)."
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
        "Create a new 'Domain' object\n\nArgs:\n    column: If there is a layout grid, use the domain for this column in the grid for this map subplot.\n    row: If there is a layout grid, use the domain for this row in the grid for this map subplot.\n    x: Sets the horizontal domain of this map subplot (in plot fraction).\n    y: Sets the vertical domain of this map subplot (in plot fraction)."
        ...

class Layer(_PlotlyObject):
    "Create a new 'Layer' object"
    below: str | Any
    "Determines if the layer will be inserted before the layer with the specified ID. If omitted or set to '', the layer will be inserted above every existing layer."
    @property
    def circle(self) -> _plotly_graph_objs_layout_map_layer.Circle | Any:
        ...
    @circle.setter
    def circle(self, value: Any) -> None: ...
    color: Any
    "Sets the primary layer color. If `type` is *circle*, color corresponds to the circle color (map.layer.paint.circle-color) If `type` is *line*, color corresponds to the line color (map.layer.paint.line-color) If `type` is *fill*, color corresponds to the fill color (map.layer.paint.fill-color) If `type` is *symbol*, color corresponds to the icon color (map.layer.paint.icon-color)"
    coordinates: Any
    "Sets the coordinates array contains [longitude, latitude] pairs for the image corners listed in clockwise order: top left, top right, bottom right, bottom left. Only has an effect for *image* `sourcetype`."
    @property
    def fill(self) -> _plotly_graph_objs_layout_map_layer.Fill | Any:
        ...
    @fill.setter
    def fill(self, value: Any) -> None: ...
    @property
    def line(self) -> _plotly_graph_objs_layout_map_layer.Line | Any:
        ...
    @line.setter
    def line(self, value: Any) -> None: ...
    maxzoom: float | Any
    "Sets the maximum zoom level (map.layer.maxzoom). At zoom levels equal to or greater than the maxzoom, the layer will be hidden."
    minzoom: float | Any
    "Sets the minimum zoom level (map.layer.minzoom). At zoom levels less than the minzoom, the layer will be hidden."
    name: str | Any
    "When used in a template, named items are created in the output figure in addition to any items the figure already has in this array. You can modify these items in the output figure by making your own item with `templateitemname` matching this `name` alongside your modifications (including `visible: false` or `enabled: false` to hide it). Has no effect outside of a template."
    opacity: float | Any
    "Sets the opacity of the layer. If `type` is *circle*, opacity corresponds to the circle opacity (map.layer.paint.circle-opacity) If `type` is *line*, opacity corresponds to the line opacity (map.layer.paint.line-opacity) If `type` is *fill*, opacity corresponds to the fill opacity (map.layer.paint.fill-opacity) If `type` is *symbol*, opacity corresponds to the icon/text opacity (map.layer.paint.text-opacity)"
    source: Any
    "Sets the source data for this layer (map.layer.source). When `sourcetype` is set to *geojson*, `source` can be a URL to a GeoJSON or a GeoJSON object. When `sourcetype` is set to *vector* or *raster*, `source` can be a URL or an array of tile URLs. When `sourcetype` is set to *image*, `source` can be a URL to an image."
    sourceattribution: str | Any
    "Sets the attribution for this source."
    sourcelayer: str | Any
    "Specifies the layer to use from a vector tile source (map.layer.source-layer). Required for *vector* source type that supports multiple layers."
    sourcetype: Any
    "Sets the source type for this layer, that is the type of the layer data."
    @property
    def symbol(self) -> _plotly_graph_objs_layout_map_layer.Symbol | Any:
        ...
    @symbol.setter
    def symbol(self, value: Any) -> None: ...
    templateitemname: str | Any
    "Used to refer to a named item in this array in the template. Named items from the template will be created even without a matching item in the input figure, but you can modify one by making an item with `templateitemname` matching its `name`, alongside your modifications (including `visible: false` or `enabled: false` to hide it). If there is no template or no matching item, this item will be hidden unless you explicitly show it with `visible: true`."
    type: Any
    "Sets the layer type, that is the how the layer data set in `source` will be rendered With `sourcetype` set to *geojson*, the following values are allowed: *circle*, *line*, *fill* and *symbol*. but note that *line* and *fill* are not compatible with Point GeoJSON geometries. With `sourcetype` set to *vector*, the following values are allowed:  *circle*, *line*, *fill* and *symbol*. With `sourcetype` set to *raster* or *image*, only the *raster* value is allowed."
    visible: bool | Any
    "Determines whether this layer is displayed"
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        below: Any = ...,
        circle: Any = ...,
        color: Any = ...,
        coordinates: Any = ...,
        fill: Any = ...,
        line: Any = ...,
        maxzoom: Any = ...,
        minzoom: Any = ...,
        name: Any = ...,
        opacity: Any = ...,
        source: Any = ...,
        sourceattribution: Any = ...,
        sourcelayer: Any = ...,
        sourcetype: Any = ...,
        symbol: Any = ...,
        templateitemname: Any = ...,
        type: Any = ...,
        visible: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Layer' object\n\nArgs:\n    below: Determines if the layer will be inserted before the layer with the specified ID. If omitted or set to '', the layer will be inserted above every existing layer.\n    color: Sets the primary layer color. If `type` is *circle*, color corresponds to the circle color (map.layer.paint.circle-color) If `type` is *line*, color corresponds to the line color (map.layer.paint.line-color) If `type` is *fill*, color corresponds to the fill color (map.layer.paint.fill-color) If `type` is *symbol*, color corresponds to the icon color (map.layer.paint.icon-color)\n    coordinates: Sets the coordinates array contains [longitude, latitude] pairs for the image corners listed in clockwise order: top left, top right, bottom right, bottom left. Only has an effect for *image* `sourcetype`.\n    maxzoom: Sets the maximum zoom level (map.layer.maxzoom). At zoom levels equal to or greater than the maxzoom, the layer will be hidden.\n    minzoom: Sets the minimum zoom level (map.layer.minzoom). At zoom levels less than the minzoom, the layer will be hidden.\n    name: When used in a template, named items are created in the output figure in addition to any items the figure already has in this array. You can modify these items in the output figure by making your own item with `templateitemname` matching this `name` alongside your modifications (including `visible: false` or `enabled: false` to hide it). Has no effect outside of a template.\n    opacity: Sets the opacity of the layer. If `type` is *circle*, opacity corresponds to the circle opacity (map.layer.paint.circle-opacity) If `type` is *line*, opacity corresponds to the line opacity (map.layer.paint.line-opacity) If `type` is *fill*, opacity corresponds to the fill opacity (map.layer.paint.fill-opacity) If `type` is *symbol*, opacity corresponds to the icon/text opacity (map.layer.paint.text-opacity)\n    source: Sets the source data for this layer (map.layer.source). When `sourcetype` is set to *geojson*, `source` can be a URL to a GeoJSON or a GeoJSON object. When `sourcetype` is set to *vector* or *raster*, `source` can be a URL or an array of tile URLs. When `sourcetype` is set to *image*, `source` can be a URL to an image.\n    sourceattribution: Sets the attribution for this source.\n    sourcelayer: Specifies the layer to use from a vector tile source (map.layer.source-layer). Required for *vector* source type that supports multiple layers.\n    sourcetype: Sets the source type for this layer, that is the type of the layer data.\n    templateitemname: Used to refer to a named item in this array in the template. Named items from the template will be created even without a matching item in the input figure, but you can modify one by making an item with `templateitemname` matching its `name`, alongside your modifications (including `visible: false` or `enabled: false` to hide it). If there is no template or no matching item, this item will be hidden unless you explicitly show it with `visible: true`.\n    type: Sets the layer type, that is the how the layer data set in `source` will be rendered With `sourcetype` set to *geojson*, the following values are allowed: *circle*, *line*, *fill* and *symbol*. but note that *line* and *fill* are not compatible with Point GeoJSON geometries. With `sourcetype` set to *vector*, the following values are allowed:  *circle*, *line*, *fill* and *symbol*. With `sourcetype` set to *raster* or *image*, only the *raster* value is allowed.\n    visible: Determines whether this layer is displayed"
        ...
