# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the source file in doc/anvil-api-stubs/source/ instead, then run:
#   pnpm -F docs build
#
"""The `anvil.js` module provides JavaScript interop functionality for Anvil apps running in the browser.

[Anvil Docs](https://anvil.works/docs/client/javascript)"""

from typing import Any, Callable, TypeVar

from anvil import BlobMedia, Component

# Import window submodule for `from anvil.js import window`
from . import window

_F = TypeVar("_F", bound=Callable[..., Any])


class ProxyType:
    """The type of a JavaScript object when accessed in Python code."""

    ...


class ExternalError(Exception):
    """An Error that occurs in Javascript will be raised in Python as an anvil.js.ExternalError.

    Typically used in a try/except block to catch a Javascript Error.

    [Anvil Docs](https://anvil.works/docs/client/javascript/accessing-javascript#catching-exceptions)"""

    original_error: Any
    """The original Javascript error that was raised."""


def await_promise(js_promise: Any, /) -> Any:
    """Await the result of a Javascript Promise in Python.

    Calls to JavaScript functions that return Promises are automatically waited
    on and return the resolved value. Do not wrap those calls in
    `await_promise()` or use Python `await` syntax. Use this function only for a
    Promise obtained without calling a JavaScript function, such as the
    Promise-valued `document.fonts.ready` property or a constructed Promise.

    This function will block until the promise resolves or rejects.
    If the promise resolves, it will return the resolved value.
    If the promise rejects, it will raise the rejected value as an exception.

    Args:
        js_promise: A JavaScript Promise object wrapped as a ProxyType.

    [Anvil Docs](https://anvil.works/docs/client/javascript/accessing-javascript#calling-asynchronous-javascript-apis)"""
    ...


def call(js_function_or_name: Any, /, *args: Any) -> Any:
    """Call a global Javascript function by name, translating arguments and return values from Python to Javascript.

    Args:
        js_function_or_name: Either a string naming a global JavaScript function, or a ProxyType function object.
        *args: Arguments to pass to the JavaScript function.

    [Anvil Docs](https://anvil.works/docs/client/javascript/accessing-javascript#calling-proxyobjects)"""
    ...


def get_dom_node(component: Component, /) -> window.HTMLElement:
    """Returns the Javascript DOM node for an Anvil component.

    If a DOM node is passed to the function it will be returned.
    Anything else throws a TypeError.

    Args:
        component: An Anvil component or DOM node.

    Returns:
        The DOM node as a ProxyType.

    [Anvil Docs](https://anvil.works/docs/client/javascript/accessing-javascript#accessing-a-dom-node)"""
    ...


def new(js_class: Any, /, *args: Any) -> Any:
    """Given a Javascript class (aka function object) that's been passed into Python, construct a new instance of it.

    Args:
        js_class: A JavaScript class/constructor function.
        *args: Arguments to pass to the constructor.

    [Anvil Docs](https://anvil.works/docs/client/javascript/accessing-javascript#calling-with-new)"""
    ...


def to_media(blob: Any, *, content_type: str = "", name: str | None = None) -> BlobMedia:
    """Convert a javascript Blob, ArrayBuffer, Uint8Array or an Array of these types to an anvil BlobMedia object.

    If a Blob, or Array of Blobs, is passed the content_type will be inferred.

    Args:
        blob: A JavaScript Blob, ArrayBuffer, Uint8Array, or Array of these types.
        content_type: The MIME type of the content. Inferred for Blobs.
        name: Optional filename for the media object.

    Returns:
        An anvil.BlobMedia object."""
    ...


def report_exceptions(wrapped_function: _F, /) -> _F:
    """Decorator for any function used as a javascript callback.

    Error handling may be suppressed by an external javascript library.
    This decorator makes sure that errors in your python code are reported.

    [Anvil Docs](https://anvil.works/docs/client/javascript/accessing-javascript#capturing-exceptions-in-callbacks)"""
    ...


def report_all_exceptions(enabled: bool, *, reraise: bool = True) -> None:
    """Set the default exception reporting behaviour for Python callbacks in Javascript.

    When set to True all exceptions will be reported by Anvil and then re-raised within Javascript.
    This may mean some exceptions are reported twice, but it ensures Exceptions in your Python code are reported correctly.

    If reraise is set to False, Exceptions raised in python code will be reported by Anvil,
    but not re-raised in Javascript. Instead the Python callback will return undefined to Javascript.

    Args:
        enabled: Whether to enable exception reporting.
        reraise: If True, re-raise exceptions after reporting. If False, return undefined instead.

    [Anvil Docs](https://anvil.works/docs/client/javascript/accessing-javascript#capturing-exceptions-in-callbacks)"""
    ...


def import_from(url: str, /) -> Any:
    """Dynamically import a Javascript Module.

    Accessing the attributes of a Javascript Module vary depending on the Module.
    See the documentation for examples.

    Args:
        url: The URL of the JavaScript module to import.

    Returns:
        The imported JavaScript module as a ProxyType.

    [Anvil Docs](https://anvil.works/docs/client/javascript/accessing-javascript#javascript-modules)"""
    ...
