# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the Plotly catalogue generator in doc/anvil-api-stubs/plotly-stubs.mjs instead, then run:
#   pnpm -F docs build
#
from plotly._base import _PlotlyObject
from typing import Any, Mapping

class Project(_PlotlyObject):
    "Create a new 'Project' object"
    x: bool | Any
    "Determines whether or not these contour lines are projected on the x plane. If `highlight` is set to *true* (the default), the projected lines are shown on hover. If `show` is set to *true*, the projected lines are shown in permanence."
    y: bool | Any
    "Determines whether or not these contour lines are projected on the y plane. If `highlight` is set to *true* (the default), the projected lines are shown on hover. If `show` is set to *true*, the projected lines are shown in permanence."
    z: bool | Any
    "Determines whether or not these contour lines are projected on the z plane. If `highlight` is set to *true* (the default), the projected lines are shown on hover. If `show` is set to *true*, the projected lines are shown in permanence."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        x: Any = ...,
        y: Any = ...,
        z: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Project' object\n\nArgs:\n    x: Determines whether or not these contour lines are projected on the x plane. If `highlight` is set to *true* (the default), the projected lines are shown on hover. If `show` is set to *true*, the projected lines are shown in permanence.\n    y: Determines whether or not these contour lines are projected on the y plane. If `highlight` is set to *true* (the default), the projected lines are shown on hover. If `show` is set to *true*, the projected lines are shown in permanence.\n    z: Determines whether or not these contour lines are projected on the z plane. If `highlight` is set to *true* (the default), the projected lines are shown on hover. If `show` is set to *true*, the projected lines are shown in permanence."
        ...
