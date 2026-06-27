from fastapi import APIRouter, Depends, Query, status

from app.core.dependencies import get_current_user
from app.core.exceptions import AppException
from app.modules.notifications.domain.errors import NotificationsError
from app.modules.notifications.presentation.controller import NotificationsController
from app.modules.notifications.presentation.schemas import (
    MarkNotificationReadResponse,
    NotificationsPaginatedResponse,
)

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.get("/", response_model=NotificationsPaginatedResponse, status_code=status.HTTP_200_OK)
async def get_notifications(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1),
    controller: NotificationsController = Depends(NotificationsController),
    current_user=Depends(get_current_user),
):
    try:
        user_id = current_user.get("id")
        return await controller.get_notifications(user_id, page, per_page)
    except AppException:
        raise
    except Exception as e:
        raise NotificationsError(str(e))


@router.patch("/{notification_id}/read", response_model=MarkNotificationReadResponse, status_code=status.HTTP_200_OK)
async def mark_notification_as_read(
    notification_id: int,
    controller: NotificationsController = Depends(NotificationsController),
    current_user=Depends(get_current_user),
):
    try:
        user_id = current_user.get("id")
        return await controller.mark_as_read(notification_id, user_id)
    except AppException:
        raise
    except Exception as e:
        raise NotificationsError(str(e))
