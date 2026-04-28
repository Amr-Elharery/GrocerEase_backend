from app.modules.products.application.services.products_service import ProductsService
from app.modules.products.presentation.schemas import (
    CategoryResponse,
    CreateCategoryRequest,
    CreateProductRequest,
    CreateShopProductRequest,
    CreateSubCategoryRequest,
    ShopProductItem,
    UpdateProductRequest,
    ProductResponse,
    ProductListResponse,
    UpdateShopProductRequest,
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
    
    async def create_category(self, payload:CreateCategoryRequest)->CategoryResponse:
        return await self.service.create_category(payload.category_name)
    
    async def get_all_categories(self)->list[CategoryResponse]:
        return await self.service.get_all_categories()

    async def create_subcategory(self,payload:CreateCategoryRequest,parent_id:int)->CategoryResponse:
        return await self.service.create_subcategory(payload.category_name,parent_id)
    
    async def delete_category(self,category_id)->None:
        return await self.service.delete_category(category_id)
    
    async def create_shop_product(self,shop_id:int,payload:CreateShopProductRequest)->ShopProductItem:
        return await self.service.create_shop_product(shop_id,payload)
    
    async def update_shop_product(self,shop_id:int,product_id,payload:UpdateShopProductRequest)->ShopProductItem:
        return await self.service.update_shop_product(shop_id,product_id,payload)