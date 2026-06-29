from typing import Any, Optional

from fastapi import Depends
from supabase import AsyncClient

from app.db.supabase_client import get_admin_client


class AreasRepositorySupabase:
    def __init__(self, admin_client: AsyncClient = Depends(get_admin_client)) -> None:
        self.client = admin_client

    async def get_all_areas(self) -> list[Any]:
        response = await self.client.from_("areas").select("*").order("area_name").execute()
        return response.data or []

    async def get_area_by_id(self, area_id: int) -> Optional[Any]:
        response = await self.client.from_("areas").select("*").eq("id", area_id).execute()
        return response.data[0] if response.data else None

    async def get_area_by_name(self, area_name: str) -> Optional[Any]:
        response = await self.client.from_("areas").select("id").eq("area_name", area_name).execute()
        return response.data[0] if response.data else None

    async def create_area(self, area_name: str, city_name: str) -> Any:
        response = await self.client.from_("areas").insert({"area_name": area_name, "city_name": city_name}).execute()
        return response.data[0] if response.data else None

    async def delete_area(self, area_id: int) -> Any:
        response = await self.client.from_("areas").delete().eq("id", area_id).execute()
        return response.data

    async def get_shops_count_for_area(self, area_id: int) -> int:
        response = await self.client.from_("shop").select("id", count="exact").eq("area_id", area_id).execute()
        count = getattr(response, "count", None)
        if count is None:
            count = len(response.data or [])
        return count
