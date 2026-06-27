from math import ceil

from fastapi import Depends
from starlette import status

from app.core.exceptions import AppException
from app.modules.notifications.domain.errors import NotificationNotFoundError
from app.modules.notifications.infrastructure.notifications_repository import NotificationsRepositorySupabase
from app.modules.notifications.presentation.schemas import (
    NotificationsPaginatedResponse,
)


class NotificationsService:
    def __init__(
        self,
        repository: NotificationsRepositorySupabase = Depends(NotificationsRepositorySupabase),
    ) -> None:
        self.repository = repository

    async def get_notifications(self, user_id: str, page: int = 1, per_page: int = 20) -> NotificationsPaginatedResponse:
        offset = (page - 1) * per_page
        try:
            notifications, total = await self.repository.get_user_notifications(user_id, per_page, offset)
        except Exception as e:
            raise AppException(f"Failed to retrieve notifications: {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR)

        total_pages = ceil(total / per_page) if total else 0
        return NotificationsPaginatedResponse(
            data=notifications,
            page=page,
            per_page=per_page,
            total=total,
            total_pages=total_pages,
        )

    async def mark_as_read(self, notification_id: int, user_id: str) -> dict:
        try:
            notification = await self.repository.get_user_notification(notification_id, user_id)
        except Exception as e:
            raise AppException(f"Failed to retrieve notification: {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR)

        if not notification:
            raise NotificationNotFoundError()

        try:
            result = await self.repository.mark_as_read(notification_id, user_id)
        except Exception as e:
            raise AppException(f"Failed to mark notification as read: {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR)

        if not result:
            raise NotificationNotFoundError()

        return {"message": "Notification marked as read successfully"}
