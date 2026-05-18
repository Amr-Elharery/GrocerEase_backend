from supabase import AsyncClient
from fastapi import Depends
from app.db.supabase_client import get_admin_client

class ProductsRepositorySupabase:
    def __init__(self, admin_client: AsyncClient = Depends(get_admin_client)) -> None:
        self.client = admin_client

    async def get_all_products(self, limit: int = 10, offset: int = 0, search: str = None):
      try:
        query = self.client.from_("products").select("*")
        if search:
          query = query.or_(f"product_name.ilike.%{search}%, description.ilike.%{search}%")
        response = await query.range(offset, offset + limit - 1).execute()
        return response.data
      except Exception as e:
        print(f"Error fetching products: {e}")
        return e

    async def create_product(self, payload):
      print(f"Creating product with payload: {payload}")
      try:
        response = await self.client.from_("products").insert(payload.dict()).execute()
        return response.data
      except Exception as e:
        print(f"Error creating product: {e}")
        return e

    async def get_product(self, product_id: str):
      try:
        response = await self.client.from_("products").select("*").eq("id", product_id).single().execute()
        return response.data
      except Exception as e:
        print(f"Error fetching product: {e}")
        return e

    async def update_product(self, product_id: str, payload):
      try:
        response = await self.client.from_("products").update(payload).eq("id", product_id).execute()
        return response.data
      except Exception as e:
        print(f"Error updating product: {e}")
        return e

    async def delete_product(self, product_id: str):
      try:
        response = await self.client.from_("products").update({"is_deleted": True}).eq("id", product_id).execute()
        return response.data
      except Exception as e:
        print(f"Error deleting product: {e}")
        return e