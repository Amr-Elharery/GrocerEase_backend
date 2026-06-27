from fastapi import status

from app.core.exceptions import AppException


class NotificationNotFoundError(AppException):
    def __init__(self) -> None:
        super().__init__("Notification not found", status.HTTP_404_NOT_FOUND)


class NotificationsError(AppException):
    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST) -> None:
        super().__init__(message, status_code)
