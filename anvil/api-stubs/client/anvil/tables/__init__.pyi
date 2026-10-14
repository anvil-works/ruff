# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the source file in doc/anvil-api-stubs/source/ instead, then run:
#   pnpm -F docs build
#
# Type stubs for anvil.tables module
# Generated files: client/anvil/tables/__init__.pyi, server/anvil/tables/__init__.pyi

from typing import Any, Generic, TypeVar, Iterator, Callable, Iterable, Mapping, overload

from anvil import Media

_T = TypeVar("_T", bound="Row")
_F = TypeVar("_F", bound="Callable[..., Any]")

class Row:
    """Base class for table rows.

    [Anvil Docs](https://anvil.works/docs/data-tables/data-tables-in-code)"""
    def __init_subclass__(
        cls,
        *,
        attrs: bool = False,
        buffered: bool = False,
        client_writable: bool = False,
        client_updatable: bool = False,
        client_creatable: bool = False,
        client_deletable: bool = False,
        **kwargs: Any
    ) -> None: ...
    def __getitem__(self, key: str, /) -> Any: ...
    def __setitem__(self, key: str, value: Any, /) -> None: ...
    def __contains__(self, key: str, /) -> bool: ...
    def __iter__(self) -> Iterator[tuple[str, Any]]: ...
    def update(self, **kwargs: Any) -> None:
        """Update multiple columns of this row at once.

        [Anvil Docs](https://anvil.works/docs/data-tables/data-tables-in-code)"""
        ...
    def delete(self) -> None:
        """Delete this row from the table.

        [Anvil Docs](https://anvil.works/docs/data-tables/data-tables-in-code)"""
        ...
    def get_id(self) -> str:
        """Get the unique ID of this row.

        [Anvil Docs](https://anvil.works/docs/data-tables/data-tables-in-code)"""
        ...
    def save(self) -> None:
        """Save buffered changes to this row.

        Only available with Accelerated Data Tables; not available with legacy Data Tables.

        [Anvil Docs](https://anvil.works/docs/data-tables/data-tables-in-code)"""
        ...
    def reset(self) -> None:
        """Reset buffered changes to this row.

        Only available with Accelerated Data Tables; not available with legacy Data Tables.

        [Anvil Docs](https://anvil.works/docs/data-tables/data-tables-in-code)"""
        ...
    def buffer_changes(self, buffered: bool | None = None) -> Any:
        """Context manager for buffered mode.

        Only available with Accelerated Data Tables; not available with legacy Data Tables.

        [Anvil Docs](https://anvil.works/docs/data-tables/data-tables-in-code)"""
        ...
    @property
    def buffered_changes(self) -> dict[str, Any] | None:
        """Pending buffered changes for this row.

        Only available with Accelerated Data Tables; not available with legacy Data Tables.

        [Anvil Docs](https://anvil.works/docs/data-tables/data-tables-in-code)"""
        ...
    def refresh(self, fetch: Any = None) -> None:
        """Refresh this row from the database.

        Only available with Accelerated Data Tables; not available with legacy Data Tables.

        [Anvil Docs](https://anvil.works/docs/data-tables/data-tables-in-code)"""
        ...
    def fetch(self, fetch: Any) -> None:
        """Fetch specific columns for this row.

        Only available with Accelerated Data Tables; not available with legacy Data Tables.

        [Anvil Docs](https://anvil.works/docs/data-tables/data-tables-in-code)"""
        ...
    def get(self, key: str, default: Any = None) -> Any:
        """Get a column value, returning default if this row has no such column.

        Only available with Accelerated Data Tables; not available with legacy Data Tables.

        [Anvil Docs](https://anvil.works/docs/data-tables/data-tables-in-code)"""
        ...
    def values(self) -> Iterator[Any]:
        """Iterator of column values.

        Only available with Accelerated Data Tables; not available with legacy Data Tables.

        [Anvil Docs](https://anvil.works/docs/data-tables/data-tables-in-code)"""
        ...
    def keys(self) -> Iterator[str]:
        """Iterator of column names.

        Only available with Accelerated Data Tables; not available with legacy Data Tables.

        [Anvil Docs](https://anvil.works/docs/data-tables/data-tables-in-code)"""
        ...
    def items(self) -> Iterator[tuple[str, Any]]:
        """Iterator of (name, value) pairs.

        Only available with Accelerated Data Tables; not available with legacy Data Tables.

        [Anvil Docs](https://anvil.works/docs/data-tables/data-tables-in-code)"""
        ...

