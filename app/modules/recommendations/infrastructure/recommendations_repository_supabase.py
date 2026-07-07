from supabase import AsyncClient
from fastapi import Depends
from app.db.supabase_client import get_admin_client


class RecommendationsRepositorySupabase:
    
    def __init__(self, admin_client: AsyncClient = Depends(get_admin_client)) -> None:
        self.client = admin_client

    async def frequently_bought_together_global(self, product_id: int, limit: int):
        try:
            response = await self.client.rpc(
                "rec_fbt_global",
                {"p_product_id": product_id, "p_limit": limit},
            ).execute()
            return response.data or []
        except Exception as e:
            print(f"Error fetching global FBT: {e}")
            raise e

    async def frequently_bought_together_shop(self, shop_id: int, product_id: int, limit: int):
        try:
            response = await self.client.rpc(
                "rec_fbt_shop",
                {"p_shop_id": shop_id, "p_product_id": product_id, "p_limit": limit},
            ).execute()
            return response.data or []
        except Exception as e:
            print(f"Error fetching shop FBT: {e}")
            raise e

    async def cart_completion_shop(self, shop_id: int, product_ids: list[int], limit: int):
        try:
            response = await self.client.rpc(
                "rec_cart_completion",
                {"p_shop_id": shop_id, "p_product_ids": product_ids, "p_limit": limit},
            ).execute()
            return response.data or []
        except Exception as e:
            print(f"Error fetching cart completion: {e}")
            raise e

    async def replenishment(self, user_id: str, limit: int):
        try:
            response = await self.client.rpc(
                "rec_replenishment",
                {"p_user_id": user_id, "p_limit": limit},
            ).execute()
            return response.data or []
        except Exception as e:
            print(f"Error fetching replenishment: {e}")
            raise e
