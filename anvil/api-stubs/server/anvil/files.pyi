# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the source file in doc/anvil-api-stubs/source/ instead, then run:
#   pnpm -F docs build
#
# Type stubs for anvil.files module
# Generated files: server/anvil/files.pyi

from typing import IO, Any

class OpenContextManager:
    """Context manager for opening data files."""

    def __enter__(self) -> IO[Any]:
        """Open the file."""
        ...
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Close the file, uploading its contents if it was opened for writing or appending."""
        ...

class EditingContextManager:
    """Context manager for editing data files."""

    def __enter__(self) -> str:
        """Begin editing the file. Returns the path to a temporary file."""
        ...
    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """End editing the file, uploading its new contents."""
        ...

class Files:
    """Access to Data Files from the Data Files Service.

    To access a file stored in the Data Files Service use square brackets
    containing the path of the desired file - `data_files['<file_path>']`."""

    def __getitem__(self, path: str) -> str:
        """Return the path of a file."""
        ...
    def editing(self, path: str) -> EditingContextManager:
        """Edit a file.

        To ensure the proper acquisition and release of the file, use the `editing`
        function in a `with` statement e.g. `with data_files.editing('test.txt') as file:`"""
        ...
    def open(self, path: str, mode: str = "r") -> OpenContextManager:
        """The open() function opens the file (if possible) and returns the corresponding file object."""
        ...

data_files: Files
"""Access Data Files from the Data Files Service.

To access a file stored in the Data Files Service use square brackets
containing the path of the desired file - `data_files['<file_path>']`."""
