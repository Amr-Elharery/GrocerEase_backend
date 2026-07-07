from typing import Any, Optional

from fastapi import Depends
from supabase import AsyncClient

from app.db.supabase_client import get_admin_client


class DeliveryProfilesRepositorySupabase:
    def __init__(self, admin_client: AsyncClient = Depends(get_admin_client)) -> None:
        self.client = admin_client

    async def get_profile_by_user(self, user_id: str) -> Optional[Any]:
        response = await self.client.from_("delivery_profiles").select("*").eq("user_id", user_id).execute()
        return response.data[0] if response.data else None

    async def get_profile(self, profile_id: int) -> Optional[Any]:
        response = await self.client.from_("delivery_profiles").select("*").eq("id", profile_id).execute()
        return response.data[0] if response.data else None

    async def create_profile(self, payload: dict) -> Optional[Any]:
        response = await self.client.from_("delivery_profiles").insert(payload).execute()
        return response.data[0] if response.data else None

    async def update_profile(self, profile_id: int, payload: dict) -> Optional[Any]:
        response = await self.client.from_("delivery_profiles").update(payload).eq("id", profile_id).execute()
        return response.data[0] if response.data else None

    async def increment_total_deliveries(self, profile_id: int) -> None:
        profile = await self.get_profile(profile_id)
        if not profile:
            return
        current = profile.get("total_deliveries") or 0
        await self.client.from_("delivery_profiles").update({"total_deliveries": current + 1}).eq("id", profile_id).execute()
