# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the Plotly catalogue generator in doc/anvil-api-stubs/plotly-stubs.mjs instead, then run:
#   pnpm -F docs build
#
from plotly._base import _PlotlyObject
from typing import Any, Mapping
import plotly.graph_objs.indicator.delta as _plotly_graph_objs_indicator_delta
import plotly.graph_objs.indicator.delta as delta
import plotly.graph_objs.indicator.gauge as _plotly_graph_objs_indicator_gauge
import plotly.graph_objs.indicator.gauge as gauge
import plotly.graph_objs.indicator.legendgrouptitle as _plotly_graph_objs_indicator_legendgrouptitle
import plotly.graph_objs.indicator.legendgrouptitle as legendgrouptitle
import plotly.graph_objs.indicator.number as _plotly_graph_objs_indicator_number
import plotly.graph_objs.indicator.number as number
import plotly.graph_objs.indicator.title as _plotly_graph_objs_indicator_title
import plotly.graph_objs.indicator.title as title

class Delta(_PlotlyObject):
    "Create a new 'Delta' object"
    @property
    def decreasing(self) -> _plotly_graph_objs_indicator_delta.Decreasing | Any:
        ...
    @decreasing.setter
    def decreasing(self, value: Any) -> None: ...
    @property
    def font(self) -> _plotly_graph_objs_indicator_delta.Font | Any:
        "Set the font used to display the delta"
        ...
    @font.setter
    def font(self, value: Any) -> None: ...
    @property
    def increasing(self) -> _plotly_graph_objs_indicator_delta.Increasing | Any:
        ...
    @increasing.setter
    def increasing(self, value: Any) -> None: ...
    position: Any
    "Sets the position of delta with respect to the number."
    prefix: str | Any
    "Sets a prefix appearing before the delta."
    reference: float | Any
    "Sets the reference value to compute the delta. By default, it is set to the current value."
    relative: bool | Any
    "Show relative change"
    suffix: str | Any
    "Sets a suffix appearing next to the delta."
    valueformat: str | Any
    "Sets the value formatting rule using d3 formatting mini-languages which are very similar to those in Python. For numbers, see: https://github.com/d3/d3-format/tree/v1.4.5#d3-format."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        decreasing: Any = ...,
        font: Any = ...,
        increasing: Any = ...,
        position: Any = ...,
        prefix: Any = ...,
        reference: Any = ...,
        relative: Any = ...,
        suffix: Any = ...,
        valueformat: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Delta' object\n\nArgs:\n    font: Set the font used to display the delta\n    position: Sets the position of delta with respect to the number.\n    prefix: Sets a prefix appearing before the delta.\n    reference: Sets the reference value to compute the delta. By default, it is set to the current value.\n    relative: Show relative change\n    suffix: Sets a suffix appearing next to the delta.\n    valueformat: Sets the value formatting rule using d3 formatting mini-languages which are very similar to those in Python. For numbers, see: https://github.com/d3/d3-format/tree/v1.4.5#d3-format."
        ...

class Domain(_PlotlyObject):
    "Create a new 'Domain' object"
    column: int | Any
    "If there is a layout grid, use the domain for this column in the grid for this indicator trace."
    row: int | Any
    "If there is a layout grid, use the domain for this row in the grid for this indicator trace."
    x: Any
    "Sets the horizontal domain of this indicator trace (in plot fraction)."
    y: Any
    "Sets the vertical domain of this indicator trace (in plot fraction)."
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
        "Create a new 'Domain' object\n\nArgs:\n    column: If there is a layout grid, use the domain for this column in the grid for this indicator trace.\n    row: If there is a layout grid, use the domain for this row in the grid for this indicator trace.\n    x: Sets the horizontal domain of this indicator trace (in plot fraction).\n    y: Sets the vertical domain of this indicator trace (in plot fraction)."
        ...

