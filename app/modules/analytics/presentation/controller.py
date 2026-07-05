from fastapi import Depends
from app.modules.analytics.application.services.analytics_service import AnalyticsService


class AnalyticsController:
    def __init__(self, service: AnalyticsService = Depends(AnalyticsService)) -> None:
        self.service = service

    async def get_shop_dashboard(self, owner_id: str):
        try:
            return await self.service.get_shop_dashboard(owner_id)
        except Exception as e:
            raise e

    async def get_admin_dashboard(self, shops_by_area_limit: int = 10, shops_by_area_offset: int = 0):
        try:
            return await self.service.get_admin_dashboard(shops_by_area_limit, shops_by_area_offset)
        except Exception as e:
            raise e
