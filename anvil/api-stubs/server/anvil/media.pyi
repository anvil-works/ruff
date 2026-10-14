# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the source file in doc/anvil-api-stubs/source/ instead, then run:
#   pnpm -F docs build
#
# Type stubs for anvil.media module
# Generated files: client/anvil/media.pyi, server/anvil/media.pyi

from typing import IO, Any

from anvil import Media


class TempFile:
    """Create a temporary file initialised with the contents of the provided media, if any."""

    def __init__(self, media: Media | None = None) -> None: ...
    def __enter__(self) -> str:
        """Returns the path to the temporary file."""
        ...
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None: ...

def from_file(filename: str, mime_type: str | None = None, name: str | None = None) -> Media:
    """Creates a Media object from the given file."""
    ...

def open(media: Media) -> IO[bytes]:
    """Open a media file as Python BytesIO object."""
    ...

def write_to_file(media: Media, filename: str) -> None:
    """Write a Media object to the given file."""
    ...
