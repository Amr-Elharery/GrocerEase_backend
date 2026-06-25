from fastapi import Depends, UploadFile
from app.modules.shops.application.services.shops_service import ShopsService
from app.modules.shops.presentation.schemas import CreateShopRequest, UpdateShopRequest, ShopResponse


class ShopsController:
    def __init__(self, service: ShopsService = Depends(ShopsService)) -> None:
        self.service = service

    async def get_all_shops(self, limit: int = 10, offset: int = 0, search: str = None, area_id: int = None):
        try:
            return await self.service.get_all_shops(limit, offset, search, area_id)
        except Exception as e:
            raise e

    async def get_shop(self, shop_id: int) -> ShopResponse:
        try:
            return await self.service.get_shop(shop_id)
        except Exception as e:
            raise e

    async def get_my_shop(self, owner_id: str) -> ShopResponse:
        try:
            return await self.service.get_my_shop(owner_id)
        except Exception as e:
            raise e

    async def create_shop(self, payload: CreateShopRequest, owner_id: str, logo: UploadFile = None) -> ShopResponse:
        try:
            return await self.service.create_shop(payload, owner_id, logo)
        except Exception as e:
            raise e

    async def update_shop(self, shop_id: int, payload: UpdateShopRequest, requester_id: str, logo: UploadFile = None) -> ShopResponse:
        try:
            return await self.service.update_shop(shop_id, payload, requester_id, logo)
        except Exception as e:
            raise e

    async def delete_shop(self, shop_id: int, requester_id: str) -> None:
        try:
            await self.service.delete_shop(shop_id, requester_id)
        except Exception as e:
            raise e