class SearchIterator(Generic[_T], Iterator[_T]):
    """Iterator returned by table.search().

    [Anvil Docs](https://anvil.works/docs/data-tables/data-tables-in-code)"""
    def __iter__(self) -> "SearchIterator[_T]": ...
    def __next__(self) -> _T: ...
    def __len__(self) -> int: ...
    @overload
    def __getitem__(self, index: int) -> _T: ...
    @overload
    def __getitem__(self, index: slice) -> list[_T]: ...
    def __getitem__(self, index: int | slice) -> _T | list[_T]: ...
    def refresh(self) -> None:
        """Clear cached results for this iterator.

        Only available with Accelerated Data Tables; not available with legacy Data Tables.

        [Anvil Docs](https://anvil.works/docs/data-tables/accelerated-tables)"""
        ...
    def to_csv(self, escape_for_excel: bool = False) -> Media:
        """Get the search results in CSV format.

        [Anvil Docs](https://anvil.works/docs/data-tables/export-csv)"""
        ...
    def delete_all_rows(self) -> None:
        """Delete all rows matching this search.

        Only available with Accelerated Data Tables; not available with legacy Data Tables.

        [Anvil Docs](https://anvil.works/docs/data-tables/data-tables-in-code)"""
        ...

class Table(Generic[_T]):
    """Base class for tables.

    [Anvil Docs](https://anvil.works/docs/data-tables/data-tables-in-code)"""
    Row: type[_T]
    def __contains__(self, row: Row, /) -> bool: ...
    def get(self, *args: Any, **kwargs: Any) -> _T | None:
        """Get a single row matching the given criteria.

        [Anvil Docs](https://anvil.works/docs/data-tables/data-tables-in-code)"""
        ...
    def get_by_id(self, row_id: str, /, fetch: Any = None) -> _T | None:
        """Get a row by its unique ID.

        The fetch argument is only available with Accelerated Data Tables; it is
        not available with legacy Data Tables.

        [Anvil Docs](https://anvil.works/docs/data-tables/data-tables-in-code)"""
        ...
    def search(self, *query_expressions: Any, **column_filters: Any) -> SearchIterator[_T]:
        """Search for rows matching the given criteria.

        Pass query expressions such as ``anvil.tables.query.fetch_only(...)``
        as positional arguments. Keyword arguments filter rows by column.
        ``fetch_only()`` controls which data is loaded; it does not create a
        column-restricted client view. For that, pass ``query.only_cols(...)``
        to a ``client_*`` view method.

        Example::

            from anvil.tables import query as q
            app_tables.employees.search(q.fetch_only("name", "email"), role="Engineer")

        [Anvil Docs](https://anvil.works/docs/data-tables/data-tables-in-code)"""
        ...
    def add_row(self, **kwargs: Any) -> _T:
        """Add a new row to this table.

        [Anvil Docs](https://anvil.works/docs/data-tables/data-tables-in-code)"""
        ...
    def add_rows(self, rows: Iterable[Mapping[str, Any]], /) -> list[_T]:
        """Add multiple rows to this table.

        Only available with Accelerated Data Tables; not available with legacy Data Tables.

        [Anvil Docs](https://anvil.works/docs/data-tables/accelerated-tables)"""
        ...
    def has_row(self, row: Row, /) -> bool:
        """Return whether this table or view contains the given row.

        [Anvil Docs](https://anvil.works/docs/data-tables/data-tables-in-code)"""
        ...
    def list_columns(self) -> list[dict[str, Any]]:
        """List all columns in this table.

        [Anvil Docs](https://anvil.works/docs/data-tables/data-tables-in-code)"""
        ...
    def delete_all_rows(self) -> None:
        """Delete all rows from this table.

        [Anvil Docs](https://anvil.works/docs/data-tables/data-tables-in-code)"""
        ...
    def restrict_columns(self, col_spec: Any, /) -> "Table[_T]":
        """Return a view restricted to the given columns.

        Only available with Accelerated Data Tables; not available with legacy Data Tables.

        [Anvil Docs](https://anvil.works/docs/data-tables/accelerated-tables#column-restricted-views)"""
        ...
    def to_csv(self, escape_for_excel: bool = False) -> Media:
        """Get the table in CSV format.

        [Anvil Docs](https://anvil.works/docs/data-tables/export-csv)"""
        ...
    def client_readable(self, *view_restrictions: Any, **row_restrictions: Any) -> "Table[_T]":
        """Return a view of this table that clients can read.

        Pass ``anvil.tables.query.only_cols(...)`` directly as a positional
        argument to restrict which columns the client can access. Keyword
        arguments restrict which rows the view contains. Return this table
        view itself when exposing it to clients; ``search()`` returns rows,
        not the view.

        Example::

            from anvil.tables import query as q
            app_tables.employees.client_readable(q.only_cols("name", "email"))

        [Anvil Docs](https://anvil.works/docs/data-tables/data-security)"""
        ...
    def client_writable(self, *view_restrictions: Any, **row_restrictions: Any) -> "Table[_T]":
        """Return a view of this table that clients can write to.

        Pass ``anvil.tables.query.only_cols(...)`` directly as a positional
        argument to restrict which columns the client can access. Keyword
        arguments restrict which rows the view contains.

        Example::

            from anvil.tables import query as q
            app_tables.employees.client_writable(q.only_cols("name", "email"))

        [Anvil Docs](https://anvil.works/docs/data-tables/data-security)"""
        ...
    def client_writable_cascade(self, *view_restrictions: Any, **row_restrictions: Any) -> "Table[_T]":
        """Return a view of this table that clients can write to, with cascading permissions.

        Pass ``anvil.tables.query.only_cols(...)`` directly as a positional
        argument to restrict which columns the client can access. Keyword
        arguments restrict which rows the view contains.

        Example::

            from anvil.tables import query as q
            app_tables.employees.client_writable_cascade(q.only_cols("name", "email"))

        [Anvil Docs](https://anvil.works/docs/data-tables/data-security)"""
        ...