class Gauge(_PlotlyObject):
    "Create a new 'Gauge' object"
    @property
    def axis(self) -> _plotly_graph_objs_indicator_gauge.Axis | Any:
        ...
    @axis.setter
    def axis(self, value: Any) -> None: ...
    @property
    def bar(self) -> _plotly_graph_objs_indicator_gauge.Bar | Any:
        "Set the appearance of the gauge's value"
        ...
    @bar.setter
    def bar(self, value: Any) -> None: ...
    bgcolor: Any
    "Sets the gauge background color."
    bordercolor: Any
    "Sets the color of the border enclosing the gauge."
    borderwidth: float | Any
    "Sets the width (in px) of the border enclosing the gauge."
    shape: Any
    "Set the shape of the gauge"
    @property
    def step(self) -> _plotly_graph_objs_indicator_gauge.Step | Any:
        ...
    @step.setter
    def step(self, value: Any) -> None: ...
    @property
    def threshold(self) -> _plotly_graph_objs_indicator_gauge.Threshold | Any:
        ...
    @threshold.setter
    def threshold(self, value: Any) -> None: ...
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        axis: Any = ...,
        bar: Any = ...,
        bgcolor: Any = ...,
        bordercolor: Any = ...,
        borderwidth: Any = ...,
        shape: Any = ...,
        step: Any = ...,
        threshold: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Gauge' object\n\nArgs:\n    bar: Set the appearance of the gauge's value\n    bgcolor: Sets the gauge background color.\n    bordercolor: Sets the color of the border enclosing the gauge.\n    borderwidth: Sets the width (in px) of the border enclosing the gauge.\n    shape: Set the shape of the gauge"
        ...

class Legendgrouptitle(_PlotlyObject):
    "Create a new 'Legendgrouptitle' object"
    @property
    def font(self) -> _plotly_graph_objs_indicator_legendgrouptitle.Font | Any:
        "Sets this legend group's title font."
        ...
    @font.setter
    def font(self, value: Any) -> None: ...
    text: str | Any
    "Sets the title of the legend group."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        font: Any = ...,
        text: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Legendgrouptitle' object\n\nArgs:\n    font: Sets this legend group's title font.\n    text: Sets the title of the legend group."
        ...

class Number(_PlotlyObject):
    "Create a new 'Number' object"
    @property
    def font(self) -> _plotly_graph_objs_indicator_number.Font | Any:
        "Set the font used to display main number"
        ...
    @font.setter
    def font(self, value: Any) -> None: ...
    prefix: str | Any
    "Sets a prefix appearing before the number."
    suffix: str | Any
    "Sets a suffix appearing next to the number."
    valueformat: str | Any
    "Sets the value formatting rule using d3 formatting mini-languages which are very similar to those in Python. For numbers, see: https://github.com/d3/d3-format/tree/v1.4.5#d3-format."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        font: Any = ...,
        prefix: Any = ...,
        suffix: Any = ...,
        valueformat: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Number' object\n\nArgs:\n    font: Set the font used to display main number\n    prefix: Sets a prefix appearing before the number.\n    suffix: Sets a suffix appearing next to the number.\n    valueformat: Sets the value formatting rule using d3 formatting mini-languages which are very similar to those in Python. For numbers, see: https://github.com/d3/d3-format/tree/v1.4.5#d3-format."
        ...

class Title(_PlotlyObject):
    "Create a new 'Title' object"
    align: Any
    "Sets the horizontal alignment of the title. It defaults to `center` except for bullet charts for which it defaults to right."
    @property
    def font(self) -> _plotly_graph_objs_indicator_title.Font | Any:
        "Set the font used to display the title"
        ...
    @font.setter
    def font(self, value: Any) -> None: ...
    text: str | Any
    "Sets the title of this indicator."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        align: Any = ...,
        font: Any = ...,
        text: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Title' object\n\nArgs:\n    align: Sets the horizontal alignment of the title. It defaults to `center` except for bullet charts for which it defaults to right.\n    font: Set the font used to display the title\n    text: Sets the title of this indicator."
        ...
