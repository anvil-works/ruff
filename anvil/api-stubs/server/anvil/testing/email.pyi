# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the source file in doc/anvil-api-stubs/source/ instead, then run:
#   pnpm -F docs build
#
"""Helpers for testing code that sends email."""

from contextlib import AbstractContextManager

from anvil import Media


class SentEmail:
    """An email the app's code sent inside a `capture_emails()` block.

    Its attributes are the arguments the code passed to `anvil.email.send()`.
    """

    to: str | list[str] | None
    """The to argument the code passed to anvil.email.send: a string, a list of strings, or None."""
    cc: str | list[str] | None
    """The cc argument the code passed to anvil.email.send: a string, a list of strings, or None."""
    bcc: str | list[str] | None
    """The bcc argument the code passed to anvil.email.send: a string, a list of strings, or None."""
    from_address: str | None
    """The from_address the code passed to anvil.email.send, if any."""
    from_name: str | None
    """The from_name the code passed to anvil.email.send, if any."""
    subject: str | None
    """The subject line."""
    text: str | None
    """The plain-text content."""
    html: str | None
    """The HTML content."""
    attachments: list[Media]
    """The attachments."""
    inline_attachments: dict[str, Media]
    """The inline attachments, by Content-ID."""
    in_reply_to: str | None
    """The Message-ID this email replies to, eg when sent with Message.reply()."""
    references: str | None
    """The References header."""
    message_id: str
    """The Message-ID that anvil.email.send returned in its SendReport."""


def capture_emails() -> AbstractContextManager[list[SentEmail]]:
    """Use in a `with` block to capture the emails the app's code sends, including from background tasks and `Message.reply()`.

    Yields a list when the block ends, filled with `SentEmail` objects for the emails sent inside the block.
    Tests never send real email.
    To check emails sent from background tasks, call `anvil.testing.server.wait_for_background_tasks_to_finish()` inside the block.

    ```python
    with capture_emails() as emails:
        place_order(user, items)

    [email] = emails
    assert email.to == ["Alice <alice@example.com>"]
    ```
    """
    ...
