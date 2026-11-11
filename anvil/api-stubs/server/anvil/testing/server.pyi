# AUTO-GENERATED FILE - DO NOT EDIT
# Edit the source file in doc/anvil-api-stubs/source/ instead, then run:
#   pnpm -F docs build
#
"""Helpers for testing code that uses anvil.server."""


def wait_for_background_tasks_to_finish(timeout: float = 5) -> None:
    """If the app's code has launched background tasks in this test run, wait for them to finish.

    Raises `anvil.server.TimeoutError` if any are still running after `timeout` seconds.

    ```python
    with capture_emails() as emails:
        place_order(user, items)  # Sends a receipt from a background task
        wait_for_background_tasks_to_finish()

    [receipt] = emails
    ```
    """
    ...
