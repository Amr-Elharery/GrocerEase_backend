from app.core.exceptions import AppException
from fastapi import status

class ProductsError(AppException):
    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST) -> None:
        super().__init__(message, status_code)
class ProductNotFoundError(AppException):
    def __init__(self) -> None:
        super().__init__("Product not found", status.HTTP_404_NOT_FOUND)

class ProductAlreadyExistsError(AppException):
    def __init__(self) -> None:
        super().__init__("Product already exists", status.HTTP_409_CONFLICT)
class CategoryNotFoundError(AppException):
    def __init__(self) -> None:
        super().__init__("Category is Not Found", status.HTTP_404_NOT_FOUND)