from app.core.exceptions import AppException
from fastapi import status


class ProductNotFoundError(AppException):
    def __init__(self) -> None:
        super().__init__("Product not found", status.HTTP_404_NOT_FOUND)


class ProductAlreadyExistsError(AppException):
    def __init__(self) -> None:
        super().__init__("Product already exists", status.HTTP_409_CONFLICT)

class CategoryNotFoundError(AppException):
    def __init__(self) -> None:
        super().__init__("Category is Not Found", status.HTTP_404_NOT_FOUND)
        
class CategoryNameAlreadyExistsError(AppException):
    def __init__(self) -> None:
        super().__init__("Category Name Already Exists", status.HTTP_409_CONFLICT)
        
class SubCategoryCannotHaveChildrenError(AppException):
    def __init__(self) -> None:
        super().__init__("A sub-category cannot have sub-categories", status.HTTP_400_BAD_REQUEST)
        
class CategoryHasProductsError(AppException):
    def __init__(self, count: int) -> None:
        super().__init__(f"Cannot delete — {count} products are assigned here", status.HTTP_400_BAD_REQUEST)