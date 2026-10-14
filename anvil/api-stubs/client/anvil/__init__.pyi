# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the source file in doc/anvil-api-stubs/source/ instead, then run:
#   pnpm -F docs build
#
# Type stubs for Anvil
# Generated files: client/anvil/__init__.pyi, server/anvil/__init__.pyi

from typing import Any, Callable, TypeVar, overload, Iterator, Mapping, Literal, TypedDict
from typing_extensions import Unpack, deprecated, override

from . import property_utils

_T = TypeVar("_T")
_F = TypeVar("_F", bound=Callable[..., Any])

SpacingLength = str | int | float | None
MarginPropertyValue = (
    SpacingLength
    | tuple[SpacingLength, SpacingLength]
    | tuple[SpacingLength, SpacingLength, SpacingLength]
    | tuple[SpacingLength, SpacingLength, SpacingLength, SpacingLength]
)
PaddingPropertyValue = MarginPropertyValue
_ClassesValue = str | list[str] | Mapping[str, bool] | None
_StyleScalar = str | int | float
_StylePropertyValue = _StyleScalar | list[_StyleScalar]
_StyleUpdatePropertyValue = _StylePropertyValue | None
_StyleValue = str | Mapping[str, _StylePropertyValue] | None
_AttrValue = Any
_AttrsValue = Mapping[str, _AttrValue] | None

class SpacingPropertyValue(TypedDict, total=False):
    margin: MarginPropertyValue
    padding: PaddingPropertyValue


_LayoutLength = str | int | float | None


class _IndexLayoutKwargs(TypedDict, total=False):
    index: int | None


class _ColumnPanelLayoutKwargs(_IndexLayoutKwargs, total=False):
    full_width_row: bool
    row_background: str | None
    grid_position: str


class _FlowPanelLayoutKwargs(_IndexLayoutKwargs, total=False):
    width: _LayoutLength
    expand: bool


class _GridPanelLayoutKwargs(TypedDict, total=False):
    row: str
    col_xs: int
    width_xs: int
    col_sm: int
    width_sm: int
    col_md: int
    width_md: int
    col_lg: int
    width_lg: int


class _XYPanelLayoutKwargs(TypedDict, total=False):
    x: _LayoutLength
    y: _LayoutLength
    width: _LayoutLength


class _DataGridLayoutKwargs(_IndexLayoutKwargs, total=False):
    pinned: bool
    slot: Literal["footer"] | None


class _DataRowPanelLayoutKwargs(TypedDict, total=False):
    column: str | None


class _HtmlComponentLayoutKwargs(_IndexLayoutKwargs, total=False):
    dropzone: str | None


class _SlottedLayoutKwargs(_IndexLayoutKwargs, total=False):
    slot: str
    width: _LayoutLength

# ============================================================================
# Media Classes
# ============================================================================

class Media:
    """A Media object represents binary data, such as a file.

    [Anvil Docs](https://anvil.works/docs/media)"""

    content_type: str
    """The MIME type of this Media."""

    name: str | None
    """The file name associated with this Media, or None if it has no name."""

    url: str | None
    """The URL where you can download this Media, or None if it is not downloadable."""

    length: int
    """The length of this Media, in bytes."""

    def get_bytes(self) -> bytes:
        """Get a binary string of the data represented by this Media object.

        [Anvil Docs](https://anvil.works/docs/media)"""
        ...

    def get_url(self) -> str | None:
        """Get a Media object's URL, or None if there isn't one associated with it.

        [Anvil Docs](https://anvil.works/docs/media)"""
        ...


class BlobMedia(Media):
    """Create a Media object with the specified content_type and content.

    Optionally specify a filename as well.

    [Anvil Docs](https://anvil.works/docs/media)"""

    def __init__(self, content_type: str, content: bytes, *, name: str | None = None) -> None: ...


class URLMedia(Media):
    """Create a Media object representing the data at a specific URL.

    For an app theme asset stored at ``theme/assets/<path>``, use
    ``URLMedia("_/theme/<path>")``. Do not add a leading slash or an
    ``assets`` path segment.

    Caution: Getting data from URLs directly in your code will often fail
    for security reasons, or fail to handle binary data.

    [Anvil Docs](https://anvil.works/docs/media)"""

    def __init__(self, url: str, /) -> None: ...


# ============================================================================
# App Information
# ============================================================================

class AppEnvironment:
    """Information about the current app environment."""

    name: str
    """The name of the current environment."""

    tags: list[str]
    """Tags associated with the current environment."""


class AppInfo:
    """Information about the current app.

    [Anvil Docs](https://anvil.works/docs/deployment/environment-variables)"""

    id: str
    """A unique identifier for the current app."""

    branch: str
    """The Git branch from which the current app is being run.

    This is 'master' for development apps or apps without a published version,
    and 'published' if this app is being run from its published version."""

    package_name: str
    """The package name of this app."""

    environment: AppEnvironment
    """The environment in which the current app is being run."""

    theme_colors: Mapping[str, str]
    """Theme colors for this app as a readonly dict."""

    def get_asset(self, path: str | None = None) -> Media:
        """Get an asset file from the app's theme assets."""
        ...

    def get_client_config(self, package_name: str | None = None) -> dict[str, Any]:
        """Get the client config for the specified package.

        If no package name is specified, the client config for the current app is returned."""
        ...

    def get_server_config(self, package_name: str | None = None) -> dict[str, Any]:
        """Get the server config for the specified package.

        If no package name is specified, the server config for the current app is returned."""
        ...


app: AppInfo
"""Information about the current app, as an instance of AppInfo."""


# ============================================================================
# Utility Functions
# ============================================================================

def is_server_side() -> Literal[False]:
    """Check whether Anvil is running server side or not."""
    ...


# ============================================================================
# Alert and Notification Functions (client-only)
# ============================================================================

def alert(
    content: str | Any,
    *,
    title: str = "",
    buttons: list[Any] | None = None,
    large: bool = False,
    dismissible: bool = True,
    role: str | list[str] | None = None,
) -> Any:
    """Pop up an alert box.

    By default, it will have a single "OK" button which will return True when clicked.

    [Anvil Docs](https://anvil.works/docs/client/python/alerts-and-notifications)"""
    ...


def confirm(
    content: str | Any,
    *,
    title: str = "",
    buttons: list[Any] | None = None,
    large: bool = False,
    dismissible: bool = False,
    role: str | list[str] | None = None,
) -> bool:
    """Pop up a confirmation box.

    By default, it will have "Yes" and "No" buttons which will return True and False
    respectively when clicked.

    [Anvil Docs](https://anvil.works/docs/client/python/alerts-and-notifications)"""
    ...


