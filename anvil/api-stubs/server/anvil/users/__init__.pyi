# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the source file in doc/anvil-api-stubs/source/ instead, then run:
#   pnpm -F docs build
#
# Type stubs for anvil.users module
# Generated files: client/anvil/users/__init__.pyi, server/anvil/users/__init__.pyi

from typing import Any
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

def force_login(user_row: Row, remember: bool = False) -> Row | None:
    """Set the specified user object (a row from a Data Table) as the current logged-in user. It must be a row from the users table. By default, login status is not remembered between sessions.

    [Anvil Docs](https://anvil.works/docs/users)"""
    ...
