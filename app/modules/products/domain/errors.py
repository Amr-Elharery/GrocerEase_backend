from app.core.exceptions import AppException
from fastapi import status


class ProductNotFoundError(AppException):
    def __init__(self) -> None:
        super().__init__("Product not found", status.HTTP_404_NOT_FOUND)


class ProductAlreadyExistsError(AppException):
    def __init__(self) -> None:
        super().__init__("Product already exists", status.HTTP_409_CONFLICT)
