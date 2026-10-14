# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the source file in doc/anvil-api-stubs/source/ instead, then run:
#   pnpm -F docs build
#
# Type stubs for anvil.users module
# Generated files: client/anvil/users/__init__.pyi, server/anvil/users/__init__.pyi

from typing import Any
from typing import Literal, overload
from anvil.tables import Row
from anvil.users import mfa as mfa

# Exceptions (available in both environments)
class UserExists(Exception): ...
class AuthenticationFailed(Exception): ...
class EmailNotConfirmed(AuthenticationFailed): ...
class AccountIsNotEnabled(AuthenticationFailed): ...
class TooManyPasswordFailures(AuthenticationFailed): ...
class PasswordNotAcceptable(Exception): ...
class MFARequired(AuthenticationFailed): ...
class MFAException(AuthenticationFailed): ...
class PasswordResetRequested(Exception): ...

# Functions available in both environments
def get_user(allow_remembered: bool = True) -> Row | None:
    """Get the row from the users table that corresponds to the currently logged-in user. If allow_remembered is true (the default), the user may have logged in in a previous session. Returns None if no user is logged in.

    [Anvil Docs](https://anvil.works/docs/users)"""
    ...

def logout(invalidate_client_objects: bool = False) -> None:
    """Forget the current logged-in user.

If invalidate_client_objects is true, all live objects (table rows, Capabilities, unfetched Media, etc) will be invalidated

    [Anvil Docs](https://anvil.works/docs/users)"""
    ...

def login_with_email(email: str, password: str, remember: bool = False) -> Row | None:
    """Log in with the specified email address and password. Raises anvil.users.AuthenticationFailed exception if the login failed.

By default, login status is not remembered between sessions; set remember=True to remember login status.

    [Anvil Docs](https://anvil.works/docs/users/email_login)"""
    ...

def signup_with_email(email: str, password: str, remember: bool = False) -> Row | None:
    """Sign up for a new account with the specified email address and password. Raises anvil.users.UserExists if an account is already registered with this email address.

By default, login status is not remembered between sessions; set remember=True to remember login status.

    [Anvil Docs](https://anvil.works/docs/users/email_login)"""
    ...

def send_password_reset_email(email_address: str) -> None:
    """Send a password-reset email to the specified user

    [Anvil Docs](https://anvil.works/docs/users/email_login)"""
    ...

def send_token_login_email(email_address: str) -> None:
    """Send a login link email to the specified user

    [Anvil Docs](https://anvil.works/docs/users/email_login)"""
    ...

def reset_password(old_password: str, new_password: str) -> None:
    """Reset the password for the current user

    [Anvil Docs](https://anvil.works/docs/users/email_login)"""
    ...

def send_mfa_reset_email(email_address: str) -> None:
    """Send a two-factor authentication reset email to the specified user.

    [Anvil Docs](https://anvil.works/docs/users/mfa)"""
    ...


def login_with_google(additional_scopes: list[str] | None = None, remember: bool = False) -> Row | None:
    """Log in with a Google account. Prompts the user to authenticate with Google, then logs in with their Google email address (if that user exists). Returns None if the login was cancelled or we have no record of this user.

additional_scopes: If supplied, these are passed on to anvil.google.auth.login().

By default, login status is not remembered between sessions; set remember=True to remember login status.

    [Anvil Docs](https://anvil.works/docs/users/google)"""
    ...

def signup_with_google(additional_scopes: list[str] | None = None, remember: bool = False) -> Row | None:
    """Sign up for a new account with the email address associated with the user's Google account. Prompts the user to authenticate with Google, then registers a new user with that email address. Raises anvil.users.UserExists if this email address is already registered; returns new user or None if cancelled.

additional_scopes: If supplied, these are passed on to anvil.google.auth.login().

By default, login status is not remembered between sessions; set remember=True to remember login status.

    [Anvil Docs](https://anvil.works/docs/users/google)"""
    ...

def login_with_facebook(additional_scopes: list[str] | None = None, remember: bool = False) -> Row | None:
    """Log in with a Facebook account. Prompts the user to authenticate with Facebook, then logs in with their Facebook email address (if that user exists). Returns None if the login was cancelled or we have no record of this user.

additional_scopes: If supplied, these are passed on to anvil.facebook.auth.login().

By default, login status is not remembered between sessions; set remember=True to remember login status.

    [Anvil Docs](https://anvil.works/docs/users/facebook)"""
    ...

