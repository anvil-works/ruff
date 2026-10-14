# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the source file in doc/anvil-api-stubs/source/ instead, then run:
#   pnpm -F docs build
#
# Type stubs for anvil.tables.query module
# Generated files: client/anvil/tables/query.pyi, server/anvil/tables/query.pyi

from typing import Any

def like(pattern: str, /) -> Any:
    """Match values using a case-sensitive LIKE query, using the % wildcard character."""
    ...

def ilike(pattern: str, /) -> Any:
    """Match values using a case-insensitive ILIKE query, using the % wildcard character."""
    ...

def greater_than(value: Any, /) -> Any:
    """Match values greater than the provided value."""
    ...

def less_than(value: Any, /) -> Any:
    """Match values less than the provided value."""
    ...

def greater_than_or_equal_to(value: Any, /) -> Any:
    """Match values greater than or equal to the provided value."""
    ...

def less_than_or_equal_to(value: Any, /) -> Any:
    """Match values less than or equal to the provided value."""
    ...

def between(
    min: Any,
    max: Any,
    *,
    min_inclusive: bool = True,
    max_inclusive: bool = False,
) -> Any:
    """Match values between the provided min and max, optionally inclusive."""
    ...

def full_text_match(query: str, *, raw: bool = False) -> Any:
    """Match values that match the provided full-text search query."""
    ...

def all_of(*query_expressions: Any, **kwargs: Any) -> Any:
    """Match all query parameters given as arguments and keyword arguments."""
    ...

def any_of(*query_expressions: Any, **kwargs: Any) -> Any:
    """Match any query parameters given as arguments and keyword arguments."""
    ...

def none_of(*query_expressions: Any, **kwargs: Any) -> Any:
    """Match none of the query parameters given as arguments and keyword arguments."""
    ...

def not_(value: Any, /) -> Any:
    """Match none of the query parameters given as arguments and keyword arguments."""
    ...

def page_size(rows: int) -> Any:
    """Define the number of rows that are fetched per round trip to the server."""
    ...

def fetch_only(*only_cols: str, **linked_cols: Any) -> Any:
    """Control which columns are loaded from a table search to speed up queries by only fetching the data you need.

    Args:
        only_cols: Column names to fetch from the table.
            Example: fetch_only('email', group=q.fetch_only('name'))
        linked_cols: Linked columns to fetch, specified as keyword arguments.
            Each value must be another fetch_only() object.

    [Anvil Docs](https://anvil.works/docs/data-tables/accelerated-tables#explicit-cache-control)"""
    ...

def only_cols(*cols: str) -> Any:
    """Control which columns are accessible from a view, restricting access to specific columns.

    Args:
        cols: Column names to make accessible in the view.
            Example: only_cols('email', 'enabled')

    [Anvil Docs](https://anvil.works/docs/data-tables/accelerated-tables#column-restricted-views)"""
    ...
