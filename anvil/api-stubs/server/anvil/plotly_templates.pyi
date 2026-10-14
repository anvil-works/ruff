# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the source file in doc/anvil-api-stubs/source/ instead, then run:
#   pnpm -F docs build
#
# Type stubs for anvil.plotly_templates module
# Generated files: client/anvil/plotly_templates.pyi, server/anvil/plotly_templates.pyi

from typing import Any

templates: dict[str, Any]
"""A dictionary of custom templates for anvil themes."""

def set_default(template: str | Any) -> None:
    """Sets the default plotly template."""
    ...
