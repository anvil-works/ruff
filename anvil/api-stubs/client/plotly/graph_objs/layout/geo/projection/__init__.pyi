# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the Plotly catalogue generator in doc/anvil-api-stubs/plotly-stubs.mjs instead, then run:
#   pnpm -F docs build
#
from plotly._base import _PlotlyObject
from typing import Any, Mapping

class Rotation(_PlotlyObject):
    "Create a new 'Rotation' object"
    lat: float | Any
    "Rotates the map along meridians (in degrees North)."
    lon: float | Any
    "Rotates the map along parallels (in degrees East). Defaults to the center of the `lonaxis.range` values."
    roll: float | Any
    "Roll the map (in degrees) For example, a roll of *180* makes the map appear upside down."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        lat: Any = ...,
        lon: Any = ...,
        roll: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Rotation' object\n\nArgs:\n    lat: Rotates the map along meridians (in degrees North).\n    lon: Rotates the map along parallels (in degrees East). Defaults to the center of the `lonaxis.range` values.\n    roll: Roll the map (in degrees) For example, a roll of *180* makes the map appear upside down."
        ...
