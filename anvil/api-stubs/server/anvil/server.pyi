# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the source file in doc/anvil-api-stubs/source/ instead, then run:
#   pnpm -F docs build
#
# Type stubs for anvil.server module
# Generated files: client/anvil/server.pyi, server/anvil/server.pyi

from typing import Any, Callable, TypeVar, overload, Literal
from typing_extensions import ParamSpec
from anvil.tables import Row

_T = TypeVar("_T")
_P = ParamSpec("_P")
_UserCheck = Callable[[Row | None], bool]


# ============================================================================
# Exceptions
# ============================================================================

class AnvilWrappedError(Exception):
    """Base class for exceptions transported between client and server."""

    message: Any

    def __init__(self, message: Any = "") -> None: ...


# Private compatibility for existing code; portable exceptions will supersede it.
def _register_exception_type(name: str, cls: type[Exception]) -> None: ...


class SerializationError(Exception):
    """Raised when serialization fails."""
    ...


class AppOfflineError(Exception):
    """Raised when the app is offline."""
    ...


class ScriptExitError(Exception):
    """Raised when a script exits with a non-zero status."""
    ...


class SessionExpiredError(Exception):
    """Raised when the session has expired."""
    ...


class UplinkDisconnectedError(Exception):
    """Raised when the uplink connection is lost."""
    ...


class ExecutionTerminatedError(Exception):
    """Raised when execution is terminated."""
    ...


class TimeoutError(Exception):
    """Raised when a server call times out."""
    ...


class InternalError(Exception):
    """Raised when an internal server error occurs."""
    ...


class RuntimeUnavailableError(Exception):
    """Raised when the runtime is unavailable."""
    ...


class QuotaExceededError(Exception):
    """Raised when a quota is exceeded."""
    ...


class NoServerFunctionError(Exception):
    """Raised when a server function is not found."""
    ...


class PermissionDenied(Exception):
    """Raised when permission is denied."""
    ...


class InvalidResponseError(Exception):
    """Raised when an invalid response is received."""
    ...


class ServiceNotAdded(Exception):
    """Raised when a required service is not added to the app."""
    ...


class BackgroundTaskError(Exception):
    """Raised when a background task encounters an error."""
    ...


class BackgroundTaskKilled(Exception):
    """Raised when a background task is killed."""
    ...


class BackgroundTaskNotFound(Exception):
    """Raised when a background task is not found."""
    ...


# ============================================================================
# Capabilities
# ============================================================================

class Capability:
    """A Capability represents the ability to perform an action.

    [Anvil Docs](https://anvil.works/docs/server/capabilities)"""

    ANY: Any
    """Sentinel value for unwrap_capability."""

    scope: list[Any]
    """A list representing what this capability represents.

    It can be extended by calling narrow(), but not shortened.
    Eg: ['my_resource', 42, 'foo']"""

    is_valid: bool
    """True if this Capability is still valid; False if it has been invalidated."""

    def narrow(self, additional_scope: Any) -> "Capability":
        """Return a new capability that is narrower than this one.

        Appends additional scope element(s) to it."""
        ...

    def set_update_handler(
        self,
        apply_update: Callable[..., Any],
        get_update: Callable[..., Any] | None = None,
    ) -> None:
        """Set a handler for what happens when an update is sent to this capability.

        Optionally provide a function for aggregating updates."""
        ...

    def send_update(self, update: Any) -> None:
        """Send an update to the update handler for this capability."""
        ...


def unwrap_capability(capability: Capability, scope_pattern: list[Any]) -> list[Any]:
    """Check that the first argument is a valid Capability and its scope matches the pattern.

    To match, the scope must:
    - Be at least as broad as the pattern (ie the same length or shorter)
    - Contain the same values in the same position as the pattern - unless that
      position in the pattern is Capability.ANY, which matches any value

    Returns a list of matched scope elements, of the same length as the pattern."""
    ...


# ============================================================================
# Call Context
# ============================================================================

class _ClientInfo:
    """Information about the client that initiated the current session."""

    type: str
    """The type of client (e.g., 'browser', 'uplink')."""

    ip: str | None
    """The IP address of the client."""

    location: "_Location | None"
    """The location of the client, if available."""


class _Location:
    """Geographic location information."""

    city: str | None
    country: str | None
    latitude: float | None
    longitude: float | None


class _StackFrame:
    """Information about a call stack frame."""

    type: str
    """The execution environment type."""

    is_trusted: bool
    """Whether this call is from trusted (server-side) code."""


class CallContext:
    """Contains information about what triggered the currently running code."""

    client: _ClientInfo
    """An object that describes the client that initiated the current session."""

    type: str
    """The execution environment this code is running in.

    May be 'browser', 'server_module' or 'uplink'."""

    remote_caller: _StackFrame | None
    """An object describing the code that called this @anvil.server.callable function."""

    background_task_id: str | None
    """The ID of the currently running background task, if there is one."""


context: CallContext
"""Contains information about what triggered the currently running code."""

