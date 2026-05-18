from app.modules.products.infrastructure.products_repository_supabase import ProductsRepositorySupabase
from fastapi import Depends
class ProductsService:
    def __init__(self, repository: ProductsRepositorySupabase = Depends(ProductsRepositorySupabase)) -> None:
        self.repository = repository

    async def get_all_products(self, limit: int = 10, offset: int = 0, search: str = None):
        try:
            return await self.repository.get_all_products(limit, offset, search)
        except Exception as e:
            return e
    async def create_product(self, payload):
        try:
            return await self.repository.create_product(payload)
        except Exception as e:
            return e

    async def get_product(self, product_id: str):
        try:
            return await self.repository.get_product(product_id)
        except Exception as e:
            return e

    async def update_product(self, product_id: str, payload):
        pass

    async def delete_product(self, product_id: str):
        try:
            return await self.repository.delete_product(product_id)
        except Exception as e:
            return e
