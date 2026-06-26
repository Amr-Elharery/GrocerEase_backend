from fastapi import Depends, HTTPException, status
from app.modules.shop_products.infrastructure.shop_products_repository_supabase import ShopProductsRepositorySupabase
from app.modules.shops.infrastructure.shops_repository_supabase import ShopsRepositorySupabase


class ShopProductsService:
    def __init__(
        self,
        repository: ShopProductsRepositorySupabase = Depends(ShopProductsRepositorySupabase),
        shops_repository: ShopsRepositorySupabase = Depends(ShopsRepositorySupabase),
    ) -> None:
        self.repository = repository
        self.shops_repository = shops_repository

    async def get_all_shop_products(self, shop_id: int, limit: int = 10, offset: int = 0):
        try:
            return await self.repository.get_all_shop_products(shop_id, limit, offset)
        except Exception as e:
            raise e

    async def get_shop_product(self, shop_product_id: int):
        try:
            shop_product = await self.repository.get_shop_product(shop_product_id)
            if not shop_product:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shop product not found")
            return shop_product
        except Exception as e:
            raise e

    async def create_shop_product(self, payload, requester_id: str):
        try:
            shop = await self.shops_repository.get_shop(payload.shop_id)
            if not shop:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shop not found")
            if shop.get("owner_id") != requester_id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the owner of this shop")

            existing = await self.repository.get_by_shop_and_product(payload.shop_id, payload.product_id)
            if existing:
                if existing.get("is_active"):
                    raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="This product is already added to your shop")
                return await self.repository.update_shop_product(existing["id"], {"is_active": True, "price": payload.price, "available_stock": payload.available_stock})

            return await self.repository.create_shop_product(payload.dict())
        except Exception as e:
            raise e

    async def update_shop_product(self, shop_product_id: int, payload, requester_id: str):
        try:
            shop_product = await self.repository.get_shop_product(shop_product_id)
            if not shop_product:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shop product not found")

            shop = await self.shops_repository.get_shop(shop_product.get("shop_id"))
            if shop.get("owner_id") != requester_id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the owner of this shop")

            data = {k: v for k, v in payload.dict().items() if v is not None}
            return await self.repository.update_shop_product(shop_product_id, data)
        except Exception as e:
            raise e

    async def delete_shop_product(self, shop_product_id: int, requester_id: str):
        try:
            shop_product = await self.repository.get_shop_product(shop_product_id)
            if not shop_product:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shop product not found")

            shop = await self.shops_repository.get_shop(shop_product.get("shop_id"))
            if shop.get("owner_id") != requester_id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the owner of this shop")

            return await self.repository.delete_shop_product(shop_product_id)
        except Exception as e:
            raise e
