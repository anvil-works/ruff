# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the source file in doc/anvil-api-stubs/source/ instead, then run:
#   pnpm -F docs build
#
# Type stubs for anvil.designer module
# Generated files: client/anvil/designer.pyi, server/anvil/designer.pyi

from typing import Any, Callable, Mapping, TypeVar
from anvil import Component

_ComponentClass = TypeVar("_ComponentClass", bound=type[Component])

in_designer: bool
"""True when code is running in the Anvil designer, otherwise False.

[Anvil Docs](https://anvil.works/docs/client/advanced-layouts/component-api/designer-module)"""

def get_design_name(component: Any, /) -> str | None:
    """Get the design-time name for a component, if available."""
    ...

def get_designer_state(component: Any, /) -> Mapping[str, Any]:
    """Get component-specific state managed by the designer."""
    ...

def update_component_properties(
    component: Any,
    properties: dict[str, Any] | None = None,
    layout_properties: dict[str, Any] | None = None,
) -> None:
    """Store updated component/container properties in the designer."""
    ...

def update_component_sections(
    component: Any,
    section_updates: dict[str, dict[str, Any] | None] | None = None,
) -> None:
    """Notify the designer that sections have moved, changed, or been removed."""
    ...

def start_editing_subform(form_component: Any, /) -> None:
    """Request that the designer start editing a nested form component."""
    ...

def start_editing_form(requesting_component: Any, form_property_value: str, /) -> None:
    """Request that the designer switch to editing another form."""
    ...

def register_interaction(
    component: Any,
    dom_element: Any,
    event: str | None = "dblclick",
    callback: Callable[[Any], Any] | None = None,
) -> None:
    """Register a design-time mouse interaction callback for a component."""
    ...

def notify_interactions_changed(component: Any, /) -> None:
    """Notify the designer that available interactions may have changed."""
    ...

def get_design_component(component_class: _ComponentClass, /) -> _ComponentClass:
    """Get the design-time class for a component class.

    [Anvil Docs](https://anvil.works/docs/client/advanced-layouts/component-api/designer-module)"""
    ...

def request_form_property_change(
    requesting_component: Any,
    form: str,
    property_name: str,
    property_value: Any,
    /,
) -> None:
    """Request a property change on a form selected by a form-property value."""
    ...

def start_inline_editing(
    component: Any,
    property_name: str,
    dom_element: Any | None = None,
    *,
    on_finished: Callable[[], Any] | None = None,
) -> None:
    """Request inline editing for a string property in the designer."""
    ...
