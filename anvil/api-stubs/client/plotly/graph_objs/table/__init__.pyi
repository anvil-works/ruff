# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the Plotly catalogue generator in doc/anvil-api-stubs/plotly-stubs.mjs instead, then run:
#   pnpm -F docs build
#
from plotly._base import _PlotlyObject
from typing import Any, Mapping
import plotly.graph_objs.table.cells as _plotly_graph_objs_table_cells
import plotly.graph_objs.table.cells as cells
import plotly.graph_objs.table.header as _plotly_graph_objs_table_header
import plotly.graph_objs.table.header as header
import plotly.graph_objs.table.hoverlabel as _plotly_graph_objs_table_hoverlabel
import plotly.graph_objs.table.hoverlabel as hoverlabel
import plotly.graph_objs.table.legendgrouptitle as _plotly_graph_objs_table_legendgrouptitle
import plotly.graph_objs.table.legendgrouptitle as legendgrouptitle

class Cells(_PlotlyObject):
    "Create a new 'Cells' object"
    align: Any
    "Sets the horizontal alignment of the `text` within the box. Has an effect only if `text` spans two or more lines (i.e. `text` contains one or more <br> HTML tags) or if an explicit width is set to override the text width."
    @property
    def fill(self) -> _plotly_graph_objs_table_cells.Fill | Any:
        ...
    @fill.setter
    def fill(self, value: Any) -> None: ...
    @property
    def font(self) -> _plotly_graph_objs_table_cells.Font | Any:
        ...
    @font.setter
    def font(self, value: Any) -> None: ...
    format: Any
    "Sets the cell value formatting rule using d3 formatting mini-languages which are very similar to those in Python. For numbers, see: https://github.com/d3/d3-format/tree/v1.4.5#d3-format."
    height: float | Any
    "The height of cells."
    @property
    def line(self) -> _plotly_graph_objs_table_cells.Line | Any:
        ...
    @line.setter
    def line(self, value: Any) -> None: ...
    prefix: str | Any
    "Prefix for cell values."
    suffix: str | Any
    "Suffix for cell values."
    values: Any
    "Cell values. `values[m][n]` represents the value of the `n`th point in column `m`, therefore the `values[m]` vector length for all columns must be the same (longer vectors will be truncated). Each value must be a finite number or a string."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        align: Any = ...,
        fill: Any = ...,
        font: Any = ...,
        format: Any = ...,
        height: Any = ...,
        line: Any = ...,
        prefix: Any = ...,
        suffix: Any = ...,
        values: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Cells' object\n\nArgs:\n    align: Sets the horizontal alignment of the `text` within the box. Has an effect only if `text` spans two or more lines (i.e. `text` contains one or more <br> HTML tags) or if an explicit width is set to override the text width.\n    format: Sets the cell value formatting rule using d3 formatting mini-languages which are very similar to those in Python. For numbers, see: https://github.com/d3/d3-format/tree/v1.4.5#d3-format.\n    height: The height of cells.\n    prefix: Prefix for cell values.\n    suffix: Suffix for cell values.\n    values: Cell values. `values[m][n]` represents the value of the `n`th point in column `m`, therefore the `values[m]` vector length for all columns must be the same (longer vectors will be truncated). Each value must be a finite number or a string."
        ...

class Domain(_PlotlyObject):
    "Create a new 'Domain' object"
    column: int | Any
    "If there is a layout grid, use the domain for this column in the grid for this table trace."
    row: int | Any
    "If there is a layout grid, use the domain for this row in the grid for this table trace."
    x: Any
    "Sets the horizontal domain of this table trace (in plot fraction)."
    y: Any
    "Sets the vertical domain of this table trace (in plot fraction)."
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
        "Create a new 'Domain' object\n\nArgs:\n    column: If there is a layout grid, use the domain for this column in the grid for this table trace.\n    row: If there is a layout grid, use the domain for this row in the grid for this table trace.\n    x: Sets the horizontal domain of this table trace (in plot fraction).\n    y: Sets the vertical domain of this table trace (in plot fraction)."
        ...

