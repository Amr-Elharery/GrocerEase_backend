from app.core.exceptions import AppException
from fastapi import status


class ProductRequestsError(AppException):
    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST) -> None:
        super().__init__(message, status_code)

class ProductRequestNotFoundError(AppException):
    def __init__(self) -> None:
        super().__init__("Product request not found", status.HTTP_404_NOT_FOUND)
