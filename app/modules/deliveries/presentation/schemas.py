from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class AssignDeliveryRequest(BaseModel):
    order_id: int
    delivery_user_id: str


class UpdateOrderStatusRequest(BaseModel):
    new_status: str


class DeliveryAssignmentResponse(BaseModel):
    id: int
    order_id: int
    delivery_user_id: str
    assigned_at: datetime | None = None


class AreaSummary(BaseModel):
    id: int
    area_name: str
    city_name: str


class DeliveryAddressResponse(BaseModel):
    id: int
    street: str
    building: str
    floor: str
    apt_number: str
    latitude: float
    longitude: float
    additional_directions: Optional[str] = None
    label: str
    area: Optional[AreaSummary] = None


class DeliveryShopResponse(BaseModel):
    id: int
    shop_name: str
    address: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    phone_number: str | None = None


class DeliveryOrderItemResponse(BaseModel):
    id: int
    shop_product_id: int
    quantity: float
    total: float


class DeliveryOrderResponse(BaseModel):
    id: int
    customer_id: str
    shop_id: int
    status: str
    subtotal: float
    delivery_fee: float
    payment_method: str
    created_at: datetime | None = None
    order_items: List[DeliveryOrderItemResponse] | None = None
    customer_address: Optional[DeliveryAddressResponse] = None
    shop: Optional[DeliveryShopResponse] = None


class DeliveryAssignmentDetailResponse(BaseModel):
    id: int
    order_id: int
    delivery_user_id: str
    assigned_at: datetime | None = None
    order: Optional[DeliveryOrderResponse] = None
