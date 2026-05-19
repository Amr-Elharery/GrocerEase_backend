from starlette import status
from supabase import AsyncClient

from app.core.exceptions import AppException
from app.modules.categories.domain.errors import (
    CategoryNameAlreadyExistsError,
    CategoryNotFoundError,
    SubCategoryCannotHaveChildrenError,
)
from app.modules.categories.presentation.schemas import (
    CategoryItem,
    CategoryResponse,
)


class CategoriesService:
    def __init__(self, admin_client: AsyncClient, anon_client: AsyncClient) -> None:
        self.client = admin_client
        self._anon = anon_client

    async def create_category(self, category_name: str) -> CategoryResponse:
        existingCategory = await self.client.from_("category").select("id").eq("category_name", category_name).is_("parent_id", None).execute()

        if existingCategory.data:
            raise CategoryNameAlreadyExistsError()

        try:
            result = await self.client.from_("category").insert({"category_name": category_name, "parent_id": None}).execute()
        except Exception as e:
            raise AppException(f"Failed to create category: {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR)

        row = result.data[0]
        return CategoryResponse(id=row["id"], category_name=row["category_name"])

    async def get_all_categories(self) -> list[CategoryResponse]:
        try:
            result = await self.client.from_("category").select("*").order("parent_id").execute()
        except Exception as e:
            raise AppException(f"Failed to retrieve categories: {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR)

        categories = result.data
        tree = {}
        for category in categories:  # id category_name parent_id
            if category["parent_id"] is None:
                tree[category["id"]] = CategoryResponse(id=category["id"], category_name=category["category_name"])

        for category in categories:
            if category["parent_id"] is not None and category["parent_id"] in tree:
                tree[category["parent_id"]].subcategories.append(CategoryItem(id=category["id"], category_name=category["category_name"]))

        return list(tree.values())

    async def create_subcategory(self, category_name: str, parent_id: int) -> CategoryItem:
        try:
            parent_result = await self.client.from_("category").select("id, parent_id").eq("id", parent_id).execute()
        except Exception as e:
            raise AppException(f"Failed Retrieving the parent {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR)

        if not parent_result.data:
            raise CategoryNotFoundError()

        if parent_result.data[0]["parent_id"] is not None:
            raise SubCategoryCannotHaveChildrenError()

        try:
            insert_result = await self.client.from_("category").insert({"category_name": category_name, "parent_id": parent_id}).execute()
        except Exception as e:
            raise AppException(f"Failed inserting the data {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR)

        response = insert_result.data[0]
        return CategoryItem(id=response["id"], category_name=response["category_name"])

    async def delete_category(self, category_id: int) -> None:
        try:
            result = await self.client.from_("category").delete().eq("id", category_id).execute()
        except Exception as e:
            raise AppException(f"Failed deleting category {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR)

        if not result.data:
            raise CategoryNotFoundError()
