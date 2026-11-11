# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the source file in doc/anvil-api-stubs/source/ instead, then run:
#   pnpm -F docs build
#
"""The `anvil.email` module contains functions for sending and receiving email in your Anvil app.

[Anvil Docs](https://anvil.works/docs/server/email)"""

from typing import Callable, Mapping, Sequence, TypeVar, overload

from anvil import Media

# TypeVar for email handler functions
_MessageHandler = TypeVar("_MessageHandler", bound=Callable[["Message"], None])


class SendFailure(Exception):
    """Raised when sending an email fails."""
    ...


class DeliveryFailure(Exception):
    """While handling an error, you can raise a DeliveryFailure exception to reject email delivery.

    Optionally, you may specify a message and SMTP error code with the rejection.

    [Anvil Docs](https://anvil.works/docs/server/email/sending-and-receiving#rejecting-email)"""

    def __init__(self, message: str | None = None, smtp_code: int = 554) -> None: ...


class Address:
    """Represents an email address."""
    address: str
    """The email address this object represents."""
    name: str
    """The name associated with the address this object represents."""
    raw_value: str
    """The full string value of this address."""


class SendReport:
    """Report returned after sending an email."""
    message_id: str
    """The Message-ID header given to this outgoing message."""


class Message:
    """Represents an incoming email message.

    [Anvil Docs](https://anvil.works/docs/server/email/sending-and-receiving#receiving-email)"""

    class Envelope:
        """The sender and recipient of an email, according to the SMTP envelope."""
        from_address: str
        """The email address from which this message was sent, according to the SMTP envelope."""
        recipient: str
        """The email address that received this message.

        Note that this email address may not appear in any of the headers (eg if the email has been BCCed or blind forwarded)."""

    class DKIM:
        """Object describing whether a message was signed by the sending domain."""
        valid_from_sender: bool
        """Was this message signed by the domain in its envelope "from" address?"""
        domains: list[str]
        """A list of the DKIM domains that signed this message."""

    class Addressees:
        """The addresses an email was sent from and to, according to the headers."""
        to_addresses: list[Address]
        """The addresses this message was sent to."""
        from_address: Address | None
        """The address this message was sent from."""
        cc_addresses: list[Address]
        """The addresses this message was copied to."""

    envelope: Envelope
    """The sender and recipient of this email, according to the SMTP envelope."""
    dkim: DKIM
    """Object describing whether this message was signed by the sending domain."""
    addressees: Addressees
    """The addresses this email was sent from and to, according to the headers."""
    headers: list[tuple[str, str]]
    """All the headers in this email, as a list of (name, value) pairs."""
    text: str | None
    """The plain-text content of this email, or None if there is no plain-text part."""
    subject: str | None
    """The subject of this email, or None if there is no subject."""
    html: str | None
    """The HTML content of this email, or None if there is no HTML part."""
    attachments: list[Media]
    """A list of this email's attachments."""
    inline_attachments: dict[str, Media]
    """A dictionary of this email's inline attachments. Keys are ContentID headers, values are the attachments as Media Objects."""

    def __init__(
        self,
        from_address: str | None = "Sender <sender@example.com>",
        to: str | Sequence[str] | None = "App <app@example.com>",
        cc: str | Sequence[str] | None = None,
        subject: str | None = None,
        text: str | None = None,
        html: str | None = None,
        attachments: Sequence[Media] | None = None,
        inline_attachments: Mapping[str, Media] | None = None,
        headers: Sequence[tuple[str, str]] | dict[str, str] | None = None,
        envelope_from: str | None = None,
        envelope_recipient: str | None = None,
        dkim: bool = True,
    ) -> None:
        """Build an incoming email, to pass to an `@anvil.email.handle_message` function in a test.

        There's no reason to construct a Message except for testing.

        In a test you can call the decorated function with the Message, eg
        `incoming_email(Message(from_address="Alice <alice@example.com>", text="Hi"))`.

        Args:
            from_address: The From address. Can be bare ('alice@example.com') or include a display name ('Alice <alice@example.com>').
            to: The To address or addresses.
            cc: The Cc address or addresses.
            subject: The subject line.
            text: The plain-text content.
            html: The HTML content.
            attachments: A list of Media objects.
            inline_attachments: A dictionary of Content-IDs to Media objects.
            headers: Extra headers, as (name, value) pairs or a dictionary. They replace the From, To, Cc, Subject and Message-ID headers the message would otherwise have.
            envelope_from: The sender according to the SMTP envelope. Defaults to the From address.
            envelope_recipient: The recipient according to the SMTP envelope, eg for a message received as a Bcc. Defaults to the first To address.
            dkim: If False, the message isn't signed by its sender's domain, so `require_dkim=True` handlers reject it.
        """
        ...

    def get_header(self, header_name: str, default: str | None = None) -> str | None:
        """Return the value of the specified header, or default value if it is not present.

        Case-insensitive. If the header is specified multiple times, returns the first value."""
        ...

    def list_header(self, header_name: str) -> list[str]:
        """Return a list containing every value of the specified header. Case-insensitive."""
        ...

    def reply(
        self,
        *,
        to: str | list[str] | None = None,
        cc: str | list[str] | None = None,
        bcc: str | list[str] | None = None,
        from_address: str | None = None,
        from_name: str | None = None,
        subject: str | None = None,
        text: str | None = None,
        html: str | None = None,
        attachments: list[Media] | None = None,
    ) -> SendReport:
        """Reply to this email."""
        ...


