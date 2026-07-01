from typing import Any, Optional

from fastapi import Depends
from supabase import AsyncClient

from app.db.supabase_client import get_admin_client

SELECT_FIELDS = """
    id,
    user_id,
    area_id,
    street,
    building,
    floor,
    apt_number,
    latitude,
    longitude,
    additional_directions,
    label,
    is_default,
    created_at,
    area:area_id (
        id,
        area_name,
        city_name
    )
"""


class AddressesRepositorySupabase:
    def __init__(self, admin_client: AsyncClient = Depends(get_admin_client)) -> None:
        self.client = admin_client

    async def get_all_addresses(self, user_id: str) -> list[Any]:
        response = await self.client.from_("customer_address").select(SELECT_FIELDS).eq("user_id", user_id).eq("is_deleted", False).execute()
        return response.data or []

    async def get_address(self, address_id: int) -> Optional[Any]:
        response = await self.client.from_("customer_address").select(SELECT_FIELDS).eq("id", address_id).eq("is_deleted", False).execute()
        return response.data[0] if response.data else None

    async def create_address(self, payload: dict) -> Optional[Any]:
        response = await self.client.from_("customer_address").insert(payload).execute()
        if response.data:
            return await self.get_address(response.data[0]["id"])
        return None

    async def update_address(self, address_id: int, payload: dict) -> Optional[Any]:
        await self.client.from_("customer_address").update(payload).eq("id", address_id).execute()
        return await self.get_address(address_id)

    async def delete_address(self, address_id: int) -> Any:
        response = await self.client.from_("customer_address").update({"is_deleted": True}).eq("id", address_id).execute()
        return response.data

    async def has_any_address(self, user_id: str) -> bool:
        response = await self.client.from_("customer_address").select("id").eq("user_id", user_id).eq("is_deleted", False).limit(1).execute()
        return bool(response.data)

    async def clear_default(self, user_id: str) -> None:
        await self.client.from_("customer_address").update({"is_default": False}).eq("user_id", user_id).eq("is_default", True).eq("is_deleted", False).execute()
