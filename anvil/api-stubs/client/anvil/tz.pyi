# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the source file in doc/anvil-api-stubs/source/ instead, then run:
#   pnpm -F docs build
#
"""Timezone utilities for Anvil applications.

This module provides timezone classes for working with datetime objects.
"""

import datetime

class tzoffset(datetime.tzinfo):
    """Create a timezone with a specific offset.

    Use an offset in seconds, minutes or hours. Only one of the three
    keyword arguments should be provided.

    Args:
        seconds: Offset from UTC in seconds.
        minutes: Offset from UTC in minutes.
        hours: Offset from UTC in hours.

    Example:
        ```python
        import anvil.tz
        import datetime

        # Create a timezone 5 hours behind UTC
        eastern = anvil.tz.tzoffset(hours=-5)
        dt = datetime.datetime.now(eastern)
        ```
    """

    def __init__(
        self,
        *,
        seconds: int | None = None,
        minutes: int | None = None,
        hours: int | None = None,
    ) -> None: ...
    def utcoffset(self, dt: datetime.datetime | None) -> datetime.timedelta: ...
    def dst(self, dt: datetime.datetime | None) -> datetime.timedelta: ...
    def tzname(self, dt: datetime.datetime | None) -> str | None: ...

class tzlocal(tzoffset):
    """Use the local timezone of the browser.

    Creates a timezone object representing the local timezone where the
    code is running (browser for client code, server for server code).

    Example:
        ```python
        import anvil.tz
        import datetime

        local_tz = anvil.tz.tzlocal()
        local_time = datetime.datetime.now(local_tz)
        ```
    """

    def __init__(self) -> None: ...

class tzutc(tzoffset):
    """Create a timezone set to UTC.

    Creates a timezone object representing Coordinated Universal Time (UTC).

    Example:
        ```python
        import anvil.tz
        import datetime

        utc_tz = anvil.tz.tzutc()
        utc_time = datetime.datetime.now(utc_tz)
        ```
    """

    def __init__(self) -> None: ...

UTC: tzutc
"""An object representing the UTC timezone.

A pre-instantiated `tzutc` object for convenience.

Example:
    ```python
    import anvil.tz
    import datetime

    utc_time = datetime.datetime.now(anvil.tz.UTC)
    ```
"""
