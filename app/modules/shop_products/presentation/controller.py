from fastapi import Depends
from app.modules.shop_products.application.services.shop_products_service import ShopProductsService
from app.modules.shop_products.presentation.schemas import CreateShopProductRequest, UpdateShopProductRequest, ShopProductResponse


class ShopProductsController:
    def __init__(self, service: ShopProductsService = Depends(ShopProductsService)) -> None:
        self.service = service

    async def get_all_shop_products(self, shop_id: int, limit: int = 10, offset: int = 0):
        try:
            return await self.service.get_all_shop_products(shop_id, limit, offset)
        except Exception as e:
            raise e

    async def get_shop_product(self, shop_product_id: int) -> ShopProductResponse:
        try:
            return await self.service.get_shop_product(shop_product_id)
        except Exception as e:
            raise e

    async def create_shop_product(self, payload: CreateShopProductRequest, requester_id: str) -> ShopProductResponse:
        try:
            return await self.service.create_shop_product(payload, requester_id)
        except Exception as e:
            raise e

    async def update_shop_product(self, shop_product_id: int, payload: UpdateShopProductRequest, requester_id: str) -> ShopProductResponse:
        try:
            return await self.service.update_shop_product(shop_product_id, payload, requester_id)
        except Exception as e:
            raise e

    async def delete_shop_product(self, shop_product_id: int, requester_id: str) -> None:
        try:
            await self.service.delete_shop_product(shop_product_id, requester_id)
        except Exception as e:
            raise e
