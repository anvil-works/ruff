# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the source file in doc/anvil-api-stubs/source/ instead, then run:
#   pnpm -F docs build
#
"""Portable URL locations and client browser-history navigation.

Runtime contracts are defined in runtime/client/js/modules/history/ and
runtime/downlink/python/anvil/history.py; this module is not yet in index.json.
"""

from typing import Any, Callable, Literal, Protocol


class Location(dict[str, Any]):
    """A portable URL location whose dictionary keys are also attributes."""

    path: str
    search: str
    hash: str
    state: Any
    key: str

    def __init__(
        self, path: str = "", search: str | None = "", hash: str | None = "",
        state: Any = None, key: str | None = None,
    ) -> None: ...

    @property
    def search_params(self) -> dict[str, str]: ...

    def get_url(self, full: bool = False) -> str: ...

    @classmethod
    def from_url(cls, url: str, state: Any = None, key: str | None = None) -> "Location": ...


class History:
    """Server placeholder; browser-history operations raise RuntimeError."""
    ...


history: History
hash_history: History
