# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the source file in doc/anvil-api-stubs/source/ instead, then run:
#   pnpm -F docs build
#
# Type stubs for anvil.http module
# Generated files: client/anvil/http.pyi, server/anvil/http.pyi

from typing import Any

from anvil import Media

class HttpError(Exception):
    """HTTP error with status code and content.

    [Anvil Docs](https://anvil.works/docs/http-apis/making-http-requests)"""

    status: int
    """The numeric HTTP status error (eg 404 for "not found").

    Status will be 0 for errors that prevent the request completing at all
    (eg cross-origin policy in the browser)."""

    content: Media
    """The content returned by the request (eg the body of a 404 response)."""

class UrlEncodingError(Exception):
    """URL encoding/decoding error."""
    ...

def request(
    url: str,
    *,
    method: str = "GET",
    data: Any = None,
    json: bool = False,
    headers: dict[str, str] | None = None,
    username: str | None = None,
    password: str | None = None,
    timeout: int | float | None = None,
) -> Media | Any:
    """Make an HTTP request to the specified URL.

    Args:
        url: The request will be made to this URL.
        method: The HTTP method. Defaults to 'GET'.
        data: The data to send in the request body.
        json: If set to True, the response is parsed into Python objects (dicts/lists/etc),
            and 'data' is JSON-encoded before sending. If False, the response will be a Media object.
        headers: A dict of strings to set HTTP headers.
        username: If specified, used to perform HTTP Basic authentication.
        password: If specified, used to perform HTTP Basic authentication.
        timeout: An int or float representing the amount of time, in seconds, to wait for a response.
            Default is 60 seconds.

    [Anvil Docs](https://anvil.works/docs/http-apis/making-http-requests)"""
    ...

def url_encode(string_to_encode: str, /) -> str:
    """URL-encode a string."""
    ...

def url_decode(string_to_decode: str, /) -> str:
    """URL-decode a string.

    Raises UrlEncodingError on failure."""
    ...
