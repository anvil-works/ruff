# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the source file in doc/anvil-api-stubs/source/ instead, then run:
#   pnpm -F docs build
#
# Type stubs for anvil.users.mfa module
# Generated files: client/anvil/users/mfa.pyi, server/anvil/users/mfa.pyi

from typing import Any, Literal

from anvil.tables import Row

def create_fido_mfa_method(email_address: str) -> Any:
    """Generate a WebAuthn challenge that can be used to register a new hardware token for two-factor authentication."""
    ...

def get_fido_mfa_login(email_address: str, password: str) -> Any:
    """Generate a WebAuthn challenge that the given user can use to log in with a previously registered hardware token."""
    ...

def get_totp_mfa_login(code: str) -> Any:
    """Get an MFA login object representing a TOTP login code.

    This can be passed to the login_with_email function as the mfa argument."""
    ...

def get_twilio_mfa_login(code: str) -> Any:
    """Get an MFA login object representing a Twilio Verify token.

    This can be passed to the login_with_email function as the mfa argument."""
    ...

def generate_totp_secret(email_address: str) -> dict[str, Any]:
    """Generate a TOTP secret that can be added as two-factor authentication for the current user."""
    ...

def validate_totp_code(mfa_method: Any, code: str) -> bool:
    """Validate the given TOTP code against the given MFA method from a User row."""
    ...

def generate_twilio_mfa_method(phone: str) -> Any:
    """Generate a Twilio MFA method from the provided phone number."""
    ...

def send_twilio_token(mfa_method: Any, channel: Literal["sms", "call"]) -> None:
    """Send a Twilio Verify token using the given MFA method from a User row."""
    ...

def check_twilio_token(mfa_method: Any, token: str) -> bool:
    """Validate the given Twilio Verify token against the given MFA method from a User row."""
    ...

def add_mfa_method(password: str, mfa_method: Any, *, clear_existing: bool = False) -> None:
    """Add an MFA method to the current user by passing the user's password and the mfa method.

    Optionally clearing all existing methods."""
    ...

def get_available_mfa_types(email_address: str, password: str) -> list[str]:
    """Get the available MFA types for the given user by passing their email and password."""
    ...

def get_enabled_mfa_types() -> list[str]:
    """Get all the enabled MFA types for this app."""
    ...

def mfa_login_with_form(email_address: str, password: str) -> Row | None:
    """Display a form to collect two-factor authentication credentials from the user currently logging in.

    Pass the function their email and password."""
    ...

def configure_mfa_with_form(*, allow_cancel: bool = False) -> None:
    """Display a form for the user to configure 2-factor authentication.

    allow_cancel: if True, the signup form has a Cancel button that the user can use to dismiss the form."""
    ...
