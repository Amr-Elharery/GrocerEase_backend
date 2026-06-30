from fastapi import Depends
from app.modules.recommendations.infrastructure.recommendations_repository_supabase import (
    RecommendationsRepositorySupabase,
)


class RecommendationsService:
    def __init__(
        self,
        repository: RecommendationsRepositorySupabase = Depends(RecommendationsRepositorySupabase),
    ) -> None:
        self.repository = repository

    async def frequently_bought_together_global(self, product_id: int, limit: int):
        return await self.repository.frequently_bought_together_global(product_id, limit)

    async def frequently_bought_together_shop(self, shop_id: int, product_id: int, limit: int):
        return await self.repository.frequently_bought_together_shop(shop_id, product_id, limit)

    async def cart_completion_shop(self, shop_id: int, product_ids: list[int], limit: int):
        return await self.repository.cart_completion_shop(shop_id, product_ids, limit)

    async def replenishment(self, user_id: str, limit: int):
        return await self.repository.replenishment(user_id, limit)
