# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the source file in doc/anvil-api-stubs/source/ instead, then run:
#   pnpm -F docs build
#
# Type stubs for anvil.pdf module
# Generated files: server/anvil/pdf.pyi

from typing import Any, Literal

from anvil import Media

class PDFRenderer:
    """Configure options for PDF rendering. Returns an object with a render_form() method.

    [Anvil Docs](https://anvil.works/docs/media/creating_pdfs)"""

    def __init__(
        self,
        *,
        filename: str = "print.pdf",
        landscape: bool = False,
        margins: dict[str, float] | float | None = None,
        page_size: str | tuple[float, float] = "letter",
        quality: Literal["original", "screen", "printer", "prepress", "default"] = "default",
        scale: float = 1.0,
    ) -> None:
        """Create a PDF renderer with specified options.

        Args:
            filename: The name of the generated PDF file.
            landscape: Generate a PDF in landscape orientation.
            margins: Page margins (in centimetres), as a dictionary specifying margins on each side
                (eg {'top': 1.0, 'bottom': 1.0, 'left': 1.0, 'right': 1.0}) or as a number specifying
                a global margin. The default value is 1.0.
            page_size: Can be the name of a standard page size ('letter' or 'A0'-'A10'),
                or a tuple of (width, height) in centimetres.
            quality: The quality of the generated PDF, which has a large impact on file size.
                Available values are: 'original', 'screen', 'printer', 'prepress', 'default'.
            scale: The scale (zoom level) at which you are printing. The default value is 1.0.
        """
        ...

    def render_form(self, form_name: str, *args: Any, **kwargs: Any) -> Media:
        """Render an Anvil form to PDF.

        Pass the name of the form you want to render, plus any arguments you want
        to pass to its constructor.

        Returns a PDF as an Anvil Media object."""
        ...

def render_form(form_name: str, *args: Any, **kwargs: Any) -> Media:
    """Render an Anvil form to PDF.

    Pass the name of the form you want to render, plus any arguments you want
    to pass to its constructor.

    Returns a PDF as an Anvil Media object.

    [Anvil Docs](https://anvil.works/docs/working-with-files/creating-pdf-files)"""
    ...
