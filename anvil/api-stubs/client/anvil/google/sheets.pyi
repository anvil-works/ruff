# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the source file in doc/anvil-api-stubs/source/ instead, then run:
#   pnpm -F docs build
#
# Type stubs for anvil.google.sheets module
# Generated files: client/anvil/google/sheets.pyi, server/anvil/google/sheets.pyi

from typing import Any, Iterator

class Cell:
    """A cell in a Google Sheets worksheet."""

    row: int
    """This cell's row index (starting from 1)."""

    col: int
    """This cell's column index (starting from 1)."""

    value: str
    """The value in this cell."""

    input_value: str
    """The value that was entered into the cell."""

class Row:
    """A row in a Google Sheets worksheet."""

    def __getattr__(self, name: str) -> Any: ...
    def __setattr__(self, name: str, value: Any) -> None: ...
    def delete(self) -> None:
        """Delete this row from the worksheet.

        This will cause data in subsequent rows to shift up."""
        ...

class Worksheet:
    """A worksheet (tab) in a Google Sheets spreadsheet."""

    title: str
    """The title of this worksheet."""

    row_count: int
    """The number of rows in this worksheet."""

    column_count: int
    """The number of columns in this worksheet."""

    fields: list[str]
    """The fields in this worksheet (ie the column headers, or the values in the first row)."""

    rows: list[Row]
    """The rows in this worksheet (excluding the header)."""

    cells: list[Cell]
    """A list of all the cells in this worksheet."""

    def list_rows(self, **query: Any) -> list[Row]:
        """List rows in this worksheet.

        Optionally restricting to rows with the specified column values
        specified as keyword arguments."""
        ...
    def add_row(self, **fields: Any) -> Row:
        """Add a row to the end of the worksheet.

        Specifying values for columns as keywords arguments."""
        ...
    def list_cells(
        self,
        *,
        min_row: int | None = None,
        max_row: int | None = None,
        min_col: int | None = None,
        max_col: int | None = None,
    ) -> list[Cell]:
        """List cells in the worksheet, optionally specifying a region."""
        ...
    def get_cell(self, row: int, col: int) -> Cell:
        """Get a particular cell from the spreadsheet."""
        ...
    def __iter__(self) -> Iterator[Cell]: ...

class Spreadsheet:
    """A Google Sheets spreadsheet."""

    title: str
    """The title of this spreadsheet."""

    id: str
    """The ID of this spreadsheet in Google Drive."""

    worksheets: list[Worksheet]
    """The worksheets in this spreadsheet."""

    def list_worksheets(self) -> list[Worksheet]:
        """Get a list of all worksheets in this spreadsheet."""
        ...
    def __iter__(self) -> Iterator[Worksheet]: ...
