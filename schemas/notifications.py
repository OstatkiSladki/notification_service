from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class NotificationResponse(BaseModel):
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
    model_config = ConfigDict(extra="forbid")

    items: list[NotificationResponse] = Field(default_factory=list)
    total: int | None = None
    page: int | None = None
    limit: int | None = None


class UpdateNotificationRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str | None = None
    message: str | None = None
    data_json: dict[str, Any] | None = None


class NotificationFilterParams(BaseModel):
    is_read: bool | None = Field(
        default=None,
        description="Фильтр по статусу прочтения",
    )
    page: int = Field(default=1, ge=1)
    limit: int = Field(default=20, le=100)