# Call a server function
def call(fn_name: str, /, *args: Any, **kwargs: Any) -> Any:
    """Call a server function by name.

    [Anvil Docs](https://anvil.works/docs/server)"""
    ...

def call_s(fn_name: str, /, *args: Any, **kwargs: Any) -> Any:
    """Call a server function by name without showing a loading indicator.

    [Anvil Docs](https://anvil.works/docs/server)"""
    ...

# Callable decorator (server-only - marks functions as callable from client code)
@overload
def callable(fn: Callable[_P, _T], /) -> Callable[_P, _T]: ...
@overload
def callable(name: str | None = None, /, *, require_user: bool | _UserCheck = False) -> Callable[[Callable[_P, _T]], Callable[_P, _T]]: ...
def callable(fn_or_name: Callable[_P, _T] | str | None = ..., /, *, require_user: bool | _UserCheck = False) -> Callable[_P, _T] | Callable[[Callable[_P, _T]], Callable[_P, _T]]:
    """Mark a function as callable from client code.

    [Anvil Docs](https://anvil.works/docs/server/server-modules)"""
    ...

# Server method decorator (for methods in portable classes)
@overload
def server_method(fn: Callable[_P, _T]) -> Callable[_P, _T]: ...
@overload
def server_method(*, require_user: bool | Callable[..., bool] | None = None) -> Callable[[Callable[_P, _T]], Callable[_P, _T]]: ...
def server_method(
    fn: Callable[_P, _T] | None = ...,
    *,
    require_user: bool | Callable[..., bool] | None = None
) -> Callable[_P, _T] | Callable[[Callable[_P, _T]], Callable[_P, _T]]:
    """Mark a method in a portable class as callable from client code.

    Methods decorated with @anvil.server.server_method can be called on portable
    class instances from client code, and will execute on the server.

    [Anvil Docs](https://anvil.works/docs/server/portable-classes#server-methods)"""
    ...

# Background task decorator
@overload
def background_task(fn: Callable[_P, _T]) -> Callable[_P, _T]: ...
@overload
def background_task() -> Callable[[Callable[_P, _T]], Callable[_P, _T]]: ...
def background_task(fn: Callable[_P, _T] | None = None) -> Callable[_P, _T] | Callable[[Callable[_P, _T]], Callable[_P, _T]]:
    """Mark a function as a background task.

    [Anvil Docs](https://anvil.works/docs/background-tasks)"""
    ...

# Launch a background task
def launch_background_task(task_name: str, /, *args: Any, **kwargs: Any) -> Any:
    """Launch a background task by name.

    [Anvil Docs](https://anvil.works/docs/background-tasks)"""
    ...

# Run a script and wait for its result
def run_script(script_name: str, /, *args: Any) -> Any:
    """Run one of this app's scripts as a Background Task, wait for it to finish, and
    return its return value (whatever the script set anvil.script.return_value to).

    Positional arguments are available to the script as sys.argv[1:] and anvil.script.args
    (Media arguments appear in sys.argv as the names of temporary files containing their
    content); scripts do not accept keyword arguments.

    If the script raises an exception, exits with a non-zero status (ScriptExitError), or
    is killed (BackgroundTaskKilled), that error is raised here. To call a script from
    client code, allow it in the app's script_config.

    [Anvil Docs](https://anvil.works/docs/background-tasks)"""
    ...

# Request context
class request:
    """HTTP request context for http_endpoint handlers.

    [Anvil Docs](https://anvil.works/docs/server/http-endpoints)"""
    method: str
    path: str
    body: bytes
    body_json: Any | None
    remote_address: str
    headers: dict[str, str]
    query_params: dict[str, str]
    form_params: dict[str, str]
    cookies: dict[str, str]
    user: Any
    @staticmethod
    def get_header(name: str) -> str | None: ...

# Session handling
class session:
    """Server-side session storage.

    [Anvil Docs](https://anvil.works/docs/server/sessions)"""
    @staticmethod
    def get(key: str, default: Any = None) -> Any: ...
    @staticmethod
    def set(key: str, value: Any) -> None: ...
    @staticmethod
    def clear() -> None: ...

# HTTP endpoint decorator
def http_endpoint(path: str, methods: list[str] | None = None, authenticate_users: bool = False, enable_cors: bool = False, cross_site_session: bool = False) -> Callable[[Callable[_P, _T]], Callable[_P, _T]]:
    """Legacy decorator to create an HTTP endpoint.

    For new HTTP endpoints, use anvil.server.route instead: route("/orders") serves /orders, without /_/api.
    The endpoint URL is the app origin followed by /_/api and path:
    http_endpoint("/orders") is accessible at /_/api/orders.

    [Anvil Docs](https://anvil.works/docs/server/http-endpoints)"""
    ...

