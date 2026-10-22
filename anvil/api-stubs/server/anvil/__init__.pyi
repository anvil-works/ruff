# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the source file in doc/anvil-api-stubs/source/ instead, then run:
#   pnpm -F docs build
#
# Type stubs for Anvil
# Generated files: client/anvil/__init__.pyi, server/anvil/__init__.pyi

from datetime import date as _date, datetime as _datetime
from typing import Any, Callable, ClassVar, Generic, Iterable, overload, Iterator, Mapping, Literal, TypedDict
from typing_extensions import TypeVar, Unpack, deprecated, override


_T = TypeVar("_T")
_F = TypeVar("_F", bound=Callable[..., Any])

SpacingLength = str | int | float | None
MarginPropertyValue = (
    SpacingLength
    | tuple[SpacingLength, SpacingLength]
    | tuple[SpacingLength, SpacingLength, SpacingLength]
    | tuple[SpacingLength, SpacingLength, SpacingLength, SpacingLength]
)
PaddingPropertyValue = MarginPropertyValue
_ClassesValue = str | list[str] | Mapping[str, bool] | None
_StyleScalar = str | int | float
_StylePropertyValue = _StyleScalar | list[_StyleScalar]
_StyleUpdatePropertyValue = _StylePropertyValue | None
_StyleValue = str | Mapping[str, _StylePropertyValue] | None
_AttrValue = Any
_AttrsValue = Mapping[str, _AttrValue] | None

class SpacingPropertyValue(TypedDict, total=False):
    margin: MarginPropertyValue
    padding: PaddingPropertyValue


_LayoutLength = str | int | float | None


class _IndexLayoutKwargs(TypedDict, total=False):
    index: int | None


class _ColumnPanelLayoutKwargs(_IndexLayoutKwargs, total=False):
    full_width_row: bool
    row_background: str | None
    grid_position: str


class _FlowPanelLayoutKwargs(_IndexLayoutKwargs, total=False):
    width: _LayoutLength
    expand: bool


class _GridPanelLayoutKwargs(TypedDict, total=False):
    row: str
    col_xs: int
    width_xs: int
    col_sm: int
    width_sm: int
    col_md: int
    width_md: int
    col_lg: int
    width_lg: int


class _XYPanelLayoutKwargs(TypedDict, total=False):
    x: _LayoutLength
    y: _LayoutLength
    width: _LayoutLength


class _DataGridLayoutKwargs(_IndexLayoutKwargs, total=False):
    pinned: bool
    slot: Literal["footer"] | None


class _DataRowPanelLayoutKwargs(TypedDict, total=False):
    column: str | None


class _HtmlComponentLayoutKwargs(_IndexLayoutKwargs, total=False):
    dropzone: str | None


class _SlottedLayoutKwargs(_IndexLayoutKwargs, total=False):
    slot: str
    width: _LayoutLength

# ============================================================================
# Media Classes
# ============================================================================

class Media:
    """A Media object represents binary data, such as a file.

    [Anvil Docs](https://anvil.works/docs/other-concepts/working-with-files/media)"""

    content_type: str
    """The MIME type of this Media."""

    name: str | None
    """The file name associated with this Media, or None if it has no name."""

    url: str | None
    """The URL where you can download this Media, or None if it is not downloadable."""

    length: int
    """The length of this Media, in bytes."""

    def get_bytes(self) -> bytes:
        """Get a binary string of the data represented by this Media object.

        [Anvil Docs](https://anvil.works/docs/other-concepts/working-with-files/media)"""
        ...

    def get_url(self) -> str | None:
        """Get a Media object's URL, or None if there isn't one associated with it.

        [Anvil Docs](https://anvil.works/docs/other-concepts/working-with-files/media)"""
        ...


class BlobMedia(Media):
    """Create a Media object with the specified content_type and content.

    Optionally specify a filename as well.

    [Anvil Docs](https://anvil.works/docs/other-concepts/working-with-files/media)"""

    def __init__(self, content_type: str, content: bytes, *, name: str | None = None) -> None: ...


class URLMedia(Media):
    """Create a Media object representing the data at a specific URL.

    For an app theme asset stored at ``theme/assets/<path>``, use
    ``URLMedia("_/theme/<path>")``. Do not add a leading slash or an
    ``assets`` path segment.

    Caution: Getting data from URLs directly in your code will often fail
    for security reasons, or fail to handle binary data.

    [Anvil Docs](https://anvil.works/docs/other-concepts/working-with-files/media)"""

    def __init__(self, url: str, /) -> None: ...


# ============================================================================
# App Information
# ============================================================================

class AppEnvironment:
    """Information about the current app environment."""

    name: str
    """The name of the current environment."""

    tags: list[str]
    """Tags associated with the current environment."""


class AppInfo:
    """Information about the current app.

    [Anvil Docs](https://anvil.works/docs/api/anvil#AppInfo)"""

    id: str
    """A unique identifier for the current app."""

    branch: str
    """The Git branch from which the current app is being run.

    This is 'master' for development apps or apps without a published version,
    and 'published' if this app is being run from its published version."""

    package_name: str
    """The package name of this app."""

    environment: AppEnvironment
    """The environment in which the current app is being run."""

    theme_colors: Mapping[str, str]
    """Theme colors for this app as a readonly dict."""

    def get_asset(self, path: str | None = None) -> Media:
        """Get an asset file from the app's theme assets."""
        ...

    def get_client_config(self, package_name: str | None = None) -> dict[str, Any]:
        """Get the client config for the specified package.

        If no package name is specified, the client config for the current app is returned."""
        ...

    def get_server_config(self, package_name: str | None = None) -> dict[str, Any]:
        """Get the server config for the specified package.

        If no package name is specified, the server config for the current app is returned."""
        ...


app: AppInfo
"""Information about the current app, as an instance of AppInfo."""


# ============================================================================
# Utility Functions
# ============================================================================


def is_server_side() -> Literal[True]:
    """Check whether Anvil is running server side or not."""
    ...


# ============================================================================
# Server-Only: Secrets Access
# ============================================================================

class _Secrets:
    """Access to app secrets.

    [Anvil Docs](https://anvil.works/docs/workflows/security/encrypting-secret-data)"""

    def get_secret(self, name: str) -> str | None: ...
    def __getattr__(self, name: str) -> str | None: ...


secrets: _Secrets
