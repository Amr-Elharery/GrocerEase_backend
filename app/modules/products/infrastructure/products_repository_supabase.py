from supabase import AsyncClient
from fastapi import Depends
from app.db.supabase_client import get_admin_client

class ProductsRepositorySupabase:
    def __init__(self, admin_client: AsyncClient = Depends(get_admin_client)) -> None:
        self.client = admin_client

    async def get_all_products(self, limit: int = 10, offset: int = 0, search: str = None):
      try:
        query = self.client.from_("products").select("""
                id,
                product_name,
                description,
                brand,
                unit,

                category:category_id (
                    id,
                    category_name
                ),

                product_images (
                    id,
                    image_url,
                    variant,
                    is_primary
                )
            """).eq("is_deleted", False)
        if search:
          query = query.or_(f"product_name.ilike.%{search}%, description.ilike.%{search}%")
        response = await query.range(offset, offset + limit - 1).execute()
        return response.data
      except Exception as e:
        print(f"Error fetching products: {e}")
        raise e

    async def create_product(self, payload):
      print(f"Creating product with payload: {payload}")
      try:
        # accept either a pydantic model or a dict if hasattr(payload, "dict") else dict(payload)
        response = await self.client.from_("products").insert(payload).execute()
        return response.data
      except Exception as e:
        print(f"Error creating product: {e}")
        raise e

    async def create_product_image(self, product_id: str, image_url: str, variant: str = None, is_primary: bool = False):
      print(f"Creating product image for product_id={product_id} with image_url={image_url}")
      try:
        payload = {"product_id": product_id, "image_url": image_url, "variant": variant, "is_primary": is_primary}
        response = await self.client.from_("product_images").insert(payload).execute()
        return response.data
      except Exception as e:
        print(f"Error creating product image: {e}")
        raise e

    async def get_product(self, product_id: str):
      try:
        response = await self.client.from_("products").select("""
                          id,
                          product_name,
                          description,
                          brand,
                          unit,

                          category:category_id (
                              id,
                              category_name
                          ),

                          sub_category:sub_category_id (
                              id,
                              category_name
                          ),

                          product_images (
                              id,
                              image_url,
                              variant,
                              is_primary
                          )
        """).eq("id", product_id).single().execute()
        return response.data
      except Exception as e:
        print(f"Error fetching product: {e}")
        raise e

    async def update_product(self, product_id: str, payload):
      try:
        response = await self.client.from_("products").update(payload).eq("id", product_id).execute()
        return response.data
      except Exception as e:
        print(f"Error updating product: {e}")
        raise e

    async def delete_product(self, product_id: str):
      try:
        response = await self.client.from_("products").update({"is_deleted": True}).eq("id", product_id).execute()
        return response.data
      except Exception as e:
        print(f"Error deleting product: {e}")
        raise e