# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the source file in doc/anvil-api-stubs/source/ instead, then run:
#   pnpm -F docs build
#
# Type stubs for anvil.google.mail module
# Generated files: server/anvil/google/mail.pyi

def send(
    *,
    to: str | list[str] | None = None,
    subject: str | None = None,
    text: str | None = None,
    html: str | None = None,
    cc: str | list[str] | None = None,
    bcc: str | list[str] | None = None,
    from_address: str | None = None,
    draft: bool = False,
) -> None:
    """Send an email via GMail.

    'to', 'cc' and 'bcc' may be strings (email addresses) or lists of strings (multiple addresses).
    At least one of 'text' and 'html' need to be provided (both strings).
    Passing draft=True will create a draft message rather than sending it."""
    ...
