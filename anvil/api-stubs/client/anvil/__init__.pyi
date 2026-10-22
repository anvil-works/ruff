# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the source file in doc/anvil-api-stubs/source/ instead, then run:
#   pnpm -F docs build
#
# Type stubs for Anvil
# Generated files: client/anvil/__init__.pyi, server/anvil/__init__.pyi

from datetime import date as _date, datetime as _datetime
from typing import Any, Callable, ClassVar, Generic, Iterable, overload, Iterator, Mapping, Literal, TypedDict
from typing_extensions import TypeVar, Unpack, deprecated, override

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

    [Anvil Docs](https://anvil.works/docs/other-concepts/working-with-files/media)"""

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

        [Anvil Docs](https://anvil.works/docs/other-concepts/working-with-files/media)"""
        ...

    def get_url(self) -> str | None:
        """Get a Media object's URL, or None if there isn't one associated with it.

        [Anvil Docs](https://anvil.works/docs/other-concepts/working-with-files/media)"""
        ...


class BlobMedia(Media):
    """Create a Media object with the specified content_type and content.

    Optionally specify a filename as well.

    [Anvil Docs](https://anvil.works/docs/other-concepts/working-with-files/media)"""

    def __init__(self, content_type: str, content: bytes, *, name: str | None = None) -> None: ...


class URLMedia(Media):
    """Create a Media object representing the data at a specific URL.

    For an app theme asset stored at ``theme/assets/<path>``, use
    ``URLMedia("_/theme/<path>")``. Do not add a leading slash or an
    ``assets`` path segment.

    Caution: Getting data from URLs directly in your code will often fail
    for security reasons, or fail to handle binary data.

    [Anvil Docs](https://anvil.works/docs/other-concepts/working-with-files/media)"""

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

    [Anvil Docs](https://anvil.works/docs/api/anvil#AppInfo)"""

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

    [Anvil Docs](https://anvil.works/docs/client/adding-ui-elements/alerts-and-notifications)"""
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

    [Anvil Docs](https://anvil.works/docs/client/adding-ui-elements/alerts-and-notifications)"""
    ...


class Notification:
    """Create a popup notification. Call the show() method to display it.

    Set timeout to None or 0 to keep it visible until dismissed.
    Set role to a theme role name or list of names.
    The style argument is deprecated; use role and theme CSS instead.
    Can also be used as a context manager.

    [Anvil Docs](https://anvil.works/docs/client/adding-ui-elements/alerts-and-notifications)"""

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

    [Anvil Docs](https://anvil.works/docs/client/navigation#using-open_form)"""
    ...


def open_form(form: str | Any, *args: Any, **kwargs: Any) -> None:
    """Open the specified form as a new page.

    If 'form' is a string, a new form will be created (extra arguments will be passed
    to its constructor). If 'form' is a Form object, it will be opened directly.

    [Anvil Docs](https://anvil.works/docs/client/navigation#using-open_form)"""
    ...


def get_url_hash() -> str | dict[str, str]:
    """Get the decoded hash (the part after the '#' character) of the URL used to open this app.

    If the first character of the hash is a question mark (eg '#?a=foo&b=bar'),
    it will be interpreted as query-string-type parameters and returned as a dictionary
    (eg {'a': 'foo', 'b': 'bar'}).

    [Anvil Docs](https://anvil.works/docs/api/anvil#get_url_hash)"""
    ...


def set_url_hash(val: str | dict[str, str], /) -> None:
    """Sets the hash of the currently open URL.

    If val is a string, it is added to the URL after a #.
    If val is a dictionary, it will be interpreted as query-string-type parameters
    and added to the URL after a hash and question mark (eg '#?a=foo&b=bar').

    [Anvil Docs](https://anvil.works/docs/api/anvil#set_url_hash)"""
    ...


# ============================================================================
# Other Client-Only Functions
# ============================================================================

def download(media: Media, /) -> None:
    """Download the given Media Object immediately in the user's browser.

    [Anvil Docs](https://anvil.works/docs/other-concepts/working-with-files/media)"""
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

    [Anvil Docs](https://anvil.works/docs/client/customisation/custom-components/html-components)"""

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
    def update(self, updates: Mapping[str, bool], /, **kwargs: bool) -> None:
        """Merge class names into this class-list helper. Truthy values add classes; falsey values remove them.

        [Anvil Docs](https://anvil.works/docs/client/customisation/custom-components/html-components)"""
        ...
    def clear(self) -> None:
        """Remove all class names."""
        ...


class Style:
    """A live inline-style helper for an HtmlComponent's root element.

    [Anvil Docs](https://anvil.works/docs/client/customisation/custom-components/html-components)"""

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
    def get(self, property: str, default: _T) -> str | _T:
        """Return a CSS property value, or `default` when it is not set.

        [Anvil Docs](https://anvil.works/docs/client/customisation/custom-components/html-components)"""
        ...
    @overload
    def update(self, /, **kwargs: _StyleUpdatePropertyValue) -> None: ...
    @overload
    def update(
        self,
        updates: Mapping[str, _StyleUpdatePropertyValue],
        /,
        **kwargs: _StyleUpdatePropertyValue,
    ) -> None:
        """Merge CSS properties into this style object. `None` or empty values remove properties.

        [Anvil Docs](https://anvil.works/docs/client/customisation/custom-components/html-components)"""
        ...
    def clear(self) -> None:
        """Remove all CSS properties."""
        ...


class Attrs:
    """A live HTML attribute helper for an HtmlComponent's root element.

    [Anvil Docs](https://anvil.works/docs/client/customisation/custom-components/html-components)"""

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
    def update(self, updates: Mapping[str, _AttrValue], /, **kwargs: _AttrValue) -> None:
        """Merge attribute names and values into this attrs object. `None` values remove attributes.

        [Anvil Docs](https://anvil.works/docs/client/customisation/custom-components/html-components)"""
        ...
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

    [Anvil Docs](https://anvil.works/docs/client/customisation/javascript)"""

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

    [Anvil Docs](https://anvil.works/docs/components)"""

    def __init__(self, **properties: Any) -> None: ...

    parent: Any
    """[Anvil Docs](https://anvil.works/docs/components)"""
    @property
    def tag(self) -> Any:
        """Use this property to store any extra information about this component

        [Anvil Docs](https://anvil.works/docs/components)"""
        ...
    @tag.setter
    def tag(self, value: Any) -> None: ...

    def add_event_handler(self, event_name: _ComponentEvents | str, handler_func: Callable[..., Any], /) -> None:
        """Add an event handler function to be called when the event happens on this component.

        Event handlers will be called in the order they are added. Adding the same event
        handler multiple times will mean it gets called multiple times.

        [Anvil Docs](https://anvil.works/docs/client/events)"""
        ...

    def remove_event_handler(self, event_name: _ComponentEvents | str, handler_func: Callable[..., Any] | None = None, /) -> None:
        """Remove a specific event handler function for a given event.

        Calling remove_event_handler with just the event name will remove all the handlers for this event.

        [Anvil Docs](https://anvil.works/docs/client/events)"""
        ...

    def set_event_handler(self, event_name: _ComponentEvents | str, handler_func: Callable[..., Any] | None, /) -> None:
        """Set a function to call when the 'event_name' event happens on this component.

        Using set_event_handler removes all other handlers.
        Setting the handler function to None removes all handlers.

        [Anvil Docs](https://anvil.works/docs/client/events)"""
        ...

    def get_event_handlers(self, event_name: _ComponentEvents | str, /) -> tuple[Callable[..., Any], ...]:
        """Get the list of event handler functions for a given event.

        [Anvil Docs](https://anvil.works/docs/client/events)"""
        ...

    def remove_from_parent(self) -> None:
        """Remove this component from its parent container.

        [Anvil Docs](https://anvil.works/docs/components)"""
        ...

    def raise_event(self, event_name: _ComponentEvents | str, /, **event_args: Any) -> None:
        """Raise an event on this component.

        [Anvil Docs](https://anvil.works/docs/client/events)"""
        ...

    def scroll_into_view(self, *, smooth: bool = False, align: str = "center") -> None:
        """Scroll this component into view.

        [Anvil Docs](https://anvil.works/docs/components)"""
        ...


_ContainerChild = TypeVar("_ContainerChild", bound=Component, default=Component)


class Container(Component, Generic[_ContainerChild]):
    """Base class for container components.

    [Anvil Docs](https://anvil.works/docs/components)"""

    def add_component(self, component: Component, /, **layout_props: Any) -> None:
        """Add a component to this container.

        [Anvil Docs](https://anvil.works/docs/components)"""
        ...

    def clear(self) -> None:
        """Remove all components from this container.

        [Anvil Docs](https://anvil.works/docs/components)"""
        ...

    def get_components(self) -> list[_ContainerChild]:
        """Get a list of components in this container.

        [Anvil Docs](https://anvil.works/docs/components)"""
        ...

    def raise_event_on_children(self, event_name: str, /, **event_args: Any) -> None:
        """Trigger the 'event_name' event on all children of this component.

        Any keyword arguments are passed to the handler function.

        [Anvil Docs](https://anvil.works/docs/components)"""
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

    [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#label)"""

    @property
    def visible(self) -> bool:
        """Should this component be displayed?

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#label)"""
        ...
    @visible.setter
    def visible(self, value: bool) -> None: ...
    @property
    def tooltip(self) -> str:
        """Text to display when you hover the mouse over this component

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#label)"""
        ...
    @tooltip.setter
    def tooltip(self, value: str) -> None: ...
    @property
    def role(self) -> str | list[str] | None:
        """Choose how this component can appear, based on your app's visual theme.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#label)"""
        ...
    @role.setter
    def role(self, value: str | list[str] | None) -> None: ...

    @property
    def text(self) -> str:
        """The text displayed on this component

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#label)"""
        ...
    @text.setter
    def text(self, value: str) -> None: ...
    @property
    def icon(self) -> str:
        """The icon to display on this component. Either a URL, or a FontAwesome Icon, e.g. 'fa:user'.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#label)"""
        ...
    @icon.setter
    def icon(self, value: str) -> None: ...
    @property
    def icon_align(self) -> str:
        """The alignment of the icon on this component. Set to 'top' for a centred icon on a component with no text.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#label)"""
        ...
    @icon_align.setter
    def icon_align(self, value: str) -> None: ...
    @property
    def font_size(self) -> int | float | None:
        """The height of text displayed on this component in pixels

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#label)"""
        ...
    @font_size.setter
    def font_size(self, value: int | float | None) -> None: ...
    @property
    def font(self) -> str:
        """The font to use for this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#label)"""
        ...
    @font.setter
    def font(self, value: str) -> None: ...
    @property
    def bold(self) -> bool:
        """Display this component's text in bold

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#label)"""
        ...
    @bold.setter
    def bold(self, value: bool) -> None: ...
    @property
    def italic(self) -> bool:
        """Display this component's text in italics

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#label)"""
        ...
    @italic.setter
    def italic(self, value: bool) -> None: ...
    @property
    def underline(self) -> bool:
        """Display this component's text underlined

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#label)"""
        ...
    @underline.setter
    def underline(self, value: bool) -> None: ...
    @property
    def foreground(self) -> str:
        """The foreground colour of this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#label)"""
        ...
    @foreground.setter
    def foreground(self, value: str) -> None: ...
    @property
    def background(self) -> str:
        """The background colour of this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#label)"""
        ...
    @background.setter
    def background(self, value: str) -> None: ...
    @property
    def border(self) -> str:
        """The border of this component. Can take any valid CSS border value.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#label)"""
        ...
    @border.setter
    def border(self, value: str) -> None: ...
    @property
    def align(self) -> str:
        """Align this component's text

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#label)"""
        ...
    @align.setter
    def align(self, value: str) -> None: ...
    @property
    def spacing_above(self) -> Literal["none", "small", "medium", "large"] | None:
        """The vertical space above this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#label)"""
        ...
    @spacing_above.setter
    def spacing_above(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...
    @property
    def spacing_below(self) -> Literal["none", "small", "medium", "large"] | None:
        """The vertical space below this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#label)"""
        ...
    @spacing_below.setter
    def spacing_below(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...


    @property
    def spacing(self) -> SpacingPropertyValue:
        """Margin and padding for this container. Only available in apps that have been migrated to use Layouts.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#label)"""
        ...
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

    [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#link)"""

    @property
    def visible(self) -> bool:
        """[Anvil Docs](https://anvil.works/docs/components/standard-components/basic#link)"""
        ...
    @visible.setter
    def visible(self, value: bool) -> None: ...
    @property
    def tooltip(self) -> str:
        """Text to display when you hover the mouse over this component

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#link)"""
        ...
    @tooltip.setter
    def tooltip(self, value: str) -> None: ...
    @property
    def role(self) -> str | list[str] | None:
        """[Anvil Docs](https://anvil.works/docs/components/standard-components/basic#link)"""
        ...
    @role.setter
    def role(self, value: str | list[str] | None) -> None: ...

    @property
    def text(self) -> str:
        """The text displayed on this component

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#link)"""
        ...
    @text.setter
    def text(self, value: str) -> None: ...
    @property
    def url(self) -> str:
        """The target URL of the link. Can be set to a URL string or to a Media object.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#link)"""
        ...
    @url.setter
    def url(self, value: str) -> None: ...
    @property
    def icon(self) -> str:
        """The icon to display on this component. Either a URL, or a FontAwesome Icon, e.g. 'fa:user'.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#link)"""
        ...
    @icon.setter
    def icon(self, value: str) -> None: ...
    @property
    def icon_align(self) -> str:
        """The alignment of the icon on this component. Set to 'top' for a centred icon on a component with no text.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#link)"""
        ...
    @icon_align.setter
    def icon_align(self, value: str) -> None: ...
    @property
    def font_size(self) -> int | float | None:
        """The height of text displayed on this component in pixels

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#link)"""
        ...
    @font_size.setter
    def font_size(self, value: int | float | None) -> None: ...
    @property
    def font(self) -> str:
        """The font to use for this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#link)"""
        ...
    @font.setter
    def font(self, value: str) -> None: ...
    @property
    def bold(self) -> bool:
        """Display this component's text in bold

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#link)"""
        ...
    @bold.setter
    def bold(self, value: bool) -> None: ...
    @property
    def italic(self) -> bool:
        """Display this component's text in italics

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#link)"""
        ...
    @italic.setter
    def italic(self, value: bool) -> None: ...
    @property
    def underline(self) -> bool:
        """Display this component's text underlined

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#link)"""
        ...
    @underline.setter
    def underline(self, value: bool) -> None: ...
    @property
    def foreground(self) -> str:
        """[Anvil Docs](https://anvil.works/docs/components/standard-components/basic#link)"""
        ...
    @foreground.setter
    def foreground(self, value: str) -> None: ...
    @property
    def background(self) -> str:
        """[Anvil Docs](https://anvil.works/docs/components/standard-components/basic#link)"""
        ...
    @background.setter
    def background(self, value: str) -> None: ...
    @property
    def border(self) -> str:
        """[Anvil Docs](https://anvil.works/docs/components/standard-components/basic#link)"""
        ...
    @border.setter
    def border(self, value: str) -> None: ...
    @property
    def align(self) -> str:
        """Align this component's text

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#link)"""
        ...
    @align.setter
    def align(self, value: str) -> None: ...


    @property
    def text_padding(self) -> PaddingPropertyValue:
        """Padding for the link text. Only available in apps that have been migrated to use Layouts.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#link)"""
        ...
    @text_padding.setter
    def text_padding(self, value: PaddingPropertyValue) -> None: ...

    @override
    def add_event_handler(self, event_name: _LinkEvents | str, handler_func: Callable[..., Any], /) -> None:
        """Add an event handler function to be called when the event happens on this component. Event handlers will be called in the order they are added. Adding the same event handler multiple times will mean it gets called multiple times.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#link)"""
        ...
    @override
    def remove_event_handler(self, event_name: _LinkEvents | str, handler_func: Callable[..., Any] | None = None, /) -> None:
        """Remove a specific event handler function for a given event. Calling remove_event_handler with just the event name will remove all the handlers for this event

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#link)"""
        ...
    @override
    def set_event_handler(self, event_name: _LinkEvents | str, handler_func: Callable[..., Any] | None, /) -> None:
        """Set a function to call when the 'event_name' event happens on this component. Using set_event_handler removes all other handlers. Setting the handler function to None removes all handlers.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#link)"""
        ...
    @override
    def get_event_handlers(self, event_name: _LinkEvents | str, /) -> tuple[Callable[..., Any], ...]: ...
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

    [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#image)"""

    @property
    def visible(self) -> bool:
        """Should this component be displayed?

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#image)"""
        ...
    @visible.setter
    def visible(self, value: bool) -> None: ...
    @property
    def tooltip(self) -> str:
        """Text to display when you hover the mouse over this component

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#image)"""
        ...
    @tooltip.setter
    def tooltip(self, value: str) -> None: ...
    @property
    def role(self) -> str | list[str] | None:
        """Choose how this component can appear, based on your app's visual theme.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#image)"""
        ...
    @role.setter
    def role(self, value: str | list[str] | None) -> None: ...

    @property
    def source(self) -> str | Media:
        """The image to display, as a Media object or URL string.

        For an app theme asset stored at ``theme/assets/<path>``, use the
        runtime-relative URL ``_/theme/<path>`` (for example,
        ``_/theme/puppy.png``). Do not add a leading slash or an ``assets``
        path segment.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#image)"""
        ...
    @source.setter
    def source(self, value: str | Media) -> None: ...
    @property
    def alt_text(self) -> str:
        """Textual replacement for the image used by screen readers and displayed on the page if the image can't be loaded

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#image)"""
        ...
    @alt_text.setter
    def alt_text(self, value: str) -> None: ...
    @property
    def display_mode(self) -> str:
        """Determines how the image's size should be adjusted to fit the size of this Image component.

         - `shrink_to_fit` scales the image to fit while maintaining its aspect ratio.
        - `zoom_to_fill` scales the image to fill the entire container while maintaining its aspect ratio. If the image is too large, it will be cropped to fit.
        - `fill_width` shrinks or grows the image so the width fits the container.
        - `original_size` - displays the image at whatever the browser thinks the original size is. If that would cause the image to be wider than the Image component, it shrinks the image to ensure it fits within the width of the Image component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#image)"""
        ...
    @display_mode.setter
    def display_mode(self, value: str) -> None: ...
    @property
    def horizontal_align(self) -> str:
        """Position the image horizontally within this component

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#image)"""
        ...
    @horizontal_align.setter
    def horizontal_align(self, value: str) -> None: ...
    @property
    def vertical_align(self) -> str:
        """Position the image vertically within this component

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#image)"""
        ...
    @vertical_align.setter
    def vertical_align(self, value: str) -> None: ...
    @property
    def height(self) -> str:
        """The height of this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#image)"""
        ...
    @height.setter
    def height(self, value: str) -> None: ...


    @property
    def background(self) -> str:
        """The background colour of this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#image)"""
        ...
    @background.setter
    def background(self, value: str) -> None: ...
    @property
    def border(self) -> str:
        """The border of this component. Can take any valid CSS border value.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#image)"""
        ...
    @border.setter
    def border(self, value: str) -> None: ...
    @property
    def border_radius(self) -> str:
        """The border radius of this component

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#image)"""
        ...
    @border_radius.setter
    def border_radius(self, value: str) -> None: ...
    @property
    def foreground(self) -> str:
        """The foreground colour of this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#image)"""
        ...
    @foreground.setter
    def foreground(self, value: str) -> None: ...
    @property
    def margin(self) -> MarginPropertyValue:
        """Margin for this component. Only available in apps that have been migrated to use Layouts.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#image)"""
        ...
    @margin.setter
    def margin(self, value: MarginPropertyValue) -> None: ...
    @property
    def spacing_above(self) -> Literal["none", "small", "medium", "large"] | None:
        """The vertical space above this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#image)"""
        ...
    @spacing_above.setter
    def spacing_above(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...
    @property
    def spacing_below(self) -> Literal["none", "small", "medium", "large"] | None:
        """The vertical space below this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#image)"""
        ...
    @spacing_below.setter
    def spacing_below(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...

    @override
    def add_event_handler(self, event_name: _ImageEvents | str, handler_func: Callable[..., Any], /) -> None:
        """Add an event handler function to be called when the event happens on this component. Event handlers will be called in the order they are added. Adding the same event handler multiple times will mean it gets called multiple times.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#image)"""
        ...
    @override
    def remove_event_handler(self, event_name: _ImageEvents | str, handler_func: Callable[..., Any] | None = None, /) -> None:
        """Remove a specific event handler function for a given event. Calling remove_event_handler with just the event name will remove all the handlers for this event

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#image)"""
        ...
    @override
    def set_event_handler(self, event_name: _ImageEvents | str, handler_func: Callable[..., Any] | None, /) -> None:
        """Set a function to call when the 'event_name' event happens on this component. Using set_event_handler removes all other handlers. Setting the handler function to None removes all handlers.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#image)"""
        ...
    @override
    def get_event_handlers(self, event_name: _ImageEvents | str, /) -> tuple[Callable[..., Any], ...]: ...
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

    [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#spacer)"""

    @property
    def visible(self) -> bool:
        """Should this component be displayed?

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#spacer)"""
        ...
    @visible.setter
    def visible(self, value: bool) -> None: ...
    @property
    def tooltip(self) -> str:
        """Text to display when you hover the mouse over this component

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#spacer)"""
        ...
    @tooltip.setter
    def tooltip(self, value: str) -> None: ...

    @property
    def height(self) -> int:
        """The height of this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#spacer)"""
        ...
    @height.setter
    def height(self, value: int) -> None: ...


    @property
    def spacing_above(self) -> Literal["none", "small", "medium", "large"] | None:
        """The vertical space above this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#spacer)"""
        ...
    @spacing_above.setter
    def spacing_above(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...
    @property
    def spacing_below(self) -> Literal["none", "small", "medium", "large"] | None:
        """The vertical space below this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#spacer)"""
        ...
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

    [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#richtext)"""

    @property
    def visible(self) -> bool:
        """Should this component be displayed?

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#richtext)"""
        ...
    @visible.setter
    def visible(self, value: bool) -> None: ...
    @property
    def tooltip(self) -> str:
        """Text to display when you hover the mouse over this component

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#richtext)"""
        ...
    @tooltip.setter
    def tooltip(self, value: str) -> None: ...
    @property
    def role(self) -> str | list[str] | None:
        """Choose how this component can appear, based on your app's visual theme.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#richtext)"""
        ...
    @role.setter
    def role(self, value: str | list[str] | None) -> None: ...

    @property
    def content(self) -> str:
        """The content to render in this component, in the format specified by the 'format' property

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#richtext)"""
        ...
    @content.setter
    def content(self, value: str) -> None: ...
    @property
    def text(self) -> str:
        """[Anvil Docs](https://anvil.works/docs/components/standard-components/containers#richtext)"""
        ...
    @text.setter
    def text(self, value: str) -> None: ...
    @property
    def format(self) -> str:
        """The format of the content of this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#richtext)"""
        ...
    @format.setter
    def format(self, value: str) -> None: ...
    @property
    def enable_slots(self) -> bool:
        """If true {braces} in content define slots. If false, braces in content display normally.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#richtext)"""
        ...
    @enable_slots.setter
    def enable_slots(self, value: bool) -> None: ...
    @property
    def data(self) -> dict[str, Any]:
        """A dict of data or Components to populate the named content {slots}. Can also be a dict-like object.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#richtext)"""
        ...
    @data.setter
    def data(self, value: dict[str, Any]) -> None: ...


    @property
    def align(self) -> str:
        """Align this component's text

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#richtext)"""
        ...
    @align.setter
    def align(self, value: str) -> None: ...
    @property
    def font_size(self) -> int | float | None:
        """The height of text displayed on this component in pixels

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#richtext)"""
        ...
    @font_size.setter
    def font_size(self, value: int | float | None) -> None: ...
    @property
    def font(self) -> str:
        """The font to use for this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#richtext)"""
        ...
    @font.setter
    def font(self, value: str) -> None: ...
    @property
    def bold(self) -> bool:
        """[Anvil Docs](https://anvil.works/docs/components/standard-components/containers#richtext)"""
        ...
    @bold.setter
    def bold(self, value: bool) -> None: ...
    @property
    def italic(self) -> bool:
        """[Anvil Docs](https://anvil.works/docs/components/standard-components/containers#richtext)"""
        ...
    @italic.setter
    def italic(self, value: bool) -> None: ...
    @property
    def underline(self) -> bool:
        """[Anvil Docs](https://anvil.works/docs/components/standard-components/containers#richtext)"""
        ...
    @underline.setter
    def underline(self, value: bool) -> None: ...
    @property
    def background(self) -> str:
        """The background colour of this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#richtext)"""
        ...
    @background.setter
    def background(self, value: str) -> None: ...
    @property
    def border(self) -> str:
        """The border of this component. Can take any valid CSS border value.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#richtext)"""
        ...
    @border.setter
    def border(self, value: str) -> None: ...
    @property
    def foreground(self) -> str:
        """The foreground colour of this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#richtext)"""
        ...
    @foreground.setter
    def foreground(self, value: str) -> None: ...
    @property
    def spacing(self) -> SpacingPropertyValue:
        """Margin and padding for this container. Only available in apps that have been migrated to use Layouts.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#richtext)"""
        ...
    @spacing.setter
    def spacing(self, value: SpacingPropertyValue) -> None: ...
    @property
    def spacing_above(self) -> Literal["none", "small", "medium", "large"] | None:
        """The vertical space above this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#richtext)"""
        ...
    @spacing_above.setter
    def spacing_above(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...
    @property
    def spacing_below(self) -> Literal["none", "small", "medium", "large"] | None:
        """The vertical space below this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#richtext)"""
        ...
    @spacing_below.setter
    def spacing_below(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...

    @overload
    def add_component(self, component: Component, /, **layout_props: Unpack[_SlottedLayoutKwargs]) -> None: ...
    @overload
    def add_component(self, component: Component, /, **layout_props: Any) -> None:
        """Add a component to this panel, in the specified slot

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#richtext)"""
        ...
    def clear(self, *, slot: str | None = None) -> None:
        """clear the Rich Text Component of all components or clear a specific slot of components.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#richtext)"""
        ...

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

    [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#button)"""

    @property
    def enabled(self) -> bool:
        """True if this component should allow user interaction.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#button)"""
        ...
    @enabled.setter
    def enabled(self, value: bool) -> None: ...
    @property
    def visible(self) -> bool:
        """Should this component be displayed?

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#button)"""
        ...
    @visible.setter
    def visible(self, value: bool) -> None: ...
    @property
    def tooltip(self) -> str:
        """Text to display when you hover the mouse over this component

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#button)"""
        ...
    @tooltip.setter
    def tooltip(self, value: str) -> None: ...
    @property
    def role(self) -> str | list[str] | None:
        """Choose how this component can appear, based on your app's visual theme.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#button)"""
        ...
    @role.setter
    def role(self, value: str | list[str] | None) -> None: ...

    @property
    def text(self) -> str:
        """The text displayed on this component

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#button)"""
        ...
    @text.setter
    def text(self, value: str) -> None: ...
    @property
    def icon(self) -> str:
        """The icon to display on this component. Either a URL, or a FontAwesome Icon, e.g. 'fa:user'.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#button)"""
        ...
    @icon.setter
    def icon(self, value: str) -> None: ...
    @property
    def icon_align(self) -> str:
        """The alignment of the icon on this component. Set to 'top' for a centred icon on a component with no text.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#button)"""
        ...
    @icon_align.setter
    def icon_align(self, value: str) -> None: ...
    @property
    def font_size(self) -> int | float | None:
        """The height of text displayed on this component in pixels

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#button)"""
        ...
    @font_size.setter
    def font_size(self, value: int | float | None) -> None: ...
    @property
    def font(self) -> str:
        """The font to use for this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#button)"""
        ...
    @font.setter
    def font(self, value: str) -> None: ...
    @property
    def bold(self) -> bool:
        """Display this component's text in bold

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#button)"""
        ...
    @bold.setter
    def bold(self, value: bool) -> None: ...
    @property
    def italic(self) -> bool:
        """Display this component's text in italics

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#button)"""
        ...
    @italic.setter
    def italic(self, value: bool) -> None: ...
    @property
    def underline(self) -> bool:
        """Display this component's text underlined

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#button)"""
        ...
    @underline.setter
    def underline(self, value: bool) -> None: ...
    @property
    def foreground(self) -> str:
        """The foreground colour of this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#button)"""
        ...
    @foreground.setter
    def foreground(self, value: str) -> None: ...
    @property
    def background(self) -> str:
        """The background colour of this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#button)"""
        ...
    @background.setter
    def background(self, value: str) -> None: ...
    @property
    def border(self) -> str:
        """The border of this component. Can take any valid CSS border value.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#button)"""
        ...
    @border.setter
    def border(self, value: str) -> None: ...
    @property
    def align(self) -> Literal["left", "center", "right", "full"] | str:
        """The position of this button in the available space.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#button)"""
        ...
    @align.setter
    def align(self, value: Literal["left", "center", "right", "full"] | str) -> None: ...


    @property
    def spacing(self) -> SpacingPropertyValue:
        """Margin and padding for this container. Only available in apps that have been migrated to use Layouts.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#button)"""
        ...
    @spacing.setter
    def spacing(self, value: SpacingPropertyValue) -> None: ...
    @property
    def spacing_above(self) -> Literal["none", "small", "medium", "large"] | None:
        """The vertical space above this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#button)"""
        ...
    @spacing_above.setter
    def spacing_above(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...
    @property
    def spacing_below(self) -> Literal["none", "small", "medium", "large"] | None:
        """The vertical space below this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#button)"""
        ...
    @spacing_below.setter
    def spacing_below(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...

    @override
    def add_event_handler(self, event_name: _ButtonEvents | str, handler_func: Callable[..., Any], /) -> None:
        """Add an event handler function to be called when the event happens on this component. Event handlers will be called in the order they are added. Adding the same event handler multiple times will mean it gets called multiple times.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#button)"""
        ...
    @override
    def remove_event_handler(self, event_name: _ButtonEvents | str, handler_func: Callable[..., Any] | None = None, /) -> None:
        """Remove a specific event handler function for a given event. Calling remove_event_handler with just the event name will remove all the handlers for this event

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#button)"""
        ...
    @override
    def set_event_handler(self, event_name: _ButtonEvents | str, handler_func: Callable[..., Any] | None, /) -> None:
        """Set a function to call when the 'event_name' event happens on this component. Using set_event_handler removes all other handlers. Setting the handler function to None removes all handlers.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#button)"""
        ...
    @override
    def get_event_handlers(self, event_name: _ButtonEvents | str, /) -> tuple[Callable[..., Any], ...]: ...
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
        align: Literal["left", "center", "right", "full"] | str = ...,
        spacing: SpacingPropertyValue = ...,
        spacing_above: Literal["none", "small", "medium", "large"] | None = ...,
        spacing_below: Literal["none", "small", "medium", "large"] | None = ...,
    ) -> None: ...

class TextBox(Component):
    """A single-line text input component.

    [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#textbox)"""

    @property
    def enabled(self) -> bool:
        """True if this component should allow user interaction.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#textbox)"""
        ...
    @enabled.setter
    def enabled(self, value: bool) -> None: ...
    @property
    def visible(self) -> bool:
        """Should this component be displayed?

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#textbox)"""
        ...
    @visible.setter
    def visible(self, value: bool) -> None: ...
    @property
    def tooltip(self) -> str:
        """Text to display when you hover the mouse over this component

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#textbox)"""
        ...
    @tooltip.setter
    def tooltip(self, value: str) -> None: ...
    @property
    def role(self) -> str | list[str] | None:
        """Choose how this component can appear, based on your app's visual theme.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#textbox)"""
        ...
    @role.setter
    def role(self, value: str | list[str] | None) -> None: ...

    @property
    def text(self) -> str:
        """The text displayed on this component

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#textbox)"""
        ...
    @text.setter
    def text(self, value: str) -> None: ...
    @property
    def placeholder(self) -> str:
        """The text to be displayed when the component is empty.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#textbox)"""
        ...
    @placeholder.setter
    def placeholder(self, value: str) -> None: ...
    @property
    def type(self) -> str:
        """What type of data will be entered into this box?

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#textbox)"""
        ...
    @type.setter
    def type(self, value: str) -> None: ...
    @property
    def hide_text(self) -> bool:
        """Display stars instead of the text in this box

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#textbox)"""
        ...
    @hide_text.setter
    def hide_text(self, value: bool) -> None: ...
    @property
    def font_size(self) -> int | float | None:
        """The height of text displayed on this component in pixels

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#textbox)"""
        ...
    @font_size.setter
    def font_size(self, value: int | float | None) -> None: ...
    @property
    def font(self) -> str:
        """The font to use for this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#textbox)"""
        ...
    @font.setter
    def font(self, value: str) -> None: ...
    @property
    def bold(self) -> bool:
        """Display this component's text in bold

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#textbox)"""
        ...
    @bold.setter
    def bold(self, value: bool) -> None: ...
    @property
    def italic(self) -> bool:
        """Display this component's text in italics

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#textbox)"""
        ...
    @italic.setter
    def italic(self, value: bool) -> None: ...
    @property
    def underline(self) -> bool:
        """Display this component's text underlined

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#textbox)"""
        ...
    @underline.setter
    def underline(self, value: bool) -> None: ...
    @property
    def foreground(self) -> str:
        """The foreground colour of this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#textbox)"""
        ...
    @foreground.setter
    def foreground(self, value: str) -> None: ...
    @property
    def background(self) -> str:
        """The background colour of this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#textbox)"""
        ...
    @background.setter
    def background(self, value: str) -> None: ...
    @property
    def border(self) -> str:
        """The border of this component. Can take any valid CSS border value.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#textbox)"""
        ...
    @border.setter
    def border(self, value: str) -> None: ...
    @property
    def align(self) -> str:
        """Align this component's text

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#textbox)"""
        ...
    @align.setter
    def align(self, value: str) -> None: ...


    @property
    def margin(self) -> MarginPropertyValue:
        """Margin for this component. Only available in apps that have been migrated to use Layouts.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#textbox)"""
        ...
    @margin.setter
    def margin(self, value: MarginPropertyValue) -> None: ...
    @property
    def spacing_above(self) -> Literal["none", "small", "medium", "large"] | None:
        """The vertical space above this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#textbox)"""
        ...
    @spacing_above.setter
    def spacing_above(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...
    @property
    def spacing_below(self) -> Literal["none", "small", "medium", "large"] | None:
        """The vertical space below this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#textbox)"""
        ...
    @spacing_below.setter
    def spacing_below(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...

    @override
    def add_event_handler(self, event_name: _TextBoxEvents | str, handler_func: Callable[..., Any], /) -> None:
        """Add an event handler function to be called when the event happens on this component. Event handlers will be called in the order they are added. Adding the same event handler multiple times will mean it gets called multiple times.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#textbox)"""
        ...
    @override
    def remove_event_handler(self, event_name: _TextBoxEvents | str, handler_func: Callable[..., Any] | None = None, /) -> None:
        """Remove a specific event handler function for a given event. Calling remove_event_handler with just the event name will remove all the handlers for this event

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#textbox)"""
        ...
    @override
    def set_event_handler(self, event_name: _TextBoxEvents | str, handler_func: Callable[..., Any] | None, /) -> None:
        """Set a function to call when the 'event_name' event happens on this component. Using set_event_handler removes all other handlers. Setting the handler function to None removes all handlers.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#textbox)"""
        ...
    @override
    def get_event_handlers(self, event_name: _TextBoxEvents | str, /) -> tuple[Callable[..., Any], ...]: ...
    @override
    def raise_event(self, event_name: _TextBoxEvents | str, /, **event_args: Any) -> None: ...

    def focus(self) -> None:
        """Set focus to this text box.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#textbox)"""
        ...

    def select(self) -> None:
        """Select all text in this text box.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#textbox)"""
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

    [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#textarea)"""

    @property
    def enabled(self) -> bool:
        """True if this component should allow user interaction.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#textarea)"""
        ...
    @enabled.setter
    def enabled(self, value: bool) -> None: ...
    @property
    def visible(self) -> bool:
        """Should this component be displayed?

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#textarea)"""
        ...
    @visible.setter
    def visible(self, value: bool) -> None: ...
    @property
    def tooltip(self) -> str:
        """Text to display when you hover the mouse over this component

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#textarea)"""
        ...
    @tooltip.setter
    def tooltip(self, value: str) -> None: ...
    @property
    def role(self) -> str | list[str] | None:
        """Choose how this component can appear, based on your app's visual theme.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#textarea)"""
        ...
    @role.setter
    def role(self, value: str | list[str] | None) -> None: ...

    @property
    def text(self) -> str:
        """The text displayed on this component

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#textarea)"""
        ...
    @text.setter
    def text(self, value: str) -> None: ...
    @property
    def placeholder(self) -> str:
        """The text to be displayed when the component is empty.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#textarea)"""
        ...
    @placeholder.setter
    def placeholder(self, value: str) -> None: ...
    @property
    def auto_expand(self) -> bool:
        """If true, the text area will expand vertically to fit its contents

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#textarea)"""
        ...
    @auto_expand.setter
    def auto_expand(self, value: bool) -> None: ...
    @property
    def height(self) -> str:
        """The height of this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#textarea)"""
        ...
    @height.setter
    def height(self, value: str) -> None: ...
    @property
    def font_size(self) -> int | float | None:
        """The height of text displayed on this component in pixels

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#textarea)"""
        ...
    @font_size.setter
    def font_size(self, value: int | float | None) -> None: ...
    @property
    def font(self) -> str:
        """The font to use for this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#textarea)"""
        ...
    @font.setter
    def font(self, value: str) -> None: ...
    @property
    def bold(self) -> bool:
        """Display this component's text in bold

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#textarea)"""
        ...
    @bold.setter
    def bold(self, value: bool) -> None: ...
    @property
    def italic(self) -> bool:
        """Display this component's text in italics

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#textarea)"""
        ...
    @italic.setter
    def italic(self, value: bool) -> None: ...
    @property
    def underline(self) -> bool:
        """Display this component's text underlined

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#textarea)"""
        ...
    @underline.setter
    def underline(self, value: bool) -> None: ...
    @property
    def foreground(self) -> str:
        """The foreground colour of this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#textarea)"""
        ...
    @foreground.setter
    def foreground(self, value: str) -> None: ...
    @property
    def background(self) -> str:
        """The background colour of this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#textarea)"""
        ...
    @background.setter
    def background(self, value: str) -> None: ...
    @property
    def border(self) -> str:
        """The border of this component. Can take any valid CSS border value.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#textarea)"""
        ...
    @border.setter
    def border(self, value: str) -> None: ...


    @property
    def align(self) -> str:
        """Align this component's text

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#textarea)"""
        ...
    @align.setter
    def align(self, value: str) -> None: ...
    @property
    def margin(self) -> MarginPropertyValue:
        """Margin for this component. Only available in apps that have been migrated to use Layouts.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#textarea)"""
        ...
    @margin.setter
    def margin(self, value: MarginPropertyValue) -> None: ...
    @property
    def spacing_above(self) -> Literal["none", "small", "medium", "large"] | None:
        """The vertical space above this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#textarea)"""
        ...
    @spacing_above.setter
    def spacing_above(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...
    @property
    def spacing_below(self) -> Literal["none", "small", "medium", "large"] | None:
        """The vertical space below this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#textarea)"""
        ...
    @spacing_below.setter
    def spacing_below(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...

    @override
    def add_event_handler(self, event_name: _TextAreaEvents | str, handler_func: Callable[..., Any], /) -> None:
        """Add an event handler function to be called when the event happens on this component. Event handlers will be called in the order they are added. Adding the same event handler multiple times will mean it gets called multiple times.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#textarea)"""
        ...
    @override
    def remove_event_handler(self, event_name: _TextAreaEvents | str, handler_func: Callable[..., Any] | None = None, /) -> None:
        """Remove a specific event handler function for a given event. Calling remove_event_handler with just the event name will remove all the handlers for this event

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#textarea)"""
        ...
    @override
    def set_event_handler(self, event_name: _TextAreaEvents | str, handler_func: Callable[..., Any] | None, /) -> None:
        """Set a function to call when the 'event_name' event happens on this component. Using set_event_handler removes all other handlers. Setting the handler function to None removes all handlers.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#textarea)"""
        ...
    @override
    def get_event_handlers(self, event_name: _TextAreaEvents | str, /) -> tuple[Callable[..., Any], ...]: ...
    @override
    def raise_event(self, event_name: _TextAreaEvents | str, /, **event_args: Any) -> None: ...

    def focus(self) -> None:
        """Set focus to this text area.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#textarea)"""
        ...

    def select(self) -> None:
        """Select all text in this text area.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#textarea)"""
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

    [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#checkbox)"""

    @property
    def enabled(self) -> bool:
        """True if this component should allow user interaction.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#checkbox)"""
        ...
    @enabled.setter
    def enabled(self, value: bool) -> None: ...
    @property
    def visible(self) -> bool:
        """Should this component be displayed?

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#checkbox)"""
        ...
    @visible.setter
    def visible(self, value: bool) -> None: ...
    @property
    def tooltip(self) -> str:
        """Text to display when you hover the mouse over this component

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#checkbox)"""
        ...
    @tooltip.setter
    def tooltip(self, value: str) -> None: ...
    @property
    def role(self) -> str | list[str] | None:
        """Choose how this component can appear, based on your app's visual theme.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#checkbox)"""
        ...
    @role.setter
    def role(self, value: str | list[str] | None) -> None: ...

    @property
    def checked(self) -> bool:
        """The status of the checkbox

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#checkbox)"""
        ...
    @checked.setter
    def checked(self, value: bool) -> None: ...
    @property
    def allow_indeterminate(self) -> bool:
        """Support an indeterminate state. The indeterminate state can only be set in code by setting checked=None.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#checkbox)"""
        ...
    @allow_indeterminate.setter
    def allow_indeterminate(self, value: bool) -> None: ...
    @property
    def text(self) -> str:
        """The text displayed on this component

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#checkbox)"""
        ...
    @text.setter
    def text(self, value: str) -> None: ...
    @property
    def font_size(self) -> int | float | None:
        """The height of text displayed on this component in pixels

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#checkbox)"""
        ...
    @font_size.setter
    def font_size(self, value: int | float | None) -> None: ...
    @property
    def font(self) -> str:
        """The font to use for this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#checkbox)"""
        ...
    @font.setter
    def font(self, value: str) -> None: ...
    @property
    def bold(self) -> bool:
        """Display this component's text in bold

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#checkbox)"""
        ...
    @bold.setter
    def bold(self, value: bool) -> None: ...
    @property
    def italic(self) -> bool:
        """Display this component's text in italics

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#checkbox)"""
        ...
    @italic.setter
    def italic(self, value: bool) -> None: ...
    @property
    def underline(self) -> bool:
        """Display this component's text underlined

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#checkbox)"""
        ...
    @underline.setter
    def underline(self, value: bool) -> None: ...
    @property
    def foreground(self) -> str:
        """The foreground colour of this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#checkbox)"""
        ...
    @foreground.setter
    def foreground(self, value: str) -> None: ...
    @property
    def background(self) -> str:
        """The background colour of this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#checkbox)"""
        ...
    @background.setter
    def background(self, value: str) -> None: ...
    @property
    def border(self) -> str:
        """The border of this component. Can take any valid CSS border value.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#checkbox)"""
        ...
    @border.setter
    def border(self, value: str) -> None: ...
    @property
    def align(self) -> str:
        """Align this component's text

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#checkbox)"""
        ...
    @align.setter
    def align(self, value: str) -> None: ...


    @property
    def spacing(self) -> SpacingPropertyValue:
        """Margin and padding for this container. Only available in apps that have been migrated to use Layouts.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#checkbox)"""
        ...
    @spacing.setter
    def spacing(self, value: SpacingPropertyValue) -> None: ...
    @property
    def spacing_above(self) -> Literal["none", "small", "medium", "large"] | None:
        """The vertical space above this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#checkbox)"""
        ...
    @spacing_above.setter
    def spacing_above(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...
    @property
    def spacing_below(self) -> Literal["none", "small", "medium", "large"] | None:
        """The vertical space below this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#checkbox)"""
        ...
    @spacing_below.setter
    def spacing_below(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...

    @override
    def add_event_handler(self, event_name: _CheckBoxEvents | str, handler_func: Callable[..., Any], /) -> None:
        """Add an event handler function to be called when the event happens on this component. Event handlers will be called in the order they are added. Adding the same event handler multiple times will mean it gets called multiple times.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#checkbox)"""
        ...
    @override
    def remove_event_handler(self, event_name: _CheckBoxEvents | str, handler_func: Callable[..., Any] | None = None, /) -> None:
        """Remove a specific event handler function for a given event. Calling remove_event_handler with just the event name will remove all the handlers for this event

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#checkbox)"""
        ...
    @override
    def set_event_handler(self, event_name: _CheckBoxEvents | str, handler_func: Callable[..., Any] | None, /) -> None:
        """Set a function to call when the 'event_name' event happens on this component. Using set_event_handler removes all other handlers. Setting the handler function to None removes all handlers.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#checkbox)"""
        ...
    @override
    def get_event_handlers(self, event_name: _CheckBoxEvents | str, /) -> tuple[Callable[..., Any], ...]: ...
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

    [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#radiobutton)"""

    @property
    def enabled(self) -> bool:
        """True if this component should allow user interaction.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#radiobutton)"""
        ...
    @enabled.setter
    def enabled(self, value: bool) -> None: ...
    @property
    def visible(self) -> bool:
        """Should this component be displayed?

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#radiobutton)"""
        ...
    @visible.setter
    def visible(self, value: bool) -> None: ...
    @property
    def tooltip(self) -> str:
        """Text to display when you hover the mouse over this component

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#radiobutton)"""
        ...
    @tooltip.setter
    def tooltip(self, value: str) -> None: ...
    @property
    def role(self) -> str | list[str] | None:
        """Choose how this component can appear, based on your app's visual theme.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#radiobutton)"""
        ...
    @role.setter
    def role(self, value: str | list[str] | None) -> None: ...

    @property
    def selected(self) -> bool:
        """The status of the radio button

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#radiobutton)"""
        ...
    @selected.setter
    def selected(self, value: bool) -> None: ...
    @property
    def value(self) -> Any:
        """The value of the group when this radio button is selected

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#radiobutton)"""
        ...
    @value.setter
    def value(self, value: Any) -> None: ...
    @property
    def group_name(self) -> str:
        """The name of the group this radio button belongs to.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#radiobutton)"""
        ...
    @group_name.setter
    def group_name(self, value: str) -> None: ...
    @property
    def text(self) -> str:
        """The text displayed on this component

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#radiobutton)"""
        ...
    @text.setter
    def text(self, value: str) -> None: ...
    @property
    def font_size(self) -> int | float | None:
        """The height of text displayed on this component in pixels

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#radiobutton)"""
        ...
    @font_size.setter
    def font_size(self, value: int | float | None) -> None: ...
    @property
    def font(self) -> str:
        """The font to use for this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#radiobutton)"""
        ...
    @font.setter
    def font(self, value: str) -> None: ...
    @property
    def bold(self) -> bool:
        """Display this component's text in bold

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#radiobutton)"""
        ...
    @bold.setter
    def bold(self, value: bool) -> None: ...
    @property
    def italic(self) -> bool:
        """Display this component's text in italics

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#radiobutton)"""
        ...
    @italic.setter
    def italic(self, value: bool) -> None: ...
    @property
    def underline(self) -> bool:
        """Display this component's text underlined

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#radiobutton)"""
        ...
    @underline.setter
    def underline(self, value: bool) -> None: ...
    @property
    def foreground(self) -> str:
        """The foreground colour of this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#radiobutton)"""
        ...
    @foreground.setter
    def foreground(self, value: str) -> None: ...
    @property
    def background(self) -> str:
        """The background colour of this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#radiobutton)"""
        ...
    @background.setter
    def background(self, value: str) -> None: ...
    @property
    def border(self) -> str:
        """The border of this component. Can take any valid CSS border value.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#radiobutton)"""
        ...
    @border.setter
    def border(self, value: str) -> None: ...
    @property
    def align(self) -> str:
        """Align this component's text

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#radiobutton)"""
        ...
    @align.setter
    def align(self, value: str) -> None: ...


    @property
    def spacing(self) -> SpacingPropertyValue:
        """Margin and padding for this container. Only available in apps that have been migrated to use Layouts.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#radiobutton)"""
        ...
    @spacing.setter
    def spacing(self, value: SpacingPropertyValue) -> None: ...
    @property
    def spacing_above(self) -> Literal["none", "small", "medium", "large"] | None:
        """The vertical space above this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#radiobutton)"""
        ...
    @spacing_above.setter
    def spacing_above(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...
    @property
    def spacing_below(self) -> Literal["none", "small", "medium", "large"] | None:
        """The vertical space below this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#radiobutton)"""
        ...
    @spacing_below.setter
    def spacing_below(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...

    @override
    def add_event_handler(self, event_name: _RadioButtonEvents | str, handler_func: Callable[..., Any], /) -> None:
        """Add an event handler function to be called when the event happens on this component. Event handlers will be called in the order they are added. Adding the same event handler multiple times will mean it gets called multiple times.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#radiobutton)"""
        ...
    @override
    def remove_event_handler(self, event_name: _RadioButtonEvents | str, handler_func: Callable[..., Any] | None = None, /) -> None:
        """Remove a specific event handler function for a given event. Calling remove_event_handler with just the event name will remove all the handlers for this event

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#radiobutton)"""
        ...
    @override
    def set_event_handler(self, event_name: _RadioButtonEvents | str, handler_func: Callable[..., Any] | None, /) -> None:
        """Set a function to call when the 'event_name' event happens on this component. Using set_event_handler removes all other handlers. Setting the handler function to None removes all handlers.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#radiobutton)"""
        ...
    @override
    def get_event_handlers(self, event_name: _RadioButtonEvents | str, /) -> tuple[Callable[..., Any], ...]: ...
    @override
    def raise_event(self, event_name: _RadioButtonEvents | str, /, **event_args: Any) -> None: ...

    @staticmethod
    def get_group_value(group_name: str) -> Any:
        """Get the selected value from a radio button group.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#radiobutton)"""
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

    [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#dropdown)"""

    @property
    def enabled(self) -> bool:
        """True if this component should allow user interaction.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#dropdown)"""
        ...
    @enabled.setter
    def enabled(self, value: bool) -> None: ...
    @property
    def visible(self) -> bool:
        """Should this component be displayed?

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#dropdown)"""
        ...
    @visible.setter
    def visible(self, value: bool) -> None: ...
    @property
    def tooltip(self) -> str:
        """Text to display when you hover the mouse over this component

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#dropdown)"""
        ...
    @tooltip.setter
    def tooltip(self, value: str) -> None: ...
    @property
    def role(self) -> str | list[str] | None:
        """Choose how this component can appear, based on your app's visual theme.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#dropdown)"""
        ...
    @role.setter
    def role(self, value: str | list[str] | None) -> None: ...

    @property
    def items(self) -> list[Any]:
        """The items to display in this dropdown.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#dropdown)"""
        ...
    @items.setter
    def items(self, value: list[Any]) -> None: ...
    @property
    def selected_value(self) -> Any:
        """The value of the currently selected item. Can only be set at runtime.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#dropdown)"""
        ...
    @selected_value.setter
    def selected_value(self, value: Any) -> None: ...
    @property
    def include_placeholder(self) -> bool:
        """Whether to add a placeholder item to the list with value None

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#dropdown)"""
        ...
    @include_placeholder.setter
    def include_placeholder(self, value: bool) -> None: ...
    @property
    def placeholder(self) -> str:
        """The text to be displayed when the selected_value is None.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#dropdown)"""
        ...
    @placeholder.setter
    def placeholder(self, value: str) -> None: ...
    @property
    def font_size(self) -> int | float | None:
        """The height of text displayed on this component in pixels

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#dropdown)"""
        ...
    @font_size.setter
    def font_size(self, value: int | float | None) -> None: ...
    @property
    def font(self) -> str:
        """The font to use for this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#dropdown)"""
        ...
    @font.setter
    def font(self, value: str) -> None: ...
    @property
    def bold(self) -> bool:
        """Display this component's text in bold

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#dropdown)"""
        ...
    @bold.setter
    def bold(self, value: bool) -> None: ...
    @property
    def italic(self) -> bool:
        """Display this component's text in italics

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#dropdown)"""
        ...
    @italic.setter
    def italic(self, value: bool) -> None: ...
    @property
    def underline(self) -> bool:
        """Display this component's text underlined

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#dropdown)"""
        ...
    @underline.setter
    def underline(self, value: bool) -> None: ...
    @property
    def foreground(self) -> str:
        """The foreground colour of this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#dropdown)"""
        ...
    @foreground.setter
    def foreground(self, value: str) -> None: ...
    @property
    def background(self) -> str:
        """The background colour of this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#dropdown)"""
        ...
    @background.setter
    def background(self, value: str) -> None: ...
    @property
    def border(self) -> str:
        """The border of this component. Can take any valid CSS border value.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#dropdown)"""
        ...
    @border.setter
    def border(self, value: str) -> None: ...
    @property
    def align(self) -> str:
        """The position of this dropdown in the available space.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#dropdown)"""
        ...
    @align.setter
    def align(self, value: str) -> None: ...


    @property
    def margin(self) -> MarginPropertyValue:
        """Margin for this component. Only available in apps that have been migrated to use Layouts.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#dropdown)"""
        ...
    @margin.setter
    def margin(self, value: MarginPropertyValue) -> None: ...
    @property
    def spacing_above(self) -> Literal["none", "small", "medium", "large"] | None:
        """The vertical space above this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#dropdown)"""
        ...
    @spacing_above.setter
    def spacing_above(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...
    @property
    def spacing_below(self) -> Literal["none", "small", "medium", "large"] | None:
        """The vertical space below this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#dropdown)"""
        ...
    @spacing_below.setter
    def spacing_below(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...

    @override
    def add_event_handler(self, event_name: _DropDownEvents | str, handler_func: Callable[..., Any], /) -> None:
        """Add an event handler function to be called when the event happens on this component. Event handlers will be called in the order they are added. Adding the same event handler multiple times will mean it gets called multiple times.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#dropdown)"""
        ...
    @override
    def remove_event_handler(self, event_name: _DropDownEvents | str, handler_func: Callable[..., Any] | None = None, /) -> None:
        """Remove a specific event handler function for a given event. Calling remove_event_handler with just the event name will remove all the handlers for this event

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#dropdown)"""
        ...
    @override
    def set_event_handler(self, event_name: _DropDownEvents | str, handler_func: Callable[..., Any] | None, /) -> None:
        """Set a function to call when the 'event_name' event happens on this component. Using set_event_handler removes all other handlers. Setting the handler function to None removes all handlers.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#dropdown)"""
        ...
    @override
    def get_event_handlers(self, event_name: _DropDownEvents | str, /) -> tuple[Callable[..., Any], ...]: ...
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

    [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#datepicker)"""

    @property
    def enabled(self) -> bool:
        """True if this component should allow user interaction.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#datepicker)"""
        ...
    @enabled.setter
    def enabled(self, value: bool) -> None: ...
    @property
    def visible(self) -> bool:
        """Should this component be displayed?

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#datepicker)"""
        ...
    @visible.setter
    def visible(self, value: bool) -> None: ...
    @property
    def tooltip(self) -> str:
        """Text to display when you hover the mouse over this component

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#datepicker)"""
        ...
    @tooltip.setter
    def tooltip(self, value: str) -> None: ...
    @property
    def role(self) -> str | list[str] | None:
        """Choose how this component can appear, based on your app's visual theme.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#datepicker)"""
        ...
    @role.setter
    def role(self, value: str | list[str] | None) -> None: ...

    @property
    def date(self) -> _date | _datetime | None:
        """The date selected on this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#datepicker)"""
        ...
    @date.setter
    def date(self, value: _date | _datetime | str | None) -> None: ...
    @property
    def min_date(self) -> Any:
        """The minimum date the user can select.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#datepicker)"""
        ...
    @min_date.setter
    def min_date(self, value: Any) -> None: ...
    @property
    def max_date(self) -> Any:
        """The maximum date the user can select.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#datepicker)"""
        ...
    @max_date.setter
    def max_date(self, value: Any) -> None: ...
    @property
    def format(self) -> str:
        """The format in which to display the selected date.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#datepicker)"""
        ...
    @format.setter
    def format(self, value: str) -> None: ...
    @property
    def pick_time(self) -> bool:
        """Whether the user should be able to select a time as well as a date

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#datepicker)"""
        ...
    @pick_time.setter
    def pick_time(self, value: bool) -> None: ...
    @property
    def placeholder(self) -> str:
        """A string to display when the DatePicker is empty.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#datepicker)"""
        ...
    @placeholder.setter
    def placeholder(self, value: str) -> None: ...
    @property
    def font_size(self) -> int | float | None:
        """The height of text displayed on this component in pixels

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#datepicker)"""
        ...
    @font_size.setter
    def font_size(self, value: int | float | None) -> None: ...
    @property
    def font(self) -> str:
        """The font to use for this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#datepicker)"""
        ...
    @font.setter
    def font(self, value: str) -> None: ...
    @property
    def bold(self) -> bool:
        """Display this component's text in bold

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#datepicker)"""
        ...
    @bold.setter
    def bold(self, value: bool) -> None: ...
    @property
    def italic(self) -> bool:
        """Display this component's text in italics

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#datepicker)"""
        ...
    @italic.setter
    def italic(self, value: bool) -> None: ...
    @property
    def underline(self) -> bool:
        """Display this component's text underlined

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#datepicker)"""
        ...
    @underline.setter
    def underline(self, value: bool) -> None: ...
    @property
    def foreground(self) -> str:
        """The foreground colour of this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#datepicker)"""
        ...
    @foreground.setter
    def foreground(self, value: str) -> None: ...
    @property
    def background(self) -> str:
        """The background colour of this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#datepicker)"""
        ...
    @background.setter
    def background(self, value: str) -> None: ...
    @property
    def border(self) -> str:
        """The border of this component. Can take any valid CSS border value.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#datepicker)"""
        ...
    @border.setter
    def border(self, value: str) -> None: ...
    @property
    def align(self) -> str:
        """Align this component's text

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#datepicker)"""
        ...
    @align.setter
    def align(self, value: str) -> None: ...


    @property
    def margin(self) -> MarginPropertyValue:
        """Margin for this component. Only available in apps that have been migrated to use Layouts.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#datepicker)"""
        ...
    @margin.setter
    def margin(self, value: MarginPropertyValue) -> None: ...
    @property
    def spacing_above(self) -> Literal["none", "small", "medium", "large"] | None:
        """The vertical space above this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#datepicker)"""
        ...
    @spacing_above.setter
    def spacing_above(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...
    @property
    def spacing_below(self) -> Literal["none", "small", "medium", "large"] | None:
        """The vertical space below this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#datepicker)"""
        ...
    @spacing_below.setter
    def spacing_below(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...

    @override
    def add_event_handler(self, event_name: _DatePickerEvents | str, handler_func: Callable[..., Any], /) -> None:
        """Add an event handler function to be called when the event happens on this component. Event handlers will be called in the order they are added. Adding the same event handler multiple times will mean it gets called multiple times.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#datepicker)"""
        ...
    @override
    def remove_event_handler(self, event_name: _DatePickerEvents | str, handler_func: Callable[..., Any] | None = None, /) -> None:
        """Remove a specific event handler function for a given event. Calling remove_event_handler with just the event name will remove all the handlers for this event

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#datepicker)"""
        ...
    @override
    def set_event_handler(self, event_name: _DatePickerEvents | str, handler_func: Callable[..., Any] | None, /) -> None:
        """Set a function to call when the 'event_name' event happens on this component. Using set_event_handler removes all other handlers. Setting the handler function to None removes all handlers.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#datepicker)"""
        ...
    @override
    def get_event_handlers(self, event_name: _DatePickerEvents | str, /) -> tuple[Callable[..., Any], ...]: ...
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
        date: _date | _datetime | str | None = ...,
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

    [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#fileloader)"""

    @property
    def enabled(self) -> bool:
        """True if this component should allow user interaction.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#fileloader)"""
        ...
    @enabled.setter
    def enabled(self, value: bool) -> None: ...
    @property
    def visible(self) -> bool:
        """Should this component be displayed?

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#fileloader)"""
        ...
    @visible.setter
    def visible(self, value: bool) -> None: ...
    @property
    def tooltip(self) -> str:
        """Text to display when you hover the mouse over this component

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#fileloader)"""
        ...
    @tooltip.setter
    def tooltip(self, value: str) -> None: ...
    @property
    def role(self) -> str | list[str] | None:
        """Choose how this component can appear, based on your app's visual theme.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#fileloader)"""
        ...
    @role.setter
    def role(self, value: str | list[str] | None) -> None: ...

    @property
    def file(self) -> Media | None:
        """The currently selected file (or the first, if multiple files are selected). This is a Media object.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#fileloader)"""
        ...
    @file.setter
    def file(self, value: Media | None) -> None: ...
    @property
    def files(self) -> list[Media]:
        """A list of currently selected files. Each file is a Media object.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#fileloader)"""
        ...
    @files.setter
    def files(self, value: list[Media]) -> None: ...
    @property
    def multiple(self) -> bool:
        """If True, this FileLoader can load multiple files at the same time

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#fileloader)"""
        ...
    @multiple.setter
    def multiple(self, value: bool) -> None: ...
    @property
    def show_state(self) -> bool:
        """If True, display a message describing selected files.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#fileloader)"""
        ...
    @show_state.setter
    def show_state(self, value: bool) -> None: ...
    @property
    def file_types(self) -> str:
        """Specify what type of file to upload. Can accept a MIME type (eg "image/png" or "image/*"), or an extension (eg ".png"), or a comma-separated set of them (eg ".png,.jpg,.jpeg")

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#fileloader)"""
        ...
    @file_types.setter
    def file_types(self, value: str) -> None: ...
    @property
    def text(self) -> str:
        """The text displayed on this component

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#fileloader)"""
        ...
    @text.setter
    def text(self, value: str) -> None: ...
    @property
    def font_size(self) -> int | float | None:
        """The height of text displayed on this component in pixels

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#fileloader)"""
        ...
    @font_size.setter
    def font_size(self, value: int | float | None) -> None: ...
    @property
    def font(self) -> str:
        """The font to use for this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#fileloader)"""
        ...
    @font.setter
    def font(self, value: str) -> None: ...
    @property
    def bold(self) -> bool:
        """Display this component's text in bold

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#fileloader)"""
        ...
    @bold.setter
    def bold(self, value: bool) -> None: ...
    @property
    def italic(self) -> bool:
        """Display this component's text in italics

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#fileloader)"""
        ...
    @italic.setter
    def italic(self, value: bool) -> None: ...
    @property
    def underline(self) -> bool:
        """Display this component's text underlined

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#fileloader)"""
        ...
    @underline.setter
    def underline(self, value: bool) -> None: ...
    @property
    def foreground(self) -> str:
        """The foreground colour of this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#fileloader)"""
        ...
    @foreground.setter
    def foreground(self, value: str) -> None: ...
    @property
    def background(self) -> str:
        """The background colour of this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#fileloader)"""
        ...
    @background.setter
    def background(self, value: str) -> None: ...
    @property
    def border(self) -> str:
        """The border of this component. Can take any valid CSS border value.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#fileloader)"""
        ...
    @border.setter
    def border(self, value: str) -> None: ...
    @property
    def align(self) -> str:
        """Align this component's text

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#fileloader)"""
        ...
    @align.setter
    def align(self, value: str) -> None: ...
    @property
    def icon(self) -> str:
        """The icon to display on this component. Either a URL, or a FontAwesome Icon, e.g. 'fa:user'.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#fileloader)"""
        ...
    @icon.setter
    def icon(self, value: str) -> None: ...
    @property
    def icon_align(self) -> str:
        """The alignment of the icon on this component. Set to 'top' for a centred icon on a component with no text.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#fileloader)"""
        ...
    @icon_align.setter
    def icon_align(self, value: str) -> None: ...


    @property
    def spacing(self) -> SpacingPropertyValue:
        """Margin and padding for this container. Only available in apps that have been migrated to use Layouts.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#fileloader)"""
        ...
    @spacing.setter
    def spacing(self, value: SpacingPropertyValue) -> None: ...
    @property
    def spacing_above(self) -> Literal["none", "small", "medium", "large"] | None:
        """The vertical space above this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#fileloader)"""
        ...
    @spacing_above.setter
    def spacing_above(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...
    @property
    def spacing_below(self) -> Literal["none", "small", "medium", "large"] | None:
        """The vertical space below this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#fileloader)"""
        ...
    @spacing_below.setter
    def spacing_below(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...

    @override
    def add_event_handler(self, event_name: _FileLoaderEvents | str, handler_func: Callable[..., Any], /) -> None:
        """Add an event handler function to be called when the event happens on this component. Event handlers will be called in the order they are added. Adding the same event handler multiple times will mean it gets called multiple times.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#fileloader)"""
        ...
    @override
    def remove_event_handler(self, event_name: _FileLoaderEvents | str, handler_func: Callable[..., Any] | None = None, /) -> None:
        """Remove a specific event handler function for a given event. Calling remove_event_handler with just the event name will remove all the handlers for this event

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#fileloader)"""
        ...
    @override
    def set_event_handler(self, event_name: _FileLoaderEvents | str, handler_func: Callable[..., Any] | None, /) -> None:
        """Set a function to call when the 'event_name' event happens on this component. Using set_event_handler removes all other handlers. Setting the handler function to None removes all handlers.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#fileloader)"""
        ...
    @override
    def get_event_handlers(self, event_name: _FileLoaderEvents | str, /) -> tuple[Callable[..., Any], ...]: ...
    @overload
    @override
    def raise_event(self, event_name: Literal["change"], /, *, file: Media | None, files: list[Media], **event_args: Any) -> None: ...
    @overload
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

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#fileloader)"""
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

    [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#columnpanel)"""

    @property
    def visible(self) -> bool:
        """Should this component be displayed?

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#columnpanel)"""
        ...
    @visible.setter
    def visible(self, value: bool) -> None: ...
    @property
    def tooltip(self) -> str:
        """Text to display when you hover the mouse over this component

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#columnpanel)"""
        ...
    @tooltip.setter
    def tooltip(self, value: str) -> None: ...
    @property
    def role(self) -> str | list[str] | None:
        """Choose how this component can appear, based on your app's visual theme.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#columnpanel)"""
        ...
    @role.setter
    def role(self, value: str | list[str] | None) -> None: ...

    @property
    def col_widths(self) -> str:
        """Custom column widths in this panel

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#columnpanel)"""
        ...
    @col_widths.setter
    def col_widths(self, value: str) -> None: ...
    @property
    def col_spacing(self) -> str:
        """Space between columns

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#columnpanel)"""
        ...
    @col_spacing.setter
    def col_spacing(self, value: str) -> None: ...
    @property
    def wrap_on(self) -> str:
        """The largest display on which to wrap columns in this panel

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#columnpanel)"""
        ...
    @wrap_on.setter
    def wrap_on(self, value: str) -> None: ...
    @property
    def background(self) -> str:
        """The background colour of this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#columnpanel)"""
        ...
    @background.setter
    def background(self, value: str) -> None: ...
    @property
    def foreground(self) -> str:
        """The foreground colour of this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#columnpanel)"""
        ...
    @foreground.setter
    def foreground(self, value: str) -> None: ...
    @property
    def border(self) -> str:
        """The border of this component. Can take any valid CSS border value.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#columnpanel)"""
        ...
    @border.setter
    def border(self, value: str) -> None: ...
    @property
    def spacing_above(self) -> Literal["none", "small", "medium", "large"] | None:
        """The vertical space above this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#columnpanel)"""
        ...
    @spacing_above.setter
    def spacing_above(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...
    @property
    def spacing_below(self) -> Literal["none", "small", "medium", "large"] | None:
        """The vertical space below this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#columnpanel)"""
        ...
    @spacing_below.setter
    def spacing_below(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...


    @property
    def spacing(self) -> SpacingPropertyValue:
        """Margin and padding for this container. Only available in apps that have been migrated to use Layouts.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#columnpanel)"""
        ...
    @spacing.setter
    def spacing(self, value: SpacingPropertyValue) -> None: ...

    @overload
    def add_component(self, component: Component, /, **layout_props: Unpack[_ColumnPanelLayoutKwargs]) -> None: ...
    @overload
    def add_component(self, component: Component, /, **layout_props: Any) -> None:
        """Add a component to this ColumnPanel at the 'index'th position. If 'index' is not specified, adds to the bottom. Useful layout properties:

          full_width_row = True|False
          row_background = [colour]

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#columnpanel)"""
        ...

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

    [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#flowpanel)"""

    @property
    def visible(self) -> bool:
        """Should this component be displayed?

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#flowpanel)"""
        ...
    @visible.setter
    def visible(self, value: bool) -> None: ...
    @property
    def tooltip(self) -> str:
        """Text to display when you hover the mouse over this component

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#flowpanel)"""
        ...
    @tooltip.setter
    def tooltip(self, value: str) -> None: ...
    @property
    def role(self) -> str | list[str] | None:
        """Choose how this component can appear, based on your app's visual theme.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#flowpanel)"""
        ...
    @role.setter
    def role(self, value: str | list[str] | None) -> None: ...

    @property
    def align(self) -> str:
        """Align this component's content

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#flowpanel)"""
        ...
    @align.setter
    def align(self, value: str) -> None: ...
    @property
    def spacing(self) -> SpacingPropertyValue:
        """Margin and padding for this container. Only available in apps that have been migrated to use Layouts.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#flowpanel)"""
        ...
    @spacing.setter
    def spacing(self, value: SpacingPropertyValue) -> None: ...
    @property
    def vertical_align(self) -> str:
        """Align this component's content

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#flowpanel)"""
        ...
    @vertical_align.setter
    def vertical_align(self, value: str) -> None: ...
    @property
    def background(self) -> str:
        """The background colour of this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#flowpanel)"""
        ...
    @background.setter
    def background(self, value: str) -> None: ...
    @property
    def foreground(self) -> str:
        """The foreground colour of this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#flowpanel)"""
        ...
    @foreground.setter
    def foreground(self, value: str) -> None: ...
    @property
    def border(self) -> str:
        """The border of this component. Can take any valid CSS border value.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#flowpanel)"""
        ...
    @border.setter
    def border(self, value: str) -> None: ...
    @property
    def spacing_above(self) -> Literal["none", "small", "medium", "large"] | None:
        """The vertical space above this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#flowpanel)"""
        ...
    @spacing_above.setter
    def spacing_above(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...
    @property
    def spacing_below(self) -> Literal["none", "small", "medium", "large"] | None:
        """The vertical space below this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#flowpanel)"""
        ...
    @spacing_below.setter
    def spacing_below(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...


    @property
    def gap(self) -> str:
        """Gap between components

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#flowpanel)"""
        ...
    @gap.setter
    def gap(self, value: str) -> None: ...

    @overload
    def add_component(self, component: Component, /, **layout_props: Unpack[_FlowPanelLayoutKwargs]) -> None: ...
    @overload
    def add_component(self, component: Component, /, **layout_props: Any) -> None:
        """Add a component to this panel. Optionally specify the position in the panel to add it, or the width to apply to components that can't self-size width-wise.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#flowpanel)"""
        ...

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

    [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#linearpanel)"""

    @property
    def visible(self) -> bool:
        """Should this component be displayed?

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#linearpanel)"""
        ...
    @visible.setter
    def visible(self, value: bool) -> None: ...
    @property
    def tooltip(self) -> str:
        """Text to display when you hover the mouse over this component

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#linearpanel)"""
        ...
    @tooltip.setter
    def tooltip(self, value: str) -> None: ...
    @property
    def role(self) -> str | list[str] | None:
        """Choose how this component can appear, based on your app's visual theme.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#linearpanel)"""
        ...
    @role.setter
    def role(self, value: str | list[str] | None) -> None: ...

    @property
    def background(self) -> str:
        """The background colour of this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#linearpanel)"""
        ...
    @background.setter
    def background(self, value: str) -> None: ...
    @property
    def foreground(self) -> str:
        """The foreground colour of this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#linearpanel)"""
        ...
    @foreground.setter
    def foreground(self, value: str) -> None: ...
    @property
    def border(self) -> str:
        """The border of this component. Can take any valid CSS border value.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#linearpanel)"""
        ...
    @border.setter
    def border(self, value: str) -> None: ...
    @property
    def spacing_above(self) -> Literal["none", "small", "medium", "large"] | None:
        """The vertical space above this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#linearpanel)"""
        ...
    @spacing_above.setter
    def spacing_above(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...
    @property
    def spacing_below(self) -> Literal["none", "small", "medium", "large"] | None:
        """The vertical space below this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#linearpanel)"""
        ...
    @spacing_below.setter
    def spacing_below(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...


    @property
    def spacing(self) -> SpacingPropertyValue:
        """Margin and padding for this container. Only available in apps that have been migrated to use Layouts.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#linearpanel)"""
        ...
    @spacing.setter
    def spacing(self, value: SpacingPropertyValue) -> None: ...

    @overload
    def add_component(self, component: Component, /, **layout_props: Unpack[_IndexLayoutKwargs]) -> None: ...
    @overload
    def add_component(self, component: Component, /, **layout_props: Any) -> None:
        """Add a component to this LinearPanel, in the 'index'th position. If 'index' is not specified, adds to the bottom.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#linearpanel)"""
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
        spacing_above: Literal["none", "small", "medium", "large"] | None = ...,
        spacing_below: Literal["none", "small", "medium", "large"] | None = ...,
        spacing: SpacingPropertyValue = ...,
    ) -> None: ...

class GridPanel(Container):
    """A container that arranges components in a grid.

    [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#gridpanel)"""

    @property
    def visible(self) -> bool:
        """Should this component be displayed?

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#gridpanel)"""
        ...
    @visible.setter
    def visible(self, value: bool) -> None: ...
    @property
    def tooltip(self) -> str:
        """Text to display when you hover the mouse over this component

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#gridpanel)"""
        ...
    @tooltip.setter
    def tooltip(self, value: str) -> None: ...
    @property
    def role(self) -> str | list[str] | None:
        """Choose how this component can appear, based on your app's visual theme.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#gridpanel)"""
        ...
    @role.setter
    def role(self, value: str | list[str] | None) -> None: ...

    @property
    def background(self) -> str:
        """The background colour of this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#gridpanel)"""
        ...
    @background.setter
    def background(self, value: str) -> None: ...
    @property
    def foreground(self) -> str:
        """The foreground colour of this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#gridpanel)"""
        ...
    @foreground.setter
    def foreground(self, value: str) -> None: ...
    @property
    def border(self) -> str:
        """The border of this component. Can take any valid CSS border value.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#gridpanel)"""
        ...
    @border.setter
    def border(self, value: str) -> None: ...


    @property
    def spacing(self) -> SpacingPropertyValue:
        """Margin and padding for this container. Only available in apps that have been migrated to use Layouts.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#gridpanel)"""
        ...
    @spacing.setter
    def spacing(self, value: SpacingPropertyValue) -> None: ...
    @property
    def spacing_above(self) -> Literal["none", "small", "medium", "large"] | None:
        """The vertical space above this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#gridpanel)"""
        ...
    @spacing_above.setter
    def spacing_above(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...
    @property
    def spacing_below(self) -> Literal["none", "small", "medium", "large"] | None:
        """The vertical space below this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#gridpanel)"""
        ...
    @spacing_below.setter
    def spacing_below(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...

    @overload
    def add_component(self, component: Component, /, **layout_props: Unpack[_GridPanelLayoutKwargs]) -> None: ...
    @overload
    def add_component(self, component: Component, /, **layout_props: Any) -> None:
        """Add a component to this GridPanel

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#gridpanel)"""
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
        spacing: SpacingPropertyValue = ...,
        spacing_above: Literal["none", "small", "medium", "large"] | None = ...,
        spacing_below: Literal["none", "small", "medium", "large"] | None = ...,
    ) -> None: ...

class XYPanel(Container):
    """A container that positions components at absolute coordinates.

    [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#xypanel)"""

    @property
    def visible(self) -> bool:
        """Should this component be displayed?

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#xypanel)"""
        ...
    @visible.setter
    def visible(self, value: bool) -> None: ...
    @property
    def tooltip(self) -> str:
        """Text to display when you hover the mouse over this component

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#xypanel)"""
        ...
    @tooltip.setter
    def tooltip(self, value: str) -> None: ...
    @property
    def role(self) -> str | list[str] | None:
        """Choose how this component can appear, based on your app's visual theme.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#xypanel)"""
        ...
    @role.setter
    def role(self, value: str | list[str] | None) -> None: ...

    @property
    def background(self) -> str:
        """The background colour of this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#xypanel)"""
        ...
    @background.setter
    def background(self, value: str) -> None: ...
    @property
    def foreground(self) -> str:
        """The foreground colour of this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#xypanel)"""
        ...
    @foreground.setter
    def foreground(self, value: str) -> None: ...
    @property
    def border(self) -> str:
        """The border of this component. Can take any valid CSS border value.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#xypanel)"""
        ...
    @border.setter
    def border(self, value: str) -> None: ...
    @property
    def height(self) -> str:
        """The height of this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#xypanel)"""
        ...
    @height.setter
    def height(self, value: str) -> None: ...
    @property
    def width(self) -> str:
        """[Anvil Docs](https://anvil.works/docs/components/standard-components/containers#xypanel)"""
        ...
    @width.setter
    def width(self, value: str) -> None: ...


    @property
    def align(self) -> str:
        """Align this component's content

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#xypanel)"""
        ...
    @align.setter
    def align(self, value: str) -> None: ...
    @property
    def margin(self) -> MarginPropertyValue:
        """Margin for this component. Only available in apps that have been migrated to use Layouts.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#xypanel)"""
        ...
    @margin.setter
    def margin(self, value: MarginPropertyValue) -> None: ...
    @property
    def spacing_above(self) -> Literal["none", "small", "medium", "large"] | None:
        """The vertical space above this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#xypanel)"""
        ...
    @spacing_above.setter
    def spacing_above(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...
    @property
    def spacing_below(self) -> Literal["none", "small", "medium", "large"] | None:
        """The vertical space below this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#xypanel)"""
        ...
    @spacing_below.setter
    def spacing_below(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...

    @overload
    def add_component(self, component: Component, /, **layout_props: Unpack[_XYPanelLayoutKwargs]) -> None: ...
    @overload
    def add_component(self, component: Component, /, **layout_props: Any) -> None:
        """Add a component to this XYPanel, at the specified coordinates. If the component's width is not specified, uses the component's default width.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/containers#xypanel)"""
        ...

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

    [Anvil Docs](https://anvil.works/docs/components/standard-components/data-grids)"""

    @property
    def visible(self) -> bool:
        """Should this component be displayed?

        [Anvil Docs](https://anvil.works/docs/components/standard-components/data-grids)"""
        ...
    @visible.setter
    def visible(self, value: bool) -> None: ...
    @property
    def tooltip(self) -> str:
        """Text to display when you hover the mouse over this component

        [Anvil Docs](https://anvil.works/docs/components/standard-components/data-grids)"""
        ...
    @tooltip.setter
    def tooltip(self, value: str) -> None: ...
    @property
    def role(self) -> str | list[str] | None:
        """Choose how this component can appear, based on your app's visual theme.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/data-grids)"""
        ...
    @role.setter
    def role(self, value: str | list[str] | None) -> None: ...

    @property
    def columns(self) -> list[dict[str, Any]]:
        """A list of columns to display in this Data Grid.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/data-grids)"""
        ...
    @columns.setter
    def columns(self, value: list[dict[str, Any]]) -> None: ...
    @property
    def rows_per_page(self) -> int | None:
        """The maximum number of rows to display at one time.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/data-grids)"""
        ...
    @rows_per_page.setter
    def rows_per_page(self, value: int | None) -> None: ...
    @property
    def show_page_controls(self) -> bool:
        """Whether to display the next/previous page buttons.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/data-grids)"""
        ...
    @show_page_controls.setter
    def show_page_controls(self, value: bool) -> None: ...
    @property
    def auto_header(self) -> bool:
        """Whether to display an automatic header at the top of this Data Grid.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/data-grids)"""
        ...
    @auto_header.setter
    def auto_header(self, value: bool) -> None: ...
    @property
    def wrap_on(self) -> str:
        """The largest display on which to wrap columns in this DataGrid

        [Anvil Docs](https://anvil.works/docs/components/standard-components/data-grids)"""
        ...
    @wrap_on.setter
    def wrap_on(self, value: str) -> None: ...
    @property
    def background(self) -> str:
        """The background colour of this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/data-grids)"""
        ...
    @background.setter
    def background(self, value: str) -> None: ...
    @property
    def foreground(self) -> str:
        """The foreground colour of this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/data-grids)"""
        ...
    @foreground.setter
    def foreground(self, value: str) -> None: ...
    @property
    def border(self) -> str:
        """The border of this component. Can take any valid CSS border value.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/data-grids)"""
        ...
    @border.setter
    def border(self, value: str) -> None: ...


    @property
    def margin(self) -> MarginPropertyValue:
        """Margin for this component. Only available in apps that have been migrated to use Layouts.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/data-grids)"""
        ...
    @margin.setter
    def margin(self, value: MarginPropertyValue) -> None: ...
    @property
    def spacing_above(self) -> Literal["none", "small", "medium", "large"] | None:
        """The vertical space above this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/data-grids)"""
        ...
    @spacing_above.setter
    def spacing_above(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...
    @property
    def spacing_below(self) -> Literal["none", "small", "medium", "large"] | None:
        """The vertical space below this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/data-grids)"""
        ...
    @spacing_below.setter
    def spacing_below(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...

    @override
    def add_event_handler(self, event_name: _DataGridEvents | str, handler_func: Callable[..., Any], /) -> None:
        """Add an event handler function to be called when the event happens on this component. Event handlers will be called in the order they are added. Adding the same event handler multiple times will mean it gets called multiple times.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/data-grids)"""
        ...
    @override
    def remove_event_handler(self, event_name: _DataGridEvents | str, handler_func: Callable[..., Any] | None = None, /) -> None:
        """Remove a specific event handler function for a given event. Calling remove_event_handler with just the event name will remove all the handlers for this event

        [Anvil Docs](https://anvil.works/docs/components/standard-components/data-grids)"""
        ...
    @override
    def set_event_handler(self, event_name: _DataGridEvents | str, handler_func: Callable[..., Any] | None, /) -> None:
        """Set a function to call when the 'event_name' event happens on this component. Using set_event_handler removes all other handlers. Setting the handler function to None removes all handlers.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/data-grids)"""
        ...
    @override
    def get_event_handlers(self, event_name: _DataGridEvents | str, /) -> tuple[Callable[..., Any], ...]: ...
    @override
    def raise_event(self, event_name: _DataGridEvents | str, /, **event_args: Any) -> None: ...

    @overload
    def add_component(self, component: Component, /, **layout_props: Unpack[_DataGridLayoutKwargs]) -> None: ...
    @overload
    def add_component(self, component: Component, /, **layout_props: Any) -> None:
        """Add a component to this DataGrid, in the 'index'th position. If 'index' is not specified, adds to the bottom.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/data-grids)"""
        ...

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

    [Anvil Docs](https://anvil.works/docs/components/standard-components/data-grids)"""

    @property
    def visible(self) -> bool:
        """Should this component be displayed?

        [Anvil Docs](https://anvil.works/docs/components/standard-components/data-grids)"""
        ...
    @visible.setter
    def visible(self, value: bool) -> None: ...
    @property
    def tooltip(self) -> str:
        """Text to display when you hover the mouse over this component

        [Anvil Docs](https://anvil.works/docs/components/standard-components/data-grids)"""
        ...
    @tooltip.setter
    def tooltip(self, value: str) -> None: ...
    @property
    def role(self) -> str | list[str] | None:
        """Choose how this component can appear, based on your app's visual theme.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/data-grids)"""
        ...
    @role.setter
    def role(self, value: str | list[str] | None) -> None: ...

    @property
    def item(self) -> dict[str, Any]:
        """The data to display in this row by default.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/data-grids)"""
        ...
    @item.setter
    def item(self, value: dict[str, Any]) -> None: ...
    @property
    def auto_display_data(self) -> bool:
        """Whether to automatically display data in this row.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/data-grids)"""
        ...
    @auto_display_data.setter
    def auto_display_data(self, value: bool) -> None: ...
    @property
    def background(self) -> str:
        """The background colour of this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/data-grids)"""
        ...
    @background.setter
    def background(self, value: str) -> None: ...
    @property
    def foreground(self) -> str:
        """The foreground colour of this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/data-grids)"""
        ...
    @foreground.setter
    def foreground(self, value: str) -> None: ...
    @property
    def border(self) -> str:
        """The border of this component. Can take any valid CSS border value.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/data-grids)"""
        ...
    @border.setter
    def border(self, value: str) -> None: ...


    @property
    def align(self) -> str:
        """Align this component's text

        [Anvil Docs](https://anvil.works/docs/components/standard-components/data-grids)"""
        ...
    @align.setter
    def align(self, value: str) -> None: ...
    @property
    def font_size(self) -> int | float | None:
        """The height of text displayed on this component in pixels

        [Anvil Docs](https://anvil.works/docs/components/standard-components/data-grids)"""
        ...
    @font_size.setter
    def font_size(self, value: int | float | None) -> None: ...
    @property
    def font(self) -> str:
        """The font to use for this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/data-grids)"""
        ...
    @font.setter
    def font(self, value: str) -> None: ...
    @property
    def bold(self) -> bool:
        """Display this component's text in bold

        [Anvil Docs](https://anvil.works/docs/components/standard-components/data-grids)"""
        ...
    @bold.setter
    def bold(self, value: bool) -> None: ...
    @property
    def italic(self) -> bool:
        """Display this component's text in italics

        [Anvil Docs](https://anvil.works/docs/components/standard-components/data-grids)"""
        ...
    @italic.setter
    def italic(self, value: bool) -> None: ...
    @property
    def underline(self) -> bool:
        """Display this component's text underlined

        [Anvil Docs](https://anvil.works/docs/components/standard-components/data-grids)"""
        ...
    @underline.setter
    def underline(self, value: bool) -> None: ...
    @property
    def margin(self) -> MarginPropertyValue:
        """Margin for this component. Only available in apps that have been migrated to use Layouts.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/data-grids)"""
        ...
    @margin.setter
    def margin(self, value: MarginPropertyValue) -> None: ...
    @property
    def spacing_above(self) -> Literal["none", "small", "medium", "large"] | None:
        """The vertical space above this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/data-grids)"""
        ...
    @spacing_above.setter
    def spacing_above(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...
    @property
    def spacing_below(self) -> Literal["none", "small", "medium", "large"] | None:
        """The vertical space below this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/data-grids)"""
        ...
    @spacing_below.setter
    def spacing_below(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...

    @overload
    def add_component(self, component: Component, /, **layout_props: Unpack[_DataRowPanelLayoutKwargs]) -> None: ...
    @overload
    def add_component(self, component: Component, /, **layout_props: Any) -> None:
        """Add a component to the specified column of this DataRowPanel. TODO: If 'column' is not specified, adds the component full-width.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/data-grids)"""
        ...

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

class RepeatingPanel(Container[_ContainerChild]):
    """A panel that repeats a template for each item in a list.

    [Anvil Docs](https://anvil.works/docs/components/standard-components/repeating-panel)"""

    @property
    def visible(self) -> bool:
        """Should this component be displayed?

        [Anvil Docs](https://anvil.works/docs/components/standard-components/repeating-panel)"""
        ...
    @visible.setter
    def visible(self, value: bool) -> None: ...
    @property
    def tooltip(self) -> str:
        """Text to display when you hover the mouse over this component

        [Anvil Docs](https://anvil.works/docs/components/standard-components/repeating-panel)"""
        ...
    @tooltip.setter
    def tooltip(self, value: str) -> None: ...
    @property
    def role(self) -> str | list[str] | None:
        """Choose how this component can appear, based on your app's visual theme.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/repeating-panel)"""
        ...
    @role.setter
    def role(self, value: str | list[str] | None) -> None: ...

    @property
    def items(self) -> list[Any] | Iterator[Any]:
        """A list of items for which the 'item_template' will be instantiated.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/repeating-panel)"""
        ...
    @items.setter
    def items(self, value: list[Any] | Iterator[Any]) -> None: ...
    item_template: Any
    """The name of the form to repeat for every item

    [Anvil Docs](https://anvil.works/docs/components/standard-components/repeating-panel)"""
    @property
    def background(self) -> str:
        """The background colour of this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/repeating-panel)"""
        ...
    @background.setter
    def background(self, value: str) -> None: ...
    @property
    def foreground(self) -> str:
        """The foreground colour of this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/repeating-panel)"""
        ...
    @foreground.setter
    def foreground(self, value: str) -> None: ...
    @property
    def border(self) -> str:
        """The border of this component. Can take any valid CSS border value.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/repeating-panel)"""
        ...
    @border.setter
    def border(self, value: str) -> None: ...


    @property
    def margin(self) -> MarginPropertyValue:
        """Margin for this component. Only available in apps that have been migrated to use Layouts.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/repeating-panel)"""
        ...
    @margin.setter
    def margin(self, value: MarginPropertyValue) -> None: ...
    @property
    def spacing_above(self) -> Literal["none", "small", "medium", "large"] | None:
        """The vertical space above this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/repeating-panel)"""
        ...
    @spacing_above.setter
    def spacing_above(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...
    @property
    def spacing_below(self) -> Literal["none", "small", "medium", "large"] | None:
        """The vertical space below this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/repeating-panel)"""
        ...
    @spacing_below.setter
    def spacing_below(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...

    @override
    def get_components(self) -> list[_ContainerChild]:
        """Get all repeated template instances.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/repeating-panel)"""
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

    dom_nodes: Mapping[str, Any]

    @property
    def visible(self) -> bool:
        """Should this component be displayed?

        [Anvil Docs](https://anvil.works/docs/client/customisation/custom-components/html-components)"""
        ...
    @visible.setter
    def visible(self, value: bool) -> None: ...

    @property
    def html(self) -> str:
        """The HTML from which this component is defined.

        [Anvil Docs](https://anvil.works/docs/client/customisation/custom-components/html-components)"""
        ...
    @html.setter
    def html(self, value: str) -> None: ...

    @property
    def classes(self) -> Classes:
        """The class names applied to this HtmlComponent's root element.

        [Anvil Docs](https://anvil.works/docs/client/customisation/custom-components/html-components)"""
        ...
    @classes.setter
    def classes(self, value: _ClassesValue | Classes) -> None: ...

    @property
    def style(self) -> Style:
        """The inline styles applied to this HtmlComponent's root element.

        [Anvil Docs](https://anvil.works/docs/client/customisation/custom-components/html-components)"""
        ...
    @style.setter
    def style(self, value: _StyleValue | Style) -> None: ...

    @property
    def attrs(self) -> Attrs:
        """The HTML attributes applied to this HtmlComponent's root element.

        [Anvil Docs](https://anvil.works/docs/client/customisation/custom-components/html-components)"""
        ...
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

    [Anvil Docs](https://anvil.works/docs/api/anvil#HtmlTemplate)"""

    dom_nodes: Mapping[str, Any]
    """A read-only dictionary allowing you to look up the DOM node by name for any HTML tag in this component's HTML that has an anvil-name= attribute.

    [Anvil Docs](https://anvil.works/docs/api/anvil#HtmlTemplate)"""

    @property
    def visible(self) -> bool:
        """Should this component be displayed?

        [Anvil Docs](https://anvil.works/docs/api/anvil#HtmlTemplate)"""
        ...
    @visible.setter
    def visible(self, value: bool) -> None: ...
    @property
    def tooltip(self) -> str:
        """Text to display when you hover the mouse over this component

        [Anvil Docs](https://anvil.works/docs/api/anvil#HtmlTemplate)"""
        ...
    @tooltip.setter
    def tooltip(self, value: str) -> None: ...
    @property
    def role(self) -> str | list[str] | None:
        """Choose how this component can appear, based on your app's visual theme.

        [Anvil Docs](https://anvil.works/docs/api/anvil#HtmlTemplate)"""
        ...
    @role.setter
    def role(self, value: str | list[str] | None) -> None: ...

    @property
    def html(self) -> str:
        """The HTML from which this panel is defined

        [Anvil Docs](https://anvil.works/docs/api/anvil#HtmlTemplate)"""
        ...
    @html.setter
    def html(self, value: str) -> None: ...


    @property
    def background(self) -> str:
        """The background colour of this component.

        [Anvil Docs](https://anvil.works/docs/api/anvil#HtmlTemplate)"""
        ...
    @background.setter
    def background(self, value: str) -> None: ...
    @property
    def border(self) -> str:
        """The border of this component. Can take any valid CSS border value.

        [Anvil Docs](https://anvil.works/docs/api/anvil#HtmlTemplate)"""
        ...
    @border.setter
    def border(self, value: str) -> None: ...
    @property
    def foreground(self) -> str:
        """The foreground colour of this component.

        [Anvil Docs](https://anvil.works/docs/api/anvil#HtmlTemplate)"""
        ...
    @foreground.setter
    def foreground(self, value: str) -> None: ...

    @overload
    def add_component(self, component: Component, /, **layout_props: Unpack[_SlottedLayoutKwargs]) -> None: ...
    @overload
    def add_component(self, component: Component, /, **layout_props: Any) -> None:
        """Add a component to the named slot of this HTML templated panel. If no slot is specified, the 'default' slot will be used.

        [Anvil Docs](https://anvil.works/docs/api/anvil#HtmlTemplate)"""
        ...

    def call_js(self, fn_name: str, *args: Any) -> Any:
        """Call a JavaScript function defined in the HTML.

        [Anvil Docs](https://anvil.works/docs/client/customisation/javascript)"""
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

    [Anvil Docs](https://anvil.works/docs/components/standard-components/canvas)"""

    @property
    def visible(self) -> bool:
        """Should this component be displayed?

        [Anvil Docs](https://anvil.works/docs/components/standard-components/canvas)"""
        ...
    @visible.setter
    def visible(self, value: bool) -> None: ...
    @property
    def tooltip(self) -> str:
        """Text to display when you hover the mouse over this component

        [Anvil Docs](https://anvil.works/docs/components/standard-components/canvas)"""
        ...
    @tooltip.setter
    def tooltip(self, value: str) -> None: ...
    @property
    def role(self) -> str | list[str] | None:
        """Choose how this component can appear, based on your app's visual theme.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/canvas)"""
        ...
    @role.setter
    def role(self, value: str | list[str] | None) -> None: ...

    @property
    def width(self) -> int:
        """[Anvil Docs](https://anvil.works/docs/components/standard-components/canvas)"""
        ...
    @width.setter
    def width(self, value: int) -> None: ...
    @property
    def height(self) -> int:
        """The height of this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/canvas)"""
        ...
    @height.setter
    def height(self, value: int) -> None: ...
    @property
    def background(self) -> str:
        """The background colour of this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/canvas)"""
        ...
    @background.setter
    def background(self, value: str) -> None: ...


    @property
    def border(self) -> str:
        """The border of this component. Can take any valid CSS border value.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/canvas)"""
        ...
    @border.setter
    def border(self, value: str) -> None: ...
    @property
    def foreground(self) -> str:
        """The foreground colour of this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/canvas)"""
        ...
    @foreground.setter
    def foreground(self, value: str) -> None: ...
    @property
    def margin(self) -> MarginPropertyValue:
        """Margin for this component. Only available in apps that have been migrated to use Layouts.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/canvas)"""
        ...
    @margin.setter
    def margin(self, value: MarginPropertyValue) -> None: ...
    @property
    def spacing_above(self) -> Literal["none", "small", "medium", "large"] | None:
        """The vertical space above this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/canvas)"""
        ...
    @spacing_above.setter
    def spacing_above(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...
    @property
    def spacing_below(self) -> Literal["none", "small", "medium", "large"] | None:
        """The vertical space below this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/canvas)"""
        ...
    @spacing_below.setter
    def spacing_below(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...

    @override
    def add_event_handler(self, event_name: _CanvasEvents | str, handler_func: Callable[..., Any], /) -> None:
        """Add an event handler function to be called when the event happens on this component. Event handlers will be called in the order they are added. Adding the same event handler multiple times will mean it gets called multiple times.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/canvas)"""
        ...
    @override
    def remove_event_handler(self, event_name: _CanvasEvents | str, handler_func: Callable[..., Any] | None = None, /) -> None:
        """Remove a specific event handler function for a given event. Calling remove_event_handler with just the event name will remove all the handlers for this event

        [Anvil Docs](https://anvil.works/docs/components/standard-components/canvas)"""
        ...
    @override
    def set_event_handler(self, event_name: _CanvasEvents | str, handler_func: Callable[..., Any] | None, /) -> None:
        """Set a function to call when the 'event_name' event happens on this component. Using set_event_handler removes all other handlers. Setting the handler function to None removes all handlers.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/canvas)"""
        ...
    @override
    def get_event_handlers(self, event_name: _CanvasEvents | str, /) -> tuple[Callable[..., Any], ...]: ...
    @override
    def raise_event(self, event_name: _CanvasEvents | str, /, **event_args: Any) -> None: ...

    # Drawing state lives on the canvas context, rather than component properties.
    fill_style: str | _CanvasGradient
    """The color or gradient to use when filling shapes and paths.

    [Anvil Docs](https://anvil.works/docs/components/standard-components/canvas)"""
    stroke_style: str | _CanvasGradient
    """The color or gradient to use when drawing outlines.

    [Anvil Docs](https://anvil.works/docs/components/standard-components/canvas)"""
    font: str
    """The font to use when drawing text on this canvas.

    [Anvil Docs](https://anvil.works/docs/components/standard-components/canvas)"""
    global_alpha: float
    """The global opacity to draw with, in the range 0-1.

    [Anvil Docs](https://anvil.works/docs/components/standard-components/canvas)"""
    global_composite_operation: str
    """The global composite operation to draw with. Defaults to 'source-over'

    [Anvil Docs](https://anvil.works/docs/components/standard-components/canvas)"""
    line_cap: Literal["butt", "round", "square"]
    """The line cap to use when drawing lines on this canvas.

    [Anvil Docs](https://anvil.works/docs/components/standard-components/canvas)"""
    line_join: Literal["bevel", "round", "miter"]
    """The line join to use when connecting lines on this canvas.

    [Anvil Docs](https://anvil.works/docs/components/standard-components/canvas)"""
    line_width: float
    """The width of lines drawn on this canvas.

    [Anvil Docs](https://anvil.works/docs/components/standard-components/canvas)"""
    miter_limit: float
    """The limit of line join miters, in pixels.

    [Anvil Docs](https://anvil.works/docs/components/standard-components/canvas)"""
    shadow_blur: float
    """The required shadow blur, in pixels.

    [Anvil Docs](https://anvil.works/docs/components/standard-components/canvas)"""
    shadow_color: str
    """The color to use for shadows.

    [Anvil Docs](https://anvil.works/docs/components/standard-components/canvas)"""
    shadow_offset_x: float
    """The horizontal shadow offset, in pixels.

    [Anvil Docs](https://anvil.works/docs/components/standard-components/canvas)"""
    shadow_offset_y: float
    """The vertical shadow offset, in pixels.

    [Anvil Docs](https://anvil.works/docs/components/standard-components/canvas)"""
    text_align: Literal["start", "end", "left", "right", "center"]
    """Text alignment, relative to the drawing point.

    [Anvil Docs](https://anvil.works/docs/components/standard-components/canvas)"""
    text_baseline: Literal["top", "hanging", "middle", "alphabetic", "ideographic", "bottom"]
    """Text baseline, relative to the drawing point.

    [Anvil Docs](https://anvil.works/docs/components/standard-components/canvas)"""

    Gradient: type[_CanvasGradient]

    def get_width(self) -> int | float:
        """Get the canvas width in pixels."""
        ...

    def get_height(self) -> int | float:
        """Get the canvas height in pixels."""
        ...

    def get_image(self) -> Media:
        """Get the canvas content as a media object.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/canvas)"""
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

        [Anvil Docs](https://anvil.works/docs/components/standard-components/canvas)"""
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

    [Anvil Docs](https://anvil.works/docs/components/standard-components/plots)"""

    @property
    def visible(self) -> bool:
        """Should this component be displayed?

        [Anvil Docs](https://anvil.works/docs/components/standard-components/plots)"""
        ...
    @visible.setter
    def visible(self, value: bool) -> None: ...
    @property
    def tooltip(self) -> str:
        """Text to display when you hover the mouse over this component

        [Anvil Docs](https://anvil.works/docs/components/standard-components/plots)"""
        ...
    @tooltip.setter
    def tooltip(self, value: str) -> None: ...

    @property
    def data(self) -> list[dict[str, Any]]:
        """Plot traces

        [Anvil Docs](https://anvil.works/docs/components/standard-components/plots)"""
        ...
    @data.setter
    def data(self, value: list[dict[str, Any]]) -> None: ...
    @property
    def layout(self) -> dict[str, Any]:
        """Plot layout

        [Anvil Docs](https://anvil.works/docs/components/standard-components/plots)"""
        ...
    @layout.setter
    def layout(self, value: dict[str, Any]) -> None: ...
    @property
    def config(self) -> dict[str, Any]:
        """Plot config

        [Anvil Docs](https://anvil.works/docs/components/standard-components/plots)"""
        ...
    @config.setter
    def config(self, value: dict[str, Any]) -> None: ...
    @property
    def figure(self) -> dict[str, Any]:
        """The Plotly figure to display. Specifies layout and data.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/plots)"""
        ...
    @figure.setter
    def figure(self, value: dict[str, Any]) -> None: ...
    @property
    def interactive(self) -> bool:
        """Whether this plot should be interactive

        [Anvil Docs](https://anvil.works/docs/components/standard-components/plots)"""
        ...
    @interactive.setter
    def interactive(self, value: bool) -> None: ...


    @property
    def height(self) -> str:
        """The height of this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/plots)"""
        ...
    @height.setter
    def height(self, value: str) -> None: ...
    @property
    def margin(self) -> MarginPropertyValue:
        """Margin for this component. Only available in apps that have been migrated to use Layouts.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/plots)"""
        ...
    @margin.setter
    def margin(self, value: MarginPropertyValue) -> None: ...
    @property
    def spacing_above(self) -> Literal["none", "small", "medium", "large"] | None:
        """The vertical space above this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/plots)"""
        ...
    @spacing_above.setter
    def spacing_above(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...
    @property
    def spacing_below(self) -> Literal["none", "small", "medium", "large"] | None:
        """The vertical space below this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/plots)"""
        ...
    @spacing_below.setter
    def spacing_below(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...

    @override
    def add_event_handler(self, event_name: _PlotEvents | str, handler_func: Callable[..., Any], /) -> None:
        """Add an event handler function to be called when the event happens on this component. Event handlers will be called in the order they are added. Adding the same event handler multiple times will mean it gets called multiple times.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/plots)"""
        ...
    @override
    def remove_event_handler(self, event_name: _PlotEvents | str, handler_func: Callable[..., Any] | None = None, /) -> None:
        """Remove a specific event handler function for a given event. Calling remove_event_handler with just the event name will remove all the handlers for this event

        [Anvil Docs](https://anvil.works/docs/components/standard-components/plots)"""
        ...
    @override
    def set_event_handler(self, event_name: _PlotEvents | str, handler_func: Callable[..., Any] | None, /) -> None:
        """Set a function to call when the 'event_name' event happens on this component. Using set_event_handler removes all other handlers. Setting the handler function to None removes all handlers.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/plots)"""
        ...
    @override
    def get_event_handlers(self, event_name: _PlotEvents | str, /) -> tuple[Callable[..., Any], ...]: ...
    @override
    def raise_event(self, event_name: _PlotEvents | str, /, **event_args: Any) -> None: ...

    templates: dict[str, Any]
    """plotly templates, see plotly docs for valid template names. Set the default template using Plot.templates.default = 'seaborn'.

    [Anvil Docs](https://anvil.works/docs/components/standard-components/plots)"""

    def redraw(self) -> None:
        """Redraw the plot.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/plots)"""
        ...

    def to_image(self, options: Mapping[str, Any] | None = None, /) -> Media:
        """Export the plot as an image.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/plots)"""
        ...

    def relayout(self, update: Mapping[str, Any], /) -> None:
        """Update the plot layout.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/plots)"""
        ...

    def extend_traces(self, data: Mapping[str, Any], traces: list[int], /) -> None:
        """Extend trace data.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/plots)"""
        ...

    def prepend_traces(self, data: Mapping[str, Any], traces: list[int], /) -> None:
        """Prepend trace data.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/plots)"""
        ...

    def restyle(self, update: Mapping[str, Any], traces: list[int], /) -> None:
        """Update attributes on one or more traces.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/plots)"""
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

    [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""

    lat: float
    """Returns the latitude in degrees.

    [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
    lng: float
    """Returns the longitude in degrees.

    [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""

    def __init__(self, lat: float, lng: float) -> None: ...


_MapOverlayEvents = Literal["show", "hide", "click", "dblclick", "drag", "dragend", "dragstart", "mousedown", "mouseout", "mouseover", "mouseup", "rightclick"]
_MapMarkerEvents = _MapOverlayEvents | Literal["animation_changed", "clickable_changed", "cursor_changed", "draggable_changed", "icon_changed", "position_changed", "shape_changed", "title_changed", "visible_changed", "z_index_changed"]
_MapCircleEvents = _MapOverlayEvents | Literal["center_changed", "radius_changed"]
_MapRectangleEvents = _MapOverlayEvents | Literal["bounds_changed"]


class _MapSize:
    def __init__(self, x: float, y: float) -> None: ...


class _LatLngBounds:
    def __init__(self, south_west: _LatLng, north_east: _LatLng) -> None: ...
    def contains(self, point: _LatLng) -> bool:
        """Returns True if the given lat/lng is in this bounds."""
        ...
    def equals(self, other: _LatLngBounds) -> bool:
        """Returns True if this bounds approximately equals the given bounds."""
        ...
    def extend(self, point: _LatLng) -> _LatLngBounds:
        """Extends this bounds to contain the given point."""
        ...
    def get_center(self) -> _LatLng:
        """Computes the center of this LatLngBounds"""
        ...
    def get_north_east(self) -> _LatLng:
        """Returns the north-east corner of this bounds."""
        ...
    def get_south_west(self) -> _LatLng:
        """Returns the south-west corner of this bounds."""
        ...
    def intersects(self, other: _LatLngBounds) -> bool:
        """Returns True if this bounds shares any points with the other bounds."""
        ...
    def is_empty(self) -> bool:
        """Returns True if the bounds are empty."""
        ...
    def to_json(self) -> dict[str, float]:
        """Converts to JSON representation."""
        ...
    def to_span(self) -> _LatLng:
        """Converts the given map bounds to a lat/lng span."""
        ...
    def to_url_value(self, precision: int = 6) -> str:
        """Returns a string of the form 'lat_lo,lng_lo,lat_hi,lng_hi' for this bounds."""
        ...
    def union(self, other: _LatLngBounds) -> _LatLngBounds:
        """Extends this bounds to contain the union of this and the given bounds."""
        ...


class _MapOverlay(Component):
    """Base class for map overlays.

    [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""

    @property
    def clickable(self) -> bool:
        """True if this overlay raises mouse events.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
        ...
    @clickable.setter
    def clickable(self, value: bool) -> None: ...

    @property
    def draggable(self) -> bool:
        """True if this overlay can be dragged.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
        ...
    @draggable.setter
    def draggable(self, value: bool) -> None: ...

    @property
    def visible(self) -> bool:
        """True if this overlay should be displayed.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
        ...
    @visible.setter
    def visible(self, value: bool) -> None: ...

    @property
    def z_index(self) -> float:
        """The z-index compared to other overlays.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
        ...
    @z_index.setter
    def z_index(self, value: float) -> None: ...

    @override
    def add_event_handler(self, event_name: _MapOverlayEvents | str, handler_func: Callable[..., Any], /) -> None:
        """Add an event handler function to be called when the event happens on this component. Event handlers will be called in the order they are added. Adding the same event handler multiple times will mean it gets called multiple times.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
        ...
    @override
    def remove_event_handler(self, event_name: _MapOverlayEvents | str, handler_func: Callable[..., Any] | None = None, /) -> None:
        """Remove a specific event handler function for a given event. Calling remove_event_handler with just the event name will remove all the handlers for this event

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
        ...
    @override
    def set_event_handler(self, event_name: _MapOverlayEvents | str, handler_func: Callable[..., Any] | None, /) -> None:
        """Set a function to call when the 'event_name' event happens on this component. Using set_event_handler removes all other handlers. Setting the handler function to None removes all handlers.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
        ...
    @override
    def get_event_handlers(self, event_name: _MapOverlayEvents | str, /) -> tuple[Callable[..., Any], ...]: ...
    @override
    def raise_event(self, event_name: _MapOverlayEvents | str, /, **event_args: Any) -> None: ...


    def __init__(
        self,
        *,
        tag: Any = ...,
        clickable: bool = ...,
        draggable: bool = ...,
        visible: bool = ...,
        z_index: float = ...,
    ) -> None: ...

class _MapArea(_MapOverlay):
    """Shared rectangle, circle and polygon styling.

    [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""

    @property
    def editable(self) -> bool:
        """True if this overlay can be edited by the user.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
        ...
    @editable.setter
    def editable(self, value: bool) -> None: ...

    @property
    def stroke_color(self) -> str:
        """The color to draw the overlay outline.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
        ...
    @stroke_color.setter
    def stroke_color(self, value: str) -> None: ...

    @property
    def stroke_opacity(self) -> float:
        """The opacity of the overlay outline.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
        ...
    @stroke_opacity.setter
    def stroke_opacity(self, value: float) -> None: ...

    @property
    def stroke_weight(self) -> float:
        """The weight of the overlay outline

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
        ...
    @stroke_weight.setter
    def stroke_weight(self, value: float) -> None: ...

    @property
    def stroke_position(self) -> Any:
        """The stroke position. Defaults to CENTER.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
        ...
    @stroke_position.setter
    def stroke_position(self, value: Any) -> None: ...

    @property
    def fill_color(self) -> str:
        """The color to draw the overlay outline.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
        ...
    @fill_color.setter
    def fill_color(self, value: str) -> None: ...

    @property
    def fill_opacity(self) -> float:
        """The opacity of the overlay outline.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
        ...
    @fill_opacity.setter
    def fill_opacity(self, value: float) -> None: ...


    def __init__(
        self,
        *,
        tag: Any = ...,
        clickable: bool = ...,
        draggable: bool = ...,
        visible: bool = ...,
        z_index: float = ...,
        editable: bool = ...,
        stroke_color: str = ...,
        stroke_opacity: float = ...,
        stroke_weight: float = ...,
        stroke_position: Any = ...,
        fill_color: str = ...,
        fill_opacity: float = ...,
    ) -> None: ...

class _MapCircle(_MapArea):
    """A circular overlay on a GoogleMap.

    [Anvil Docs](https://anvil.works/docs/components/standard-components/maps#googlemapcircle)"""

    @property
    def center(self) -> _LatLng:
        """The center of the Circle.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps#googlemapcircle)"""
        ...
    @center.setter
    def center(self, value: _LatLng) -> None: ...

    @property
    def radius(self) -> float:
        """The radius of the Circle.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps#googlemapcircle)"""
        ...
    @radius.setter
    def radius(self, value: float) -> None: ...

    @override
    def add_event_handler(self, event_name: _MapCircleEvents | str, handler_func: Callable[..., Any], /) -> None:
        """Add an event handler function to be called when the event happens on this component. Event handlers will be called in the order they are added. Adding the same event handler multiple times will mean it gets called multiple times.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps#googlemapcircle)"""
        ...
    @override
    def remove_event_handler(self, event_name: _MapCircleEvents | str, handler_func: Callable[..., Any] | None = None, /) -> None:
        """Remove a specific event handler function for a given event. Calling remove_event_handler with just the event name will remove all the handlers for this event

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps#googlemapcircle)"""
        ...
    @override
    def set_event_handler(self, event_name: _MapCircleEvents | str, handler_func: Callable[..., Any] | None, /) -> None:
        """Set a function to call when the 'event_name' event happens on this component. Using set_event_handler removes all other handlers. Setting the handler function to None removes all handlers.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps#googlemapcircle)"""
        ...
    @override
    def get_event_handlers(self, event_name: _MapCircleEvents | str, /) -> tuple[Callable[..., Any], ...]: ...
    @override
    def raise_event(self, event_name: _MapCircleEvents | str, /, **event_args: Any) -> None: ...


    def __init__(
        self,
        *,
        tag: Any = ...,
        clickable: bool = ...,
        draggable: bool = ...,
        visible: bool = ...,
        z_index: float = ...,
        editable: bool = ...,
        stroke_color: str = ...,
        stroke_opacity: float = ...,
        stroke_weight: float = ...,
        stroke_position: Any = ...,
        fill_color: str = ...,
        fill_opacity: float = ...,
        center: _LatLng = ...,
        radius: float = ...,
    ) -> None: ...

class _MapRectangle(_MapArea):
    """A rectangular overlay on a GoogleMap.

    [Anvil Docs](https://anvil.works/docs/components/standard-components/maps#googlemaprectangle)"""

    @property
    def bounds(self) -> _LatLngBounds:
        """The bounds of the Rectangle.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps#googlemaprectangle)"""
        ...
    @bounds.setter
    def bounds(self, value: _LatLngBounds) -> None: ...

    @override
    def add_event_handler(self, event_name: _MapRectangleEvents | str, handler_func: Callable[..., Any], /) -> None:
        """Add an event handler function to be called when the event happens on this component. Event handlers will be called in the order they are added. Adding the same event handler multiple times will mean it gets called multiple times.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps#googlemaprectangle)"""
        ...
    @override
    def remove_event_handler(self, event_name: _MapRectangleEvents | str, handler_func: Callable[..., Any] | None = None, /) -> None:
        """Remove a specific event handler function for a given event. Calling remove_event_handler with just the event name will remove all the handlers for this event

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps#googlemaprectangle)"""
        ...
    @override
    def set_event_handler(self, event_name: _MapRectangleEvents | str, handler_func: Callable[..., Any] | None, /) -> None:
        """Set a function to call when the 'event_name' event happens on this component. Using set_event_handler removes all other handlers. Setting the handler function to None removes all handlers.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps#googlemaprectangle)"""
        ...
    @override
    def get_event_handlers(self, event_name: _MapRectangleEvents | str, /) -> tuple[Callable[..., Any], ...]: ...
    @override
    def raise_event(self, event_name: _MapRectangleEvents | str, /, **event_args: Any) -> None: ...


    def __init__(
        self,
        *,
        tag: Any = ...,
        clickable: bool = ...,
        draggable: bool = ...,
        visible: bool = ...,
        z_index: float = ...,
        editable: bool = ...,
        stroke_color: str = ...,
        stroke_opacity: float = ...,
        stroke_weight: float = ...,
        stroke_position: Any = ...,
        fill_color: str = ...,
        fill_opacity: float = ...,
        bounds: _LatLngBounds = ...,
    ) -> None: ...

class _MapInfoWindow(Component):
    """A popup on a GoogleMap.

    [Anvil Docs](https://anvil.works/docs/components/standard-components/maps#googlemapinfowindow)"""

    @property
    def content(self) -> str | Component | None:
        """Content to display in the InfoWindow. Can be a string or an Anvil Component

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps#googlemapinfowindow)"""
        ...
    @content.setter
    def content(self, value: str | Component | None) -> None: ...

    @property
    def disable_auto_pan(self) -> bool:
        """Disable auto-pan on open.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps#googlemapinfowindow)"""
        ...
    @disable_auto_pan.setter
    def disable_auto_pan(self, value: bool) -> None: ...

    @property
    def max_width(self) -> float:
        """Maximum width of the infowindow, regardless of content's width.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps#googlemapinfowindow)"""
        ...
    @max_width.setter
    def max_width(self, value: float) -> None: ...

    @property
    def pixel_offset(self) -> _MapSize:
        """The offset, in pixels, of the tip of the info window from the point on the map at whose geographical coordinates the info window is anchored.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps#googlemapinfowindow)"""
        ...
    @pixel_offset.setter
    def pixel_offset(self, value: _MapSize) -> None: ...

    @property
    def position(self) -> _LatLng:
        """The LatLng at which to display this InfoWindow. Not required if this popup is anchored to a component

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps#googlemapinfowindow)"""
        ...
    @position.setter
    def position(self, value: _LatLng) -> None: ...

    @property
    def z_index(self) -> float:
        """All InfoWindows are displayed on the map in order of their zIndex, with higher values displaying in front of InfoWindows with lower values.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps#googlemapinfowindow)"""
        ...
    @z_index.setter
    def z_index(self, value: float) -> None: ...

    def open(self, map: GoogleMap, anchor: _MapOverlay | None = None) -> None:
        """Display this InfoWindow on the specified map. If anchor is specified, the InfoWindow does not need to have its own position property set.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps#googlemapinfowindow)"""
        ...
    def close(self) -> None:
        """Hide this InfoWindow. The user can also cause this to happen by clicking the close button in the top-right of the popup.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps#googlemapinfowindow)"""
        ...


    def __init__(
        self,
        *,
        tag: Any = ...,
        content: str | Component | None = ...,
        disable_auto_pan: bool = ...,
        max_width: float = ...,
        pixel_offset: _MapSize = ...,
        position: _LatLng = ...,
        z_index: float = ...,
    ) -> None: ...

class _MapMarker(_MapOverlay):
    """A marker on a GoogleMap.

    [Anvil Docs](https://anvil.works/docs/components/standard-components/maps#googlemapmarker)"""

    @property
    def enabled(self) -> bool:
        """[Anvil Docs](https://anvil.works/docs/components/standard-components/maps#googlemapmarker)"""
        ...
    @enabled.setter
    def enabled(self, value: bool) -> None: ...
    @property
    def tooltip(self) -> str:
        """[Anvil Docs](https://anvil.works/docs/components/standard-components/maps#googlemapmarker)"""
        ...
    @tooltip.setter
    def tooltip(self, value: str) -> None: ...
    @property
    def role(self) -> str | list[str] | None:
        """[Anvil Docs](https://anvil.works/docs/components/standard-components/maps#googlemapmarker)"""
        ...
    @role.setter
    def role(self, value: str | list[str] | None) -> None: ...

    @property
    def title(self) -> str:
        """The tooltip text for this Marker.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps#googlemapmarker)"""
        ...
    @title.setter
    def title(self, value: str) -> None: ...

    @property
    def cursor(self) -> str:
        """The cursor to display over this Marker.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps#googlemapmarker)"""
        ...
    @cursor.setter
    def cursor(self, value: str) -> None: ...

    @property
    def opacity(self) -> float:
        """The opacity of this Marker.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps#googlemapmarker)"""
        ...
    @opacity.setter
    def opacity(self, value: float) -> None: ...

    @override
    def add_event_handler(self, event_name: _MapMarkerEvents | str, handler_func: Callable[..., Any], /) -> None:
        """Add an event handler function to be called when the event happens on this component. Event handlers will be called in the order they are added. Adding the same event handler multiple times will mean it gets called multiple times.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps#googlemapmarker)"""
        ...
    @override
    def remove_event_handler(self, event_name: _MapMarkerEvents | str, handler_func: Callable[..., Any] | None = None, /) -> None:
        """Remove a specific event handler function for a given event. Calling remove_event_handler with just the event name will remove all the handlers for this event

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps#googlemapmarker)"""
        ...
    @override
    def set_event_handler(self, event_name: _MapMarkerEvents | str, handler_func: Callable[..., Any] | None, /) -> None:
        """Set a function to call when the 'event_name' event happens on this component. Using set_event_handler removes all other handlers. Setting the handler function to None removes all handlers.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps#googlemapmarker)"""
        ...
    @override
    def get_event_handlers(self, event_name: _MapMarkerEvents | str, /) -> tuple[Callable[..., Any], ...]: ...
    @override
    def raise_event(self, event_name: _MapMarkerEvents | str, /, **event_args: Any) -> None: ...

    @property
    def animation(self) -> Any:
        """The animation of this Marker.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps#googlemapmarker)"""
        ...
    @animation.setter
    def animation(self, value: Any) -> None: ...
    """The animation of this Marker."""

    @property
    def position(self) -> _LatLng:
        """The LatLng position of this Marker

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps#googlemapmarker)"""
        ...
    @position.setter
    def position(self, value: _LatLng) -> None: ...
    """The LatLng position of this Marker."""

    @property
    def icon(self) -> Any:
        """The icon to display at the position of this Marker.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps#googlemapmarker)"""
        ...
    @icon.setter
    def icon(self, value: Any) -> None: ...
    """The icon to display at the position of this Marker."""

    @property
    def label(self) -> Any:
        """The label to display on this Marker.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps#googlemapmarker)"""
        ...
    @label.setter
    def label(self, value: Any) -> None: ...
    """The label to display on this Marker."""

    def remove(self) -> None:
        """Remove this marker from the map."""
        ...


    def __init__(
        self,
        *,
        tag: Any = ...,
        clickable: bool = ...,
        draggable: bool = ...,
        visible: bool = ...,
        z_index: float = ...,
        enabled: bool = ...,
        tooltip: str = ...,
        role: str | list[str] | None = ...,
        title: str = ...,
        cursor: str = ...,
        opacity: float = ...,
        animation: Any = ...,
        position: _LatLng = ...,
        icon: Any = ...,
        label: Any = ...,
    ) -> None: ...

class _MapPolygon(_MapArea):
    """A polygon overlay on a GoogleMap.

    [Anvil Docs](https://anvil.works/docs/components/standard-components/maps#googlemappolygon)"""

    @property
    def enabled(self) -> bool:
        """[Anvil Docs](https://anvil.works/docs/components/standard-components/maps#googlemappolygon)"""
        ...
    @enabled.setter
    def enabled(self, value: bool) -> None: ...
    @property
    def tooltip(self) -> str:
        """[Anvil Docs](https://anvil.works/docs/components/standard-components/maps#googlemappolygon)"""
        ...
    @tooltip.setter
    def tooltip(self, value: str) -> None: ...
    @property
    def role(self) -> str | list[str] | None:
        """[Anvil Docs](https://anvil.works/docs/components/standard-components/maps#googlemappolygon)"""
        ...
    @role.setter
    def role(self, value: str | list[str] | None) -> None: ...

    @property
    def path(self) -> list[_LatLng]:
        """The ordered sequence of LatLng coordinates of the Polygon.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps#googlemappolygon)"""
        ...
    @path.setter
    def path(self, value: list[_LatLng]) -> None: ...
    """The ordered sequence of LatLng coordinates of the Polygon."""

    @property
    def geodesic(self) -> bool:
        """When true, edges of the polygon are interpreted as geodesic and will follow the curvature of the Earth.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps#googlemappolygon)"""
        ...
    @geodesic.setter
    def geodesic(self, value: bool) -> None: ...
    """When true, edges of the polygon are interpreted as geodesic."""

    def remove(self) -> None:
        """Remove this polygon from the map."""
        ...


    def __init__(
        self,
        *,
        tag: Any = ...,
        clickable: bool = ...,
        draggable: bool = ...,
        visible: bool = ...,
        z_index: float = ...,
        editable: bool = ...,
        stroke_color: str = ...,
        stroke_opacity: float = ...,
        stroke_weight: float = ...,
        stroke_position: Any = ...,
        fill_color: str = ...,
        fill_opacity: float = ...,
        enabled: bool = ...,
        tooltip: str = ...,
        role: str | list[str] | None = ...,
        path: list[_LatLng] = ...,
        geodesic: bool = ...,
    ) -> None: ...

class _MapPolyline(_MapOverlay):
    """A polyline overlay on a GoogleMap.

    [Anvil Docs](https://anvil.works/docs/components/standard-components/maps#googlemappolyline)"""

    @property
    def enabled(self) -> bool:
        """[Anvil Docs](https://anvil.works/docs/components/standard-components/maps#googlemappolyline)"""
        ...
    @enabled.setter
    def enabled(self, value: bool) -> None: ...
    @property
    def tooltip(self) -> str:
        """[Anvil Docs](https://anvil.works/docs/components/standard-components/maps#googlemappolyline)"""
        ...
    @tooltip.setter
    def tooltip(self, value: str) -> None: ...
    @property
    def role(self) -> str | list[str] | None:
        """[Anvil Docs](https://anvil.works/docs/components/standard-components/maps#googlemappolyline)"""
        ...
    @role.setter
    def role(self, value: str | list[str] | None) -> None: ...

    @property
    def icons(self) -> list[Any]:
        """The icons to be rendered along the polyline.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps#googlemappolyline)"""
        ...
    @icons.setter
    def icons(self, value: list[Any]) -> None: ...
    """The icons to be rendered along the polyline."""

    @property
    def path(self) -> list[_LatLng]:
        """The ordered sequence of LatLng coordinates of the Polyline.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps#googlemappolyline)"""
        ...
    @path.setter
    def path(self, value: list[_LatLng]) -> None: ...
    """The ordered sequence of LatLng coordinates of the Polyline."""

    @property
    def geodesic(self) -> bool:
        """When true, edges of the polygon are interpreted as geodesic and will follow the curvature of the Earth.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps#googlemappolyline)"""
        ...
    @geodesic.setter
    def geodesic(self, value: bool) -> None: ...
    """When true, edges of the polyline are interpreted as geodesic."""

    @property
    def editable(self) -> bool:
        """True if this overlay can be edited by the user.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps#googlemappolyline)"""
        ...
    @editable.setter
    def editable(self, value: bool) -> None: ...
    """True if this overlay can be edited by the user."""

    @property
    def stroke_color(self) -> str:
        """The color to draw the overlay outline.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps#googlemappolyline)"""
        ...
    @stroke_color.setter
    def stroke_color(self, value: str) -> None: ...
    """The stroke color."""

    @property
    def stroke_opacity(self) -> float:
        """The opacity of the overlay outline.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps#googlemappolyline)"""
        ...
    @stroke_opacity.setter
    def stroke_opacity(self, value: float) -> None: ...
    """The stroke opacity between 0.0 and 1.0."""

    @property
    def stroke_weight(self) -> int:
        """The weight of the overlay outline

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps#googlemappolyline)"""
        ...
    @stroke_weight.setter
    def stroke_weight(self, value: int) -> None: ...
    """The stroke width in pixels."""

    def remove(self) -> None:
        """Remove this polyline from the map."""
        ...


    def __init__(
        self,
        *,
        tag: Any = ...,
        clickable: bool = ...,
        draggable: bool = ...,
        visible: bool = ...,
        z_index: float = ...,
        enabled: bool = ...,
        tooltip: str = ...,
        role: str | list[str] | None = ...,
        icons: list[Any] = ...,
        path: list[_LatLng] = ...,
        geodesic: bool = ...,
        editable: bool = ...,
        stroke_color: str = ...,
        stroke_opacity: float = ...,
        stroke_weight: int = ...,
    ) -> None: ...

class _MapPoint:
    def __init__(self, x: float, y: float) -> None: ...


class _MapLatLngLiteral:
    lat: float
    """The latitude in degrees."""
    lng: float
    """The longitude in degrees."""
    def __init__(self, *, lat: float = ..., lng: float = ...) -> None: ...


class _MapLatLngBoundsLiteral:
    north: float
    """The latitude of the north edge of the bounds, in degrees."""
    east: float
    """The longitude of the east edge of the bounds, in degrees."""
    south: float
    """The latitude of the south edge of the bounds, in degrees."""
    west: float
    """The longitude of the west edge of the bounds, in degrees."""
    def __init__(self, *, north: float = ..., east: float = ..., south: float = ..., west: float = ...) -> None: ...


class _MapIcon:
    anchor: _MapPoint
    label_origin: _MapPoint
    """The origin of the label relative to the top-left corner of the icon image, if a label is supplied by the marker. By default, the origin is located in the center point of the image."""
    origin: _MapPoint
    """The position of the image within a sprite, if any. By default, the origin is located at the top left corner of the image (0, 0)."""
    scaled_size: _MapSize
    size: _MapSize
    url: str
    """The URL of the image or sprite sheet."""
    def __init__(
        self,
        *,
        anchor: _MapPoint = ...,
        label_origin: _MapPoint = ...,
        origin: _MapPoint = ...,
        scaled_size: _MapSize = ...,
        size: _MapSize = ...,
        url: str = ...,
    ) -> None: ...


class _MapSymbol:
    stroke_color: str
    stroke_opacity: float
    stroke_weight: float
    anchor: _MapPoint
    fill_color: str
    """The fill color of this symbol."""
    fill_opacity: float
    """The fill opacity of this symbol. Defaults to 0."""
    label_origin: _MapPoint
    path: int | str
    rotation: float
    """The angle by which to rotate the symbol, expressed clockwise in degrees."""
    scale: float
    """The amount by which the symbol is scaled in size."""
    strokeColor: str
    """The symbol's stroke color."""
    strokeOpacity: float
    """The symbol's stroke opacity."""
    strokeWeight: float
    """The symbol's stroke weight."""
    def __init__(
        self,
        *,
        anchor: _MapPoint = ...,
        fill_color: str = ...,
        fill_opacity: float = ...,
        label_origin: _MapPoint = ...,
        path: int | str = ...,
        rotation: float = ...,
        scale: float = ...,
        stroke_color: str = ...,
        stroke_opacity: float = ...,
        stroke_weight: float = ...,
        strokeColor: str = ...,
        strokeOpacity: float = ...,
        strokeWeight: float = ...,
    ) -> None: ...


class _MapIconSequence:
    icon: _MapSymbol
    fixed_rotation: bool
    """If true, each icon in the sequence has the same fixed rotation regardless of the angle of the edge on which it lies. Defaults to false."""
    offset: float | str
    """The distance from the start of the line at which an icon is to be rendered."""
    repeat: str
    """The distance between consecutive icons on the line."""
    def __init__(self, *, icon: _MapSymbol = ..., fixed_rotation: bool = ..., offset: float | str = ..., repeat: str = ...) -> None: ...


class _MapFullscreenControlOptions:
    position: int
    def __init__(self, *, position: int = ...) -> None: ...


class _MapMapTypeControlOptions:
    position: int
    style: int
    map_type_ids: list[str]
    """IDs of map types to show in the control."""
    def __init__(self, *, position: int = ..., style: int = ..., map_type_ids: list[str] = ...) -> None: ...


class _MapMotionTrackingControlOptions:
    position: int
    def __init__(self, *, position: int = ...) -> None: ...


class _MapRotateControlOptions:
    position: int
    def __init__(self, *, position: int = ...) -> None: ...


class _MapScaleControlOptions:
    position: int
    def __init__(self, *, position: int = ...) -> None: ...


class _MapStreetViewControlOptions:
    position: int
    def __init__(self, *, position: int = ...) -> None: ...


class _MapZoomControlOptions:
    position: int
    def __init__(self, *, position: int = ...) -> None: ...


class _MapMarkerLabel:
    color: str
    """The color of the label text. Default color is black."""
    font_family: str
    """The font family of the label text."""
    font_size: str
    """The font size of the label text."""
    font_weight: str
    """The font weight of the label text."""
    text: str
    """The text to be displayed in the label."""
    def __init__(
        self,
        *,
        color: str = ...,
        font_family: str = ...,
        font_size: str = ...,
        font_weight: str = ...,
        text: str = ...,
    ) -> None: ...


class _MapGeocoderAddressComponent:
    long_name: str
    """The full text of the address component"""
    short_name: str
    """The abbreviated, short text of the given address component."""
    types: list[str]
    """An array of strings denoting the type of this address component."""
    def __init__(self, *, long_name: str = ..., short_name: str = ..., types: list[str] = ...) -> None: ...


class _MapGeocoderGeometry:
    bounds: _LatLngBounds | None
    location: _LatLng
    location_type: str
    viewport: _LatLngBounds
    def __init__(
        self,
        *,
        bounds: _LatLngBounds | None = ...,
        location: _LatLng = ...,
        location_type: str = ...,
        viewport: _LatLngBounds = ...,
    ) -> None: ...


class _MapGeocoderResult:
    address_components: list[_MapGeocoderAddressComponent]
    formatted_address: str
    """A string containing the human-readable address of this location."""
    geometry: _MapGeocoderGeometry
    partial_match: bool | None
    """Whether the geocoder did not return an exact match for the original request, though it was able to match part of the requested address."""
    place_id: str
    """The place ID associated with the location. Place IDs uniquely identify a place in the Google Places database and on Google Maps."""
    postcode_localities: list[str] | None
    """An array of strings denoting all the localities contained in a postal code. This is only present when the result is a postal code that contains multiple localities."""
    types: list[str]
    """An array of strings denoting the type of the returned geocoded element."""
    def __init__(
        self,
        *,
        address_components: list[_MapGeocoderAddressComponent] = ...,
        formatted_address: str = ...,
        geometry: _MapGeocoderGeometry = ...,
        partial_match: bool | None = ...,
        place_id: str = ...,
        postcode_localities: list[str] | None = ...,
        types: list[str] = ...,
    ) -> None: ...


# Both spellings are accepted by the runtime's keyword-to-JavaScript conversion.
class _MapDataStyleKwargs(TypedDict, total=False):
    clickable: bool
    cursor: str
    draggable: bool
    editable: bool
    fill_color: str
    fill_opacity: float
    icon: _MapSymbol
    shape: Any
    stroke_color: str
    stroke_opacity: float
    stroke_weight: float
    title: str
    visible: bool
    z_index: float
    fillColor: str
    fillOpacity: float
    strokeColor: str
    strokeOpacity: float
    strokeWeight: float
    zIndex: float


class _MapDataStyleOptions:
    clickable: bool
    """If true, the marker receives mouse and touch events. Default value is true."""
    cursor: str
    """Mouse cursor to show on hover. Only applies to point geometries."""
    draggable: bool
    """If true, the object can be dragged across the map and the underlying feature will have its geometry updated."""
    editable: bool
    """If true, the object can be edited by dragging control points and the underlying feature will have its geometry updated."""
    fill_color: str
    """The fill color."""
    fill_opacity: float
    """The fill opacity between 0.0 and 1.0."""
    icon: _MapSymbol
    stroke_color: str
    """The stroke color."""
    stroke_opacity: float
    """The stroke opacity between 0.0 and 1.0."""
    stroke_weight: float
    """The stroke width in pixels."""
    title: str
    """Rollover text."""
    visible: bool
    """Whether the feature is visible."""
    z_index: float
    """All features are displayed on the map in order of their zIndex, with higher values displaying in front of features with lower values."""
    def __init__(
        self,
        *,
        clickable: bool = ...,
        cursor: str = ...,
        draggable: bool = ...,
        editable: bool = ...,
        fill_color: str = ...,
        fill_opacity: float = ...,
        icon: _MapSymbol = ...,
        stroke_color: str = ...,
        stroke_opacity: float = ...,
        stroke_weight: float = ...,
        title: str = ...,
        visible: bool = ...,
        z_index: float = ...,
    ) -> None: ...


class _MapAnimation:
    BOUNCE: ClassVar[int]
    """Marker bounces until animation is stopped."""
    DROP: ClassVar[int]
    """Marker falls from the top of the map ending with a small bounce."""


class _MapGeocoderLocationType:
    APPROXIMATE: ClassVar[str]
    """The returned result is approximate."""
    GEOMETRIC_CENTER: ClassVar[str]
    """The returned result is the geometric center of a result such a line (e.g. street) or polygon (region)."""
    RANGE_INTERPOLATED: ClassVar[str]
    """The returned result reflects an approximation (usually on a road) interpolated between two precise points (such as intersections)."""
    ROOFTOP: ClassVar[str]
    """The returned result reflects a precise geocode."""


class _MapSymbolPath:
    BACKWARD_CLOSED_ARROW: ClassVar[int]
    BACKWARD_OPEN_ARROW: ClassVar[int]
    CIRCLE: ClassVar[int]
    FORWARD_CLOSED_ARROW: ClassVar[int]
    FORWARD_OPEN_ARROW: ClassVar[int]


class _MapMapTypeId:
    HYBRID: ClassVar[str]
    """This map type displays a transparent layer of major streets on satellite images."""
    ROADMAP: ClassVar[str]
    """This map type displays a normal street map."""
    SATELLITE: ClassVar[str]
    """This map type displays satellite images."""
    TERRAIN: ClassVar[str]
    """This map type displays maps with physical features such as terrain and vegetation."""


class _MapStrokePosition:
    CENTER: ClassVar[int]
    INSIDE: ClassVar[int]
    OUTSIDE: ClassVar[int]


class _MapMapTypeControlStyle:
    DEFAULT: ClassVar[int]
    DROPDOWN_MENU: ClassVar[int]
    HORIZONTAL_BAR: ClassVar[int]


class _MapControlPosition:
    BOTTOM_CENTER: ClassVar[int]
    BOTTOM_LEFT: ClassVar[int]
    BOTTOM_RIGHT: ClassVar[int]
    LEFT_BOTTOM: ClassVar[int]
    LEFT_CENTER: ClassVar[int]
    LEFT_TOP: ClassVar[int]
    RIGHT_BOTTOM: ClassVar[int]
    RIGHT_CENTER: ClassVar[int]
    RIGHT_TOP: ClassVar[int]
    TOP_CENTER: ClassVar[int]
    TOP_LEFT: ClassVar[int]
    TOP_RIGHT: ClassVar[int]


class _MapDataGeometry:
    def get_type(self) -> str:
        """Returns the type of the geometry object."""
        ...


class _MapDataPoint(_MapDataGeometry):
    def __init__(self, lat_lng: _LatLng | _MapLatLngLiteral) -> None: ...
    def get(self) -> _LatLng:
        """Returns the contained LatLng."""
        ...


class _MapDataGeometryArray(_MapDataGeometry, Generic[_T]):
    def __init__(self, points: Iterable[_T]) -> None: ...
    def get_array(self) -> list[_T]:
        """Returns an array of the contained LatLngs. A new array is returned each time get_array() is called."""
        ...
    def get_at(self, n: int) -> _T:
        """Returns the n-th contained LatLng."""
        ...
    def get_length(self) -> int:
        """Returns the number of contained LatLngs."""
        ...


class _MapDataMultiPoint(_MapDataGeometryArray[_LatLng]):
    def __init__(self, points: Iterable[_LatLng | _MapLatLngLiteral]) -> None: ...


class _MapDataLineString(_MapDataGeometryArray[_LatLng]):
    def __init__(self, points: Iterable[_LatLng | _MapLatLngLiteral]) -> None: ...


class _MapDataLinearRing(_MapDataGeometryArray[_LatLng]):
    def __init__(self, points: Iterable[_LatLng | _MapLatLngLiteral]) -> None: ...


class _MapDataMultiLineString(_MapDataGeometryArray[_MapDataLineString]):
    def __init__(self, points: Iterable[_MapDataLineString | Iterable[_LatLng | _MapLatLngLiteral]]) -> None: ...


class _MapDataPolygon(_MapDataGeometryArray[_MapDataLinearRing]):
    def __init__(self, points: Iterable[_MapDataLinearRing | Iterable[_LatLng | _MapLatLngLiteral]]) -> None: ...


class _MapDataMultiPolygon(_MapDataGeometryArray[_MapDataPolygon]):
    def __init__(self, points: Iterable[_MapDataPolygon | Iterable[_MapDataLinearRing | Iterable[_LatLng | _MapLatLngLiteral]]]) -> None: ...


class _MapDataGeometryCollection(_MapDataGeometryArray[_MapDataGeometry]):
    def __init__(self, points: Iterable[_MapDataGeometry | _LatLng | _MapLatLngLiteral]) -> None: ...


class _MapDataFeature:
    @property
    def geometry(self) -> _MapDataGeometry | None: ...
    @geometry.setter
    def geometry(self, value: _MapDataGeometry | _LatLng | None) -> None: ...
    id: str | int | None
    """Feature ID is optional."""
    def __init__(self, *, geometry: _MapDataGeometry | _LatLng | None = None, id: str | int | None = None, properties: Mapping[str, Any] | None = None) -> None: ...
    def __getitem__(self, name: str) -> Any: ...
    def __setitem__(self, name: str, value: Any) -> None: ...
    def to_geo_json(self) -> dict[str, Any]:
        """Exports this feature as a GeoJSON object."""
        ...


class _MapData:
    StyleOptions = _MapDataStyleOptions
    """Create a new 'StyleOptions' object"""
    Geometry = _MapDataGeometry
    """Create a new 'Geometry' object"""
    Point = _MapDataPoint
    """Create a new Point at the specified position."""
    MultiPoint = _MapDataMultiPoint
    """Create a new MultiPoint geometry containing the specified points."""
    LineString = _MapDataLineString
    """Create a new LineString geometry from the specified points."""
    MultiLineString = _MapDataMultiLineString
    """Constructs a Data.MultiLineString from the given Data.LineStrings or arrays of positions."""
    LinearRing = _MapDataLinearRing
    """Constructs a Data.LinearRing from the given LatLngs"""
    Polygon = _MapDataPolygon
    """Constructs a Data.Polygon from the given LinearRings or arrays of positions."""
    MultiPolygon = _MapDataMultiPolygon
    """Constructs a Data.MultiPolygon from the given Polygons or arrays of positions."""
    GeometryCollection = _MapDataGeometryCollection
    """Constructs a Data.GeometryCollection from the given geometry objects or LatLngs."""
    Feature = _MapDataFeature
    """Create a new Feature."""

    control_position: int
    controls: list[Literal["Point", "LineString", "Polygon"]]
    """Describes which drawing modes are available for the user to select, in the order they are displayed. Possible drawing modes are "Point", "LineString" or "Polygon"."""
    drawing_mode: Literal["Point", "LineString", "Polygon"] | None
    """The current drawing mode of the given Data layer. Possible drawing modes are "Point", "LineString" or "Polygon"."""
    style: _MapDataStyleOptions | Callable[[_MapDataFeature], _MapDataStyleOptions]
    def __init__(self, **options: Any) -> None: ...
    def add(
        self,
        feature: _MapDataFeature | None = None,
        /,
        *,
        geometry: _MapDataGeometry | _LatLng | None = None,
        id: str | int | None = None,
        properties: Mapping[str, Any] | None = None,
    ) -> _MapDataFeature:
        """Adds a feature to the collection, and returns the added feature."""
        ...
    def contains(self, feature: _MapDataFeature) -> bool:
        """Checks whether the given feature is in the collection."""
        ...
    def get_feature_by_id(self, id: str | int) -> _MapDataFeature | None:
        """Returns the feature with the given ID, if it exists in the collection."""
        ...
    def load_geo_json(self, url: str, *, id_property_name: str = ..., callback: Callable[[list[_MapDataFeature]], Any] | None = None) -> None:
        """Loads GeoJSON from a URL, and adds the features to the collection."""
        ...
    def remove(self, feature: _MapDataFeature) -> None:
        """Removes a feature from the collection."""
        ...
    def revert_style(self, feature: _MapDataFeature | None = None) -> None:
        """Removes the effect of previous override_style() calls. The style of the given feature reverts to the style specified by set_style()."""
        ...
    def override_style(self, feature: _MapDataFeature, style: _MapDataStyleOptions | None = None, /, **options: Unpack[_MapDataStyleKwargs]) -> None:
        """Sets the style for all features in the collection. Styles specified on a per-feature basis via override_style() continue to apply."""
        ...
    def to_geo_json(self) -> dict[str, Any]:
        """Exports the features in the collection to a GeoJSON object."""
        ...
    # The runtime wrapper currently discards the Google API's returned features.
    def add_geo_json(self, geo_json: Mapping[str, Any], *, id_property_name: str = ...) -> None:
        """Adds GeoJSON features to the collection. Give this method a parsed JSON. The imported features are returned."""
        ...


class GoogleMap(Component):
    """A Google Maps component.

    [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""

    @property
    def visible(self) -> bool:
        """Should this component be displayed?

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
        ...
    @visible.setter
    def visible(self, value: bool) -> None: ...

    @property
    def center(self) -> _LatLng | Any:
        """The Map center.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
        ...
    @center.setter
    def center(self, value: _LatLng | Any) -> None: ...
    @property
    def zoom(self) -> int:
        """The map zoom level.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
        ...
    @zoom.setter
    def zoom(self, value: int) -> None: ...
    @property
    def map_type(self) -> str:
        """[Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
        ...
    @map_type.setter
    def map_type(self, value: str) -> None: ...
    @property
    def markers(self) -> list[_MapMarker]:
        """[Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
        ...
    @markers.setter
    def markers(self, value: list[_MapMarker]) -> None: ...
    @property
    def map_data(self) -> _MapData:
        """Map data

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
        ...
    @map_data.setter
    def map_data(self, value: _MapData) -> None: ...
    @property
    def background_color(self) -> str:
        """Color used for the background of the Map div. This color will be visible when tiles have not yet loaded as the user pans.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
        ...
    @background_color.setter
    def background_color(self, value: str) -> None: ...
    @property
    def clickable_icons(self) -> bool:
        """When false, map icons are not clickable. A map icon represents a point of interest

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
        ...
    @clickable_icons.setter
    def clickable_icons(self, value: bool) -> None: ...
    @property
    def disable_default_ui(self) -> bool:
        """Enables/disables all default UI.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
        ...
    @disable_default_ui.setter
    def disable_default_ui(self, value: bool) -> None: ...
    @property
    def disable_double_click_zoom(self) -> bool:
        """Enables/disables zoom and center on double click.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
        ...
    @disable_double_click_zoom.setter
    def disable_double_click_zoom(self, value: bool) -> None: ...
    @property
    def draggable(self) -> bool:
        """If false, prevents the map from being dragged.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
        ...
    @draggable.setter
    def draggable(self, value: bool) -> None: ...
    @property
    def draggable_cursor(self) -> str:
        """The name or url of the cursor to display when mousing over a draggable map.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
        ...
    @draggable_cursor.setter
    def draggable_cursor(self, value: str) -> None: ...
    @property
    def dragging_cursor(self) -> str:
        """The name or url of the cursor to display when the map is being dragged.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
        ...
    @dragging_cursor.setter
    def dragging_cursor(self, value: str) -> None: ...
    @property
    def fullscreen_control(self) -> bool:
        """The enabled/disabled state of the Fullscreen control.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
        ...
    @fullscreen_control.setter
    def fullscreen_control(self, value: bool) -> None: ...
    @property
    def fullscreen_control_options(self) -> _MapFullscreenControlOptions:
        """The display options for the Fullscreen control.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
        ...
    @fullscreen_control_options.setter
    def fullscreen_control_options(self, value: _MapFullscreenControlOptions) -> None: ...
    @property
    def gesture_handling(self) -> str:
        """This setting controls how gestures on the map are handled.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
        ...
    @gesture_handling.setter
    def gesture_handling(self, value: str) -> None: ...
    @property
    def heading(self) -> int | float:
        """The heading for aerial imagery in degrees measured clockwise from cardinal direction North.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
        ...
    @heading.setter
    def heading(self, value: int | float) -> None: ...
    @property
    def keyboard_shortcuts(self) -> bool:
        """If false, prevents the map from being controlled by the keyboard.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
        ...
    @keyboard_shortcuts.setter
    def keyboard_shortcuts(self, value: bool) -> None: ...
    @property
    def map_type_control(self) -> bool:
        """The enabled/disabled state of the Map type control.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
        ...
    @map_type_control.setter
    def map_type_control(self, value: bool) -> None: ...
    @property
    def map_type_control_options(self) -> _MapMapTypeControlOptions:
        """The display options for the Map type control.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
        ...
    @map_type_control_options.setter
    def map_type_control_options(self, value: _MapMapTypeControlOptions) -> None: ...
    @property
    def map_type_id(self) -> Any:
        """The map type ID. Defaults to MapTypeId.ROADMAP

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
        ...
    @map_type_id.setter
    def map_type_id(self, value: Any) -> None: ...
    @property
    def max_zoom(self) -> int | float:
        """The maximum zoom level which will be displayed on the map.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
        ...
    @max_zoom.setter
    def max_zoom(self, value: int | float) -> None: ...
    @property
    def min_zoom(self) -> int | float:
        """The minimum zoom level which will be displayed on the map.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
        ...
    @min_zoom.setter
    def min_zoom(self, value: int | float) -> None: ...
    @property
    def rotate_control(self) -> bool:
        """The enabled/disabled state of the rotate control.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
        ...
    @rotate_control.setter
    def rotate_control(self, value: bool) -> None: ...
    @property
    def rotate_control_options(self) -> _MapRotateControlOptions:
        """The display options for the rotate control.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
        ...
    @rotate_control_options.setter
    def rotate_control_options(self, value: _MapRotateControlOptions) -> None: ...
    @property
    def scale_control(self) -> bool:
        """The enabled/disabled state of the scale control.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
        ...
    @scale_control.setter
    def scale_control(self, value: bool) -> None: ...
    @property
    def scale_control_options(self) -> _MapScaleControlOptions:
        """The display options for the scale control.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
        ...
    @scale_control_options.setter
    def scale_control_options(self, value: _MapScaleControlOptions) -> None: ...
    @property
    def scroll_wheel(self) -> bool:
        """If false, disables scrollwheel zooming on the map.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
        ...
    @scroll_wheel.setter
    def scroll_wheel(self, value: bool) -> None: ...
    @property
    def street_view_control(self) -> bool:
        """The enabled/disabled state of the street view control.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
        ...
    @street_view_control.setter
    def street_view_control(self, value: bool) -> None: ...
    @property
    def street_view_control_options(self) -> _MapStreetViewControlOptions:
        """The display options for the street view control.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
        ...
    @street_view_control_options.setter
    def street_view_control_options(self, value: _MapStreetViewControlOptions) -> None: ...
    @property
    def zoom_control(self) -> bool:
        """The enabled/disabled state of the zoom control.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
        ...
    @zoom_control.setter
    def zoom_control(self, value: bool) -> None: ...
    @property
    def zoom_control_options(self) -> _MapZoomControlOptions:
        """The display options for the zoom control.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
        ...
    @zoom_control_options.setter
    def zoom_control_options(self, value: _MapZoomControlOptions) -> None: ...

    Point = _MapPoint
    """Create a new Point at the specified coordinates.

    [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
    LatLngLiteral = _MapLatLngLiteral
    """Create a new LatLngLiteral object at the specified latitude and longitude.

    [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
    LatLngBoundsLiteral = _MapLatLngBoundsLiteral
    """Construct a LatLngBoundsLiteral with the specified edges.

    [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
    Icon = _MapIcon
    """Construct an Icon with the specified options.

    [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
    Symbol = _MapSymbol
    """Construct a Symbol with the specified options.

    [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
    IconSequence = _MapIconSequence
    """Construct a new IconSequence with the specified options.

    [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
    FullscreenControlOptions = _MapFullscreenControlOptions
    """Construct new FullscreenControlOptions with the specified options.

    [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
    MapTypeControlOptions = _MapMapTypeControlOptions
    """Construct new MapTypeControlOptions with the specified options.

    [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
    MotionTrackingControlOptions = _MapMotionTrackingControlOptions
    """Construct new MotionTrackingControlOptions with the specified options.

    [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
    RotateControlOptions = _MapRotateControlOptions
    """Construct new RotateControlOptions with the specified options.

    [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
    ScaleControlOptions = _MapScaleControlOptions
    """Construct new ScaleControlOptions with the specified options.

    [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
    StreetViewControlOptions = _MapStreetViewControlOptions
    """Construct new StreetViewControlOptions with the specified options.

    [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
    ZoomControlOptions = _MapZoomControlOptions
    """Construct new ZoomControlOptions with the specified options.

    [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
    MarkerLabel = _MapMarkerLabel
    """Construct a new MarkerLabel with the specified options.

    [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
    GeocoderAddressComponent = _MapGeocoderAddressComponent
    """Create a new 'GeocoderAddressComponent' object

    [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
    GeocoderGeometry = _MapGeocoderGeometry
    """Create a new 'GeocoderGeometry' object

    [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
    GeocoderResult = _MapGeocoderResult
    """Create a new 'GeocoderResult' object

    [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
    Animation = _MapAnimation
    """An object containing pre-defined animations for use with Markers.

    [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
    GeocoderLocationType = _MapGeocoderLocationType
    """Describes the type of location returned from a geocode.

    [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
    SymbolPath = _MapSymbolPath
    """An object containing pre-defined symbol paths for use on maps.

    [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
    MapTypeId = _MapMapTypeId
    """An object containing pre-defined map types.

    [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
    StrokePosition = _MapStrokePosition
    """An object containing pre-defined stroke positions for shape outlines.

    [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
    MapTypeControlStyle = _MapMapTypeControlStyle
    """An object containing pre-defined control styles.

    [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
    ControlPosition = _MapControlPosition
    """An object containing pre-defined control positions.

    [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
    Data = _MapData
    """Create a new Data object with the specified options. Not fully implemented.

    [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""

    # These are classes on GoogleMap itself, rather than instance properties.
    LatLng: type[_LatLng]
    """Create a new LatLng object at the specified latitude and longitude.

    [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
    LatLngBounds: type[_LatLngBounds]
    """Create a new LatLngBounds object with the specified corners.

    [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
    Size: type[_MapSize]
    """Create a new Size at the specified coordinates.

    [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
    AbstractOverlay: type[_MapOverlay]
    """Create a new 'AbstractOverlay' object

    [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
    Marker: type[_MapMarker]
    """Create a new 'Marker' object

    [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
    Polygon: type[_MapPolygon]
    """Create a new 'Polygon' object

    [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
    Polyline: type[_MapPolyline]
    """Create a new 'Polyline' object

    [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
    Circle: type[_MapCircle]
    """Create a new 'Circle' object

    [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
    Rectangle: type[_MapRectangle]
    """Create a new 'Rectangle' object

    [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
    InfoWindow: type[_MapInfoWindow]
    """Create a new 'InfoWindow' object

    [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""

    @property
    def height(self) -> str:
        """The height of this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
        ...
    @height.setter
    def height(self, value: str) -> None: ...
    @property
    def margin(self) -> MarginPropertyValue:
        """Margin for this component. Only available in apps that have been migrated to use Layouts.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
        ...
    @margin.setter
    def margin(self, value: MarginPropertyValue) -> None: ...
    @property
    def spacing_above(self) -> Literal["none", "small", "medium", "large"] | None:
        """The vertical space above this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
        ...
    @spacing_above.setter
    def spacing_above(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...
    @property
    def spacing_below(self) -> Literal["none", "small", "medium", "large"] | None:
        """The vertical space below this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
        ...
    @spacing_below.setter
    def spacing_below(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...

    @override
    def add_event_handler(self, event_name: _GoogleMapEvents | str, handler_func: Callable[..., Any], /) -> None:
        """Add an event handler function to be called when the event happens on this component. Event handlers will be called in the order they are added. Adding the same event handler multiple times will mean it gets called multiple times.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
        ...
    @override
    def remove_event_handler(self, event_name: _GoogleMapEvents | str, handler_func: Callable[..., Any] | None = None, /) -> None:
        """Remove a specific event handler function for a given event. Calling remove_event_handler with just the event name will remove all the handlers for this event

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
        ...
    @override
    def set_event_handler(self, event_name: _GoogleMapEvents | str, handler_func: Callable[..., Any] | None, /) -> None:
        """Set a function to call when the 'event_name' event happens on this component. Using set_event_handler removes all other handlers. Setting the handler function to None removes all handlers.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
        ...
    @override
    def get_event_handlers(self, event_name: _GoogleMapEvents | str, /) -> tuple[Callable[..., Any], ...]: ...
    @override
    def raise_event(self, event_name: _GoogleMapEvents | str, /, **event_args: Any) -> None: ...

    @staticmethod
    def geocode(
        *,
        address: str = ...,
        location: _LatLng | _MapLatLngLiteral = ...,
        **options: Any,
    ) -> list[_MapGeocoderResult]:
        """Geocode the given location or address

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
        ...
    @staticmethod
    def compute_area(path: Iterable[_LatLng | _MapLatLngLiteral]) -> float:
        """Returns the area of a closed path in square meters.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
        ...
    @staticmethod
    def compute_length(path: Iterable[_LatLng | _MapLatLngLiteral]) -> float:
        """Returns the length of a path in meters.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/maps)"""
        ...

    def add_component(
        self,
        component: _MapOverlay | _MapInfoWindow,
        /,
        **layout_props: Any,
    ) -> None:
        """Add an overlay or info window to this map."""
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
        map_data: _MapData = ...,
        background_color: str = ...,
        clickable_icons: bool = ...,
        disable_default_ui: bool = ...,
        disable_double_click_zoom: bool = ...,
        draggable: bool = ...,
        draggable_cursor: str = ...,
        dragging_cursor: str = ...,
        fullscreen_control: bool = ...,
        fullscreen_control_options: _MapFullscreenControlOptions = ...,
        gesture_handling: str = ...,
        heading: int | float = ...,
        keyboard_shortcuts: bool = ...,
        map_type_control: bool = ...,
        map_type_control_options: _MapMapTypeControlOptions = ...,
        map_type_id: Any = ...,
        max_zoom: int | float = ...,
        min_zoom: int | float = ...,
        rotate_control: bool = ...,
        rotate_control_options: _MapRotateControlOptions = ...,
        scale_control: bool = ...,
        scale_control_options: _MapScaleControlOptions = ...,
        scroll_wheel: bool = ...,
        street_view_control: bool = ...,
        street_view_control_options: _MapStreetViewControlOptions = ...,
        zoom_control: bool = ...,
        zoom_control_options: _MapZoomControlOptions = ...,
        height: str = ...,
        margin: MarginPropertyValue = ...,
        spacing_above: Literal["none", "small", "medium", "large"] | None = ...,
        spacing_below: Literal["none", "small", "medium", "large"] | None = ...,
    ) -> None: ...

class YouTubeVideo(Component):
    """A YouTube video player component.

    [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#youtube-video)"""

    @property
    def visible(self) -> bool:
        """Should this component be displayed?

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#youtube-video)"""
        ...
    @visible.setter
    def visible(self, value: bool) -> None: ...
    @property
    def role(self) -> str | list[str] | None:
        """Choose how this component can appear, based on your app's visual theme.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#youtube-video)"""
        ...
    @role.setter
    def role(self, value: str | list[str] | None) -> None: ...

    @property
    def youtube_id(self) -> str:
        """The ID of the YouTube video to play

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#youtube-video)"""
        ...
    @youtube_id.setter
    def youtube_id(self, value: str) -> None: ...
    @property
    def autoplay(self) -> bool:
        """Set to true to play this video immediately

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#youtube-video)"""
        ...
    @autoplay.setter
    def autoplay(self, value: bool) -> None: ...
    @property
    def loop(self) -> bool:
        """Set to true to play this video repeatedly

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#youtube-video)"""
        ...
    @loop.setter
    def loop(self, value: bool) -> None: ...
    @property
    def mute(self) -> bool:
        """Set whether the video is muted or not.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#youtube-video)"""
        ...
    @mute.setter
    def mute(self, value: bool) -> None: ...
    @property
    def volume(self) -> float:
        """Get or set the current volume, from 0 - 100.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#youtube-video)"""
        ...
    @volume.setter
    def volume(self, value: float) -> None: ...
    @property
    def current_time(self) -> float:
        """Get or set the current playback position, in seconds.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#youtube-video)"""
        ...
    @current_time.setter
    def current_time(self, value: float) -> None: ...
    @property
    def duration(self) -> float:
        """Get the duration of the video in seconds.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#youtube-video)"""
        ...
    @duration.setter
    def duration(self, value: float) -> None: ...
    @property
    def state(self) -> str:
        """Get the current playback state of the video as a string. E.g. PLAYING

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#youtube-video)"""
        ...
    @state.setter
    def state(self, value: str) -> None: ...


    @property
    def background(self) -> str:
        """The background colour of this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#youtube-video)"""
        ...
    @background.setter
    def background(self, value: str) -> None: ...
    @property
    def border(self) -> str:
        """The border of this component. Can take any valid CSS border value.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#youtube-video)"""
        ...
    @border.setter
    def border(self, value: str) -> None: ...
    @property
    def foreground(self) -> str:
        """The foreground colour of this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#youtube-video)"""
        ...
    @foreground.setter
    def foreground(self, value: str) -> None: ...
    @property
    def height(self) -> str:
        """The height of this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#youtube-video)"""
        ...
    @height.setter
    def height(self, value: str) -> None: ...
    @property
    def margin(self) -> MarginPropertyValue:
        """Margin for this component. Only available in apps that have been migrated to use Layouts.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#youtube-video)"""
        ...
    @margin.setter
    def margin(self, value: MarginPropertyValue) -> None: ...
    @property
    def spacing_above(self) -> Literal["none", "small", "medium", "large"] | None:
        """The vertical space above this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#youtube-video)"""
        ...
    @spacing_above.setter
    def spacing_above(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...
    @property
    def spacing_below(self) -> Literal["none", "small", "medium", "large"] | None:
        """The vertical space below this component.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#youtube-video)"""
        ...
    @spacing_below.setter
    def spacing_below(self, value: Literal["none", "small", "medium", "large"] | None) -> None: ...

    @override
    def add_event_handler(self, event_name: _YouTubeVideoEvents | str, handler_func: Callable[..., Any], /) -> None:
        """Add an event handler function to be called when the event happens on this component. Event handlers will be called in the order they are added. Adding the same event handler multiple times will mean it gets called multiple times.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#youtube-video)"""
        ...
    @override
    def remove_event_handler(self, event_name: _YouTubeVideoEvents | str, handler_func: Callable[..., Any] | None = None, /) -> None:
        """Remove a specific event handler function for a given event. Calling remove_event_handler with just the event name will remove all the handlers for this event

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#youtube-video)"""
        ...
    @override
    def set_event_handler(self, event_name: _YouTubeVideoEvents | str, handler_func: Callable[..., Any] | None, /) -> None:
        """Set a function to call when the 'event_name' event happens on this component. Using set_event_handler removes all other handlers. Setting the handler function to None removes all handlers.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#youtube-video)"""
        ...
    @override
    def get_event_handlers(self, event_name: _YouTubeVideoEvents | str, /) -> tuple[Callable[..., Any], ...]: ...
    @override
    def raise_event(self, event_name: _YouTubeVideoEvents | str, /, **event_args: Any) -> None: ...

    def play(self) -> None:
        """Start playing this YouTube video.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#youtube-video)"""
        ...

    def pause(self) -> None:
        """Pause this YouTube video.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#youtube-video)"""
        ...

    def stop(self) -> None:
        """Stop playing this YouTube video.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#youtube-video)"""
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

    [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#timer)"""

    @property
    def interval(self) -> float:
        """The number of seconds between each tick. 0 switches the timer off.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#timer)"""
        ...
    @interval.setter
    def interval(self, value: float) -> None: ...

    @override
    def add_event_handler(self, event_name: _TimerEvents | str, handler_func: Callable[..., Any], /) -> None:
        """Add an event handler function to be called when the event happens on this component. Event handlers will be called in the order they are added. Adding the same event handler multiple times will mean it gets called multiple times.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#timer)"""
        ...
    @override
    def remove_event_handler(self, event_name: _TimerEvents | str, handler_func: Callable[..., Any] | None = None, /) -> None:
        """Remove a specific event handler function for a given event. Calling remove_event_handler with just the event name will remove all the handlers for this event

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#timer)"""
        ...
    @override
    def set_event_handler(self, event_name: _TimerEvents | str, handler_func: Callable[..., Any] | None, /) -> None:
        """Set a function to call when the 'event_name' event happens on this component. Using set_event_handler removes all other handlers. Setting the handler function to None removes all handlers.

        [Anvil Docs](https://anvil.works/docs/components/standard-components/basic#timer)"""
        ...
    @override
    def get_event_handlers(self, event_name: _TimerEvents | str, /) -> tuple[Callable[..., Any], ...]: ...
    @override
    def raise_event(self, event_name: _TimerEvents | str, /, **event_args: Any) -> None: ...
    def __init__(
        self,
        *,
        tag: Any = ...,
        interval: float = ...,
    ) -> None: ...