def signup_with_facebook(additional_scopes: list[str] | None = None, remember: bool = False) -> Row | None:
    """Sign up for a new account with the email address associated with the user's Facebook account. Prompts the user to authenticate with Facebook, then registers a new user with that email address. Raises anvil.users.UserExists if this email address is already registered; returns new user or None if cancelled.

additional_scopes: If supplied, these are passed on to anvil.facebook.auth.login().

By default, login status is not remembered between sessions; set remember=True to remember login status.

    [Anvil Docs](https://anvil.works/docs/users/facebook)"""
    ...

def login_with_microsoft(additional_scopes: list[str] | None = None, remember: bool = False) -> Row | None:
    """Log in with a Microsoft account. Prompts the user to authenticate with Microsoft, then logs in with their Microsoft email address (if that user exists). Returns None if the login was cancelled or we have no record of this user.

additional_scopes: If supplied, these are passed on to anvil.microsoft.auth.login().

By default, login status is not remembered between sessions; set remember=True to remember login status.

    [Anvil Docs](https://anvil.works/docs/users/microsoft)"""
    ...

def signup_with_microsoft(additional_scopes: list[str] | None = None, remember: bool = False) -> Row | None:
    """Sign up for a new account with the email address associated with the user's Microsoft account. Prompts the user to authenticate with Microsoft, then registers a new user with that email address. Raises anvil.users.UserExists if this email address is already registered; returns new user or None if cancelled.

additional_scopes: If supplied, these are passed on to anvil.microsoft.auth.login().

By default, login status is not remembered between sessions; set remember=True to remember login status.

    [Anvil Docs](https://anvil.works/docs/users/microsoft)"""
    ...

def login_with_saml(remember: bool = False) -> Row | None:
    """Log in via a SAML Identity Provider. Prompts the user to authenticate with SAML, then logs in with their email address (if that user exists). Returns None if the login was cancelled or we have no record of this user.

By default, login status is not remembered between sessions; set remember=True to remember login status.

    [Anvil Docs](https://anvil.works/docs/users/saml)"""
    ...

def signup_with_saml(remember: bool = False) -> Row | None:
    """Sign up for a new account with the email address associated with the user's SAML account. Prompts the user to authenticate via SAML, then registers a new user with that email address. Raises anvil.users.UserExists if this email address is already registered; returns new user or None if cancelled.

By default, login status is not remembered between sessions; set remember=True to remember login status.

    [Anvil Docs](https://anvil.works/docs/users/saml)"""
    ...

@overload
def login_with_form(show_signup_option: bool = True, remember_by_default: bool = True, allow_remembered: bool = True, allow_cancel: Literal[False] = False, initial_email: str | None = None) -> Row: ...
@overload
def login_with_form(show_signup_option: bool = True, remember_by_default: bool = True, allow_remembered: bool = True, allow_cancel: bool = False, initial_email: str | None = None) -> Row | None: ...
def login_with_form(show_signup_option: bool = True, remember_by_default: bool = True, allow_remembered: bool = True, allow_cancel: bool = False, initial_email: str | None = None) -> Row | None:
    """Display a login form and allow user to log in. Returns user object if logged in, or None if cancelled.

show_signup_option: if True, the form will also show the option to sign up for a new account.

remember_by_default: if True, the 'remember me' checkbox will be enabled by default.

allow_remembered: if False, users with remembered login status will still be required to log in.

allow_cancel: if True, the login form has a Cancel button that the user can use to dismiss the form.

initial_email: Optional email address to pre-fill the Email box with when email login is enabled.

    [Anvil Docs](https://anvil.works/docs/users/authentication_forms)"""
    ...

@overload
def signup_with_form(remember_by_default: bool = True, allow_cancel: Literal[False] = False) -> Row: ...
@overload
def signup_with_form(remember_by_default: bool = True, allow_cancel: bool = False) -> Row | None: ...
def signup_with_form(remember_by_default: bool = True, allow_cancel: bool = False) -> Row | None:
    """Display a sign-up form allowing a user to create a new account. Returns the new user object, or None if cancelled.

remember_by_default: if True, the 'remember me' checkbox will be enabled by default.

allow_cancel: if True, the signup form has a Cancel button that the user can use to dismiss the form.

    [Anvil Docs](https://anvil.works/docs/users/authentication_forms)"""
    ...

def change_password_with_form(require_old_password: bool = True) -> None:
    """Display a form allowing the current user to reset their password.

    [Anvil Docs](https://anvil.works/docs/users/authentication_forms)"""
    ...

def configure_account_with_form() -> None:
    """Display a form allowing the current user to configure their account. The form contains links for password reset and two-factor authentication configuration.

    [Anvil Docs](https://anvil.works/docs/users/authentication_forms)"""
    ...
