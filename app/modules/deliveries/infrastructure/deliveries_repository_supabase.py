from typing import Any, Optional

from fastapi import Depends
from supabase import AsyncClient

from app.db.supabase_client import get_admin_client


class DeliveriesRepositorySupabase:
    def __init__(self, admin_client: AsyncClient = Depends(get_admin_client)) -> None:
        self.client = admin_client

    async def get_assignment_by_order(self, order_id: int) -> Optional[Any]:
        response = await self.client.from_("delivery_assignment").select("*").eq("order_id", order_id).execute()
        return response.data[0] if response.data else None

    async def get_assignment(self, assignment_id: int) -> Optional[Any]:
        response = await self.client.from_("delivery_assignment").select("*").eq("id", assignment_id).execute()
        return response.data[0] if response.data else None

    async def get_my_assignments(self, delivery_user_id: str) -> list[Any]:
        response = await self.client.from_("delivery_assignment").select("*").eq("delivery_user_id", delivery_user_id).execute()
        return response.data or []

    async def create_assignment(self, order_id: int, delivery_user_id: str) -> Optional[Any]:
        response = await self.client.from_("delivery_assignment").insert({
            "order_id": order_id,
            "delivery_user_id": delivery_user_id,
        }).execute()
        return response.data[0] if response.data else None

    async def delete_assignment(self, assignment_id: int) -> Any:
        response = await self.client.from_("delivery_assignment").delete().eq("id", assignment_id).execute()
        return response.data
