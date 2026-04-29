from supabase import AsyncClient
from app.modules.products.domain.errors import ProductNotFoundError
from app.modules.products.infrastructure.repository_supabase import SupabaseProductRepository
from app.modules.products.presentation.schemas import (
    CreateProductRequest,
    UpdateProductRequest,
    ProductResponse,
    ProductListResponse,
)

class ProductsService:
    def __init__(self, admin_client: AsyncClient) -> None:
        self.repository = SupabaseProductRepository(admin_client)

    async def create_product(self, payload: CreateProductRequest) -> ProductResponse:
        product_data = await self.repository.create(payload.model_dump())
        return ProductResponse(**product_data)

    async def get_product(self, product_id: str) -> ProductResponse:
        product_data = await self.repository.get_by_id(product_id)
        if not product_data:
            raise ProductNotFoundError()
        return ProductResponse(**product_data)

    async def get_all_products(self) -> ProductListResponse:
        products_data = await self.repository.get_all()
        return ProductListResponse(
            products=[ProductResponse(**p) for p in products_data]
        )

    async def update_product(self, product_id: str, payload: UpdateProductRequest) -> ProductResponse:
        # exclude_unset=True ensures we only send fields provided in the request
        product_data = await self.repository.update(product_id, payload.model_dump(exclude_unset=True))
        if not product_data:
            raise ProductNotFoundError()
        return ProductResponse(**product_data)

    async def delete_product(self, product_id: str) -> None:
        success = await self.repository.delete(product_id)
        if not success:
            raise ProductNotFoundError()