from app.core.exceptions import AppException
from fastapi import status


class RecommendationsError(AppException):
    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST) -> None:
        super().__init__(message, status_code)
