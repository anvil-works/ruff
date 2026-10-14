# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the source file in doc/anvil-api-stubs/source/ instead, then run:
#   pnpm -F docs build
#
# Type stubs for anvil.google.drive module
# Generated files: client/anvil/google/drive.pyi, server/anvil/google/drive.pyi

from typing import Iterator

from anvil import Media

class DriveItem:
    """Base class for Google Drive items (files and folders)."""

    id: str
    """ID of the DriveItem."""

    def move(self, dest_folder: "Folder", /) -> None:
        """Move the DriveItem from one folder to another."""
        ...
    def trash(self) -> None:
        """Move the DriveItem to the trash folder."""
        ...
    def delete(self) -> None:
        """Delete the DriveItem (this cannot be undone)."""
        ...

class File(DriveItem, Media):
    """A Google Drive file."""

    def get_bytes(self) -> bytes:
        """Get the contents of an object representing a Google Drive file.

        Native Google files such as Docs, Slides and Sheets must first be exported
        to an appropriate file type. All other file types support get_bytes()."""
        ...
    def set_bytes(self, content: bytes, /) -> None:
        """Set the contents of an object representing a Google Drive file."""
        ...
    def set_media(self, media: Media, /) -> None:
        """Upload new contents to an existing File.

        Media must be a Media object."""
        ...

class Folder(DriveItem):
    """A Google Drive folder.

    [Anvil Docs](https://anvil.works/docs/integrations/google/google-drive#folders)"""

    folders: list["Folder"]
    """List of Folder items in the Folder."""

    files: list[File]
    """List of File items in the Folder."""

    def list_files(self) -> Iterator[File]:
        """List the files (not folders) in the Folder."""
        ...
    def list_folders(self) -> Iterator["Folder"]:
        """List the folders (not files) in the Folder."""
        ...
    def get(self, title: str, /) -> File | None:
        """Get the File item by title.

        The title argument should be a string."""
        ...
    def get_by_id(self, id: str, /) -> File | None:
        """Get the File item by ID.

        The ID argument should be a string."""
        ...
    def create_folder(self, title: str, /) -> "Folder":
        """Create a new folder within the Folder."""
        ...
    def create_file(
        self,
        title: str,
        *,
        content_bytes: bytes | None = None,
        content_type: str = "text/plain",
    ) -> File:
        """Create a new file within the Folder."""
        ...

def login(*, extra_scopes: list[str] | None = None) -> None:
    """Prompt the user to log in to their Google account and ask permission to access their Google Drive files.

    [Anvil Docs](https://anvil.works/docs/integrations/google/google-drive#user-files)"""
    ...

def get_user_files() -> Folder:
    """Return the top-level folder containing all the files in the Users drive.

    anvil.google.drive.login() must be called first.

    [Anvil Docs](https://anvil.works/docs/integrations/google/google-drive#user-files)"""
    ...

class _AppFiles:
    """Container for Google Drive app files.

    [Anvil Docs](https://anvil.works/docs/integrations/google/google-drive#app-files)"""
    ...

app_files: _AppFiles = ...