# Query operators
def order_by(column: str, /, ascending: bool = True) -> Any:
    """Create an ordering query operator.

    [Anvil Docs](https://anvil.works/docs/data-tables/data-tables-in-code#searching-and-querying-data-tables)"""
    ...

class _Query:
    """Query operators for searching tables.

    [Anvil Docs](https://anvil.works/docs/data-tables/data-tables-in-code#searching-and-querying-data-tables)"""
    @staticmethod
    def any_of(*args: Any) -> Any:
        """Match any of the given conditions.

        [Anvil Docs](https://anvil.works/docs/data-tables/data-tables-in-code#searching-and-querying-data-tables)"""
        ...
    @staticmethod
    def all_of(*args: Any) -> Any:
        """Match all of the given conditions.

        [Anvil Docs](https://anvil.works/docs/data-tables/data-tables-in-code#searching-and-querying-data-tables)"""
        ...
    @staticmethod
    def none_of(*args: Any) -> Any:
        """Match none of the given conditions.

        [Anvil Docs](https://anvil.works/docs/data-tables/data-tables-in-code#searching-and-querying-data-tables)"""
        ...
    @staticmethod
    def like(pattern: str) -> Any:
        """Match using SQL LIKE pattern (case-sensitive).

        [Anvil Docs](https://anvil.works/docs/data-tables/data-tables-in-code#searching-and-querying-data-tables)"""
        ...
    @staticmethod
    def ilike(pattern: str) -> Any:
        """Match using SQL LIKE pattern (case-insensitive).

        [Anvil Docs](https://anvil.works/docs/data-tables/data-tables-in-code#searching-and-querying-data-tables)"""
        ...
    @staticmethod
    def full_text_match(query: str, raw: bool = False) -> Any:
        """Full-text search.

        [Anvil Docs](https://anvil.works/docs/data-tables/data-tables-in-code#searching-and-querying-data-tables)"""
        ...
    @staticmethod
    def greater_than(value: Any) -> Any:
        """Match values greater than the given value.

        [Anvil Docs](https://anvil.works/docs/data-tables/data-tables-in-code#searching-and-querying-data-tables)"""
        ...
    @staticmethod
    def greater_than_or_equal_to(value: Any) -> Any:
        """Match values greater than or equal to the given value.

        [Anvil Docs](https://anvil.works/docs/data-tables/data-tables-in-code#searching-and-querying-data-tables)"""
        ...
    @staticmethod
    def less_than(value: Any) -> Any:
        """Match values less than the given value.

        [Anvil Docs](https://anvil.works/docs/data-tables/data-tables-in-code#searching-and-querying-data-tables)"""
        ...
    @staticmethod
    def less_than_or_equal_to(value: Any) -> Any:
        """Match values less than or equal to the given value.

        [Anvil Docs](https://anvil.works/docs/data-tables/data-tables-in-code#searching-and-querying-data-tables)"""
        ...
    @staticmethod
    def between(min_value: Any, max_value: Any, min_inclusive: bool = True, max_inclusive: bool = False) -> Any:
        """Match values between the given bounds.

        [Anvil Docs](https://anvil.works/docs/data-tables/data-tables-in-code#searching-and-querying-data-tables)"""
        ...
    @staticmethod
    def not_(value: Any) -> Any:
        """Negate a query condition.

        [Anvil Docs](https://anvil.works/docs/data-tables/data-tables-in-code#searching-and-querying-data-tables)"""
        ...

