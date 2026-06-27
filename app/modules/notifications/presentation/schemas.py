from datetime import datetime
from typing import Any

from pydantic import BaseModel


class NotificationResponse(BaseModel):
    id: int
    user_id: str
    notification_id: int
    is_read: bool | None = None
    read_at: datetime | None = None
    created_at: datetime | None = None
    notification: dict[str, Any] | None = None


class NotificationsPaginatedResponse(BaseModel):
    data: list[NotificationResponse]
    page: int
    per_page: int
    total: int
    total_pages: int


class MarkNotificationReadResponse(BaseModel):
    message: str
