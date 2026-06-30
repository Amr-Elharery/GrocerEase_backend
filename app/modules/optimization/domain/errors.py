from app.core.exceptions import AppException
from fastapi import status


class OptimizationError(AppException):
    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST) -> None:
        super().__init__(message, status_code)


class NoValidRouteError(AppException):
    def __init__(self) -> None:
        super().__init__("No valid route found for the given shopping list", status.HTTP_404_NOT_FOUND)
