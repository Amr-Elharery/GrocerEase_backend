from supabase import AsyncClient
from fastapi import Depends
from app.db.supabase_client import get_admin_client


class ShopsRepositorySupabase:
    def __init__(self, admin_client: AsyncClient = Depends(get_admin_client)) -> None:
        self.client = admin_client

    async def get_all_shops(self, limit: int = 10, offset: int = 0, search: str = None, area_id: int = None):
        try:
            query = self.client.from_("shop").select("""
                id,
                owner_id,
                shop_name,
                description,
                address,
                latitude,
                longitude,
                phone_number,
                logo_url,
                is_active,
                created_at,
                updated_at,
                area_id
            """).eq("is_active", True)
            if area_id:
                query = query.eq("area_id", area_id)
            if search:
                query = query.or_(f"shop_name.ilike.%{search}%, description.ilike.%{search}%, address.ilike.%{search}%")
            response = await query.range(offset, offset + limit - 1).execute()
            return response.data
        except Exception as e:
            print(f"Error fetching shops: {e}")
            raise e

    async def get_shop(self, shop_id: int):
        try:
            response = await self.client.from_("shop").select("""
                id,
                owner_id,
                shop_name,
                description,
                address,
                latitude,
                longitude,
                phone_number,
                logo_url,
                is_active,
                created_at,
                updated_at,
                area_id
            """).eq("id", shop_id).single().execute()
            return response.data
        except Exception as e:
            print(f"Error fetching shop: {e}")
            raise e

    async def get_shop_by_owner(self, owner_id: str):
        try:
            response = await self.client.from_("shop").select("""
                id,
                owner_id,
                shop_name,
                description,
                address,
                latitude,
                longitude,
                phone_number,
                logo_url,
                is_active,
                created_at,
                updated_at,
                area_id
            """).eq("owner_id", owner_id).eq("is_active", True).single().execute()
            return response.data
        except Exception as e:
            print(f"Error fetching shop by owner: {e}")
            return None

    async def create_shop(self, payload: dict):
        try:
            response = await self.client.from_("shop").insert(payload).execute()
            return response.data
        except Exception as e:
            print(f"Error creating shop: {e}")
            raise e

    async def update_shop(self, shop_id: int, payload: dict):
        try:
            response = await self.client.from_("shop").update(payload).eq("id", shop_id).execute()
            if response.data:
                return await self.get_shop(shop_id)
            return None
        except Exception as e:
            print(f"Error updating shop: {e}")
            raise e

    async def delete_shop(self, shop_id: int):
        try:
            response = await self.client.from_("shop").update({"is_active": False}).eq("id", shop_id).execute()
            return response.data
        except Exception as e:
            print(f"Error deleting shop: {e}")
            raise e
