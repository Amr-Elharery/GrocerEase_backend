from app.modules.products.infrastructure.products_repository_supabase import ProductsRepositorySupabase
from app.core.ports import ImageStorage
from app.modules.products.infrastructure.storage_supabase import SupabaseImageStorage
from fastapi import Depends, UploadFile
from typing import List


class ProductsService:
    def __init__(self, repository: ProductsRepositorySupabase = Depends(ProductsRepositorySupabase), storage: ImageStorage = Depends(SupabaseImageStorage)) -> None:
        self.repository = repository
        self.storage = storage

    async def get_all_products(self, limit: int = 10, offset: int = 0, search: str = None):
        try:
            return await self.repository.get_all_products(limit, offset, search)
        except Exception as e:
            raise e

    async def get_products_by_area(self, area_id: int, limit: int = 10, offset: int = 0, search: str = None):
        try:
            return await self.repository.get_products_by_area(area_id, limit, offset, search)
        except Exception as e:
            raise e

    async def create_product(self, payload, files: List[UploadFile] = None):
        try:
            created = await self.repository.create_product(payload.dict())

            product = created[0]

            # if file and product created, save image and create product_img record
            if files and product and product.get("id"):
                images = []
                for f in files:
                    img = await self.create_product_image(product["id"], f)
                    images.append(img)
                # mark the first image as primary if none already
                if images:
                    images[0][0]["is_primary"] = True
                product["images"] = images

            return product
        except Exception as e:
            raise e

    async def create_product_image(self, product_id: str, file: UploadFile, variant: str = None, is_primary: bool = False):
        try:
            image_url = await self.storage.save(file)
            img = await self.repository.create_product_image(product_id, image_url, variant, is_primary)
            return img
        except Exception as e:
            raise e

    async def delete_product_image(self, product_id: int, image_id: int):
        try:
            image = await self.repository.get_product_image(image_id)
            if not image or image["product_id"] != product_id:
                raise Exception(f"Image with id {image_id} does not exist for product {product_id}")

            image_path = image["image_url"]

            if image["is_primary"]:
                other_images = await self.repository.list_product_images(product_id, exclude_image_id=image_id)
                if other_images and len(other_images) > 0:
                    await self.repository.set_product_image_primary(other_images[0]["id"])

            await self.repository.delete_product_image_row(image_id)
            await self.storage.delete(image_path)
        except Exception as e:
            raise e

    async def make_primary_image(self, product_id: str, image_id: int):
        try:
            image = await self.repository.get_product_image(image_id)
            if not image or image["product_id"] != product_id:
                raise Exception(f"Image with id {image_id} does not exist for product {product_id}")

            await self.repository.set_all_product_images_non_primary(product_id)
            await self.repository.set_product_image_primary(image_id)
        except Exception as e:
            raise e

    async def get_product(self, product_id: str):
        try:
            return await self.repository.get_product(product_id)
        except Exception as e:
            raise e

    async def update_product(self, product_id: int, payload, files: List[UploadFile] = None):
        try:
            product = await self.repository.update_product(product_id, payload.dict())
            if files and product and product.get("id"):
                images = []
                for f in files:
                    img = await self.create_product_image(product["id"], f)
                    images.append(img)
                # mark the first image as primary if none already
                if images:
                    images[0][0]["is_primary"] = True
                product["images"] = images
            return product
        except Exception as e:
            raise e

    async def delete_product(self, product_id: str):
        try:
            return await self.repository.delete_product(product_id)
        except Exception as e:
            raise e