class Header(_PlotlyObject):
    "Create a new 'Header' object"
    align: Any
    "Sets the horizontal alignment of the `text` within the box. Has an effect only if `text` spans two or more lines (i.e. `text` contains one or more <br> HTML tags) or if an explicit width is set to override the text width."
    @property
    def fill(self) -> _plotly_graph_objs_table_header.Fill | Any:
        ...
    @fill.setter
    def fill(self, value: Any) -> None: ...
    @property
    def font(self) -> _plotly_graph_objs_table_header.Font | Any:
        ...
    @font.setter
    def font(self, value: Any) -> None: ...
    format: Any
    "Sets the cell value formatting rule using d3 formatting mini-languages which are very similar to those in Python. For numbers, see: https://github.com/d3/d3-format/tree/v1.4.5#d3-format."
    height: float | Any
    "The height of cells."
    @property
    def line(self) -> _plotly_graph_objs_table_header.Line | Any:
        ...
    @line.setter
    def line(self, value: Any) -> None: ...
    prefix: str | Any
    "Prefix for cell values."
    suffix: str | Any
    "Suffix for cell values."
    values: Any
    "Header cell values. `values[m][n]` represents the value of the `n`th point in column `m`, therefore the `values[m]` vector length for all columns must be the same (longer vectors will be truncated). Each value must be a finite number or a string."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        align: Any = ...,
        fill: Any = ...,
        font: Any = ...,
        format: Any = ...,
        height: Any = ...,
        line: Any = ...,
        prefix: Any = ...,
        suffix: Any = ...,
        values: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Header' object\n\nArgs:\n    align: Sets the horizontal alignment of the `text` within the box. Has an effect only if `text` spans two or more lines (i.e. `text` contains one or more <br> HTML tags) or if an explicit width is set to override the text width.\n    format: Sets the cell value formatting rule using d3 formatting mini-languages which are very similar to those in Python. For numbers, see: https://github.com/d3/d3-format/tree/v1.4.5#d3-format.\n    height: The height of cells.\n    prefix: Prefix for cell values.\n    suffix: Suffix for cell values.\n    values: Header cell values. `values[m][n]` represents the value of the `n`th point in column `m`, therefore the `values[m]` vector length for all columns must be the same (longer vectors will be truncated). Each value must be a finite number or a string."
        ...

class Hoverlabel(_PlotlyObject):
    "Create a new 'Hoverlabel' object"
    align: Any
    "Sets the horizontal alignment of the text content within hover label box. Has an effect only if the hover label text spans more two or more lines"
    bgcolor: Any
    "Sets the background color of the hover labels for this trace"
    bordercolor: Any
    "Sets the border color of the hover labels for this trace."
    @property
    def font(self) -> _plotly_graph_objs_table_hoverlabel.Font | Any:
        "Sets the font used in hover labels."
        ...
    @font.setter
    def font(self, value: Any) -> None: ...
    namelength: int | Any
    "Sets the default length (in number of characters) of the trace name in the hover labels for all traces. -1 shows the whole name regardless of length. 0-3 shows the first 0-3 characters, and an integer >3 will show the whole name if it is less than that many characters, but if it is longer, will truncate to `namelength - 3` characters and add an ellipsis."
    showarrow: bool | Any
    "Sets whether or not to show the hover label arrow/triangle pointing to the data point."
    def __init__(
        self,
        d: Mapping[str, Any] | None = None,
        *,
        align: Any = ...,
        bgcolor: Any = ...,
        bordercolor: Any = ...,
        font: Any = ...,
        namelength: Any = ...,
        showarrow: Any = ...,
        **kwargs: Any,
    ) -> None:
        "Create a new 'Hoverlabel' object\n\nArgs:\n    align: Sets the horizontal alignment of the text content within hover label box. Has an effect only if the hover label text spans more two or more lines\n    bgcolor: Sets the background color of the hover labels for this trace\n    bordercolor: Sets the border color of the hover labels for this trace.\n    font: Sets the font used in hover labels.\n    namelength: Sets the default length (in number of characters) of the trace name in the hover labels for all traces. -1 shows the whole name regardless of length. 0-3 shows the first 0-3 characters, and an integer >3 will show the whole name if it is less than that many characters, but if it is longer, will truncate to `namelength - 3` characters and add an ellipsis.\n    showarrow: Sets whether or not to show the hover label arrow/triangle pointing to the data point."
        ...

class Legendgrouptitle(_PlotlyObject):
    "Create a new 'Legendgrouptitle' object"
    @property
    def font(self) -> _plotly_graph_objs_table_legendgrouptitle.Font | Any:
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
