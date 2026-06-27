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
      try:
        response = await self.client.from_("products").insert(payload).execute()
        return response.data
      except Exception as e:
        print(f"Error creating product: {e}")
        raise e

    async def create_product_image(self, product_id: str, image_url: str, variant: str = None, is_primary: bool = False):
      try:
        payload = {"product_id": product_id, "image_url": image_url, "variant": variant, "is_primary": is_primary}
        response = await self.client.from_("product_images").insert(payload).execute()
        return response.data
      except Exception as e:
        print(f"Error creating product image: {e}")
        raise e

    async def get_product_image(self, image_id: int):
      try:
        response = await self.client.from_("product_images").select("id, product_id, image_url, is_primary").eq("id", image_id).single().execute()
        return response.data
      except Exception as e:
        print(f"Error fetching product image: {e}")
        raise e

    async def get_product_image_path(self, image_id: int) -> str:
      try:
        image = await self.get_product_image(image_id)
        if image and image["image_url"]:
          return image["image_url"]
        raise Exception(f"No image found with id: {image_id}")
      except Exception as e:
        print(f"Error fetching product image path: {e}")
        raise e

    async def list_product_images(self, product_id: str, exclude_image_id: int = None):
      try:
        query = self.client.from_("product_images").select("id").eq("product_id", product_id)
        if exclude_image_id is not None:
          query = query.neq("id", exclude_image_id)
        response = await query.execute()
        return response.data
      except Exception as e:
        print(f"Error listing product images: {e}")
        raise e

    async def set_all_product_images_non_primary(self, product_id: str):
      try:
        response = await self.client.from_("product_images").update({"is_primary": False}).eq("product_id", product_id).execute()
        return response.data
      except Exception as e:
        print(f"Error unsetting primary product images: {e}")
        raise e

    async def set_product_image_primary(self, image_id: int):
      try:
        response = await self.client.from_("product_images").update({"is_primary": True}).eq("id", image_id).execute()
        return response.data
      except Exception as e:
        print(f"Error setting product image primary: {e}")
        raise e

    async def delete_product_image_row(self, image_id: int):
      try:
        response = await self.client.from_("product_images").delete().eq("id", image_id).execute()
        return response.data
      except Exception as e:
        print(f"Error deleting product image row: {e}")
        raise e

    async def get_product(self, product_id: int):
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
                          ),

                          shops:shop_product (
                            available_stock,
                            price,
                            is_active,
                            is_available,
                            shop:shop_id (
                              id,
                              shop_name,
                              logo_url
                            )
                          )
        """).eq("id", product_id).single().execute()
        return response.data
      except Exception as e:
        print(f"Error fetching product: {e}")
        raise e

    async def update_product(self, product_id: int, payload):
      try:
        response = await self.client.from_("products").update(payload).eq("id", product_id).execute()
        if response.data:
          # This return without new images, so we need to fetch the product again to get the updated images
          product_response = await self.get_product(product_id)
          return product_response
        return None
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