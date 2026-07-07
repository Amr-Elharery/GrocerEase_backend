from typing import Any, Optional

from fastapi import Depends
from supabase import AsyncClient

from app.db.supabase_client import get_admin_client


class CategoriesRepositorySupabase:
    def __init__(self, admin_client: AsyncClient = Depends(get_admin_client)) -> None:
        self.client = admin_client

    async def get_category_by_name(self, category_name: str, parent_id: Optional[int] = None) -> Optional[Any]:
        query = self.client.from_("category").select("id").eq("category_name", category_name)
        if parent_id is None:
            query = query.is_("parent_id", None)
        else:
            query = query.eq("parent_id", parent_id)
        response = await query.execute()
        return response.data[0] if response.data else None

    async def get_category_by_id(self, category_id: int) -> Optional[Any]:
        response = await self.client.from_("category").select("id, parent_id").eq("id", category_id).single().execute()
        return response.data

    async def create_category(self, category_name: str, parent_id: Optional[int] = None) -> Any:
        payload = {"category_name": category_name, "parent_id": parent_id}
        response = await self.client.from_("category").insert(payload).execute()
        return response.data[0] if response.data else None

    async def get_all_categories(self) -> list[Any]:
        response = await self.client.from_("category").select("*").order("parent_id").execute()
        return response.data or []

    async def get_products_count_for_category(self, category_id: int) -> int:
        response = await self.client.from_("products").select("id", count="exact").or_(f"category_id.eq.{category_id},sub_category_id.eq.{category_id}").execute()
        count = getattr(response, "count", None)
        if count is None:
            count = len(response.data or [])
        return count

    async def delete_category(self, category_id: int) -> Any:
        response = await self.client.from_("category").delete().eq("id", category_id).execute()
        return response.data
