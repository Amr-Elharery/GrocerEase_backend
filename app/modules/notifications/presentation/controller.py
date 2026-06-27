from fastapi import Depends

from app.modules.notifications.application.services.notifications_service import NotificationsService
from app.modules.notifications.presentation.schemas import NotificationsPaginatedResponse


class NotificationsController:
    def __init__(self, service: NotificationsService = Depends(NotificationsService)) -> None:
        self.service = service

    async def get_notifications(self, user_id: str, page: int = 1, per_page: int = 20) -> NotificationsPaginatedResponse:
        return await self.service.get_notifications(user_id, page, per_page)

    async def mark_as_read(self, notification_id: int, user_id: str) -> dict:
        return await self.service.mark_as_read(notification_id, user_id)
