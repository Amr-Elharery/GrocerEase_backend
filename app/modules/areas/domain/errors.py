from app.core.exceptions import AppException
from fastapi import status


class AreaNotFoundError(AppException):
    def __init__(self) -> None:
        super().__init__("Area not found", status.HTTP_404_NOT_FOUND)


class AreaNameAlreadyExistsError(AppException):
    def __init__(self) -> None:
        super().__init__("Area name already exists", status.HTTP_409_CONFLICT)


class AreaHasShopsError(AppException):
    def __init__(self, count: int) -> None:
        super().__init__(f"Cannot delete — {count} shops are assigned to this area", status.HTTP_400_BAD_REQUEST)
