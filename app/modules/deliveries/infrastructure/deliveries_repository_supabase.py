from typing import Any, Optional

from fastapi import Depends
from supabase import AsyncClient

from app.db.supabase_client import get_admin_client


class DeliveriesRepositorySupabase:
    def __init__(self, admin_client: AsyncClient = Depends(get_admin_client)) -> None:
        self.client = admin_client

    async def get_delivery_by_order(self, order_id: int) -> Optional[Any]:
        response = await self.client.from_("deliveries").select("*").eq("order_id", order_id).execute()
        return response.data[0] if response.data else None

    async def get_deliveries_by_orders(self, order_ids: list[int]) -> list[Any]:
        if not order_ids:
            return []
        response = await self.client.from_("deliveries").select("*").in_("order_id", order_ids).execute()
        return response.data or []

    async def get_delivery(self, delivery_id: int) -> Optional[Any]:
        response = await self.client.from_("deliveries").select("*").eq("id", delivery_id).execute()
        return response.data[0] if response.data else None

    async def get_my_deliveries(self, delivery_profile_id: int) -> list[Any]:
        response = await self.client.from_("deliveries").select("*").eq("delivery_id", delivery_profile_id).execute()
        return response.data or []

    async def create_delivery(self, order_id: int, delivery_profile_id: int) -> Optional[Any]:
        response = await self.client.from_("deliveries").insert({
            "order_id": order_id,
            "delivery_id": delivery_profile_id,
        }).execute()
        return response.data[0] if response.data else None

    async def create_deliveries_bulk(self, order_ids: list[int], delivery_profile_id: int) -> list[Any]:
        payload = [{"order_id": order_id, "delivery_id": delivery_profile_id} for order_id in order_ids]
        response = await self.client.from_("deliveries").insert(payload).execute()
        return response.data or []

    async def delete_delivery(self, delivery_id: int) -> Any:
        response = await self.client.from_("deliveries").delete().eq("id", delivery_id).execute()
        return response.data