def send(
    *,
    to: str | list[str] | None = None,
    cc: str | list[str] | None = None,
    bcc: str | list[str] | None = None,
    from_address: str = "no-reply",
    from_name: str | None = None,
    subject: str | None = None,
    text: str | None = None,
    html: str | None = None,
    attachments: list[Media] | None = None,
    inline_attachments: dict[str, Media] | None = None,
) -> SendReport:
    """Send an email.

    Args:
        to: The email recipient[s] in the 'To' field. Can be a string or list of strings.
            Each string can be a bare address (eg 'joe@example.com') or include a display name (eg 'Joe Bloggs <joe@example.com>').
        cc: The email recipient[s] in the 'Cc' field. Can be a string or list of strings.
        bcc: The email recipient[s] in the 'Bcc' field. Can be a string or list of strings.
        from_address: The From: address from this email. If no domain is specified, or the specified domain is not a legal sending domain for this app, the address will be replaced with a valid domain.
        from_name: The name associated with the From: address for this email. (Only valid if the from_address is a bare email address.)
        subject: The subject line for this email.
        text: The plain-text (no HTML) content for this email. You must specify at least one of 'text' and 'html'.
        html: The HTML content for this email. You must specify at least one of 'text' and 'html'.
        attachments: A list of Media objects to send as attachments with this email.
        inline_attachments: Inline attachments that can be used in this email's HTML, for example in <img> tags. Must be a dictionary whose keys are IDs and values are Media objects. IDs can then be used in a message's HTML with 'cid:xxx' URIs.

    [Anvil Docs](https://anvil.works/docs/server/email)"""
    ...


@overload
def handle_message(fn: _MessageHandler) -> _MessageHandler:
    """Decorator to handle incoming emails.

    [Anvil Docs](https://anvil.works/docs/server/email/sending-and-receiving#receiving-email)"""
    ...


@overload
def handle_message(*, require_dkim: bool = False) -> Callable[[_MessageHandler], _MessageHandler]:
    """Decorator to handle incoming emails.

    Args:
        require_dkim: If True, reject emails without a valid DKIM signature from the sender.

    [Anvil Docs](https://anvil.works/docs/server/email/sending-and-receiving#receiving-email)"""
    ...


def handle_message(
    fn: _MessageHandler | None = None, require_dkim: bool = False
) -> _MessageHandler | Callable[[_MessageHandler], _MessageHandler]:
    """Decorator to handle incoming emails.

    Can be used with or without arguments:
    - `@anvil.email.handle_message` - handle all incoming emails
    - `@anvil.email.handle_message(require_dkim=True)` - only handle emails with valid DKIM

    Args:
        require_dkim: If True, reject emails without a valid DKIM signature from the sender.

    [Anvil Docs](https://anvil.works/docs/server/email/sending-and-receiving#receiving-email)"""
    ...
