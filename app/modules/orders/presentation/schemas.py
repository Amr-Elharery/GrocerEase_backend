from pydantic import BaseModel
from typing import List
from datetime import datetime


class OrderItemRequest(BaseModel):
    shop_product_id: int
    quantity: int


class CreateOrderRequest(BaseModel):
    shop_id: int
    customer_address_id: int
    payment_method: str
    items: List[OrderItemRequest]


class CreateOptimizationOrderRequest(BaseModel):
    customer_address_id: int
    payment_method: str
    orders: List[CreateOrderRequest]


class OrderItemResponse(BaseModel):
    id: int
    shop_product_id: int
    quantity: float
    total: float

class CustomerResponse(BaseModel):
    full_name: str

class OrderResponse(BaseModel):
    id: int
    customer_name: CustomerResponse
    shop_id: int
    order_group_id: int | None = None
    status: str
    subtotal: float
    delivery_fee: float
    payment_method: str
    created_at: datetime | None = None
    customer_address_id: int
    order_items: List[OrderItemResponse] | None = None

class OrderResponseWithCustomerId(BaseModel):
    id: int
    customer_id: str
    shop_id: int
    order_group_id: int | None = None
    status: str
    subtotal: float
    delivery_fee: float
    payment_method: str
    created_at: datetime | None = None
    customer_address_id: int
    order_items: List[OrderItemResponse] | None = None

class OrderGroupResponse(BaseModel):
    id: int
    customer_id: str
    created_at: datetime | None = None
    orders: List[OrderResponseWithCustomerId] | None = None
