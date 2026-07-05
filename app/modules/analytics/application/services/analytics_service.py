from fastapi import Depends
import asyncio
from app.modules.analytics.infrastructure.analytics_repository_supabase import AnalyticsRepositorySupabase
from app.modules.analytics.domain.errors import ShopNotFoundError
from app.modules.shops.infrastructure.shops_repository_supabase import ShopsRepositorySupabase


class AnalyticsService:
    def __init__(
        self,
        repository: AnalyticsRepositorySupabase = Depends(AnalyticsRepositorySupabase),
        shops_repository: ShopsRepositorySupabase = Depends(ShopsRepositorySupabase),
    ) -> None:
        self.repository = repository
        self.shops_repository = shops_repository

    async def get_shop_dashboard(self, owner_id: str) -> dict:
        shop = await self.shops_repository.get_shop_by_owner(owner_id)
        if not shop:
            raise ShopNotFoundError()
        shop_id = shop["id"]

        daily_revenue, orders_by_status, best_selling, low_stock, customer_stats = await _gather(
            self.repository.get_shop_daily_revenue(shop_id),
            self.repository.get_shop_orders_by_status(shop_id),
            self.repository.get_shop_best_selling_products(shop_id),
            self.repository.get_shop_low_stock(shop_id),
            self.repository.get_shop_customer_stats(shop_id),
        )

        return {
            "daily_revenue": daily_revenue,
            "orders_by_status": orders_by_status,
            "best_selling_products": best_selling,
            "low_stock_products": low_stock,
            "customer_stats": customer_stats,
        }

    async def get_admin_dashboard(self, shops_by_area_limit: int = 10, shops_by_area_offset: int = 0) -> dict:
        platform_overview, orders_by_status, daily_orders, top_shops, top_products, orders_by_area, delivery_stats, shops_by_area = await _gather(
            self.repository.get_admin_platform_overview(),
            self.repository.get_admin_orders_by_status(),
            self.repository.get_admin_daily_orders(),
            self.repository.get_admin_top_shops(),
            self.repository.get_admin_top_products(),
            self.repository.get_admin_orders_by_area(),
            self.repository.get_admin_delivery_stats(),
            self.repository.get_admin_shops_by_area(shops_by_area_limit, shops_by_area_offset),
        )

        return {
            "platform_overview": platform_overview,
            "orders_by_status": orders_by_status,
            "daily_orders": daily_orders,
            "top_shops": top_shops,
            "top_products": top_products,
            "orders_by_area": orders_by_area,
            "delivery_stats": delivery_stats,
            "shops_by_area": {
                "items": shops_by_area["items"],
                "total": shops_by_area["total"],
                "limit": shops_by_area_limit,
                "offset": shops_by_area_offset,
            },
        }


async def _gather(*coros):
    return await asyncio.gather(*coros)
