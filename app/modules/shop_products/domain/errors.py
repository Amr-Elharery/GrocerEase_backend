from app.core.exceptions import AppException
from fastapi import status


class ShopProductsError(AppException):
    def __init__(self, message: str, status_code: int = status.HTTP_400_BAD_REQUEST) -> None:
        super().__init__(message, status_code)

class ShopProductNotFoundError(AppException):
    def __init__(self) -> None:
        super().__init__("Shop product not found", status.HTTP_404_NOT_FOUND)

class ShopProductAlreadyExistsError(AppException):
    def __init__(self) -> None:
        super().__init__("This product is already added to your shop", status.HTTP_409_CONFLICT)
