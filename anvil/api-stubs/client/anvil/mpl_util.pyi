# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the source file in doc/anvil-api-stubs/source/ instead, then run:
#   pnpm -F docs build
#
# Type stubs for anvil.mpl_util module
# Generated files: client/anvil/mpl_util.pyi, server/anvil/mpl_util.pyi

from typing import Any

from anvil import Media

def plot_image(
    *,
    dpi: int | None = None,
    facecolor: Any | None = None,
    edgecolor: Any | None = None,
    format: str | None = None,
    transparent: bool | None = None,
    frameon: bool | None = None,
    bbox_inches: str | Any | None = None,
    pad_inches: float | None = None,
    filename: str | None = None,
) -> Media:
    """Return the current Matplotlib figure as a PNG image.

    Returns an Anvil Media object that can be displayed in Image components.

    Optional arguments have the same meaning as for 'savefig()'."""
    ...
