from pydantic import BaseModel, field_validator
from typing import Optional, List
from datetime import datetime
import re


class UpdateOrderStatusRequest(BaseModel):
    new_status: str


class CreateDeliveryProfileRequest(BaseModel):
    full_name: str
    phone_number: str
    vehicle_type: Optional[str] = None
    vehicle_plate_number: Optional[str] = None
    national_id: Optional[str] = None
    city: Optional[str] = None
    address: Optional[str] = None
    area_id: Optional[int] = None

    @field_validator("phone_number")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        if v is not None and not re.match(r"^\+[1-9]\d{7,14}$", v):
            raise ValueError("Phone must be in E.164 format (e.g. +201231255122)")
        return v


class UpdateAvailabilityRequest(BaseModel):
    is_available: bool


class UpdateLocationRequest(BaseModel):
    latitude: float
    longitude: float


class DeliveryProfileResponse(BaseModel):
    id: int
    user_id: str
    full_name: str
    phone_number: str
    vehicle_type: Optional[str] = None
    vehicle_plate_number: Optional[str] = None
    national_id: Optional[str] = None
    status: Optional[str] = None
    is_available: bool
    current_latitude: Optional[float] = None
    current_longitude: Optional[float] = None
    city: Optional[str] = None
    address: Optional[str] = None
    area_id: Optional[int] = None
    rating: Optional[float] = None
    total_deliveries: Optional[int] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class DeliveryResponse(BaseModel):
    id: int
    order_id: int
    delivery_id: int
    created_at: Optional[datetime] = None


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
    order_group_id: Optional[int] = None
    status: str
    subtotal: float
    delivery_fee: float
    payment_method: str
    created_at: datetime | None = None
    order_items: List[DeliveryOrderItemResponse] | None = None
    customer_address: Optional[DeliveryAddressResponse] = None
    shop: Optional[DeliveryShopResponse] = None


class DeliveryDetailResponse(BaseModel):
    id: int
    order_id: int
    delivery_id: int
    created_at: Optional[datetime] = None
    order: Optional[DeliveryOrderResponse] = None


class DeliveryGroupResponse(BaseModel):
    order_group_id: int
    deliveries: List[DeliveryDetailResponse]
