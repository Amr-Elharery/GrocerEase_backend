from app.core.exceptions import AppException
from fastapi import status

class ShopsError(AppException):
    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST) -> None:
        super().__init__(message, status_code)

class ShopNotFoundError(AppException):
    def __init__(self) -> None:
        super().__init__("Shop not found", status.HTTP_404_NOT_FOUND)

class ShopAlreadyExistsError(AppException):
    def __init__(self) -> None:
        super().__init__("Shop already exists", status.HTTP_409_CONFLICT)