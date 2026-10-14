# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the source file in doc/anvil-api-stubs/source/ instead, then run:
#   pnpm -F docs build
#
# Type stubs for anvil.media module
# Generated files: client/anvil/media.pyi, server/anvil/media.pyi

from typing import IO, Any

from anvil import Media

def print_media(media: Media, /) -> None:
    """Print the given Media Object immediately in the user's browser."""
    ...

def download(media: Media, /) -> None:
    """Download the given Media Object immediately in the user's browser."""
    ...

class TempUrl:
    """Creates a temporary client-side URL for a Media object, even if the media has no permanent URL.

    This URL should be revoked when you are finished with it. If you use TempUrl as a context
    manager ('with TempUrl(media) as url:'), this happens automatically; if you instantiate it
    manually you must call 'revoke()' on the instance.

    The download argument only affects LazyMedia objects."""

    url: str
    """The temporary URL."""

    def __init__(self, media: Media, *, download: bool = True) -> None: ...
    def __enter__(self) -> str:
        """Get the url using a 'with' block."""
        ...
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Revoke a url when exiting a 'with' block."""
        ...
    def revoke(self) -> None:
        """Revoke a url from a media object."""
        ...


def write_to_file(media: Media, filename: str) -> None:
    """Write a Media object to the given file."""
    ...