# Route decorator
def route(
    path: str,
    *,
    require_credentials: bool = False,
    authenticate_users: bool = False,
    methods: list[str] | None = None,
    enable_cors: bool = False,
    cross_site_session: bool = False,
) -> Callable[[Callable[_P, _T]], Callable[_P, _T]]:
    """Decorator to create a server-side HTTP route.

    The route URL is the app origin followed by path, without an /_/api prefix:
    route("/orders") is accessible at /orders.

    [Anvil Docs](https://anvil.works/docs/http-apis/creating-http-endpoints)"""
    ...

# Connect to other servers
def connect(url: str, /, **kwargs: Any) -> Any:
    """Connect to an Anvil Uplink server.

    [Anvil Docs](https://anvil.works/docs/uplink)"""
    ...

# Portable classes
def portable_class(cls: type[_T], /) -> type[_T]:
    """Decorator to make a class portable across client and server.

    [Anvil Docs](https://anvil.works/docs/server/portable-classes)"""
    ...


# ============================================================================
# URL and Origin Functions
# ============================================================================

def get_app_origin(environment_type: Literal["published"] | None = None) -> str:
    """Returns the root URL for the current app.

    By default, this function returns the URL for the current environment,
    which might be private or temporary. If you want the URL for the published
    branch, pass 'published' as an argument.

    [Anvil Docs](https://anvil.works/docs/http-apis/creating-http-endpoints#getting-the-url-for-your-api)"""
    ...


def get_api_origin(environment_type: Literal["published"] | None = None) -> str:
    """Returns the root URL of the API for the current app.

    By default, this function returns the URL for the current environment,
    which might be private or temporary. If you want the URL for the published
    branch, pass 'published' as an argument.

    [Anvil Docs](https://anvil.works/docs/http-apis/creating-http-endpoints#getting-the-url-for-your-api)"""
    ...


# ============================================================================
# Session Functions
# ============================================================================

def get_session_id() -> str | None:
    """Get the current session ID, if any."""
    ...


def reset_session() -> None:
    """Reset the current session."""
    ...


# ============================================================================
# Background Tasks
# ============================================================================

task_state: dict[str, Any]
"""State exposed by the currently running background task.

[Anvil Docs](https://anvil.works/docs/background-tasks/communicating-back)"""

class BackgroundTaskState:
    """Information about a background task."""

    task_id: str
    """The ID of the background task."""

    def get_id(self) -> str:
        """Get the ID of this background task."""
        ...

    def get_state(self) -> dict[str, Any]:
        """Get the current state of this background task."""
        ...

    def get_task_name(self) -> str:
        """Get the registered name of this background task.

        [Anvil Docs](https://anvil.works/docs/background-tasks)"""
        ...

    def get_return_value(self) -> Any:
        """Get the return value of this background task, if completed."""
        ...

    def get_error(self) -> Exception | None:
        """Get the error from this background task, if it failed."""
        ...

    def is_completed(self) -> bool:
        """Check if this background task has completed."""
        ...

    def is_running(self) -> bool:
        """Check if this background task is still running."""
        ...

    def kill(self) -> None:
        """Kill this background task."""
        ...


def get_background_task(id: str, /) -> BackgroundTaskState:
    """Returns the Task object of a background task from its id.

    You can get the task id from task.get_id().

    [Anvil Docs](https://anvil.works/docs/background-tasks/communicating-back)"""
    ...


def list_background_tasks(all_environments: bool = False) -> list[BackgroundTaskState]:
    """Returns a list of all Tasks running in the current environment.

    If all_environments is True, this function will return all of the app's
    running Tasks regardless of environment.

    [Anvil Docs](https://anvil.works/docs/background-tasks#list-background-tasks-from-code)"""
    ...


def is_app_online() -> bool:
    """Check if the app is online."""
    ...


# ============================================================================
# HTTP Response Classes
# ============================================================================

class _LoadAppResponse:
    """A response instructing the browser to load an app, form or module."""
    ...


class AppResponder:
    """Create app-loading responses with startup data and metadata.

    [Anvil Docs](https://anvil.works/docs/http-apis/creating-http-endpoints#appresponder-object)"""

    data: Any
    meta: dict[str, Any] | None

    def __init__(self, *, data: Any = None, meta: dict[str, Any] | None = None) -> None: ...
    def load_form(self, form_name: str, *args: Any, **kwargs: Any) -> _LoadAppResponse: ...
    def load_module(self, module_name: str) -> _LoadAppResponse: ...
    def load_app(self) -> _LoadAppResponse: ...


class HttpResponse:
    """An HTTP response object.

    [Anvil Docs](https://anvil.works/docs/http-apis/creating-http-endpoints)"""

    def __init__(
        self,
        status: int = 200,
        body: Any = "",
        headers: dict[str, str] | None = None,
    ) -> None: ...


class HttpRequest:
    """An HTTP request object.

    [Anvil Docs](https://anvil.works/docs/http-apis/creating-http-endpoints)"""

    method: str
    path: str
    body: bytes
    body_json: Any | None
    headers: dict[str, str]
    query_params: dict[str, str]
    form_params: dict[str, str]
    username: str | None
    password: str | None
    remote_address: str
