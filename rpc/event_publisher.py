"""Helpers to publish cross-service events.

This is a lightweight placeholder for future RabbitMQ/Kafka integration.
"""

from typing import Any


def publish_notification_event(event_name: str, payload: dict[str, Any]) -> None:
    """Publish notification event to message broker.

    Current implementation is a no-op placeholder so application code can call
    this function without tight coupling to a concrete broker library.
    """
    _ = (event_name, payload)
