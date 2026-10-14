# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the source file in doc/anvil-api-stubs/source/ instead, then run:
#   pnpm -F docs build
#
# Type stubs for stripe.checkout module
# Generated files: client/stripe/checkout.pyi, server/stripe/checkout.pyi

from typing import Any

def get_token(
    *,
    amount: int,
    currency: str,
    title: str | None = None,
    description: str | None = None,
    icon_url: str | None = None,
    billing_address: bool = False,
    zipcode: bool = False,
    raw: bool = False,
) -> tuple[str, dict[str, Any]]:
    """Show the Stripe checkout form and return a raw (token, user_details) tuple.

    The token can be used to place charges from server modules.
    The user_details are a dictionary of user-supplied data (eg 'email').

    Args:
        amount: A number, in least units of currency (eg cents or pennies).
        currency: A three-letter currency code (eg 'USD').
        title: Configures the checkout dialog title.
        description: Configures the checkout dialog description.
        icon_url: Path to an image to be used on the checkout form.
        zipcode: Setting to True requires the user to enter their postal code.
        billing_address: Setting to True requires the user to enter a billing address.
        raw: Setting to True returns a token for your own API key.

    [Anvil Docs](https://anvil.works/docs/integrations/stripe)"""
    ...


def charge(
    *,
    amount: int,
    currency: str,
    title: str | None = None,
    description: str | None = None,
    icon_url: str | None = None,
    billing_address: bool = False,
    shipping_address: bool = False,
    zipcode: bool = False,
) -> dict[str, Any]:
    """Charge the user for a one-off payment by showing a Stripe checkout form.

    Returns a dictionary of information about the transaction on success.

    Args:
        amount: A number, in least units of currency (eg cents or pennies).
        currency: A three-letter currency code (eg 'USD').
        title: Configures the checkout dialog title.
        description: Configures the checkout dialog description.
        icon_url: Path to an image to be used on the checkout form
            (eg anvil.server.get_app_origin() + '/_/theme/icon.png').
        billing_address: Setting to True requires the user to enter a billing address.
        shipping_address: Setting to True requires the user to enter a shipping and billing address.
        zipcode: Setting to True requires the user to enter their zipcode/postal code.

    [Anvil Docs](https://anvil.works/docs/integrations/stripe)"""
    ...