q: _Query

# Exceptions
class TableError(Exception):
    """Superclass of all table exceptions.

    [Anvil Docs](https://anvil.works/docs/data-tables/transactions)"""
    ...

class TransactionConflict(TableError):
    """Raised when a transaction conflicts and has been aborted.

    [Anvil Docs](https://anvil.works/docs/data-tables/transactions)"""
    ...

class NoSuchColumnError(TableError):
    """Raised when attempting to access a column that does not exist in this table."""
    ...

class QuotaExceededError(TableError):
    """Raised when an app has exceeded its quota."""
    ...

class RowDeleted(TableError):
    """Raised when attempting to access a table row that has been deleted."""
    ...

# Transaction support
class Transaction:
    """A database transaction context manager.

    [Anvil Docs](https://anvil.works/docs/data-tables/transactions)"""
    def __init__(self, relaxed: bool = False) -> None: ...
    def __enter__(self) -> "Transaction": ...
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> bool: ...
    def abort(self) -> None:
        """Abort this transaction and roll back all changes.

        [Anvil Docs](https://anvil.works/docs/data-tables/transactions)"""
        ...


def get_table_by_id(table_id: str) -> Table[Row]:
    """Get a table by id. Can pass a row id in, and the table the row belongs to will be returned.

    Only available with Accelerated Data Tables; not available with legacy Data Tables.

    [Anvil Docs](https://anvil.works/docs/data-tables/accelerated-tables)"""
    ...


# app_tables will be dynamically typed based on db_schema
class _AppTables:
    """Container for all app tables. Individual tables are generated from db_schema.

    [Anvil Docs](https://anvil.works/docs/data-tables)"""
    def __getattr__(self, name: str) -> Table[Row]: ...
    def __getitem__(self, name: str) -> Table[Row]: ...
    def __iter__(self) -> Iterator[str]: ...

app_tables: _AppTables
