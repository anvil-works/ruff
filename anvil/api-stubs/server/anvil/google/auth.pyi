# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the source file in doc/anvil-api-stubs/source/ instead, then run:
#   pnpm -F docs build
#
# Type stubs for anvil.google.auth module
# Generated files: client/anvil/google/auth.pyi, server/anvil/google/auth.pyi


def get_user_email() -> str | None:
    """Get the email address of the currently-logged-in Google user.

    To log in with Google, call anvil.google.auth.login() from form code."""
    ...

def get_user_access_token() -> str | None:
    """Get the secret access token of the currently-logged-in Google user, for use with the Google REST API.

    Requires this app to have its own Google client ID and secret."""
    ...

def get_user_refresh_token() -> str | None:
    """Get the secret refresh token of the currently-logged-in Google user, for use with the Google REST API.

    Requires this app to have its own Google client ID and secret."""
    ...

def refresh_access_token(refresh_token: str, /) -> str:
    """Get a new access token from a refresh token you have saved, for use with the Google REST API.

    Requires this app to have its own Google client ID and secret."""
    ...
