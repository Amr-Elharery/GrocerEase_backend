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

    async def get_product_image_path(self, image_id: int) -> str:
      try:
        response = await self.client.from_("product_images").select("image_url").eq("id", image_id).single().execute()
        if response.data and response.data["image_url"]:
          return response.data["image_url"]
        else:
          raise Exception(f"No image found with id: {image_id}")
      except Exception as e:
        print(f"Error fetching product image path: {e}")
        raise e

    async def delete_product_image(self, product_id: str, image_id: int):
      try:
        img = await self.client.from_("product_images").select("is_primary, product_id").eq("id", image_id).eq("product_id", product_id).single().execute()
        if img.data and img.data["is_primary"]:
          # If the image being deleted is primary, we should set another image as primary if it exists
          other_images = await self.client.from_("product_images").select("id").eq("product_id", img.data["product_id"]).neq("id", image_id).execute()
          if other_images.data and len(other_images.data) > 0:
            await self.client.from_("product_images").update({"is_primary": True}).eq("id", other_images.data[0]["id"]).execute()

        response = await self.client.from_("product_images").delete().eq("id", image_id).execute()
        return response.data
      except Exception as e:
        print(f"Error deleting product image: {e}")
        raise e

    async def make_primary_image(self, product_id: str, image_id: int):
      try:
        # Check imaege exists and belongs to product
        img = await self.client.from_("product_images").select("id").eq("id", image_id).eq("product_id", product_id).single().execute()
        if not img.data:
          raise Exception(f"Image with id {image_id} does not exist for product {product_id}")
        # First, set all images for the product to is_primary = False
        await self.client.from_("product_images").update({"is_primary": False}).eq("product_id", product_id).execute()
        # Then, set the specified image to is_primary = True
        response = await self.client.from_("product_images").update({"is_primary": True}).eq("id", image_id).execute()
        return response.data
      except Exception as e:
        print(f"Error making image primary: {e}")
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