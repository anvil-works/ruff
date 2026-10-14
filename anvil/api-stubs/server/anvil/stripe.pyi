# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the source file in doc/anvil-api-stubs/source/ instead, then run:
#   pnpm -F docs build
#
# Type stubs for anvil.stripe module
# Generated files: client/anvil/stripe.pyi, server/anvil/stripe.pyi

from typing import Any

class Customer:
    """A Stripe Customer object."""

    id: str
    email: str
    def __getattr__(self, name: str) -> Any: ...

def new_customer(email_address: str, token: str | None = None) -> Customer:
    """Create a new Stripe Customer record."""
    ...

def get_customer(customer_id: str, /) -> Customer:
    """Retrieve a Stripe Customer record by its ID."""
    ...
