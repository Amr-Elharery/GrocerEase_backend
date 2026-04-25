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
        pass

    async def get_product(self, product_id: str) -> ProductResponse:
        pass

    async def get_all_products(self) -> ProductListResponse:
        pass

    async def update_product(self, product_id: str, payload: UpdateProductRequest) -> ProductResponse:
        pass

    async def delete_product(self, product_id: str) -> None:
        pass
