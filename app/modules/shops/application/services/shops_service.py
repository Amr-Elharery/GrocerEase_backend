from fastapi import Depends, UploadFile, HTTPException, status
from app.modules.shops.infrastructure.shops_repository_supabase import ShopsRepositorySupabase
from app.modules.shops.infrastructure.storage_supabase import SupabaseImageStorage
from app.core.ports import ImageStorage


class ShopsService:
    def __init__(
        self,
        repository: ShopsRepositorySupabase = Depends(ShopsRepositorySupabase),
        storage: ImageStorage = Depends(SupabaseImageStorage),
    ) -> None:
        self.repository = repository
        self.storage = storage

    async def get_all_shops(self, limit: int = 10, offset: int = 0, search: str = None, area_id: int = None):
        try:
            return await self.repository.get_all_shops(limit, offset, search, area_id)
        except Exception as e:
            raise e

    async def get_shop(self, shop_id: int):
        try:
            return await self.repository.get_shop(shop_id)
        except Exception as e:
            raise e

    async def get_my_shop(self, owner_id: str):
        try:
            return await self.repository.get_shop_by_owner(owner_id)
        except Exception as e:
            raise e

    async def create_shop(self, payload, owner_id: str, logo: UploadFile = None):
        try:
            existing = await self.repository.get_shop_by_owner(owner_id)
            if existing:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="You already have a shop")
            data = payload.dict()
            data["owner_id"] = owner_id
            if logo:
                logo_url = await self.storage.save(logo)
                data["logo_url"] = logo_url
            created = await self.repository.create_shop(data)
            return created[0] if created else None
        except Exception as e:
            raise e

    async def update_shop(self, shop_id: int, payload, requester_id: str, logo: UploadFile = None):
        try:
            shop = await self.repository.get_shop(shop_id)
            if not shop:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shop not found")
            if not shop.get("is_active"):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot update a deleted shop")
            if shop.get("owner_id") != requester_id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the owner of this shop")
            data = {k: v for k, v in payload.dict().items() if v is not None}
            if logo:
                logo_url = await self.storage.save(logo)
                data["logo_url"] = logo_url
            return await self.repository.update_shop(shop_id, data)
        except Exception as e:
            raise e

    async def delete_shop(self, shop_id: int, requester_id: str):
        try:
            shop = await self.repository.get_shop(shop_id)
            if not shop:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shop not found")
            if shop.get("owner_id") != requester_id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the owner of this shop")
            return await self.repository.delete_shop(shop_id)
        except Exception as e:
            raise e
