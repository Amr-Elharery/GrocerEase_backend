from fastapi import Depends
from starlette import status

from app.core.exceptions import AppException
from app.modules.categories.domain.errors import (
    CategoryHasProductsError,
    CategoryNameAlreadyExistsError,
    CategoryNotFoundError,
    SubCategoryCannotHaveChildrenError,
)
from app.modules.categories.infrastructure.categories_repository_supabase import CategoriesRepositorySupabase
from app.modules.categories.presentation.schemas import (
    CategoryItem,
    CategoryResponse,
)


class CategoriesService:
    def __init__(
        self,
        repository: CategoriesRepositorySupabase = Depends(CategoriesRepositorySupabase),
    ) -> None:
        self.repository = repository

    async def create_category(self, category_name: str) -> CategoryResponse:
        existing_category = await self.repository.get_category_by_name(category_name, None)

        if existing_category:
            raise CategoryNameAlreadyExistsError()

        try:
            row = await self.repository.create_category(category_name, None)
        except Exception as e:
            raise AppException(f"Failed to create category: {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR)

        return CategoryResponse(id=row["id"], category_name=row["category_name"])

    async def get_all_categories(self) -> list[CategoryResponse]:
        try:
            categories = await self.repository.get_all_categories()
        except Exception as e:
            raise AppException(f"Failed to retrieve categories: {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR)

        tree: dict[int, CategoryResponse] = {}
        for category in categories:  # id category_name parent_id
            if category["parent_id"] is None:
                tree[category["id"]] = CategoryResponse(id=category["id"], category_name=category["category_name"])

        for category in categories:
            if category["parent_id"] is not None and category["parent_id"] in tree:
                tree[category["parent_id"]].subcategories.append(CategoryItem(id=category["id"], category_name=category["category_name"]))

        return list(tree.values())

    async def create_subcategory(self, category_name: str, parent_id: int) -> CategoryItem:
        try:
            parent = await self.repository.get_category_by_id(parent_id)
        except Exception as e:
            raise AppException(f"Failed retrieving the parent: {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR)

        if not parent:
            raise CategoryNotFoundError()

        if parent["parent_id"] is not None:
            raise SubCategoryCannotHaveChildrenError()

        try:
            response = await self.repository.create_category(category_name, parent_id)
        except Exception as e:
            raise AppException(f"Failed inserting the data: {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR)

        return CategoryItem(id=response["id"], category_name=response["category_name"])

    async def delete_category(self, category_id: int) -> None:
        try:
            product_count = await self.repository.get_products_count_for_category(category_id)
            if product_count > 0:
                raise CategoryHasProductsError(product_count)

            result = await self.repository.delete_category(category_id)
        except CategoryHasProductsError:
            raise
        except Exception as e:
            raise AppException(f"Failed deleting category {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR)

        if not result:
            raise CategoryNotFoundError()
