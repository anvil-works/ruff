# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the source file in doc/anvil-api-stubs/source/ instead, then run:
#   pnpm -F docs build
#
# Type stubs for anvil.facebook.auth module
# Generated files: client/anvil/facebook/auth.pyi, server/anvil/facebook/auth.pyi


def get_user_email() -> str | None:
    """Get the email address of the currently-logged-in Facebook user.

    To log in with Facebook, call facebook.auth.login() from form code."""
    ...

def get_user_id() -> str | None:
    """Get the Facebook user ID of the currently-logged-in Facebook user.

    To log in with Facebook, call facebook.auth.login() from form code."""
    ...

def get_user_access_token() -> str | None:
    """Get the Facebook access token of the currently-logged-in Facebook user.

    To log in with Facebook, call facebook.auth.login() from form code.

    [Anvil Docs](https://anvil.works/docs/integrations/facebook)"""
    ...
