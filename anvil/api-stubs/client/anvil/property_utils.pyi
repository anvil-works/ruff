# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the source file in doc/anvil-api-stubs/source/ instead, then run:
#   pnpm -F docs build
#
"""Utilities for working with custom component property values.

[Anvil Docs](https://anvil.works/docs/client/advanced-layouts/component-api/property-utils-module)"""

from typing import Any, Callable, Literal, Mapping, Protocol

from anvil import Component, MarginPropertyValue, PaddingPropertyValue, SpacingLength, SpacingPropertyValue
from anvil.js import window

PropertyType = Literal[
    "string",
    "number",
    "boolean",
    "text[]",
    "enum",
    "form",
    "object",
    "dict",
    "color",
    "icon",
    "themeRole",
    "uri",
    "html",
    "recordType",
    "margin",
    "padding",
    "spacing",
]


class anvil_property(property):
    """Define custom component properties.

    [Anvil Docs](https://anvil.works/docs/client/advanced-layouts/component-api)"""

    def __init__(self, type: PropertyType, /, **descriptors: Any) -> None: ...
    def __call__(self, fget: Callable[..., Any], /) -> "anvil_property": ...
    def setter(self, fset: Callable[..., Any], /) -> "anvil_property": ...

    @property
    def fget(self) -> Any: ...
    @property
    def fset(self) -> Any: ...


class InstantiatorFunction(Protocol):
    """Callable that constructs a form/component instance from a form property value."""

    def __call__(self, item: str | int = ..., /, **properties: Any) -> Component: ...


def get_form_constructor(
    parent_form: Component,
    property_value: str | type[Component] | InstantiatorFunction | None,
    prefer_live_design: bool = True,
) -> InstantiatorFunction | None:
    """Resolve a form property value to a constructor function.

    [Anvil Docs](https://anvil.works/docs/client/advanced-layouts/component-api/property-utils-module)"""
    ...


def get_margin_styles(margin: MarginPropertyValue) -> Mapping[str, str]:
    """Convert a margin property value into CSS style fragments.

    [Anvil Docs](https://anvil.works/docs/client/advanced-layouts/component-api/property-utils-module)"""
    ...


def get_padding_styles(padding: PaddingPropertyValue) -> Mapping[str, str]:
    """Convert a padding property value into CSS style fragments.

    [Anvil Docs](https://anvil.works/docs/client/advanced-layouts/component-api/property-utils-module)"""
    ...


def get_spacing_styles(spacing: SpacingPropertyValue) -> Mapping[str, str]:
    """Convert a spacing property value into CSS style fragments.

    [Anvil Docs](https://anvil.works/docs/client/advanced-layouts/component-api/property-utils-module)"""
    ...


def set_element_margin(element: window.HTMLElement, margin: MarginPropertyValue) -> None: ...
def set_element_padding(element: window.HTMLElement, padding: PaddingPropertyValue) -> None: ...
def set_element_spacing(element: window.HTMLElement, spacing: SpacingPropertyValue) -> None: ...
def set_element_visibility(element: window.HTMLElement, visible: bool) -> None: ...


def get_unset_margin(
    element: window.HTMLElement, current_value: MarginPropertyValue | None = None
) -> Mapping[str, Any]: ...
def get_unset_padding(
    element: window.HTMLElement, current_value: PaddingPropertyValue | None = None
) -> Mapping[str, Any]: ...
def get_unset_spacing(
    margin_element: window.HTMLElement,
    padding_element: window.HTMLElement,
    current_value: SpacingPropertyValue | None = None,
) -> Mapping[str, Any]: ...
def get_unset_value(element: window.HTMLElement, key: str, current_value: Any = None) -> Mapping[str, Any]: ...
