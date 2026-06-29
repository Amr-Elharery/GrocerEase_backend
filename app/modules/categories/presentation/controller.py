from fastapi import Depends
from app.modules.categories.application.services.categories_service import CategoriesService
from app.modules.categories.presentation.schemas import (
    CategoryResponse,
    CreateCategoryRequest,
    CreateSubCategoryRequest,
    CategoryItem,
)


class CategoriesController:
    def __init__(self, service: CategoriesService = Depends(CategoriesService)) -> None:
        self.service = service

    async def create_category(self, payload: CreateCategoryRequest) -> CategoryResponse:
        try:
            return await self.service.create_category(payload.category_name)
        except Exception as e:
            raise e

    async def get_all_categories(self) -> list[CategoryResponse]:
        try:
            return await self.service.get_all_categories()
        except Exception as e:
            raise e

    async def create_subcategory(self, payload: CreateSubCategoryRequest, parent_id: int) -> CategoryItem:
        try:
            return await self.service.create_subcategory(payload.category_name, parent_id)
        except Exception as e:
            raise e

    async def delete_category(self, category_id) -> None:
        try:
            return await self.service.delete_category(category_id)
        except Exception as e:
            raise e
