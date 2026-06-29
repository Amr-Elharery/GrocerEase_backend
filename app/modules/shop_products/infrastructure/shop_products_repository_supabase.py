from supabase import AsyncClient
from fastapi import Depends
from app.db.supabase_client import get_admin_client


class ShopProductsRepositorySupabase:
    def __init__(self, admin_client: AsyncClient = Depends(get_admin_client)) -> None:
        self.client = admin_client

    async def get_all_shop_products(self, shop_id: int, limit: int = 10, offset: int = 0):
        try:
            response = await self.client.from_("shop_product").select("""
                id,
                shop_id,
                product_id,
                price,
                available_stock,
                low_stock_threshold,
                is_active,
                product:product_id (
                    id,
                    product_name,
                    description,
                    brand,
                    unit,
                    product_images (
                        id,
                        image_url,
                        is_primary
                    )
                )
            """).eq("shop_id", shop_id).eq("is_active", True).range(offset, offset + limit - 1).execute()
            return response.data
        except Exception as e:
            print(f"Error fetching shop products: {e}")
            raise e

    async def get_shop_product(self, shop_product_id: int):
        try:
            response = await self.client.from_("shop_product").select("""
                id,
                shop_id,
                product_id,
                price,
                available_stock,
                low_stock_threshold,
                is_active,
                product:product_id (
                    id,
                    product_name,
                    description,
                    brand,
                    unit,
                    product_images (
                        id,
                        image_url,
                        is_primary
                    )
                )
            """).eq("id", shop_product_id).eq("is_active", True).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error fetching shop product: {e}")
            raise e

    async def create_shop_product(self, payload: dict):
        try:
            response = await self.client.from_("shop_product").insert(payload).execute()
            if response.data:
                return await self.get_shop_product(response.data[0]["id"])
            return None
        except Exception as e:
            print(f"Error creating shop product: {e}")
            raise e

    async def update_shop_product(self, shop_product_id: int, payload: dict):
        try:
            response = await self.client.from_("shop_product").update(payload).eq("id", shop_product_id).execute()
            if response.data:
                return await self.get_shop_product(shop_product_id)
            return None
        except Exception as e:
            print(f"Error updating shop product: {e}")
            raise e

    async def delete_shop_product(self, shop_product_id: int):
        try:
            response = await self.client.from_("shop_product").update({"is_active": False}).eq("id", shop_product_id).execute()
            return response.data
        except Exception as e:
            print(f"Error deleting shop product: {e}")
            raise e

    async def decrement_stock(self, shop_product_id: int, quantity: int):
        try:
            current = await self.client.from_("shop_product").select("available_stock").eq("id", shop_product_id).execute()
            if not current.data:
                return None
            current_stock = current.data[0]["available_stock"]
            if current_stock is None:
                return None
            new_stock = max(0, current_stock - quantity)
            response = await self.client.from_("shop_product").update({"available_stock": new_stock}).eq("id", shop_product_id).execute()
            return response.data
        except Exception as e:
            print(f"Error decrementing stock: {e}")
            raise e

    async def get_by_shop_and_product(self, shop_id: int, product_id: int):
        try:
            response = await self.client.from_("shop_product").select("id, is_active").eq("shop_id", shop_id).eq("product_id", product_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error checking shop product existence: {e}")
            raise e
