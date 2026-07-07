from pydantic import BaseModel
from typing import List, Optional
from datetime import date


class DailyRevenueResponse(BaseModel):
    day: date
    total_orders: int
    revenue: float


class OrdersByStatusResponse(BaseModel):
    status: str
    total: int


class BestSellingProductResponse(BaseModel):
    shop_product_id: int
    product_name: str
    total_sold: int
    total_revenue: float


class LowStockProductResponse(BaseModel):
    shop_product_id: int
    product_name: str
    available_stock: int
    low_stock_threshold: int
    is_available: bool


class ShopCustomerStatsResponse(BaseModel):
    unique_customers: int = 0
    repeat_customers: int = 0


class ShopDashboardResponse(BaseModel):
    daily_revenue: List[DailyRevenueResponse]
    orders_by_status: List[OrdersByStatusResponse]
    best_selling_products: List[BestSellingProductResponse]
    low_stock_products: List[LowStockProductResponse]
    customer_stats: ShopCustomerStatsResponse


class PlatformOverviewResponse(BaseModel):
    total_orders: int = 0
    total_revenue: float = 0.0
    orders_this_month: int = 0
    revenue_this_month: float = 0.0


class DailyOrdersResponse(BaseModel):
    day: date
    total_orders: int
    revenue: float


class TopShopResponse(BaseModel):
    shop_id: int
    shop_name: str
    total_orders: int
    total_revenue: float


class TopProductResponse(BaseModel):
    product_id: int
    product_name: str
    total_sold: int
    total_revenue: float


class AreaOrdersResponse(BaseModel):
    area_id: int
    area_name: str
    city_name: str
    total_orders: int
    total_revenue: float


class DeliveryStatsResponse(BaseModel):
    active_drivers: int = 0
    total_deliveries: int = 0
    avg_orders_per_driver: float = 0.0


class AreaShopsResponse(BaseModel):
    area_id: int
    area_name: str
    city_name: str
    total_shops: int
    active_shops: int


class PaginatedAreaShopsResponse(BaseModel):
    items: List[AreaShopsResponse]
    total: int
    limit: int
    offset: int


class AdminDashboardResponse(BaseModel):
    platform_overview: PlatformOverviewResponse
    orders_by_status: List[OrdersByStatusResponse]
    daily_orders: List[DailyOrdersResponse]
    top_shops: List[TopShopResponse]
    top_products: List[TopProductResponse]
    orders_by_area: List[AreaOrdersResponse]
    delivery_stats: DeliveryStatsResponse
    shops_by_area: PaginatedAreaShopsResponse
