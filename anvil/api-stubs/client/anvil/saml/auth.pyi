# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the source file in doc/anvil-api-stubs/source/ instead, then run:
#   pnpm -F docs build
#
# Type stubs for anvil.saml.auth module
# Generated files: client/anvil/saml/auth.pyi, server/anvil/saml/auth.pyi

from typing import Any

def login() -> None:
    """Prompt the user to log in via SAML."""
    ...

def get_user_email() -> str | None:
    """Get the email address of the currently-logged-in SAML user.

    To log in with SAML, call anvil.saml.auth.login() from form code."""
    ...

def get_user_attributes() -> dict[str, Any] | None:
    """Get the user attributes of the currently-logged-in SAML user.

    The exact attributes available will depend on your SAML Identity Provider."""
    ...
