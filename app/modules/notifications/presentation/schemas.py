from datetime import datetime
from typing import Any

from pydantic import BaseModel


class NotificationItem(BaseModel):
    id: int
    title: str
    body: str
    data: dict[str, Any] | None = None
    created_at: datetime | None = None


class UserNotificationResponse(BaseModel):
    id: int
    user_id: str
    notification_id: int
    is_read: bool | None = None
    read_at: datetime | None = None
    created_at: datetime | None = None
    notification: NotificationItem | None = None


class NotificationsPaginatedResponse(BaseModel):
    data: list[UserNotificationResponse]
    page: int
    per_page: int
    total: int
    total_pages: int


class MarkNotificationReadResponse(BaseModel):
    message: str