class Notification:
    """Create a popup notification. Call the show() method to display it.

    Set timeout to None or 0 to keep it visible until dismissed.
    Set role to a theme role name or list of names.
    The style argument is deprecated; use role and theme CSS instead.
    Can also be used as a context manager.

    [Anvil Docs](https://anvil.works/docs/client/python/alerts-and-notifications)"""

    @overload
    def __init__(
        self,
        message: str,
        *,
        title: str = "",
        timeout: int | float | None = 2,
        role: str | list[str] | None = None,
    ) -> None: ...

    @overload
    @deprecated("Notification's style argument is deprecated. Use role and theme CSS instead.")
    def __init__(
        self,
        message: str,
        *,
        title: str = "",
        style: str,
        timeout: int | float | None = 2,
        role: str | list[str] | None = None,
    ) -> None: ...

    def show(self) -> "Notification":
        """Shows the notification."""
        ...

    def hide(self) -> None:
        """Hides the notification immediately."""
        ...

    def __enter__(self) -> "Notification":
        """Show the notification when entering a 'with' block."""
        ...

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Hide the notification when exiting a 'with' block."""
        ...


# ============================================================================
# Navigation Functions (client-only)
# ============================================================================

def get_open_form() -> Any:
    """Returns the form most recently opened with open_form().

    [Anvil Docs](https://anvil.works/docs/client/python/forms-and-components)"""
    ...


def open_form(form: str | Any, *args: Any, **kwargs: Any) -> None:
    """Open the specified form as a new page.

    If 'form' is a string, a new form will be created (extra arguments will be passed
    to its constructor). If 'form' is a Form object, it will be opened directly.

    [Anvil Docs](https://anvil.works/docs/client/python/forms-and-components)"""
    ...


def get_url_hash() -> str | dict[str, str]:
    """Get the decoded hash (the part after the '#' character) of the URL used to open this app.

    If the first character of the hash is a question mark (eg '#?a=foo&b=bar'),
    it will be interpreted as query-string-type parameters and returned as a dictionary
    (eg {'a': 'foo', 'b': 'bar'}).

    [Anvil Docs](https://anvil.works/docs/client/python/navigation-and-urls)"""
    ...


def set_url_hash(val: str | dict[str, str], /) -> None:
    """Sets the hash of the currently open URL.

    If val is a string, it is added to the URL after a #.
    If val is a dictionary, it will be interpreted as query-string-type parameters
    and added to the URL after a hash and question mark (eg '#?a=foo&b=bar').

    [Anvil Docs](https://anvil.works/docs/client/python/navigation-and-urls)"""
    ...


# ============================================================================
# Other Client-Only Functions
# ============================================================================

def download(media: Media, /) -> None:
    """Download the given Media Object immediately in the user's browser.

    [Anvil Docs](https://anvil.works/docs/media)"""
    ...


def get_focused_component() -> "Component | None":
    """Get the currently focused Anvil component, or None if focus is not in a component."""
    ...


def set_default_error_handling(handler_fn: Callable[[Exception], None] | None, /) -> None:
    """Set a function to be called when an uncaught exception occurs.

    If set to None, a pop-up will appear letting the user know that an error has occurred."""
    ...


# ============================================================================
# Pluggable UI Registry (client-only)
# ============================================================================

class PluggableUI(Mapping[str, Any]):
    """Registry of pluggable UI classes and hooks."""

    def provide(self, package_name: str, updates: dict[str, Any], /) -> None:
        """Provide UI overrides for a package."""
        ...

    def provide_defaults(self, package_name: str, updates: dict[str, Any], /) -> None:
        """Provide default UI implementations for a package."""
        ...

    def add_listener(self, name: str, listener_func: _F, /) -> _F:
        """Register a listener for pluggable UI updates."""
        ...

    def remove_listener(self, listener_func: Callable[..., Any], /) -> None:
        """Remove a previously registered listener."""
        ...


pluggable_ui: PluggableUI
"""Pluggable UI object used by built-in services and theme integrations."""


# ============================================================================
# Decorators
# ============================================================================

def handle(component_name: str, event_name: str, /) -> Callable[[_F], _F]:
    """When applied to a form method as a decorator, sets the decorated method
    as an event handler for the specified component event."""
    ...


# ============================================================================
# HTML Styling Helpers (client-only)
# ============================================================================

class Classes:
    """A live class-list helper for an HtmlComponent's root element.

    [Anvil Docs](https://anvil.works/docs/client/customisation/custom-components/html-components#styling-the-root-element-from-python)"""

    def __init__(self, value: _ClassesValue = None, /) -> None: ...
    def __str__(self) -> str: ...
    def __iter__(self) -> Iterator[str]: ...
    def __len__(self) -> int: ...
    def __contains__(self, value: str) -> bool: ...
    def __getitem__(self, value: str) -> bool: ...
    def __setitem__(self, value: str, enabled: bool) -> None: ...
    def __delitem__(self, value: str) -> None: ...
    def add(self, *values: _ClassesValue) -> None:
        """Add one or more class names. Strings are split on whitespace; duplicate classes are ignored."""
        ...
    def remove(self, *values: _ClassesValue) -> None:
        """Remove one or more class names. Missing classes are ignored."""
        ...
    @overload
    def update(self, /, **kwargs: bool) -> None: ...
    @overload
    def update(self, updates: Mapping[str, bool], /, **kwargs: bool) -> None: ...
    def clear(self) -> None:
        """Remove all class names."""
        ...


class Style:
    """A live inline-style helper for an HtmlComponent's root element.

    [Anvil Docs](https://anvil.works/docs/client/customisation/custom-components/html-components#styling-the-root-element-from-python)"""

    def __init__(self, value: _StyleValue = None, /) -> None: ...
    def __str__(self) -> str: ...
    def __iter__(self) -> Iterator[str]: ...
    def __len__(self) -> int: ...
    def __contains__(self, property: str) -> bool: ...
    def __getitem__(self, property: str) -> str: ...
    def __setitem__(self, property: str, value: _StylePropertyValue) -> None: ...
    def __delitem__(self, property: str) -> None: ...
    def keys(self) -> Iterator[str]:
        """Return an iterator over the CSS property names in this style object."""
        ...
    def values(self) -> Iterator[str]:
        """Return an iterator over the CSS property values in this style object."""
        ...
    def items(self) -> Iterator[tuple[str, str]]:
        """Return an iterator over (property, value) pairs for this style object."""
        ...
    @overload
    def get(self, property: str, default: str = "") -> str: ...
    @overload
    def get(self, property: str, default: _T) -> str | _T: ...
    @overload
    def update(self, /, **kwargs: _StyleUpdatePropertyValue) -> None: ...
    @overload
    def update(
        self,
        updates: Mapping[str, _StyleUpdatePropertyValue],
        /,
        **kwargs: _StyleUpdatePropertyValue,
    ) -> None: ...
    def clear(self) -> None:
        """Remove all CSS properties."""
        ...


class Attrs:
    """A live HTML attribute helper for an HtmlComponent's root element.

    [Anvil Docs](https://anvil.works/docs/client/customisation/custom-components/html-components#styling-the-root-element-from-python)"""

    def __init__(self, value: _AttrsValue = None, /) -> None: ...
    def __str__(self) -> str: ...
    def __iter__(self) -> Iterator[str]: ...
    def __len__(self) -> int: ...
    def __contains__(self, name: str) -> bool: ...
    def __getitem__(self, name: str) -> str | None: ...
    def __setitem__(self, name: str, value: _AttrValue) -> None: ...
    def __delitem__(self, name: str) -> None: ...
    def keys(self) -> Iterator[str]:
        """Return an iterator over the attribute names in this attrs object."""
        ...
    def values(self) -> Iterator[str]:
        """Return an iterator over the attribute values in this attrs object."""
        ...
    def items(self) -> Iterator[tuple[str, str]]:
        """Return an iterator over (name, value) pairs for this attrs object."""
        ...
    @overload
    def update(self, /, **kwargs: _AttrValue) -> None: ...
    @overload
    def update(self, updates: Mapping[str, _AttrValue], /, **kwargs: _AttrValue) -> None: ...
    def clear(self) -> None:
        """Remove all managed HTML attributes."""
        ...


# ============================================================================
# Slot and Layout Classes (client-only)
# ============================================================================

class Slot:
    """A Slot class represents a way to add components to an underlying container.

    You will rarely instantiate a Slot on its own; instead your form's layout
    will contain Slots to which you can add components."""

    def __init__(
        self,
        target_container: "Container",
        insertion_index: int,
        layout_properties: dict[str, Any] | None = None,
    ) -> None:
        """Create a new Slot.

        Args:
            target_container: The target container into which components added to this slot will be added.
            insertion_index: The starting index (within the target container) at which components
                added to this slot will be inserted.
            layout_properties: A dictionary of layout properties that will be passed as keyword
                arguments to the target container's add_component() call.
        """
        ...

    def add_component(
        self,
        component: "Component",
        *,
        index: int | None = None,
        **layout_properties: Any,
    ) -> None:
        """Add a component to this slot.

        Calling add_component() on a Slot will add the specified component to its target container.

        Args:
            component: The component to add to this slot.
            index: The index, within the slot, at which the component is to be inserted.
            **layout_properties: Layout properties will be passed on as keyword arguments
                to the target container's add_component() method.
        """
        ...

    def get_components(self) -> list["Component"]:
        """Return the components added to this slot.

        [Anvil Docs](https://anvil.works/docs/api/anvil#Slot)"""
        ...

    def clear(self) -> None:
        """Remove all components added to this slot from their parent container.

        [Anvil Docs](https://anvil.works/docs/api/anvil#Slot)"""
        ...

    def offset_by_slot(self, offset_by_slot: "Slot") -> None:
        """Inform this Slot of an earlier Slot with the same target container.

        Future calls to add_component() will take account of any components inserted
        into the earlier slot when calculating the insertion index for the target container."""
        ...


class WithLayout(Component):
    """Parent class of any form with a layout."""

    @property
    def layout(self) -> "Component":
        """This form's layout."""
        ...
    @layout.setter
    def layout(self, value: "Component") -> None: ...


# ============================================================================
# JavaScript Interop (client-only)
# ============================================================================

class _JS:
    """JavaScript interop.

    [Anvil Docs](https://anvil.works/docs/client/javascript)"""

    @staticmethod
    def call(fn_name: str, *args: Any) -> Any: ...


js: _JS


# ============================================================================
# Event Type Aliases for Autocomplete
# ============================================================================

# Base Component events - inherited by all components
_ComponentEvents = Literal["show", "hide"]

# Button and Link events
_ButtonEvents = Literal["show", "hide", "click"]
_LinkEvents = Literal["show", "hide", "click"]

# Text input events
_TextBoxEvents = Literal["show", "hide", "change", "pressed_enter", "lost_focus", "focus"]
_TextAreaEvents = Literal["show", "hide", "change", "lost_focus", "focus"]

# Selection component events
_CheckBoxEvents = Literal["show", "hide", "change"]
_RadioButtonEvents = Literal["show", "hide", "clicked"]
_DropDownEvents = Literal["show", "hide", "change"]
_DatePickerEvents = Literal["show", "hide", "change"]
_FileLoaderEvents = Literal["show", "hide", "change", "lost_focus", "focus"]

# Timer events
_TimerEvents = Literal["show", "hide", "tick"]

# Mouse-enabled component events
_CanvasEvents = Literal["show", "hide", "reset", "mouse_down", "mouse_up", "mouse_move", "mouse_enter", "mouse_leave"]
_ImageEvents = Literal["show", "hide", "mouse_down", "mouse_up", "mouse_move", "mouse_enter", "mouse_leave"]

# Plot events
_PlotEvents = Literal["show", "hide", "click", "double_click", "afterplot", "hover", "unhover", "select"]

# GoogleMap events
_GoogleMapEvents = Literal[
    "show",
    "hide",
    "bounds_changed",
    "center_changed",
    "click",
    "dbl_click",
    "drag",
    "dragend",
    "dragstart",
    "heading_changed",
    "idle",
    "maptypeid_changed",
    "mousemove",
    "mouseout",
    "mouseover",
    "projection_changed",
    "rightclick",
    "tilesloaded",
    "tilt_changed",
    "zoom_changed",
    "data_addfeature",
    "data_click",
    "data_dbl_click",
    "data_mousedown",
    "data_mouseout",
    "data_mouseover",
    "data_mouseup",
    "data_removefeature",
    "data_removeproperty",
    "data_rightclick",
    "data_setgeometry",
    "data_setproperty",
]

# YouTubeVideo events
_YouTubeVideoEvents = Literal["show", "hide", "state_change"]

# DataGrid events
_DataGridEvents = Literal["show", "hide", "page_changed"]

# ============================================================================
# Component Base Classes
# ============================================================================

class Component:
    """Base class for all Anvil components.

    [Anvil Docs](https://anvil.works/docs/client/components)"""

    def __init__(self, **properties: Any) -> None: ...

    parent: Any
    @property
    def tag(self) -> Any: ...
    @tag.setter
    def tag(self, value: Any) -> None: ...

    def add_event_handler(self, event_name: _ComponentEvents | str, handler_func: Callable[..., Any], /) -> None:
        """Add an event handler function to be called when the event happens on this component.

        Event handlers will be called in the order they are added. Adding the same event
        handler multiple times will mean it gets called multiple times.

        [Anvil Docs](https://anvil.works/docs/client/python/events)"""
        ...

    def remove_event_handler(self, event_name: _ComponentEvents | str, handler_func: Callable[..., Any] | None = None, /) -> None:
        """Remove a specific event handler function for a given event.

        Calling remove_event_handler with just the event name will remove all the handlers for this event.

        [Anvil Docs](https://anvil.works/docs/client/python/events)"""
        ...

    def set_event_handler(self, event_name: _ComponentEvents | str, handler_func: Callable[..., Any] | None, /) -> None:
        """Set a function to call when the 'event_name' event happens on this component.

        Using set_event_handler removes all other handlers.
        Setting the handler function to None removes all handlers.

        [Anvil Docs](https://anvil.works/docs/client/python/events)"""
        ...

    def get_event_handlers(self, event_name: _ComponentEvents | str, /) -> tuple[Callable[..., Any], ...]:
        """Get the list of event handler functions for a given event.

        [Anvil Docs](https://anvil.works/docs/client/python/events)"""
        ...

    def remove_from_parent(self) -> None:
        """Remove this component from its parent container.

        [Anvil Docs](https://anvil.works/docs/client/components)"""
        ...

    def raise_event(self, event_name: _ComponentEvents | str, /, **event_args: Any) -> None:
        """Raise an event on this component.

        [Anvil Docs](https://anvil.works/docs/client/python/events)"""
        ...

    def scroll_into_view(self, *, smooth: bool = False, align: str = "center") -> None:
        """Scroll this component into view.

        [Anvil Docs](https://anvil.works/docs/client/components)"""
        ...


class Container(Component):
    """Base class for container components.

    [Anvil Docs](https://anvil.works/docs/client/components)"""

    def add_component(self, component: Component, /, **layout_props: Any) -> None:
        """Add a component to this container.

        [Anvil Docs](https://anvil.works/docs/client/components)"""
        ...

    def clear(self) -> None:
        """Remove all components from this container.

        [Anvil Docs](https://anvil.works/docs/client/components)"""
        ...

    def get_components(self) -> list[Component]:
        """Get a list of components in this container.

        [Anvil Docs](https://anvil.works/docs/client/components)"""
        ...

    def raise_event_on_children(self, event_name: str, /, **event_args: Any) -> None:
        """Trigger the 'event_name' event on all children of this component.

        Any keyword arguments are passed to the handler function.

        [Anvil Docs](https://anvil.works/docs/client/components)"""
        ...


    def __init__(
        self,
        *,
        tag: Any = ...,
    ) -> None: ...

# ============================================================================
# Basic Display Components
# ============================================================================

class Label(Component):
    """A label for displaying text.

    [Anvil Docs](https://anvil.works/docs/client/components/basic#label)"""

    @property
    def visible(self) -> bool: ...
    @visible.setter
    def visible(self, value: bool) -> None: ...
    @property
    def tooltip(self) -> str: ...
    @tooltip.setter
    def tooltip(self, value: str) -> None: ...
    @property
    def role(self) -> str | list[str] | None: ...
    @role.setter
    def role(self, value: str | list[str] | None) -> None: ...

    @property
    def text(self) -> str: ...
    @text.setter
    def text(self, value: str) -> None: ...
    @property
    def icon(self) -> str: ...
    @icon.setter
    def icon(self, value: str) -> None: ...
    @property
    def icon_align(self) -> str: ...
    @icon_align.setter
    def icon_align(self, value: str) -> None: ...
    @property
    def font_size(self) -> int | float | None: ...
    @font_size.setter
    def font_size(self, value: int | float | None) -> None: ...
    @property
    def font(self) -> str: ...
    @font.setter
    def font(self, value: str) -> None: ...
    @property
    def bold(self) -> bool: ...
    @bold.setter
    def bold(self, value: bool) -> None: ...
    @property
    def italic(self) -> bool: ...
    @italic.setter
    def italic(self, value: bool) -> None: ...
    @property
    def underline(self) -> bool: ...
    @underline.setter
    def underline(self, value: bool) -> None: ...
    @property
    def foreground(self) -> str: ...
    @foreground.setter
    def foreground(self, value: str) -> None: ...
    @property
    def background(self) -> str: ...
    @background.setter
    def background(self, value: str) -> None: ...
    @property
    def border(self) -> str: ...
    @border.setter
    def border(self, value: str) -> None: ...
    @property
    def align(self) -> str: ...
    @align.setter
    def align(self, value: str) -> None: ...
    @property
    def spacing_above(self) -> Literal["none", "small", "medium", "large"] | None: ...
    @spacing_above.setter
    def spacing_above(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...
    @property
    def spacing_below(self) -> Literal["none", "small", "medium", "large"] | None: ...
    @spacing_below.setter
    def spacing_below(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...


    @property
    def spacing(self) -> SpacingPropertyValue: ...
    @spacing.setter
    def spacing(self, value: SpacingPropertyValue) -> None: ...

    def __init__(
        self,
        *,
        tag: Any = ...,
        visible: bool = ...,
        tooltip: str = ...,
        role: str | list[str] | None = ...,
        text: str = ...,
        icon: str = ...,
        icon_align: str = ...,
        font_size: int | float | None = ...,
        font: str = ...,
        bold: bool = ...,
        italic: bool = ...,
        underline: bool = ...,
        foreground: str = ...,
        background: str = ...,
        border: str = ...,
        align: str = ...,
        spacing_above: Literal["none", "small", "medium", "large"] | None = ...,
        spacing_below: Literal["none", "small", "medium", "large"] | None = ...,
        spacing: SpacingPropertyValue = ...,
    ) -> None: ...

class Link(ColumnPanel):
    """A clickable link component.

    [Anvil Docs](https://anvil.works/docs/client/components/basic#link)"""

    @property
    def visible(self) -> bool: ...
    @visible.setter
    def visible(self, value: bool) -> None: ...
    @property
    def tooltip(self) -> str: ...
    @tooltip.setter
    def tooltip(self, value: str) -> None: ...
    @property
    def role(self) -> str | list[str] | None: ...
    @role.setter
    def role(self, value: str | list[str] | None) -> None: ...

    @property
    def text(self) -> str: ...
    @text.setter
    def text(self, value: str) -> None: ...
    @property
    def url(self) -> str: ...
    @url.setter
    def url(self, value: str) -> None: ...
    @property
    def icon(self) -> str: ...
    @icon.setter
    def icon(self, value: str) -> None: ...
    @property
    def icon_align(self) -> str: ...
    @icon_align.setter
    def icon_align(self, value: str) -> None: ...
    @property
    def font_size(self) -> int | float | None: ...
    @font_size.setter
    def font_size(self, value: int | float | None) -> None: ...
    @property
    def font(self) -> str: ...
    @font.setter
    def font(self, value: str) -> None: ...
    @property
    def bold(self) -> bool: ...
    @bold.setter
    def bold(self, value: bool) -> None: ...
    @property
    def italic(self) -> bool: ...
    @italic.setter
    def italic(self, value: bool) -> None: ...
    @property
    def underline(self) -> bool: ...
    @underline.setter
    def underline(self, value: bool) -> None: ...
    @property
    def foreground(self) -> str: ...
    @foreground.setter
    def foreground(self, value: str) -> None: ...
    @property
    def background(self) -> str: ...
    @background.setter
    def background(self, value: str) -> None: ...
    @property
    def border(self) -> str: ...
    @border.setter
    def border(self, value: str) -> None: ...
    @property
    def align(self) -> str: ...
    @align.setter
    def align(self, value: str) -> None: ...


    @property
    def text_padding(self) -> PaddingPropertyValue: ...
    @text_padding.setter
    def text_padding(self, value: PaddingPropertyValue) -> None: ...

    @override
    def add_event_handler(self, event_name: _LinkEvents | str, handler_func: Callable[..., Any], /) -> None: ...
    @override
    def remove_event_handler(self, event_name: _LinkEvents | str, handler_func: Callable[..., Any] | None = None, /) -> None: ...
    @override
    def set_event_handler(self, event_name: _LinkEvents | str, handler_func: Callable[..., Any] | None, /) -> None: ...
    @override
    def raise_event(self, event_name: _LinkEvents | str, /, **event_args: Any) -> None: ...


    def __init__(
        self,
        *,
        tag: Any = ...,
        visible: bool = ...,
        tooltip: str = ...,
        role: str | list[str] | None = ...,
        col_widths: str = ...,
        col_spacing: str = ...,
        wrap_on: str = ...,
        background: str = ...,
        foreground: str = ...,
        border: str = ...,
        spacing_above: Literal["none", "small", "medium", "large"] | None = ...,
        spacing_below: Literal["none", "small", "medium", "large"] | None = ...,
        spacing: SpacingPropertyValue = ...,
        text: str = ...,
        url: str = ...,
        icon: str = ...,
        icon_align: str = ...,
        font_size: int | float | None = ...,
        font: str = ...,
        bold: bool = ...,
        italic: bool = ...,
        underline: bool = ...,
        align: str = ...,
        text_padding: PaddingPropertyValue = ...,
    ) -> None: ...

class Image(Component):
    """An image display component.

    [Anvil Docs](https://anvil.works/docs/client/components/basic#image)"""

    @property
    def visible(self) -> bool: ...
    @visible.setter
    def visible(self, value: bool) -> None: ...
    @property
    def tooltip(self) -> str: ...
    @tooltip.setter
    def tooltip(self, value: str) -> None: ...
    @property
    def role(self) -> str | list[str] | None: ...
    @role.setter
    def role(self, value: str | list[str] | None) -> None: ...

    @property
    def source(self) -> str | Media:
        """The image to display, as a Media object or URL string.

        For an app theme asset stored at ``theme/assets/<path>``, use the
        runtime-relative URL ``_/theme/<path>`` (for example,
        ``_/theme/puppy.png``). Do not add a leading slash or an ``assets``
        path segment."""
        ...
    @source.setter
    def source(self, value: str | Media) -> None: ...
    @property
    def alt_text(self) -> str: ...
    @alt_text.setter
    def alt_text(self, value: str) -> None: ...
    @property
    def display_mode(self) -> str: ...
    @display_mode.setter
    def display_mode(self, value: str) -> None: ...
    @property
    def horizontal_align(self) -> str: ...
    @horizontal_align.setter
    def horizontal_align(self, value: str) -> None: ...
    @property
    def vertical_align(self) -> str: ...
    @vertical_align.setter
    def vertical_align(self, value: str) -> None: ...
    @property
    def height(self) -> str: ...
    @height.setter
    def height(self, value: str) -> None: ...


    @property
    def background(self) -> str: ...
    @background.setter
    def background(self, value: str) -> None: ...
    @property
    def border(self) -> str: ...
    @border.setter
    def border(self, value: str) -> None: ...
    @property
    def border_radius(self) -> str: ...
    @border_radius.setter
    def border_radius(self, value: str) -> None: ...
    @property
    def foreground(self) -> str: ...
    @foreground.setter
    def foreground(self, value: str) -> None: ...
    @property
    def margin(self) -> MarginPropertyValue: ...
    @margin.setter
    def margin(self, value: MarginPropertyValue) -> None: ...
    @property
    def spacing_above(self) -> Literal["none", "small", "medium", "large"] | None: ...
    @spacing_above.setter
    def spacing_above(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...
    @property
    def spacing_below(self) -> Literal["none", "small", "medium", "large"] | None: ...
    @spacing_below.setter
    def spacing_below(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...

    @override
    def add_event_handler(self, event_name: _ImageEvents | str, handler_func: Callable[..., Any], /) -> None: ...
    @override
    def remove_event_handler(self, event_name: _ImageEvents | str, handler_func: Callable[..., Any] | None = None, /) -> None: ...
    @override
    def set_event_handler(self, event_name: _ImageEvents | str, handler_func: Callable[..., Any] | None, /) -> None: ...
    @override
    def raise_event(self, event_name: _ImageEvents | str, /, **event_args: Any) -> None: ...


    def __init__(
        self,
        *,
        tag: Any = ...,
        visible: bool = ...,
        tooltip: str = ...,
        role: str | list[str] | None = ...,
        source: str | Media = ...,
        alt_text: str = ...,
        display_mode: str = ...,
        horizontal_align: str = ...,
        vertical_align: str = ...,
        height: str = ...,
        background: str = ...,
        border: str = ...,
        border_radius: str = ...,
        foreground: str = ...,
        margin: MarginPropertyValue = ...,
        spacing_above: Literal["none", "small", "medium", "large"] | None = ...,
        spacing_below: Literal["none", "small", "medium", "large"] | None = ...,
    ) -> None: ...

class Spacer(Component):
    """A spacer component for layout.

    [Anvil Docs](https://anvil.works/docs/client/components/basic#spacer)"""

    @property
    def visible(self) -> bool: ...
    @visible.setter
    def visible(self, value: bool) -> None: ...
    @property
    def tooltip(self) -> str: ...
    @tooltip.setter
    def tooltip(self, value: str) -> None: ...

    @property
    def height(self) -> int: ...
    @height.setter
    def height(self, value: int) -> None: ...


    @property
    def spacing_above(self) -> Literal["none", "small", "medium", "large"] | None: ...
    @spacing_above.setter
    def spacing_above(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...
    @property
    def spacing_below(self) -> Literal["none", "small", "medium", "large"] | None: ...
    @spacing_below.setter
    def spacing_below(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...

    def __init__(
        self,
        *,
        tag: Any = ...,
        visible: bool = ...,
        tooltip: str = ...,
        height: int = ...,
        spacing_above: Literal["none", "small", "medium", "large"] | None = ...,
        spacing_below: Literal["none", "small", "medium", "large"] | None = ...,
    ) -> None: ...

class RichText(Component):
    """A rich text display component.

    [Anvil Docs](https://anvil.works/docs/client/components/containers#richtext)"""

    @property
    def visible(self) -> bool: ...
    @visible.setter
    def visible(self, value: bool) -> None: ...
    @property
    def tooltip(self) -> str: ...
    @tooltip.setter
    def tooltip(self, value: str) -> None: ...
    @property
    def role(self) -> str | list[str] | None: ...
    @role.setter
    def role(self, value: str | list[str] | None) -> None: ...

    @property
    def content(self) -> str: ...
    @content.setter
    def content(self, value: str) -> None: ...
    @property
    def text(self) -> str: ...
    @text.setter
    def text(self, value: str) -> None: ...
    @property
    def format(self) -> str: ...
    @format.setter
    def format(self, value: str) -> None: ...
    @property
    def enable_slots(self) -> bool: ...
    @enable_slots.setter
    def enable_slots(self, value: bool) -> None: ...
    @property
    def data(self) -> dict[str, Any]: ...
    @data.setter
    def data(self, value: dict[str, Any]) -> None: ...


    @property
    def align(self) -> str: ...
    @align.setter
    def align(self, value: str) -> None: ...
    @property
    def font_size(self) -> int | float | None: ...
    @font_size.setter
    def font_size(self, value: int | float | None) -> None: ...
    @property
    def font(self) -> str: ...
    @font.setter
    def font(self, value: str) -> None: ...
    @property
    def bold(self) -> bool: ...
    @bold.setter
    def bold(self, value: bool) -> None: ...
    @property
    def italic(self) -> bool: ...
    @italic.setter
    def italic(self, value: bool) -> None: ...
    @property
    def underline(self) -> bool: ...
    @underline.setter
    def underline(self, value: bool) -> None: ...
    @property
    def background(self) -> str: ...
    @background.setter
    def background(self, value: str) -> None: ...
    @property
    def border(self) -> str: ...
    @border.setter
    def border(self, value: str) -> None: ...
    @property
    def foreground(self) -> str: ...
    @foreground.setter
    def foreground(self, value: str) -> None: ...
    @property
    def spacing(self) -> SpacingPropertyValue: ...
    @spacing.setter
    def spacing(self, value: SpacingPropertyValue) -> None: ...
    @property
    def spacing_above(self) -> Literal["none", "small", "medium", "large"] | None: ...
    @spacing_above.setter
    def spacing_above(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...
    @property
    def spacing_below(self) -> Literal["none", "small", "medium", "large"] | None: ...
    @spacing_below.setter
    def spacing_below(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...

    @overload
    def add_component(self, component: Component, /, **layout_props: Unpack[_SlottedLayoutKwargs]) -> None: ...
    @overload
    def add_component(self, component: Component, /, **layout_props: Any) -> None: ...
    def __init__(
        self,
        *,
        tag: Any = ...,
        visible: bool = ...,
        tooltip: str = ...,
        role: str | list[str] | None = ...,
        content: str = ...,
        text: str = ...,
        format: str = ...,
        enable_slots: bool = ...,
        data: dict[str, Any] = ...,
        align: str = ...,
        font_size: int | float | None = ...,
        font: str = ...,
        bold: bool = ...,
        italic: bool = ...,
        underline: bool = ...,
        background: str = ...,
        border: str = ...,
        foreground: str = ...,
        spacing: SpacingPropertyValue = ...,
        spacing_above: Literal["none", "small", "medium", "large"] | None = ...,
        spacing_below: Literal["none", "small", "medium", "large"] | None = ...,
    ) -> None: ...

# ============================================================================
# Input Components
# ============================================================================

class Button(Component):
    """A clickable button component.

    [Anvil Docs](https://anvil.works/docs/client/components/basic#button)"""

    @property
    def enabled(self) -> bool: ...
    @enabled.setter
    def enabled(self, value: bool) -> None: ...
    @property
    def visible(self) -> bool: ...
    @visible.setter
    def visible(self, value: bool) -> None: ...
    @property
    def tooltip(self) -> str: ...
    @tooltip.setter
    def tooltip(self, value: str) -> None: ...
    @property
    def role(self) -> str | list[str] | None: ...
    @role.setter
    def role(self, value: str | list[str] | None) -> None: ...

    @property
    def text(self) -> str: ...
    @text.setter
    def text(self, value: str) -> None: ...
    @property
    def icon(self) -> str: ...
    @icon.setter
    def icon(self, value: str) -> None: ...
    @property
    def icon_align(self) -> str: ...
    @icon_align.setter
    def icon_align(self, value: str) -> None: ...
    @property
    def font_size(self) -> int | float | None: ...
    @font_size.setter
    def font_size(self, value: int | float | None) -> None: ...
    @property
    def font(self) -> str: ...
    @font.setter
    def font(self, value: str) -> None: ...
    @property
    def bold(self) -> bool: ...
    @bold.setter
    def bold(self, value: bool) -> None: ...
    @property
    def italic(self) -> bool: ...
    @italic.setter
    def italic(self, value: bool) -> None: ...
    @property
    def underline(self) -> bool: ...
    @underline.setter
    def underline(self, value: bool) -> None: ...
    @property
    def foreground(self) -> str: ...
    @foreground.setter
    def foreground(self, value: str) -> None: ...
    @property
    def background(self) -> str: ...
    @background.setter
    def background(self, value: str) -> None: ...
    @property
    def border(self) -> str: ...
    @border.setter
    def border(self, value: str) -> None: ...
    @property
    def align(self) -> str: ...
    @align.setter
    def align(self, value: str) -> None: ...


    @property
    def spacing(self) -> SpacingPropertyValue: ...
    @spacing.setter
    def spacing(self, value: SpacingPropertyValue) -> None: ...
    @property
    def spacing_above(self) -> Literal["none", "small", "medium", "large"] | None: ...
    @spacing_above.setter
    def spacing_above(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...
    @property
    def spacing_below(self) -> Literal["none", "small", "medium", "large"] | None: ...
    @spacing_below.setter
    def spacing_below(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...

    @override
    def add_event_handler(self, event_name: _ButtonEvents | str, handler_func: Callable[..., Any], /) -> None: ...
    @override
    def remove_event_handler(self, event_name: _ButtonEvents | str, handler_func: Callable[..., Any] | None = None, /) -> None: ...
    @override
    def set_event_handler(self, event_name: _ButtonEvents | str, handler_func: Callable[..., Any] | None, /) -> None: ...
    @override
    def raise_event(self, event_name: _ButtonEvents | str, /, **event_args: Any) -> None: ...


    def __init__(
        self,
        *,
        tag: Any = ...,
        enabled: bool = ...,
        visible: bool = ...,
        tooltip: str = ...,
        role: str | list[str] | None = ...,
        text: str = ...,
        icon: str = ...,
        icon_align: str = ...,
        font_size: int | float | None = ...,
        font: str = ...,
        bold: bool = ...,
        italic: bool = ...,
        underline: bool = ...,
        foreground: str = ...,
        background: str = ...,
        border: str = ...,
        align: str = ...,
        spacing: SpacingPropertyValue = ...,
        spacing_above: Literal["none", "small", "medium", "large"] | None = ...,
        spacing_below: Literal["none", "small", "medium", "large"] | None = ...,
    ) -> None: ...

class TextBox(Component):
    """A single-line text input component.

    [Anvil Docs](https://anvil.works/docs/client/components/basic#textbox)"""

    @property
    def enabled(self) -> bool: ...
    @enabled.setter
    def enabled(self, value: bool) -> None: ...
    @property
    def visible(self) -> bool: ...
    @visible.setter
    def visible(self, value: bool) -> None: ...
    @property
    def tooltip(self) -> str: ...
    @tooltip.setter
    def tooltip(self, value: str) -> None: ...
    @property
    def role(self) -> str | list[str] | None: ...
    @role.setter
    def role(self, value: str | list[str] | None) -> None: ...

    @property
    def text(self) -> str: ...
    @text.setter
    def text(self, value: str) -> None: ...
    @property
    def placeholder(self) -> str: ...
    @placeholder.setter
    def placeholder(self, value: str) -> None: ...
    @property
    def type(self) -> str: ...
    @type.setter
    def type(self, value: str) -> None: ...
    @property
    def hide_text(self) -> bool: ...
    @hide_text.setter
    def hide_text(self, value: bool) -> None: ...
    @property
    def font_size(self) -> int | float | None: ...
    @font_size.setter
    def font_size(self, value: int | float | None) -> None: ...
    @property
    def font(self) -> str: ...
    @font.setter
    def font(self, value: str) -> None: ...
    @property
    def bold(self) -> bool: ...
    @bold.setter
    def bold(self, value: bool) -> None: ...
    @property
    def italic(self) -> bool: ...
    @italic.setter
    def italic(self, value: bool) -> None: ...
    @property
    def underline(self) -> bool: ...
    @underline.setter
    def underline(self, value: bool) -> None: ...
    @property
    def foreground(self) -> str: ...
    @foreground.setter
    def foreground(self, value: str) -> None: ...
    @property
    def background(self) -> str: ...
    @background.setter
    def background(self, value: str) -> None: ...
    @property
    def border(self) -> str: ...
    @border.setter
    def border(self, value: str) -> None: ...
    @property
    def align(self) -> str: ...
    @align.setter
    def align(self, value: str) -> None: ...


    @property
    def margin(self) -> MarginPropertyValue: ...
    @margin.setter
    def margin(self, value: MarginPropertyValue) -> None: ...
    @property
    def spacing_above(self) -> Literal["none", "small", "medium", "large"] | None: ...
    @spacing_above.setter
    def spacing_above(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...
    @property
    def spacing_below(self) -> Literal["none", "small", "medium", "large"] | None: ...
    @spacing_below.setter
    def spacing_below(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...

    @override
    def add_event_handler(self, event_name: _TextBoxEvents | str, handler_func: Callable[..., Any], /) -> None: ...
    @override
    def remove_event_handler(self, event_name: _TextBoxEvents | str, handler_func: Callable[..., Any] | None = None, /) -> None: ...
    @override
    def set_event_handler(self, event_name: _TextBoxEvents | str, handler_func: Callable[..., Any] | None, /) -> None: ...
    @override
    def raise_event(self, event_name: _TextBoxEvents | str, /, **event_args: Any) -> None: ...

    def focus(self) -> None:
        """Set focus to this text box.

        [Anvil Docs](https://anvil.works/docs/client/components/basic#textbox)"""
        ...

    def select(self) -> None:
        """Select all text in this text box.

        [Anvil Docs](https://anvil.works/docs/client/components/basic#textbox)"""
        ...


    def __init__(
        self,
        *,
        tag: Any = ...,
        enabled: bool = ...,
        visible: bool = ...,
        tooltip: str = ...,
        role: str | list[str] | None = ...,
        text: str = ...,
        placeholder: str = ...,
        type: str = ...,
        hide_text: bool = ...,
        font_size: int | float | None = ...,
        font: str = ...,
        bold: bool = ...,
        italic: bool = ...,
        underline: bool = ...,
        foreground: str = ...,
        background: str = ...,
        border: str = ...,
        align: str = ...,
        margin: MarginPropertyValue = ...,
        spacing_above: Literal["none", "small", "medium", "large"] | None = ...,
        spacing_below: Literal["none", "small", "medium", "large"] | None = ...,
    ) -> None: ...

class TextArea(Component):
    """A multi-line text input component.

    [Anvil Docs](https://anvil.works/docs/client/components/basic#textarea)"""

    @property
    def enabled(self) -> bool: ...
    @enabled.setter
    def enabled(self, value: bool) -> None: ...
    @property
    def visible(self) -> bool: ...
    @visible.setter
    def visible(self, value: bool) -> None: ...
    @property
    def tooltip(self) -> str: ...
    @tooltip.setter
    def tooltip(self, value: str) -> None: ...
    @property
    def role(self) -> str | list[str] | None: ...
    @role.setter
    def role(self, value: str | list[str] | None) -> None: ...

    @property
    def text(self) -> str: ...
    @text.setter
    def text(self, value: str) -> None: ...
    @property
    def placeholder(self) -> str: ...
    @placeholder.setter
    def placeholder(self, value: str) -> None: ...
    @property
    def auto_expand(self) -> bool: ...
    @auto_expand.setter
    def auto_expand(self, value: bool) -> None: ...
    @property
    def height(self) -> str: ...
    @height.setter
    def height(self, value: str) -> None: ...
    @property
    def font_size(self) -> int | float | None: ...
    @font_size.setter
    def font_size(self, value: int | float | None) -> None: ...
    @property
    def font(self) -> str: ...
    @font.setter
    def font(self, value: str) -> None: ...
    @property
    def bold(self) -> bool: ...
    @bold.setter
    def bold(self, value: bool) -> None: ...
    @property
    def italic(self) -> bool: ...
    @italic.setter
    def italic(self, value: bool) -> None: ...
    @property
    def underline(self) -> bool: ...
    @underline.setter
    def underline(self, value: bool) -> None: ...
    @property
    def foreground(self) -> str: ...
    @foreground.setter
    def foreground(self, value: str) -> None: ...
    @property
    def background(self) -> str: ...
    @background.setter
    def background(self, value: str) -> None: ...
    @property
    def border(self) -> str: ...
    @border.setter
    def border(self, value: str) -> None: ...


    @property
    def align(self) -> str: ...
    @align.setter
    def align(self, value: str) -> None: ...
    @property
    def margin(self) -> MarginPropertyValue: ...
    @margin.setter
    def margin(self, value: MarginPropertyValue) -> None: ...
    @property
    def spacing_above(self) -> Literal["none", "small", "medium", "large"] | None: ...
    @spacing_above.setter
    def spacing_above(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...
    @property
    def spacing_below(self) -> Literal["none", "small", "medium", "large"] | None: ...
    @spacing_below.setter
    def spacing_below(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...

    @override
    def add_event_handler(self, event_name: _TextAreaEvents | str, handler_func: Callable[..., Any], /) -> None: ...
    @override
    def remove_event_handler(self, event_name: _TextAreaEvents | str, handler_func: Callable[..., Any] | None = None, /) -> None: ...
    @override
    def set_event_handler(self, event_name: _TextAreaEvents | str, handler_func: Callable[..., Any] | None, /) -> None: ...
    @override
    def raise_event(self, event_name: _TextAreaEvents | str, /, **event_args: Any) -> None: ...

    def focus(self) -> None:
        """Set focus to this text area.

        [Anvil Docs](https://anvil.works/docs/client/components/basic#textarea)"""
        ...

    def select(self) -> None:
        """Select all text in this text area.

        [Anvil Docs](https://anvil.works/docs/client/components/basic#textarea)"""
        ...


    def __init__(
        self,
        *,
        tag: Any = ...,
        enabled: bool = ...,
        visible: bool = ...,
        tooltip: str = ...,
        role: str | list[str] | None = ...,
        text: str = ...,
        placeholder: str = ...,
        auto_expand: bool = ...,
        height: str = ...,
        font_size: int | float | None = ...,
        font: str = ...,
        bold: bool = ...,
        italic: bool = ...,
        underline: bool = ...,
        foreground: str = ...,
        background: str = ...,
        border: str = ...,
        align: str = ...,
        margin: MarginPropertyValue = ...,
        spacing_above: Literal["none", "small", "medium", "large"] | None = ...,
        spacing_below: Literal["none", "small", "medium", "large"] | None = ...,
    ) -> None: ...

class CheckBox(Component):
    """A checkbox input component.

    [Anvil Docs](https://anvil.works/docs/client/components/basic#checkbox)"""

    @property
    def enabled(self) -> bool: ...
    @enabled.setter
    def enabled(self, value: bool) -> None: ...
    @property
    def visible(self) -> bool: ...
    @visible.setter
    def visible(self, value: bool) -> None: ...
    @property
    def tooltip(self) -> str: ...
    @tooltip.setter
    def tooltip(self, value: str) -> None: ...
    @property
    def role(self) -> str | list[str] | None: ...
    @role.setter
    def role(self, value: str | list[str] | None) -> None: ...

    @property
    def checked(self) -> bool: ...
    @checked.setter
    def checked(self, value: bool) -> None: ...
    @property
    def allow_indeterminate(self) -> bool: ...
    @allow_indeterminate.setter
    def allow_indeterminate(self, value: bool) -> None: ...
    @property
    def text(self) -> str: ...
    @text.setter
    def text(self, value: str) -> None: ...
    @property
    def font_size(self) -> int | float | None: ...
    @font_size.setter
    def font_size(self, value: int | float | None) -> None: ...
    @property
    def font(self) -> str: ...
    @font.setter
    def font(self, value: str) -> None: ...
    @property
    def bold(self) -> bool: ...
    @bold.setter
    def bold(self, value: bool) -> None: ...
    @property
    def italic(self) -> bool: ...
    @italic.setter
    def italic(self, value: bool) -> None: ...
    @property
    def underline(self) -> bool: ...
    @underline.setter
    def underline(self, value: bool) -> None: ...
    @property
    def foreground(self) -> str: ...
    @foreground.setter
    def foreground(self, value: str) -> None: ...
    @property
    def background(self) -> str: ...
    @background.setter
    def background(self, value: str) -> None: ...
    @property
    def border(self) -> str: ...
    @border.setter
    def border(self, value: str) -> None: ...
    @property
    def align(self) -> str: ...
    @align.setter
    def align(self, value: str) -> None: ...


    @property
    def spacing(self) -> SpacingPropertyValue: ...
    @spacing.setter
    def spacing(self, value: SpacingPropertyValue) -> None: ...
    @property
    def spacing_above(self) -> Literal["none", "small", "medium", "large"] | None: ...
    @spacing_above.setter
    def spacing_above(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...
    @property
    def spacing_below(self) -> Literal["none", "small", "medium", "large"] | None: ...
    @spacing_below.setter
    def spacing_below(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...

    @override
    def add_event_handler(self, event_name: _CheckBoxEvents | str, handler_func: Callable[..., Any], /) -> None: ...
    @override
    def remove_event_handler(self, event_name: _CheckBoxEvents | str, handler_func: Callable[..., Any] | None = None, /) -> None: ...
    @override
    def set_event_handler(self, event_name: _CheckBoxEvents | str, handler_func: Callable[..., Any] | None, /) -> None: ...
    @override
    def raise_event(self, event_name: _CheckBoxEvents | str, /, **event_args: Any) -> None: ...

    def focus(self) -> None:
        """Set keyboard focus to this checkbox."""
        ...


    def __init__(
        self,
        *,
        tag: Any = ...,
        enabled: bool = ...,
        visible: bool = ...,
        tooltip: str = ...,
        role: str | list[str] | None = ...,
        checked: bool = ...,
        allow_indeterminate: bool = ...,
        text: str = ...,
        font_size: int | float | None = ...,
        font: str = ...,
        bold: bool = ...,
        italic: bool = ...,
        underline: bool = ...,
        foreground: str = ...,
        background: str = ...,
        border: str = ...,
        align: str = ...,
        spacing: SpacingPropertyValue = ...,
        spacing_above: Literal["none", "small", "medium", "large"] | None = ...,
        spacing_below: Literal["none", "small", "medium", "large"] | None = ...,
    ) -> None: ...

class RadioButton(Component):
    """A radio button input component.

    [Anvil Docs](https://anvil.works/docs/client/components/basic#radiobutton)"""

    @property
    def enabled(self) -> bool: ...
    @enabled.setter
    def enabled(self, value: bool) -> None: ...
    @property
    def visible(self) -> bool: ...
    @visible.setter
    def visible(self, value: bool) -> None: ...
    @property
    def tooltip(self) -> str: ...
    @tooltip.setter
    def tooltip(self, value: str) -> None: ...
    @property
    def role(self) -> str | list[str] | None: ...
    @role.setter
    def role(self, value: str | list[str] | None) -> None: ...

    @property
    def selected(self) -> bool: ...
    @selected.setter
    def selected(self, value: bool) -> None: ...
    @property
    def value(self) -> Any: ...
    @value.setter
    def value(self, value: Any) -> None: ...
    @property
    def group_name(self) -> str: ...
    @group_name.setter
    def group_name(self, value: str) -> None: ...
    @property
    def text(self) -> str: ...
    @text.setter
    def text(self, value: str) -> None: ...
    @property
    def font_size(self) -> int | float | None: ...
    @font_size.setter
    def font_size(self, value: int | float | None) -> None: ...
    @property
    def font(self) -> str: ...
    @font.setter
    def font(self, value: str) -> None: ...
    @property
    def bold(self) -> bool: ...
    @bold.setter
    def bold(self, value: bool) -> None: ...
    @property
    def italic(self) -> bool: ...
    @italic.setter
    def italic(self, value: bool) -> None: ...
    @property
    def underline(self) -> bool: ...
    @underline.setter
    def underline(self, value: bool) -> None: ...
    @property
    def foreground(self) -> str: ...
    @foreground.setter
    def foreground(self, value: str) -> None: ...
    @property
    def background(self) -> str: ...
    @background.setter
    def background(self, value: str) -> None: ...
    @property
    def border(self) -> str: ...
    @border.setter
    def border(self, value: str) -> None: ...
    @property
    def align(self) -> str: ...
    @align.setter
    def align(self, value: str) -> None: ...


    @property
    def spacing(self) -> SpacingPropertyValue: ...
    @spacing.setter
    def spacing(self, value: SpacingPropertyValue) -> None: ...
    @property
    def spacing_above(self) -> Literal["none", "small", "medium", "large"] | None: ...
    @spacing_above.setter
    def spacing_above(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...
    @property
    def spacing_below(self) -> Literal["none", "small", "medium", "large"] | None: ...
    @spacing_below.setter
    def spacing_below(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...

    @override
    def add_event_handler(self, event_name: _RadioButtonEvents | str, handler_func: Callable[..., Any], /) -> None: ...
    @override
    def remove_event_handler(self, event_name: _RadioButtonEvents | str, handler_func: Callable[..., Any] | None = None, /) -> None: ...
    @override
    def set_event_handler(self, event_name: _RadioButtonEvents | str, handler_func: Callable[..., Any] | None, /) -> None: ...
    @override
    def raise_event(self, event_name: _RadioButtonEvents | str, /, **event_args: Any) -> None: ...

    @staticmethod
    def get_group_value(group_name: str) -> Any:
        """Get the selected value from a radio button group.

        [Anvil Docs](https://anvil.works/docs/client/components/basic#radiobutton)"""
        ...


    def __init__(
        self,
        *,
        tag: Any = ...,
        enabled: bool = ...,
        visible: bool = ...,
        tooltip: str = ...,
        role: str | list[str] | None = ...,
        selected: bool = ...,
        value: Any = ...,
        group_name: str = ...,
        text: str = ...,
        font_size: int | float | None = ...,
        font: str = ...,
        bold: bool = ...,
        italic: bool = ...,
        underline: bool = ...,
        foreground: str = ...,
        background: str = ...,
        border: str = ...,
        align: str = ...,
        spacing: SpacingPropertyValue = ...,
        spacing_above: Literal["none", "small", "medium", "large"] | None = ...,
        spacing_below: Literal["none", "small", "medium", "large"] | None = ...,
    ) -> None: ...

class DropDown(Component):
    """A dropdown selection component.

    [Anvil Docs](https://anvil.works/docs/client/components/basic#dropdown)"""

    @property
    def enabled(self) -> bool: ...
    @enabled.setter
    def enabled(self, value: bool) -> None: ...
    @property
    def visible(self) -> bool: ...
    @visible.setter
    def visible(self, value: bool) -> None: ...
    @property
    def tooltip(self) -> str: ...
    @tooltip.setter
    def tooltip(self, value: str) -> None: ...
    @property
    def role(self) -> str | list[str] | None: ...
    @role.setter
    def role(self, value: str | list[str] | None) -> None: ...

    @property
    def items(self) -> list[Any]: ...
    @items.setter
    def items(self, value: list[Any]) -> None: ...
    @property
    def selected_value(self) -> Any: ...
    @selected_value.setter
    def selected_value(self, value: Any) -> None: ...
    @property
    def include_placeholder(self) -> bool: ...
    @include_placeholder.setter
    def include_placeholder(self, value: bool) -> None: ...
    @property
    def placeholder(self) -> str: ...
    @placeholder.setter
    def placeholder(self, value: str) -> None: ...
    @property
    def font_size(self) -> int | float | None: ...
    @font_size.setter
    def font_size(self, value: int | float | None) -> None: ...
    @property
    def font(self) -> str: ...
    @font.setter
    def font(self, value: str) -> None: ...
    @property
    def bold(self) -> bool: ...
    @bold.setter
    def bold(self, value: bool) -> None: ...
    @property
    def italic(self) -> bool: ...
    @italic.setter
    def italic(self, value: bool) -> None: ...
    @property
    def underline(self) -> bool: ...
    @underline.setter
    def underline(self, value: bool) -> None: ...
    @property
    def foreground(self) -> str: ...
    @foreground.setter
    def foreground(self, value: str) -> None: ...
    @property
    def background(self) -> str: ...
    @background.setter
    def background(self, value: str) -> None: ...
    @property
    def border(self) -> str: ...
    @border.setter
    def border(self, value: str) -> None: ...
    @property
    def align(self) -> str: ...
    @align.setter
    def align(self, value: str) -> None: ...


    @property
    def margin(self) -> MarginPropertyValue: ...
    @margin.setter
    def margin(self, value: MarginPropertyValue) -> None: ...
    @property
    def spacing_above(self) -> Literal["none", "small", "medium", "large"] | None: ...
    @spacing_above.setter
    def spacing_above(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...
    @property
    def spacing_below(self) -> Literal["none", "small", "medium", "large"] | None: ...
    @spacing_below.setter
    def spacing_below(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...

    @override
    def add_event_handler(self, event_name: _DropDownEvents | str, handler_func: Callable[..., Any], /) -> None: ...
    @override
    def remove_event_handler(self, event_name: _DropDownEvents | str, handler_func: Callable[..., Any] | None = None, /) -> None: ...
    @override
    def set_event_handler(self, event_name: _DropDownEvents | str, handler_func: Callable[..., Any] | None, /) -> None: ...
    @override
    def raise_event(self, event_name: _DropDownEvents | str, /, **event_args: Any) -> None: ...

    def focus(self) -> None:
        """Set keyboard focus to this drop-down menu."""
        ...


    def __init__(
        self,
        *,
        tag: Any = ...,
        enabled: bool = ...,
        visible: bool = ...,
        tooltip: str = ...,
        role: str | list[str] | None = ...,
        items: list[Any] = ...,
        selected_value: Any = ...,
        include_placeholder: bool = ...,
        placeholder: str = ...,
        font_size: int | float | None = ...,
        font: str = ...,
        bold: bool = ...,
        italic: bool = ...,
        underline: bool = ...,
        foreground: str = ...,
        background: str = ...,
        border: str = ...,
        align: str = ...,
        margin: MarginPropertyValue = ...,
        spacing_above: Literal["none", "small", "medium", "large"] | None = ...,
        spacing_below: Literal["none", "small", "medium", "large"] | None = ...,
    ) -> None: ...

class DatePicker(Component):
    """A date picker input component.

    [Anvil Docs](https://anvil.works/docs/client/components/basic#datepicker)"""

    @property
    def enabled(self) -> bool: ...
    @enabled.setter
    def enabled(self, value: bool) -> None: ...
    @property
    def visible(self) -> bool: ...
    @visible.setter
    def visible(self, value: bool) -> None: ...
    @property
    def tooltip(self) -> str: ...
    @tooltip.setter
    def tooltip(self, value: str) -> None: ...
    @property
    def role(self) -> str | list[str] | None: ...
    @role.setter
    def role(self, value: str | list[str] | None) -> None: ...

    @property
    def date(self) -> Any: ...  # datetime.date | None
    @date.setter
    def date(self, value: Any) -> None: ...  # datetime.date | None
    @property
    def min_date(self) -> Any: ...
    @min_date.setter
    def min_date(self, value: Any) -> None: ...
    @property
    def max_date(self) -> Any: ...
    @max_date.setter
    def max_date(self, value: Any) -> None: ...
    @property
    def format(self) -> str: ...
    @format.setter
    def format(self, value: str) -> None: ...
    @property
    def pick_time(self) -> bool: ...
    @pick_time.setter
    def pick_time(self, value: bool) -> None: ...
    @property
    def placeholder(self) -> str: ...
    @placeholder.setter
    def placeholder(self, value: str) -> None: ...
    @property
    def font_size(self) -> int | float | None: ...
    @font_size.setter
    def font_size(self, value: int | float | None) -> None: ...
    @property
    def font(self) -> str: ...
    @font.setter
    def font(self, value: str) -> None: ...
    @property
    def bold(self) -> bool: ...
    @bold.setter
    def bold(self, value: bool) -> None: ...
    @property
    def italic(self) -> bool: ...
    @italic.setter
    def italic(self, value: bool) -> None: ...
    @property
    def underline(self) -> bool: ...
    @underline.setter
    def underline(self, value: bool) -> None: ...
    @property
    def foreground(self) -> str: ...
    @foreground.setter
    def foreground(self, value: str) -> None: ...
    @property
    def background(self) -> str: ...
    @background.setter
    def background(self, value: str) -> None: ...
    @property
    def border(self) -> str: ...
    @border.setter
    def border(self, value: str) -> None: ...
    @property
    def align(self) -> str: ...
    @align.setter
    def align(self, value: str) -> None: ...


    @property
    def margin(self) -> MarginPropertyValue: ...
    @margin.setter
    def margin(self, value: MarginPropertyValue) -> None: ...
    @property
    def spacing_above(self) -> Literal["none", "small", "medium", "large"] | None: ...
    @spacing_above.setter
    def spacing_above(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...
    @property
    def spacing_below(self) -> Literal["none", "small", "medium", "large"] | None: ...
    @spacing_below.setter
    def spacing_below(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...

    @override
    def add_event_handler(self, event_name: _DatePickerEvents | str, handler_func: Callable[..., Any], /) -> None: ...
    @override
    def remove_event_handler(self, event_name: _DatePickerEvents | str, handler_func: Callable[..., Any] | None = None, /) -> None: ...
    @override
    def set_event_handler(self, event_name: _DatePickerEvents | str, handler_func: Callable[..., Any] | None, /) -> None: ...
    @override
    def raise_event(self, event_name: _DatePickerEvents | str, /, **event_args: Any) -> None: ...

    def focus(self) -> None:
        """Set keyboard focus to this date picker."""
        ...


    def __init__(
        self,
        *,
        tag: Any = ...,
        enabled: bool = ...,
        visible: bool = ...,
        tooltip: str = ...,
        role: str | list[str] | None = ...,
        date: Any = ...,
        min_date: Any = ...,
        max_date: Any = ...,
        format: str = ...,
        pick_time: bool = ...,
        placeholder: str = ...,
        font_size: int | float | None = ...,
        font: str = ...,
        bold: bool = ...,
        italic: bool = ...,
        underline: bool = ...,
        foreground: str = ...,
        background: str = ...,
        border: str = ...,
        align: str = ...,
        margin: MarginPropertyValue = ...,
        spacing_above: Literal["none", "small", "medium", "large"] | None = ...,
        spacing_below: Literal["none", "small", "medium", "large"] | None = ...,
    ) -> None: ...

class FileLoader(Component):
    """A file upload component.

    [Anvil Docs](https://anvil.works/docs/client/components/basic#fileloader)"""

    @property
    def enabled(self) -> bool: ...
    @enabled.setter
    def enabled(self, value: bool) -> None: ...
    @property
    def visible(self) -> bool: ...
    @visible.setter
    def visible(self, value: bool) -> None: ...
    @property
    def tooltip(self) -> str: ...
    @tooltip.setter
    def tooltip(self, value: str) -> None: ...
    @property
    def role(self) -> str | list[str] | None: ...
    @role.setter
    def role(self, value: str | list[str] | None) -> None: ...

    @property
    def file(self) -> Media | None: ...
    @file.setter
    def file(self, value: Media | None) -> None: ...
    @property
    def files(self) -> list[Media]: ...
    @files.setter
    def files(self, value: list[Media]) -> None: ...
    @property
    def multiple(self) -> bool: ...
    @multiple.setter
    def multiple(self, value: bool) -> None: ...
    @property
    def show_state(self) -> bool: ...
    @show_state.setter
    def show_state(self, value: bool) -> None: ...
    @property
    def file_types(self) -> str: ...
    @file_types.setter
    def file_types(self, value: str) -> None: ...
    @property
    def text(self) -> str: ...
    @text.setter
    def text(self, value: str) -> None: ...
    @property
    def font_size(self) -> int | float | None: ...
    @font_size.setter
    def font_size(self, value: int | float | None) -> None: ...
    @property
    def font(self) -> str: ...
    @font.setter
    def font(self, value: str) -> None: ...
    @property
    def bold(self) -> bool: ...
    @bold.setter
    def bold(self, value: bool) -> None: ...
    @property
    def italic(self) -> bool: ...
    @italic.setter
    def italic(self, value: bool) -> None: ...
    @property
    def underline(self) -> bool: ...
    @underline.setter
    def underline(self, value: bool) -> None: ...
    @property
    def foreground(self) -> str: ...
    @foreground.setter
    def foreground(self, value: str) -> None: ...
    @property
    def background(self) -> str: ...
    @background.setter
    def background(self, value: str) -> None: ...
    @property
    def border(self) -> str: ...
    @border.setter
    def border(self, value: str) -> None: ...
    @property
    def align(self) -> str: ...
    @align.setter
    def align(self, value: str) -> None: ...
    @property
    def icon(self) -> str: ...
    @icon.setter
    def icon(self, value: str) -> None: ...
    @property
    def icon_align(self) -> str: ...
    @icon_align.setter
    def icon_align(self, value: str) -> None: ...


    @property
    def spacing(self) -> SpacingPropertyValue: ...
    @spacing.setter
    def spacing(self, value: SpacingPropertyValue) -> None: ...
    @property
    def spacing_above(self) -> Literal["none", "small", "medium", "large"] | None: ...
    @spacing_above.setter
    def spacing_above(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...
    @property
    def spacing_below(self) -> Literal["none", "small", "medium", "large"] | None: ...
    @spacing_below.setter
    def spacing_below(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...

    @override
    def add_event_handler(self, event_name: _FileLoaderEvents | str, handler_func: Callable[..., Any], /) -> None: ...
    @override
    def remove_event_handler(self, event_name: _FileLoaderEvents | str, handler_func: Callable[..., Any] | None = None, /) -> None: ...
    @override
    def set_event_handler(self, event_name: _FileLoaderEvents | str, handler_func: Callable[..., Any] | None, /) -> None: ...
    @override
    def raise_event(self, event_name: _FileLoaderEvents | str, /, **event_args: Any) -> None: ...

    def open_file_selector(self) -> None:
        """Open the browser's file selector.

        Call this from another component's ``click`` event handler."""
        ...

    def focus(self) -> None:
        """Set keyboard focus to this file loader."""
        ...

    def clear(self) -> None:
        """Clear the selected file(s).

        [Anvil Docs](https://anvil.works/docs/client/components/basic#fileloader)"""
        ...


    def __init__(
        self,
        *,
        tag: Any = ...,
        enabled: bool = ...,
        visible: bool = ...,
        tooltip: str = ...,
        role: str | list[str] | None = ...,
        file: Media | None = ...,
        files: list[Media] = ...,
        multiple: bool = ...,
        show_state: bool = ...,
        file_types: str = ...,
        text: str = ...,
        font_size: int | float | None = ...,
        font: str = ...,
        bold: bool = ...,
        italic: bool = ...,
        underline: bool = ...,
        foreground: str = ...,
        background: str = ...,
        border: str = ...,
        align: str = ...,
        icon: str = ...,
        icon_align: str = ...,
        spacing: SpacingPropertyValue = ...,
        spacing_above: Literal["none", "small", "medium", "large"] | None = ...,
        spacing_below: Literal["none", "small", "medium", "large"] | None = ...,
    ) -> None: ...

# ============================================================================
# Container Components
# ============================================================================

class ColumnPanel(Container):
    """A container that arranges components vertically.

    [Anvil Docs](https://anvil.works/docs/client/components/containers#columnpanel)"""

    @property
    def visible(self) -> bool: ...
    @visible.setter
    def visible(self, value: bool) -> None: ...
    @property
    def tooltip(self) -> str: ...
    @tooltip.setter
    def tooltip(self, value: str) -> None: ...
    @property
    def role(self) -> str | list[str] | None: ...
    @role.setter
    def role(self, value: str | list[str] | None) -> None: ...

    @property
    def col_widths(self) -> str: ...
    @col_widths.setter
    def col_widths(self, value: str) -> None: ...
    @property
    def col_spacing(self) -> str: ...
    @col_spacing.setter
    def col_spacing(self, value: str) -> None: ...
    @property
    def wrap_on(self) -> str: ...
    @wrap_on.setter
    def wrap_on(self, value: str) -> None: ...
    @property
    def background(self) -> str: ...
    @background.setter
    def background(self, value: str) -> None: ...
    @property
    def foreground(self) -> str: ...
    @foreground.setter
    def foreground(self, value: str) -> None: ...
    @property
    def border(self) -> str: ...
    @border.setter
    def border(self, value: str) -> None: ...
    @property
    def spacing_above(self) -> Literal["none", "small", "medium", "large"] | None: ...
    @spacing_above.setter
    def spacing_above(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...
    @property
    def spacing_below(self) -> Literal["none", "small", "medium", "large"] | None: ...
    @spacing_below.setter
    def spacing_below(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...


    @property
    def spacing(self) -> SpacingPropertyValue: ...
    @spacing.setter
    def spacing(self, value: SpacingPropertyValue) -> None: ...

    @overload
    def add_component(self, component: Component, /, **layout_props: Unpack[_ColumnPanelLayoutKwargs]) -> None: ...
    @overload
    def add_component(self, component: Component, /, **layout_props: Any) -> None: ...

    def __init__(
        self,
        *,
        tag: Any = ...,
        visible: bool = ...,
        tooltip: str = ...,
        role: str | list[str] | None = ...,
        col_widths: str = ...,
        col_spacing: str = ...,
        wrap_on: str = ...,
        background: str = ...,
        foreground: str = ...,
        border: str = ...,
        spacing_above: Literal["none", "small", "medium", "large"] | None = ...,
        spacing_below: Literal["none", "small", "medium", "large"] | None = ...,
        spacing: SpacingPropertyValue = ...,
    ) -> None: ...

class FlowPanel(Container):
    """A container that arranges components in a flowing layout.

    [Anvil Docs](https://anvil.works/docs/client/components/containers#flowpanel)"""

    @property
    def visible(self) -> bool: ...
    @visible.setter
    def visible(self, value: bool) -> None: ...
    @property
    def tooltip(self) -> str: ...
    @tooltip.setter
    def tooltip(self, value: str) -> None: ...
    @property
    def role(self) -> str | list[str] | None: ...
    @role.setter
    def role(self, value: str | list[str] | None) -> None: ...

    @property
    def align(self) -> str: ...
    @align.setter
    def align(self, value: str) -> None: ...
    @property
    def spacing(self) -> SpacingPropertyValue: ...
    @spacing.setter
    def spacing(self, value: SpacingPropertyValue) -> None: ...
    @property
    def vertical_align(self) -> str: ...
    @vertical_align.setter
    def vertical_align(self, value: str) -> None: ...
    @property
    def background(self) -> str: ...
    @background.setter
    def background(self, value: str) -> None: ...
    @property
    def foreground(self) -> str: ...
    @foreground.setter
    def foreground(self, value: str) -> None: ...
    @property
    def border(self) -> str: ...
    @border.setter
    def border(self, value: str) -> None: ...
    @property
    def spacing_above(self) -> Literal["none", "small", "medium", "large"] | None: ...
    @spacing_above.setter
    def spacing_above(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...
    @property
    def spacing_below(self) -> Literal["none", "small", "medium", "large"] | None: ...
    @spacing_below.setter
    def spacing_below(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...


    @property
    def gap(self) -> str: ...
    @gap.setter
    def gap(self, value: str) -> None: ...

    @overload
    def add_component(self, component: Component, /, **layout_props: Unpack[_FlowPanelLayoutKwargs]) -> None: ...
    @overload
    def add_component(self, component: Component, /, **layout_props: Any) -> None: ...

    def __init__(
        self,
        *,
        tag: Any = ...,
        visible: bool = ...,
        tooltip: str = ...,
        role: str | list[str] | None = ...,
        align: str = ...,
        spacing: SpacingPropertyValue = ...,
        vertical_align: str = ...,
        background: str = ...,
        foreground: str = ...,
        border: str = ...,
        spacing_above: Literal["none", "small", "medium", "large"] | None = ...,
        spacing_below: Literal["none", "small", "medium", "large"] | None = ...,
        gap: str = ...,
    ) -> None: ...

class LinearPanel(Container):
    """A container that arranges components in a linear layout.

    [Anvil Docs](https://anvil.works/docs/client/components/containers#linearpanel)"""

    @property
    def visible(self) -> bool: ...
    @visible.setter
    def visible(self, value: bool) -> None: ...
    @property
    def tooltip(self) -> str: ...
    @tooltip.setter
    def tooltip(self, value: str) -> None: ...
    @property
    def role(self) -> str | list[str] | None: ...
    @role.setter
    def role(self, value: str | list[str] | None) -> None: ...

    @property
    def background(self) -> str: ...
    @background.setter
    def background(self, value: str) -> None: ...
    @property
    def foreground(self) -> str: ...
    @foreground.setter
    def foreground(self, value: str) -> None: ...
    @property
    def border(self) -> str: ...
    @border.setter
    def border(self, value: str) -> None: ...
    @property
    def spacing_above(self) -> Literal["none", "small", "medium", "large"] | None: ...
    @spacing_above.setter
    def spacing_above(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...
    @property
    def spacing_below(self) -> Literal["none", "small", "medium", "large"] | None: ...
    @spacing_below.setter
    def spacing_below(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...


    @property
    def spacing(self) -> SpacingPropertyValue: ...
    @spacing.setter
    def spacing(self, value: SpacingPropertyValue) -> None: ...

    @overload
    def add_component(self, component: Component, /, **layout_props: Unpack[_IndexLayoutKwargs]) -> None: ...
    @overload
    def add_component(self, component: Component, /, **layout_props: Any) -> None: ...

    def __init__(
        self,
        *,
        tag: Any = ...,
        visible: bool = ...,
        tooltip: str = ...,
        role: str | list[str] | None = ...,
        background: str = ...,
        foreground: str = ...,
        border: str = ...,
        spacing_above: Literal["none", "small", "medium", "large"] | None = ...,
        spacing_below: Literal["none", "small", "medium", "large"] | None = ...,
        spacing: SpacingPropertyValue = ...,
    ) -> None: ...

class GridPanel(Container):
    """A container that arranges components in a grid.

    [Anvil Docs](https://anvil.works/docs/client/components/containers#gridpanel)"""

    @property
    def visible(self) -> bool: ...
    @visible.setter
    def visible(self, value: bool) -> None: ...
    @property
    def tooltip(self) -> str: ...
    @tooltip.setter
    def tooltip(self, value: str) -> None: ...
    @property
    def role(self) -> str | list[str] | None: ...
    @role.setter
    def role(self, value: str | list[str] | None) -> None: ...

    @property
    def background(self) -> str: ...
    @background.setter
    def background(self, value: str) -> None: ...
    @property
    def foreground(self) -> str: ...
    @foreground.setter
    def foreground(self, value: str) -> None: ...
    @property
    def border(self) -> str: ...
    @border.setter
    def border(self, value: str) -> None: ...


    @property
    def spacing(self) -> SpacingPropertyValue: ...
    @spacing.setter
    def spacing(self, value: SpacingPropertyValue) -> None: ...
    @property
    def spacing_above(self) -> Literal["none", "small", "medium", "large"] | None: ...
    @spacing_above.setter
    def spacing_above(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...
    @property
    def spacing_below(self) -> Literal["none", "small", "medium", "large"] | None: ...
    @spacing_below.setter
    def spacing_below(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...

    @overload
    def add_component(self, component: Component, /, **layout_props: Unpack[_GridPanelLayoutKwargs]) -> None: ...
    @overload
    def add_component(self, component: Component, /, **layout_props: Any) -> None: ...

    def __init__(
        self,
        *,
        tag: Any = ...,
        visible: bool = ...,
        tooltip: str = ...,
        role: str | list[str] | None = ...,
        background: str = ...,
        foreground: str = ...,
        border: str = ...,
        spacing: SpacingPropertyValue = ...,
        spacing_above: Literal["none", "small", "medium", "large"] | None = ...,
        spacing_below: Literal["none", "small", "medium", "large"] | None = ...,
    ) -> None: ...

class XYPanel(Container):
    """A container that positions components at absolute coordinates.

    [Anvil Docs](https://anvil.works/docs/client/components/containers#xypanel)"""

    @property
    def visible(self) -> bool: ...
    @visible.setter
    def visible(self, value: bool) -> None: ...
    @property
    def tooltip(self) -> str: ...
    @tooltip.setter
    def tooltip(self, value: str) -> None: ...
    @property
    def role(self) -> str | list[str] | None: ...
    @role.setter
    def role(self, value: str | list[str] | None) -> None: ...

    @property
    def background(self) -> str: ...
    @background.setter
    def background(self, value: str) -> None: ...
    @property
    def foreground(self) -> str: ...
    @foreground.setter
    def foreground(self, value: str) -> None: ...
    @property
    def border(self) -> str: ...
    @border.setter
    def border(self, value: str) -> None: ...
    @property
    def height(self) -> str: ...
    @height.setter
    def height(self, value: str) -> None: ...
    @property
    def width(self) -> str: ...
    @width.setter
    def width(self, value: str) -> None: ...


    @property
    def align(self) -> str: ...
    @align.setter
    def align(self, value: str) -> None: ...
    @property
    def margin(self) -> MarginPropertyValue: ...
    @margin.setter
    def margin(self, value: MarginPropertyValue) -> None: ...
    @property
    def spacing_above(self) -> Literal["none", "small", "medium", "large"] | None: ...
    @spacing_above.setter
    def spacing_above(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...
    @property
    def spacing_below(self) -> Literal["none", "small", "medium", "large"] | None: ...
    @spacing_below.setter
    def spacing_below(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...

    @overload
    def add_component(self, component: Component, /, **layout_props: Unpack[_XYPanelLayoutKwargs]) -> None: ...
    @overload
    def add_component(self, component: Component, /, **layout_props: Any) -> None: ...

    def get_width(self) -> int | float:
        """Get this panel's width in pixels."""
        ...

    def __init__(
        self,
        *,
        tag: Any = ...,
        visible: bool = ...,
        tooltip: str = ...,
        role: str | list[str] | None = ...,
        background: str = ...,
        foreground: str = ...,
        border: str = ...,
        height: str = ...,
        width: str = ...,
        align: str = ...,
        margin: MarginPropertyValue = ...,
        spacing_above: Literal["none", "small", "medium", "large"] | None = ...,
        spacing_below: Literal["none", "small", "medium", "large"] | None = ...,
    ) -> None: ...

class DataGrid(Container):
    """A data grid component for displaying tabular data.

    [Anvil Docs](https://anvil.works/docs/client/components/data-grids)"""

    @property
    def visible(self) -> bool: ...
    @visible.setter
    def visible(self, value: bool) -> None: ...
    @property
    def tooltip(self) -> str: ...
    @tooltip.setter
    def tooltip(self, value: str) -> None: ...
    @property
    def role(self) -> str | list[str] | None: ...
    @role.setter
    def role(self, value: str | list[str] | None) -> None: ...

    @property
    def columns(self) -> list[dict[str, Any]]: ...
    @columns.setter
    def columns(self, value: list[dict[str, Any]]) -> None: ...
    @property
    def rows_per_page(self) -> int | None: ...
    @rows_per_page.setter
    def rows_per_page(self, value: int | None) -> None: ...
    @property
    def show_page_controls(self) -> bool: ...
    @show_page_controls.setter
    def show_page_controls(self, value: bool) -> None: ...
    @property
    def auto_header(self) -> bool: ...
    @auto_header.setter
    def auto_header(self, value: bool) -> None: ...
    @property
    def wrap_on(self) -> str: ...
    @wrap_on.setter
    def wrap_on(self, value: str) -> None: ...
    @property
    def background(self) -> str: ...
    @background.setter
    def background(self, value: str) -> None: ...
    @property
    def foreground(self) -> str: ...
    @foreground.setter
    def foreground(self, value: str) -> None: ...
    @property
    def border(self) -> str: ...
    @border.setter
    def border(self, value: str) -> None: ...


    @property
    def margin(self) -> MarginPropertyValue: ...
    @margin.setter
    def margin(self, value: MarginPropertyValue) -> None: ...
    @property
    def spacing_above(self) -> Literal["none", "small", "medium", "large"] | None: ...
    @spacing_above.setter
    def spacing_above(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...
    @property
    def spacing_below(self) -> Literal["none", "small", "medium", "large"] | None: ...
    @spacing_below.setter
    def spacing_below(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...

    @override
    def add_event_handler(self, event_name: _DataGridEvents | str, handler_func: Callable[..., Any], /) -> None: ...
    @override
    def remove_event_handler(self, event_name: _DataGridEvents | str, handler_func: Callable[..., Any] | None = None, /) -> None: ...
    @override
    def set_event_handler(self, event_name: _DataGridEvents | str, handler_func: Callable[..., Any] | None, /) -> None: ...
    @override
    def raise_event(self, event_name: _DataGridEvents | str, /, **event_args: Any) -> None: ...

    @overload
    def add_component(self, component: Component, /, **layout_props: Unpack[_DataGridLayoutKwargs]) -> None: ...
    @overload
    def add_component(self, component: Component, /, **layout_props: Any) -> None: ...

    def jump_to_first_page(self) -> None:
        """Display the first page."""
        ...

    def jump_to_last_page(self) -> None:
        """Display the last page."""
        ...

    def next_page(self) -> None:
        """Display the next page, if there is one."""
        ...

    def previous_page(self) -> None:
        """Display the previous page, if there is one."""
        ...

    def get_page(self) -> int | None:
        """Get the zero-based index of the current page."""
        ...

    def get_first_index_on_page(self) -> int | None:
        """Get the zero-based item index at the start of the current page."""
        ...

    def set_page(self, page: int, /) -> None:
        """Display a page by its zero-based index."""
        ...

    def repaginate(self) -> None:
        """Refresh the current page after its contents change."""
        ...


    def __init__(
        self,
        *,
        tag: Any = ...,
        visible: bool = ...,
        tooltip: str = ...,
        role: str | list[str] | None = ...,
        columns: list[dict[str, Any]] = ...,
        rows_per_page: int | None = ...,
        show_page_controls: bool = ...,
        auto_header: bool = ...,
        wrap_on: str = ...,
        background: str = ...,
        foreground: str = ...,
        border: str = ...,
        margin: MarginPropertyValue = ...,
        spacing_above: Literal["none", "small", "medium", "large"] | None = ...,
        spacing_below: Literal["none", "small", "medium", "large"] | None = ...,
    ) -> None: ...

class DataRowPanel(Container):
    """A row within a DataGrid.

    [Anvil Docs](https://anvil.works/docs/client/components/data-grids)"""

    @property
    def visible(self) -> bool: ...
    @visible.setter
    def visible(self, value: bool) -> None: ...
    @property
    def tooltip(self) -> str: ...
    @tooltip.setter
    def tooltip(self, value: str) -> None: ...
    @property
    def role(self) -> str | list[str] | None: ...
    @role.setter
    def role(self, value: str | list[str] | None) -> None: ...

    @property
    def item(self) -> dict[str, Any]: ...
    @item.setter
    def item(self, value: dict[str, Any]) -> None: ...
    @property
    def auto_display_data(self) -> bool: ...
    @auto_display_data.setter
    def auto_display_data(self, value: bool) -> None: ...
    @property
    def background(self) -> str: ...
    @background.setter
    def background(self, value: str) -> None: ...
    @property
    def foreground(self) -> str: ...
    @foreground.setter
    def foreground(self, value: str) -> None: ...
    @property
    def border(self) -> str: ...
    @border.setter
    def border(self, value: str) -> None: ...


    @property
    def align(self) -> str: ...
    @align.setter
    def align(self, value: str) -> None: ...
    @property
    def font_size(self) -> int | float | None: ...
    @font_size.setter
    def font_size(self, value: int | float | None) -> None: ...
    @property
    def font(self) -> str: ...
    @font.setter
    def font(self, value: str) -> None: ...
    @property
    def bold(self) -> bool: ...
    @bold.setter
    def bold(self, value: bool) -> None: ...
    @property
    def italic(self) -> bool: ...
    @italic.setter
    def italic(self, value: bool) -> None: ...
    @property
    def underline(self) -> bool: ...
    @underline.setter
    def underline(self, value: bool) -> None: ...
    @property
    def margin(self) -> MarginPropertyValue: ...
    @margin.setter
    def margin(self, value: MarginPropertyValue) -> None: ...
    @property
    def spacing_above(self) -> Literal["none", "small", "medium", "large"] | None: ...
    @spacing_above.setter
    def spacing_above(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...
    @property
    def spacing_below(self) -> Literal["none", "small", "medium", "large"] | None: ...
    @spacing_below.setter
    def spacing_below(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...

    @overload
    def add_component(self, component: Component, /, **layout_props: Unpack[_DataRowPanelLayoutKwargs]) -> None: ...
    @overload
    def add_component(self, component: Component, /, **layout_props: Any) -> None: ...

    def __init__(
        self,
        *,
        tag: Any = ...,
        visible: bool = ...,
        tooltip: str = ...,
        role: str | list[str] | None = ...,
        item: dict[str, Any] = ...,
        auto_display_data: bool = ...,
        background: str = ...,
        foreground: str = ...,
        border: str = ...,
        align: str = ...,
        font_size: int | float | None = ...,
        font: str = ...,
        bold: bool = ...,
        italic: bool = ...,
        underline: bool = ...,
        margin: MarginPropertyValue = ...,
        spacing_above: Literal["none", "small", "medium", "large"] | None = ...,
        spacing_below: Literal["none", "small", "medium", "large"] | None = ...,
    ) -> None: ...

class RepeatingPanel(Container):
    """A panel that repeats a template for each item in a list.

    [Anvil Docs](https://anvil.works/docs/client/components/repeating-panel)"""

    @property
    def visible(self) -> bool: ...
    @visible.setter
    def visible(self, value: bool) -> None: ...
    @property
    def tooltip(self) -> str: ...
    @tooltip.setter
    def tooltip(self, value: str) -> None: ...
    @property
    def role(self) -> str | list[str] | None: ...
    @role.setter
    def role(self, value: str | list[str] | None) -> None: ...

    @property
    def items(self) -> list[Any] | Iterator[Any]: ...
    @items.setter
    def items(self, value: list[Any] | Iterator[Any]) -> None: ...
    item_template: Any
    @property
    def background(self) -> str: ...
    @background.setter
    def background(self, value: str) -> None: ...
    @property
    def foreground(self) -> str: ...
    @foreground.setter
    def foreground(self, value: str) -> None: ...
    @property
    def border(self) -> str: ...
    @border.setter
    def border(self, value: str) -> None: ...


    @property
    def margin(self) -> MarginPropertyValue: ...
    @margin.setter
    def margin(self, value: MarginPropertyValue) -> None: ...
    @property
    def spacing_above(self) -> Literal["none", "small", "medium", "large"] | None: ...
    @spacing_above.setter
    def spacing_above(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...
    @property
    def spacing_below(self) -> Literal["none", "small", "medium", "large"] | None: ...
    @spacing_below.setter
    def spacing_below(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...

    @override
    def get_components(self) -> list[Component]:
        """Get all repeated template instances.

        [Anvil Docs](https://anvil.works/docs/client/components/repeating-panel)"""
        ...


    def __init__(
        self,
        *,
        tag: Any = ...,
        visible: bool = ...,
        tooltip: str = ...,
        role: str | list[str] | None = ...,
        items: list[Any] | Iterator[Any] = ...,
        background: str = ...,
        foreground: str = ...,
        border: str = ...,
        margin: MarginPropertyValue = ...,
        spacing_above: Literal["none", "small", "medium", "large"] | None = ...,
        spacing_below: Literal["none", "small", "medium", "large"] | None = ...,
    ) -> None: ...

# ============================================================================
# Media/Visualization Components
# ============================================================================

class HtmlComponent(Container):
    """A container that renders custom HTML.

    [Anvil Docs](https://anvil.works/docs/client/customisation/custom-components/html-components)"""

    @property
    def visible(self) -> bool: ...
    @visible.setter
    def visible(self, value: bool) -> None: ...

    @property
    def html(self) -> str: ...
    @html.setter
    def html(self, value: str) -> None: ...

    @property
    def classes(self) -> Classes: ...
    @classes.setter
    def classes(self, value: _ClassesValue | Classes) -> None: ...

    @property
    def style(self) -> Style: ...
    @style.setter
    def style(self, value: _StyleValue | Style) -> None: ...

    @property
    def attrs(self) -> Attrs: ...
    @attrs.setter
    def attrs(self, value: _AttrsValue | Attrs) -> None: ...

    @overload
    def add_component(self, component: Component, /, **layout_props: Unpack[_HtmlComponentLayoutKwargs]) -> None: ...
    @overload
    def add_component(self, component: Component, /, **layout_props: Any) -> None: ...


    def __init__(
        self,
        *,
        tag: Any = ...,
        visible: bool = ...,
        html: str = ...,
        classes: _ClassesValue | Classes = ...,
        style: _StyleValue | Style = ...,
        attrs: _AttrsValue | Attrs = ...,
    ) -> None: ...

class HtmlTemplate(Container):
    """A container that renders HTML.

    [Anvil Docs](https://anvil.works/docs/client/forms/html-in-forms#legacy-htmltemplate-forms)"""

    @property
    def visible(self) -> bool: ...
    @visible.setter
    def visible(self, value: bool) -> None: ...
    @property
    def tooltip(self) -> str: ...
    @tooltip.setter
    def tooltip(self, value: str) -> None: ...
    @property
    def role(self) -> str | list[str] | None: ...
    @role.setter
    def role(self, value: str | list[str] | None) -> None: ...

    @property
    def html(self) -> str: ...
    @html.setter
    def html(self, value: str) -> None: ...


    @property
    def background(self) -> str: ...
    @background.setter
    def background(self, value: str) -> None: ...
    @property
    def border(self) -> str: ...
    @border.setter
    def border(self, value: str) -> None: ...
    @property
    def foreground(self) -> str: ...
    @foreground.setter
    def foreground(self, value: str) -> None: ...

    @overload
    def add_component(self, component: Component, /, **layout_props: Unpack[_SlottedLayoutKwargs]) -> None: ...
    @overload
    def add_component(self, component: Component, /, **layout_props: Any) -> None: ...

    def call_js(self, fn_name: str, *args: Any) -> Any:
        """Call a JavaScript function defined in the HTML.

        [Anvil Docs](https://anvil.works/docs/client/javascript)"""
        ...


    def __init__(
        self,
        *,
        tag: Any = ...,
        visible: bool = ...,
        tooltip: str = ...,
        role: str | list[str] | None = ...,
        html: str = ...,
        background: str = ...,
        border: str = ...,
        foreground: str = ...,
    ) -> None: ...

HtmlPanel = deprecated("HtmlPanel is deprecated. Use HtmlTemplate instead.")(HtmlTemplate)


class _CanvasGradient:
    def add_color_stop(self, offset: int | float, color: str) -> None:
        """Add a color stop at an offset between 0 and 1."""
        ...


class Canvas(Component):
    """A drawing canvas component.

    [Anvil Docs](https://anvil.works/docs/client/components/canvas)"""

    @property
    def visible(self) -> bool: ...
    @visible.setter
    def visible(self, value: bool) -> None: ...
    @property
    def tooltip(self) -> str: ...
    @tooltip.setter
    def tooltip(self, value: str) -> None: ...
    @property
    def role(self) -> str | list[str] | None: ...
    @role.setter
    def role(self, value: str | list[str] | None) -> None: ...

    @property
    def width(self) -> int: ...
    @width.setter
    def width(self, value: int) -> None: ...
    @property
    def height(self) -> int: ...
    @height.setter
    def height(self, value: int) -> None: ...
    @property
    def background(self) -> str: ...
    @background.setter
    def background(self, value: str) -> None: ...


    @property
    def border(self) -> str: ...
    @border.setter
    def border(self, value: str) -> None: ...
    @property
    def foreground(self) -> str: ...
    @foreground.setter
    def foreground(self, value: str) -> None: ...
    @property
    def margin(self) -> MarginPropertyValue: ...
    @margin.setter
    def margin(self, value: MarginPropertyValue) -> None: ...
    @property
    def spacing_above(self) -> Literal["none", "small", "medium", "large"] | None: ...
    @spacing_above.setter
    def spacing_above(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...
    @property
    def spacing_below(self) -> Literal["none", "small", "medium", "large"] | None: ...
    @spacing_below.setter
    def spacing_below(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...

    @override
    def add_event_handler(self, event_name: _CanvasEvents | str, handler_func: Callable[..., Any], /) -> None: ...
    @override
    def remove_event_handler(self, event_name: _CanvasEvents | str, handler_func: Callable[..., Any] | None = None, /) -> None: ...
    @override
    def set_event_handler(self, event_name: _CanvasEvents | str, handler_func: Callable[..., Any] | None, /) -> None: ...
    @override
    def raise_event(self, event_name: _CanvasEvents | str, /, **event_args: Any) -> None: ...

    Gradient: type[_CanvasGradient]

    def get_width(self) -> int | float:
        """Get the canvas width in pixels."""
        ...

    def get_height(self) -> int | float:
        """Get the canvas height in pixels."""
        ...

    def get_image(self) -> Media:
        """Get the canvas content as a media object.

        [Anvil Docs](https://anvil.works/docs/client/components/canvas)"""
        ...

    def save(self) -> None:
        """Save the current drawing state."""
        ...

    def restore(self) -> None:
        """Restore the most recently saved drawing state."""
        ...

    def translate(self, x: int | float, y: int | float) -> None:
        """Translate subsequent drawing operations."""
        ...

    def rotate(self, angle: int | float) -> None:
        """Rotate subsequent drawing operations by an angle in radians."""
        ...

    def scale(self, x: int | float, y: int | float) -> None:
        """Scale subsequent drawing operations."""
        ...

    def transform(
        self,
        a: int | float,
        b: int | float,
        c: int | float,
        d: int | float,
        e: int | float,
        f: int | float,
    ) -> None:
        """Multiply the current transformation matrix."""
        ...

    def set_transform(
        self,
        a: int | float,
        b: int | float,
        c: int | float,
        d: int | float,
        e: int | float,
        f: int | float,
    ) -> None:
        """Replace the current transformation matrix."""
        ...

    def reset_transform(self) -> None:
        """Reset the current transformation matrix."""
        ...

    def fill_text(self, text: str, x: int | float, y: int | float) -> None:
        """Draw filled text at the specified position."""
        ...

    def stroke_text(self, text: str, x: int | float, y: int | float) -> None:
        """Draw outlined text at the specified position."""
        ...

    def measure_text(self, text: str) -> int | float:
        """Get the width of text in the current font."""
        ...

    def clear_rect(self, x: int | float, y: int | float, width: int | float, height: int | float) -> None:
        """Clear a rectangle."""
        ...

    def fill_rect(self, x: int | float, y: int | float, width: int | float, height: int | float) -> None:
        """Draw a filled rectangle."""
        ...

    def stroke_rect(self, x: int | float, y: int | float, width: int | float, height: int | float) -> None:
        """Draw an outlined rectangle."""
        ...

    def begin_path(self) -> None:
        """Begin a new path."""
        ...

    def close_path(self) -> None:
        """Close the current path."""
        ...

    def fill(self) -> None:
        """Fill the current path."""
        ...

    def stroke(self) -> None:
        """Draw the current path's outline."""
        ...

    def clip(self) -> None:
        """Use the current path as the clipping region."""
        ...

    def move_to(self, x: int | float, y: int | float) -> None:
        """Move the current path position without drawing."""
        ...

    def line_to(self, x: int | float, y: int | float) -> None:
        """Add a line segment to the current path."""
        ...

    def quadratic_curve_to(
        self,
        cpx: int | float,
        cpy: int | float,
        x: int | float,
        y: int | float,
    ) -> None:
        """Add a quadratic curve to the current path."""
        ...

    def bezier_curve_to(
        self,
        cp1x: int | float,
        cp1y: int | float,
        cp2x: int | float,
        cp2y: int | float,
        x: int | float,
        y: int | float,
    ) -> None:
        """Add a Bezier curve to the current path."""
        ...

    def arc(
        self,
        x: int | float,
        y: int | float,
        radius: int | float,
        start_angle: int | float = 0,
        end_angle: int | float = ...,
        anticlockwise: bool = False,
    ) -> None:
        """Add an arc to the current path."""
        ...

    def draw_image(
        self,
        media: Media,
        x: int | float | None = None,
        y: int | float | None = None,
        width: int | float | None = None,
        height: int | float | None = None,
    ) -> None:
        """Draw a media image, optionally scaling it."""
        ...

    def draw_image_part(
        self,
        media: Media,
        sx: int | float | None,
        sy: int | float | None,
        s_width: int | float | None,
        s_height: int | float | None,
        dx: int | float | None,
        dy: int | float | None,
        d_width: int | float | None,
        d_height: int | float | None,
    ) -> None:
        """Draw part of a media image into a destination rectangle."""
        ...

    def create_linear_gradient(
        self,
        x0: int | float,
        y0: int | float,
        x1: int | float,
        y1: int | float,
    ) -> _CanvasGradient:
        """Create a linear gradient."""
        ...

    def create_radial_gradient(
        self,
        x0: int | float,
        y0: int | float,
        r0: int | float,
        x1: int | float,
        y1: int | float,
        r1: int | float,
    ) -> _CanvasGradient:
        """Create a radial gradient."""
        ...

    def reset_context(self) -> None:
        """Reset the drawing context.

        [Anvil Docs](https://anvil.works/docs/client/components/canvas)"""
        ...


    def __init__(
        self,
        *,
        tag: Any = ...,
        visible: bool = ...,
        tooltip: str = ...,
        role: str | list[str] | None = ...,
        width: int = ...,
        height: int = ...,
        background: str = ...,
        border: str = ...,
        foreground: str = ...,
        margin: MarginPropertyValue = ...,
        spacing_above: Literal["none", "small", "medium", "large"] | None = ...,
        spacing_below: Literal["none", "small", "medium", "large"] | None = ...,
    ) -> None: ...

class Plot(Component):
    """A Plotly chart component.

    [Anvil Docs](https://anvil.works/docs/client/components/plots)"""

    @property
    def visible(self) -> bool: ...
    @visible.setter
    def visible(self, value: bool) -> None: ...
    @property
    def tooltip(self) -> str: ...
    @tooltip.setter
    def tooltip(self, value: str) -> None: ...

    @property
    def data(self) -> list[dict[str, Any]]: ...
    @data.setter
    def data(self, value: list[dict[str, Any]]) -> None: ...
    @property
    def layout(self) -> dict[str, Any]: ...
    @layout.setter
    def layout(self, value: dict[str, Any]) -> None: ...
    @property
    def config(self) -> dict[str, Any]: ...
    @config.setter
    def config(self, value: dict[str, Any]) -> None: ...
    @property
    def figure(self) -> dict[str, Any]: ...
    @figure.setter
    def figure(self, value: dict[str, Any]) -> None: ...
    @property
    def interactive(self) -> bool: ...
    @interactive.setter
    def interactive(self, value: bool) -> None: ...


    @property
    def height(self) -> str: ...
    @height.setter
    def height(self, value: str) -> None: ...
    @property
    def margin(self) -> MarginPropertyValue: ...
    @margin.setter
    def margin(self, value: MarginPropertyValue) -> None: ...
    @property
    def spacing_above(self) -> Literal["none", "small", "medium", "large"] | None: ...
    @spacing_above.setter
    def spacing_above(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...
    @property
    def spacing_below(self) -> Literal["none", "small", "medium", "large"] | None: ...
    @spacing_below.setter
    def spacing_below(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...

    @override
    def add_event_handler(self, event_name: _PlotEvents | str, handler_func: Callable[..., Any], /) -> None: ...
    @override
    def remove_event_handler(self, event_name: _PlotEvents | str, handler_func: Callable[..., Any] | None = None, /) -> None: ...
    @override
    def set_event_handler(self, event_name: _PlotEvents | str, handler_func: Callable[..., Any] | None, /) -> None: ...
    @override
    def raise_event(self, event_name: _PlotEvents | str, /, **event_args: Any) -> None: ...

    templates: dict[str, Any]

    def redraw(self) -> None:
        """Redraw the plot.

        [Anvil Docs](https://anvil.works/docs/client/components/plots)"""
        ...

    def to_image(self, options: Mapping[str, Any] | None = None, /) -> Media:
        """Export the plot as an image.

        [Anvil Docs](https://anvil.works/docs/client/components/plots)"""
        ...

    def relayout(self, update: Mapping[str, Any], /) -> None:
        """Update the plot layout.

        [Anvil Docs](https://anvil.works/docs/client/components/plots)"""
        ...

    def extend_traces(self, data: Mapping[str, Any], traces: list[int], /) -> None:
        """Extend trace data.

        [Anvil Docs](https://anvil.works/docs/client/components/plots)"""
        ...

    def prepend_traces(self, data: Mapping[str, Any], traces: list[int], /) -> None:
        """Prepend trace data.

        [Anvil Docs](https://anvil.works/docs/client/components/plots)"""
        ...

    def restyle(self, update: Mapping[str, Any], traces: list[int], /) -> None:
        """Update attributes on one or more traces.

        [Anvil Docs](https://anvil.works/docs/client/components/plots)"""
        ...


    def __init__(
        self,
        *,
        tag: Any = ...,
        visible: bool = ...,
        tooltip: str = ...,
        data: list[dict[str, Any]] = ...,
        layout: dict[str, Any] = ...,
        config: dict[str, Any] = ...,
        figure: dict[str, Any] = ...,
        interactive: bool = ...,
        height: str = ...,
        margin: MarginPropertyValue = ...,
        spacing_above: Literal["none", "small", "medium", "large"] | None = ...,
        spacing_below: Literal["none", "small", "medium", "large"] | None = ...,
    ) -> None: ...

class _LatLng:
    """A latitude/longitude pair for GoogleMap.

    [Anvil Docs](https://anvil.works/docs/client/components/maps)"""

    lat: float
    lng: float

    def __init__(self, lat: float, lng: float) -> None: ...


class _MapMarker(Component):
    """A marker on a GoogleMap.

    [Anvil Docs](https://anvil.works/docs/client/components/maps#markers)"""

    @property
    def enabled(self) -> bool: ...
    @enabled.setter
    def enabled(self, value: bool) -> None: ...
    @property
    def tooltip(self) -> str: ...
    @tooltip.setter
    def tooltip(self, value: str) -> None: ...
    @property
    def role(self) -> str | list[str] | None: ...
    @role.setter
    def role(self, value: str | list[str] | None) -> None: ...

    @property
    def animation(self) -> Any: ...
    @animation.setter
    def animation(self, value: Any) -> None: ...
    """The animation of this Marker."""

    @property
    def position(self) -> _LatLng: ...
    @position.setter
    def position(self, value: _LatLng) -> None: ...
    """The LatLng position of this Marker."""

    @property
    def icon(self) -> Any: ...
    @icon.setter
    def icon(self, value: Any) -> None: ...
    """The icon to display at the position of this Marker."""

    @property
    def label(self) -> Any: ...
    @label.setter
    def label(self, value: Any) -> None: ...
    """The label to display on this Marker."""

    @property
    def clickable(self) -> bool: ...
    @clickable.setter
    def clickable(self, value: bool) -> None: ...
    """True if this Marker can be clicked."""

    @property
    def draggable(self) -> bool: ...
    @draggable.setter
    def draggable(self, value: bool) -> None: ...
    """True if this Marker can be dragged."""

    @property
    def visible(self) -> bool: ...
    @visible.setter
    def visible(self, value: bool) -> None: ...
    """True if this Marker is visible."""

    @property
    def z_index(self) -> int: ...
    @z_index.setter
    def z_index(self, value: int) -> None: ...
    """The z-index of this Marker."""

    def remove(self) -> None:
        """Remove this marker from the map."""
        ...


    def __init__(
        self,
        *,
        tag: Any = ...,
        enabled: bool = ...,
        tooltip: str = ...,
        role: str | list[str] | None = ...,
        animation: Any = ...,
        position: _LatLng = ...,
        icon: Any = ...,
        label: Any = ...,
        clickable: bool = ...,
        draggable: bool = ...,
        visible: bool = ...,
        z_index: int = ...,
    ) -> None: ...

class _MapPolygon(Component):
    """A polygon overlay on a GoogleMap.

    [Anvil Docs](https://anvil.works/docs/client/components/maps#polygons)"""

    @property
    def enabled(self) -> bool: ...
    @enabled.setter
    def enabled(self, value: bool) -> None: ...
    @property
    def tooltip(self) -> str: ...
    @tooltip.setter
    def tooltip(self, value: str) -> None: ...
    @property
    def role(self) -> str | list[str] | None: ...
    @role.setter
    def role(self, value: str | list[str] | None) -> None: ...

    @property
    def path(self) -> list[_LatLng]: ...
    @path.setter
    def path(self, value: list[_LatLng]) -> None: ...
    """The ordered sequence of LatLng coordinates of the Polygon."""

    @property
    def geodesic(self) -> bool: ...
    @geodesic.setter
    def geodesic(self, value: bool) -> None: ...
    """When true, edges of the polygon are interpreted as geodesic."""

    @property
    def editable(self) -> bool: ...
    @editable.setter
    def editable(self, value: bool) -> None: ...
    """True if this overlay can be edited by the user."""

    @property
    def draggable(self) -> bool: ...
    @draggable.setter
    def draggable(self, value: bool) -> None: ...
    """True if this overlay can be dragged."""

    @property
    def visible(self) -> bool: ...
    @visible.setter
    def visible(self, value: bool) -> None: ...
    """True if this overlay is visible."""

    @property
    def stroke_color(self) -> str: ...
    @stroke_color.setter
    def stroke_color(self, value: str) -> None: ...
    """The stroke color."""

    @property
    def stroke_opacity(self) -> float: ...
    @stroke_opacity.setter
    def stroke_opacity(self, value: float) -> None: ...
    """The stroke opacity between 0.0 and 1.0."""

    @property
    def stroke_weight(self) -> int: ...
    @stroke_weight.setter
    def stroke_weight(self, value: int) -> None: ...
    """The stroke width in pixels."""

    @property
    def fill_color(self) -> str: ...
    @fill_color.setter
    def fill_color(self, value: str) -> None: ...
    """The fill color."""

    @property
    def fill_opacity(self) -> float: ...
    @fill_opacity.setter
    def fill_opacity(self, value: float) -> None: ...
    """The fill opacity between 0.0 and 1.0."""

    @property
    def z_index(self) -> int: ...
    @z_index.setter
    def z_index(self, value: int) -> None: ...
    """The z-index of this Polygon."""

    def remove(self) -> None:
        """Remove this polygon from the map."""
        ...


    def __init__(
        self,
        *,
        tag: Any = ...,
        enabled: bool = ...,
        tooltip: str = ...,
        role: str | list[str] | None = ...,
        path: list[_LatLng] = ...,
        geodesic: bool = ...,
        editable: bool = ...,
        draggable: bool = ...,
        visible: bool = ...,
        stroke_color: str = ...,
        stroke_opacity: float = ...,
        stroke_weight: int = ...,
        fill_color: str = ...,
        fill_opacity: float = ...,
        z_index: int = ...,
    ) -> None: ...

class _MapPolyline(Component):
    """A polyline overlay on a GoogleMap.

    [Anvil Docs](https://anvil.works/docs/client/components/maps#polylines)"""

    @property
    def enabled(self) -> bool: ...
    @enabled.setter
    def enabled(self, value: bool) -> None: ...
    @property
    def tooltip(self) -> str: ...
    @tooltip.setter
    def tooltip(self, value: str) -> None: ...
    @property
    def role(self) -> str | list[str] | None: ...
    @role.setter
    def role(self, value: str | list[str] | None) -> None: ...

    @property
    def icons(self) -> list[Any]: ...
    @icons.setter
    def icons(self, value: list[Any]) -> None: ...
    """The icons to be rendered along the polyline."""

    @property
    def path(self) -> list[_LatLng]: ...
    @path.setter
    def path(self, value: list[_LatLng]) -> None: ...
    """The ordered sequence of LatLng coordinates of the Polyline."""

    @property
    def geodesic(self) -> bool: ...
    @geodesic.setter
    def geodesic(self, value: bool) -> None: ...
    """When true, edges of the polyline are interpreted as geodesic."""

    @property
    def editable(self) -> bool: ...
    @editable.setter
    def editable(self, value: bool) -> None: ...
    """True if this overlay can be edited by the user."""

    @property
    def draggable(self) -> bool: ...
    @draggable.setter
    def draggable(self, value: bool) -> None: ...
    """True if this overlay can be dragged."""

    @property
    def visible(self) -> bool: ...
    @visible.setter
    def visible(self, value: bool) -> None: ...
    """True if this overlay is visible."""

    @property
    def stroke_color(self) -> str: ...
    @stroke_color.setter
    def stroke_color(self, value: str) -> None: ...
    """The stroke color."""

    @property
    def stroke_opacity(self) -> float: ...
    @stroke_opacity.setter
    def stroke_opacity(self, value: float) -> None: ...
    """The stroke opacity between 0.0 and 1.0."""

    @property
    def stroke_weight(self) -> int: ...
    @stroke_weight.setter
    def stroke_weight(self, value: int) -> None: ...
    """The stroke width in pixels."""

    @property
    def z_index(self) -> int: ...
    @z_index.setter
    def z_index(self, value: int) -> None: ...
    """The z-index of this Polyline."""

    def remove(self) -> None:
        """Remove this polyline from the map."""
        ...


    def __init__(
        self,
        *,
        tag: Any = ...,
        enabled: bool = ...,
        tooltip: str = ...,
        role: str | list[str] | None = ...,
        icons: list[Any] = ...,
        path: list[_LatLng] = ...,
        geodesic: bool = ...,
        editable: bool = ...,
        draggable: bool = ...,
        visible: bool = ...,
        stroke_color: str = ...,
        stroke_opacity: float = ...,
        stroke_weight: int = ...,
        z_index: int = ...,
    ) -> None: ...

class GoogleMap(Component):
    """A Google Maps component.

    [Anvil Docs](https://anvil.works/docs/client/components/maps)"""

    @property
    def visible(self) -> bool: ...
    @visible.setter
    def visible(self, value: bool) -> None: ...

    @property
    def center(self) -> _LatLng | Any: ...
    @center.setter
    def center(self, value: _LatLng | Any) -> None: ...
    @property
    def zoom(self) -> int: ...
    @zoom.setter
    def zoom(self, value: int) -> None: ...
    @property
    def map_type(self) -> str: ...
    @map_type.setter
    def map_type(self, value: str) -> None: ...
    @property
    def markers(self) -> list[_MapMarker]: ...
    @markers.setter
    def markers(self, value: list[_MapMarker]) -> None: ...
    @property
    def map_data(self) -> Any: ...
    @map_data.setter
    def map_data(self, value: Any) -> None: ...
    @property
    def background_color(self) -> str: ...
    @background_color.setter
    def background_color(self, value: str) -> None: ...
    @property
    def clickable_icons(self) -> bool: ...
    @clickable_icons.setter
    def clickable_icons(self, value: bool) -> None: ...
    @property
    def disable_default_ui(self) -> bool: ...
    @disable_default_ui.setter
    def disable_default_ui(self, value: bool) -> None: ...
    @property
    def disable_double_click_zoom(self) -> bool: ...
    @disable_double_click_zoom.setter
    def disable_double_click_zoom(self, value: bool) -> None: ...
    @property
    def draggable(self) -> bool: ...
    @draggable.setter
    def draggable(self, value: bool) -> None: ...
    @property
    def draggable_cursor(self) -> str: ...
    @draggable_cursor.setter
    def draggable_cursor(self, value: str) -> None: ...
    @property
    def dragging_cursor(self) -> str: ...
    @dragging_cursor.setter
    def dragging_cursor(self, value: str) -> None: ...
    @property
    def fullscreen_control(self) -> bool: ...
    @fullscreen_control.setter
    def fullscreen_control(self, value: bool) -> None: ...
    @property
    def fullscreen_control_options(self) -> Any: ...
    @fullscreen_control_options.setter
    def fullscreen_control_options(self, value: Any) -> None: ...
    @property
    def gesture_handling(self) -> str: ...
    @gesture_handling.setter
    def gesture_handling(self, value: str) -> None: ...
    @property
    def heading(self) -> int | float: ...
    @heading.setter
    def heading(self, value: int | float) -> None: ...
    @property
    def keyboard_shortcuts(self) -> bool: ...
    @keyboard_shortcuts.setter
    def keyboard_shortcuts(self, value: bool) -> None: ...
    @property
    def map_type_control(self) -> bool: ...
    @map_type_control.setter
    def map_type_control(self, value: bool) -> None: ...
    @property
    def map_type_control_options(self) -> Any: ...
    @map_type_control_options.setter
    def map_type_control_options(self, value: Any) -> None: ...
    @property
    def map_type_id(self) -> Any: ...
    @map_type_id.setter
    def map_type_id(self, value: Any) -> None: ...
    @property
    def max_zoom(self) -> int | float: ...
    @max_zoom.setter
    def max_zoom(self, value: int | float) -> None: ...
    @property
    def min_zoom(self) -> int | float: ...
    @min_zoom.setter
    def min_zoom(self, value: int | float) -> None: ...
    @property
    def rotate_control(self) -> bool: ...
    @rotate_control.setter
    def rotate_control(self, value: bool) -> None: ...
    @property
    def rotate_control_options(self) -> Any: ...
    @rotate_control_options.setter
    def rotate_control_options(self, value: Any) -> None: ...
    @property
    def scale_control(self) -> bool: ...
    @scale_control.setter
    def scale_control(self, value: bool) -> None: ...
    @property
    def scale_control_options(self) -> Any: ...
    @scale_control_options.setter
    def scale_control_options(self, value: Any) -> None: ...
    @property
    def scroll_wheel(self) -> bool: ...
    @scroll_wheel.setter
    def scroll_wheel(self, value: bool) -> None: ...
    @property
    def street_view_control(self) -> bool: ...
    @street_view_control.setter
    def street_view_control(self, value: bool) -> None: ...
    @property
    def street_view_control_options(self) -> Any: ...
    @street_view_control_options.setter
    def street_view_control_options(self, value: Any) -> None: ...
    @property
    def zoom_control(self) -> bool: ...
    @zoom_control.setter
    def zoom_control(self, value: bool) -> None: ...
    @property
    def zoom_control_options(self) -> Any: ...
    @zoom_control_options.setter
    def zoom_control_options(self, value: Any) -> None: ...

    # Nested classes
    @property
    def LatLng(self) -> type[_LatLng]: ...
    @LatLng.setter
    def LatLng(self, value: type[_LatLng]) -> None: ...
    @property
    def Marker(self) -> type[_MapMarker]: ...
    @Marker.setter
    def Marker(self, value: type[_MapMarker]) -> None: ...
    @property
    def Polygon(self) -> type[_MapPolygon]: ...
    @Polygon.setter
    def Polygon(self, value: type[_MapPolygon]) -> None: ...
    @property
    def Polyline(self) -> type[_MapPolyline]: ...
    @Polyline.setter
    def Polyline(self, value: type[_MapPolyline]) -> None: ...


    @property
    def height(self) -> str: ...
    @height.setter
    def height(self, value: str) -> None: ...
    @property
    def margin(self) -> MarginPropertyValue: ...
    @margin.setter
    def margin(self, value: MarginPropertyValue) -> None: ...
    @property
    def spacing_above(self) -> Literal["none", "small", "medium", "large"] | None: ...
    @spacing_above.setter
    def spacing_above(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...
    @property
    def spacing_below(self) -> Literal["none", "small", "medium", "large"] | None: ...
    @spacing_below.setter
    def spacing_below(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...

    @override
    def add_event_handler(self, event_name: _GoogleMapEvents | str, handler_func: Callable[..., Any], /) -> None: ...
    @override
    def remove_event_handler(self, event_name: _GoogleMapEvents | str, handler_func: Callable[..., Any] | None = None, /) -> None: ...
    @override
    def set_event_handler(self, event_name: _GoogleMapEvents | str, handler_func: Callable[..., Any] | None, /) -> None: ...
    @override
    def raise_event(self, event_name: _GoogleMapEvents | str, /, **event_args: Any) -> None: ...

    def add_component(
        self,
        component: _MapMarker | _MapPolygon | _MapPolyline,
        /,
        **layout_props: Any,
    ) -> None:
        """Add a marker, polygon, or polyline to this map."""
        ...


    def __init__(
        self,
        *,
        tag: Any = ...,
        visible: bool = ...,
        center: _LatLng | Any = ...,
        zoom: int = ...,
        map_type: str = ...,
        markers: list[_MapMarker] = ...,
        map_data: Any = ...,
        background_color: str = ...,
        clickable_icons: bool = ...,
        disable_default_ui: bool = ...,
        disable_double_click_zoom: bool = ...,
        draggable: bool = ...,
        draggable_cursor: str = ...,
        dragging_cursor: str = ...,
        fullscreen_control: bool = ...,
        fullscreen_control_options: Any = ...,
        gesture_handling: str = ...,
        heading: int | float = ...,
        keyboard_shortcuts: bool = ...,
        map_type_control: bool = ...,
        map_type_control_options: Any = ...,
        map_type_id: Any = ...,
        max_zoom: int | float = ...,
        min_zoom: int | float = ...,
        rotate_control: bool = ...,
        rotate_control_options: Any = ...,
        scale_control: bool = ...,
        scale_control_options: Any = ...,
        scroll_wheel: bool = ...,
        street_view_control: bool = ...,
        street_view_control_options: Any = ...,
        zoom_control: bool = ...,
        zoom_control_options: Any = ...,
        LatLng: type[_LatLng] = ...,
        Marker: type[_MapMarker] = ...,
        Polygon: type[_MapPolygon] = ...,
        Polyline: type[_MapPolyline] = ...,
        height: str = ...,
        margin: MarginPropertyValue = ...,
        spacing_above: Literal["none", "small", "medium", "large"] | None = ...,
        spacing_below: Literal["none", "small", "medium", "large"] | None = ...,
    ) -> None: ...

class YouTubeVideo(Component):
    """A YouTube video player component.

    [Anvil Docs](https://anvil.works/docs/client/components/basic#youtube-video)"""

    @property
    def visible(self) -> bool: ...
    @visible.setter
    def visible(self, value: bool) -> None: ...
    @property
    def role(self) -> str | list[str] | None: ...
    @role.setter
    def role(self, value: str | list[str] | None) -> None: ...

    @property
    def youtube_id(self) -> str: ...
    @youtube_id.setter
    def youtube_id(self, value: str) -> None: ...
    @property
    def autoplay(self) -> bool: ...
    @autoplay.setter
    def autoplay(self, value: bool) -> None: ...
    @property
    def loop(self) -> bool: ...
    @loop.setter
    def loop(self, value: bool) -> None: ...
    @property
    def mute(self) -> bool: ...
    @mute.setter
    def mute(self, value: bool) -> None: ...
    @property
    def volume(self) -> float: ...
    @volume.setter
    def volume(self, value: float) -> None: ...
    @property
    def current_time(self) -> float: ...
    @current_time.setter
    def current_time(self, value: float) -> None: ...
    @property
    def duration(self) -> float: ...
    @duration.setter
    def duration(self, value: float) -> None: ...
    @property
    def state(self) -> str: ...
    @state.setter
    def state(self, value: str) -> None: ...


    @property
    def background(self) -> str: ...
    @background.setter
    def background(self, value: str) -> None: ...
    @property
    def border(self) -> str: ...
    @border.setter
    def border(self, value: str) -> None: ...
    @property
    def foreground(self) -> str: ...
    @foreground.setter
    def foreground(self, value: str) -> None: ...
    @property
    def height(self) -> str: ...
    @height.setter
    def height(self, value: str) -> None: ...
    @property
    def margin(self) -> MarginPropertyValue: ...
    @margin.setter
    def margin(self, value: MarginPropertyValue) -> None: ...
    @property
    def spacing_above(self) -> Literal["none", "small", "medium", "large"] | None: ...
    @spacing_above.setter
    def spacing_above(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...
    @property
    def spacing_below(self) -> Literal["none", "small", "medium", "large"] | None: ...
    @spacing_below.setter
    def spacing_below(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...

    @override
    def add_event_handler(self, event_name: _YouTubeVideoEvents | str, handler_func: Callable[..., Any], /) -> None: ...
    @override
    def remove_event_handler(self, event_name: _YouTubeVideoEvents | str, handler_func: Callable[..., Any] | None = None, /) -> None: ...
    @override
    def set_event_handler(self, event_name: _YouTubeVideoEvents | str, handler_func: Callable[..., Any] | None, /) -> None: ...
    @override
    def raise_event(self, event_name: _YouTubeVideoEvents | str, /, **event_args: Any) -> None: ...

    def play(self) -> None:
        """Start playing this YouTube video.

        [Anvil Docs](https://anvil.works/docs/client/components/basic#youtube-video)"""
        ...

    def pause(self) -> None:
        """Pause this YouTube video.

        [Anvil Docs](https://anvil.works/docs/client/components/basic#youtube-video)"""
        ...

    def stop(self) -> None:
        """Stop playing this YouTube video.

        [Anvil Docs](https://anvil.works/docs/client/components/basic#youtube-video)"""
        ...


    def __init__(
        self,
        *,
        tag: Any = ...,
        visible: bool = ...,
        role: str | list[str] | None = ...,
        youtube_id: str = ...,
        autoplay: bool = ...,
        loop: bool = ...,
        mute: bool = ...,
        volume: float = ...,
        current_time: float = ...,
        duration: float = ...,
        state: str = ...,
        background: str = ...,
        border: str = ...,
        foreground: str = ...,
        height: str = ...,
        margin: MarginPropertyValue = ...,
        spacing_above: Literal["none", "small", "medium", "large"] | None = ...,
        spacing_below: Literal["none", "small", "medium", "large"] | None = ...,
    ) -> None: ...

# ============================================================================
# Utility Components
# ============================================================================

class Timer(Component):
    """Raise the ``tick`` event repeatedly at the configured interval.

    Set ``interval`` to 0 to switch the timer off.

    [Anvil Docs](https://anvil.works/docs/client/components/basic#timer)"""

    @property
    def interval(self) -> float: ...
    @interval.setter
    def interval(self, value: float) -> None: ...

    @override
    def add_event_handler(self, event_name: _TimerEvents | str, handler_func: Callable[..., Any], /) -> None: ...
    @override
    def remove_event_handler(self, event_name: _TimerEvents | str, handler_func: Callable[..., Any] | None = None, /) -> None: ...
    @override
    def set_event_handler(self, event_name: _TimerEvents | str, handler_func: Callable[..., Any] | None, /) -> None: ...
    @override
    def raise_event(self, event_name: _TimerEvents | str, /, **event_args: Any) -> None: ...
    def __init__(
        self,
        *,
        tag: Any = ...,
        interval: float = ...,
    ) -> None: ...
