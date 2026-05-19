from app.modules.categories.application.services.categories_service import CategoriesService
from app.modules.categories.presentation.schemas import (
    CategoryResponse,
    CreateCategoryRequest,
    CreateSubCategoryRequest,
    CategoryItem,
)


class CategoriesController:
    def __init__(self, service: CategoriesService) -> None:
        self.service = service

    async def create_category(self, payload: CreateCategoryRequest) -> CategoryResponse:
        return await self.service.create_category(payload.category_name)

    async def get_all_categories(self) -> list[CategoryResponse]:
        return await self.service.get_all_categories()

    async def create_subcategory(self, payload: CreateSubCategoryRequest, parent_id: int) -> CategoryItem:
        return await self.service.create_subcategory(payload.category_name, parent_id)

    async def delete_category(self, category_id) -> None:
        return await self.service.delete_category(category_id)
