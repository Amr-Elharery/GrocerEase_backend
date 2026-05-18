from fastapi import Depends
from app.modules.products.application.services.products_service import ProductsService
from app.modules.products.presentation.schemas import (
    CreateProductRequest,
    UpdateProductRequest,
    ProductResponse,
    ProductListResponse,
)


class ProductsController:
    def __init__(self, service: ProductsService = Depends(ProductsService)) -> None:
        self.service = service

    async def get_all_products(self, limit: int = 10, offset: int = 0, search: str = None):
        try:
            return await self.service.get_all_products(limit, offset, search)
        except Exception as e:
            return e
    async def create_product(self, payload: CreateProductRequest) -> ProductResponse:
        try:
            return await self.service.create_product(payload)
        except Exception as e:
            return e

    async def get_product(self, product_id: str) -> ProductResponse:
        try:
            return await self.service.get_product(product_id)
        except Exception as e:
            return e

    async def update_product(self, product_id: str, payload: UpdateProductRequest) -> ProductResponse:
        pass

    async def delete_product(self, product_id: str) -> None:
        try:
            await self.service.delete_product(product_id)
        except Exception as e:
            return e