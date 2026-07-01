from fastapi import Depends
from supabase import AsyncClient
from app.db.supabase_client import get_admin_client


class AnalyticsRepositorySupabase:
    def __init__(self, admin_client: AsyncClient = Depends(get_admin_client)) -> None:
        self.client = admin_client

    async def get_shop_daily_revenue(self, shop_id: int) -> list[dict]:
        try:
            response = await self.client.from_("shop_daily_revenue").select("*").eq("shop_id", shop_id).order("day", desc=True).execute()
            return response.data or []
        except Exception as e:
            print(f"Error fetching shop daily revenue: {e}")
            raise e

    async def get_shop_orders_by_status(self, shop_id: int) -> list[dict]:
        try:
            response = await self.client.from_("shop_orders_by_status").select("*").eq("shop_id", shop_id).execute()
            return response.data or []
        except Exception as e:
            print(f"Error fetching shop orders by status: {e}")
            raise e

    async def get_shop_best_selling_products(self, shop_id: int, limit: int = 5) -> list[dict]:
        try:
            response = await self.client.from_("shop_best_selling_products").select("*").eq("shop_id", shop_id).order("total_sold", desc=True).limit(limit).execute()
            return response.data or []
        except Exception as e:
            print(f"Error fetching best selling products: {e}")
            raise e

    async def get_shop_low_stock(self, shop_id: int) -> list[dict]:
        try:
            response = await self.client.from_("shop_low_stock").select("*").eq("shop_id", shop_id).execute()
            return response.data or []
        except Exception as e:
            print(f"Error fetching low stock products: {e}")
            raise e

    async def get_shop_customer_stats(self, shop_id: int) -> dict:
        try:
            response = await self.client.from_("shop_customer_stats").select("*").eq("shop_id", shop_id).execute()
            return response.data[0] if response.data else {}
        except Exception as e:
            print(f"Error fetching shop customer stats: {e}")
            raise e

    async def get_admin_platform_overview(self) -> dict:
        try:
            response = await self.client.from_("admin_platform_overview").select("*").execute()
            return response.data[0] if response.data else {}
        except Exception as e:
            print(f"Error fetching platform overview: {e}")
            raise e

    async def get_admin_orders_by_status(self) -> list[dict]:
        try:
            response = await self.client.from_("admin_orders_by_status").select("*").execute()
            return response.data or []
        except Exception as e:
            print(f"Error fetching admin orders by status: {e}")
            raise e

    async def get_admin_daily_orders(self) -> list[dict]:
        try:
            response = await self.client.from_("admin_daily_orders").select("*").execute()
            return response.data or []
        except Exception as e:
            print(f"Error fetching admin daily orders: {e}")
            raise e

    async def get_admin_top_shops(self, limit: int = 5) -> list[dict]:
        try:
            response = await self.client.from_("admin_top_shops").select("*").limit(limit).execute()
            return response.data or []
        except Exception as e:
            print(f"Error fetching top shops: {e}")
            raise e

    async def get_admin_top_products(self, limit: int = 5) -> list[dict]:
        try:
            response = await self.client.from_("admin_top_products").select("*").limit(limit).execute()
            return response.data or []
        except Exception as e:
            print(f"Error fetching top products: {e}")
            raise e

    async def get_admin_orders_by_area(self) -> list[dict]:
        try:
            response = await self.client.from_("admin_orders_by_area").select("*").execute()
            return response.data or []
        except Exception as e:
            print(f"Error fetching orders by area: {e}")
            raise e

    async def get_admin_delivery_stats(self) -> dict:
        try:
            response = await self.client.from_("admin_delivery_stats").select("*").execute()
            return response.data[0] if response.data else {}
        except Exception as e:
            print(f"Error fetching delivery stats: {e}")
            raise e

    async def get_admin_shops_by_area(self) -> list[dict]:
        try:
            response = await self.client.from_("admin_shops_by_area").select("*").execute()
            return response.data or []
        except Exception as e:
            print(f"Error fetching shops by area: {e}")
            raise e
