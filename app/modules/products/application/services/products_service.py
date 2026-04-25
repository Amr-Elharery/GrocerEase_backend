from supabase import AsyncClient

from app.modules.products.domain.errors import ProductNotFoundError
from app.modules.products.presentation.schemas import (
    CreateProductRequest,
    UpdateProductRequest,
    ProductResponse,
    ProductListResponse,
)


class ProductsService:
    def __init__(self, admin_client: AsyncClient) -> None:
        self.client = admin_client

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
