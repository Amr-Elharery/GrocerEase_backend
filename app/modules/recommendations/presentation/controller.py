from fastapi import Depends
from app.modules.recommendations.application.services.recommendations_service import (
    RecommendationsService,
)


class RecommendationsController:
    def __init__(self, service: RecommendationsService = Depends(RecommendationsService)) -> None:
        self.service = service

    async def frequently_bought_together_global(self, product_id: int, limit: int):
        return await self.service.frequently_bought_together_global(product_id, limit)

    async def frequently_bought_together_shop(self, shop_id: int, product_id: int, limit: int):
        return await self.service.frequently_bought_together_shop(shop_id, product_id, limit)

    async def cart_completion_shop(self, shop_id: int, product_ids: list[int], limit: int):
        return await self.service.cart_completion_shop(shop_id, product_ids, limit)

    async def replenishment(self, user_id: str, limit: int):
        return await self.service.replenishment(user_id, limit)
