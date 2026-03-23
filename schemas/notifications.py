"""Pydantic schemas for notifications API."""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class NotificationResponse(BaseModel):
    """Serialized notification returned by the API."""

    model_config = ConfigDict(extra="forbid", from_attributes=True)

    id: int | None = None
    user_id: int | None = None
    type: str | None = None
    title: str | None = None
    message: str | None = None
    data_json: dict[str, Any] | None = None
    is_read: bool | None = None
    created_at: datetime | None = None
    read_at: datetime | None = None


class NotificationListResponse(BaseModel):
    """Paginated notification list response."""

    model_config = ConfigDict(extra="forbid")

    items: list[NotificationResponse] = Field(default_factory=list)
    total: int | None = None
    page: int | None = None
    limit: int | None = None


class UpdateNotificationRequest(BaseModel):
    """Request body for notification partial updates."""

    model_config = ConfigDict(extra="forbid")

    title: str | None = None
    message: str | None = None
    data_json: dict[str, Any] | None = None
