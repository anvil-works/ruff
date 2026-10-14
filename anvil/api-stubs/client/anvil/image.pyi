# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the source file in doc/anvil-api-stubs/source/ instead, then run:
#   pnpm -F docs build
#
# Type stubs for anvil.image module
# Generated files: client/anvil/image.pyi, server/anvil/image.pyi

from anvil import Media

class ImageException(Exception):
    """Image processing exception."""
    ...

def get_dimensions(image_media: Media, /) -> tuple[int, int]:
    """Get the dimensions of an image (width, height).

    Pass in an anvil.Media object representing the image."""
    ...

def generate_thumbnail(image_media: Media, max_size: int, /) -> Media:
    """Resize the supplied image so that neither width nor height exceeds max_size (in pixels).

    Pass in an anvil.Media object representing the image."""
    ...

def rotate(image_media: Media, angle: float, /) -> Media:
    """Rotate the supplied image clockwise by the given number of degrees.

    Pass in an anvil.Media object representing the image."""
    ...
