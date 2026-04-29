from app.modules.products.application.services.products_service import ProductsService
from app.modules.products.presentation.schemas import (
    CreateProductRequest,
    UpdateProductRequest,
    ProductResponse,
    ProductListResponse,
)

class ProductsController:
    def __init__(self, service: ProductsService) -> None:
        self.service = service

    async def create_product(self, payload: CreateProductRequest) -> ProductResponse:
        return await self.service.create_product(payload)

    async def get_product(self, product_id: str) -> ProductResponse:
        return await self.service.get_product(product_id)

    async def get_all_products(self) -> ProductListResponse:
        return await self.service.get_all_products()

    async def update_product(self, product_id: str, payload: UpdateProductRequest) -> ProductResponse:
        return await self.service.update_product(product_id, payload)

    async def delete_product(self, product_id: str) -> None:
        await self.service.delete_product(product_id)