from fastapi import Depends
from app.modules.orders.application.services.orders_service import OrdersService
from app.modules.orders.presentation.schemas import CreateOrderRequest, CreateOptimizationOrderRequest, OrderResponse, OrderGroupResponse


class OrdersController:
    def __init__(self, service: OrdersService = Depends(OrdersService)) -> None:
        self.service = service

    async def get_all_orders(self, customer_id: str, limit: int = 10, offset: int = 0):
        try:
            return await self.service.get_all_orders(customer_id, limit, offset)
        except Exception as e:
            raise e

    async def get_order(self, order_id: int, customer_id: str) -> OrderResponse:
        try:
            return await self.service.get_order(order_id, customer_id)
        except Exception as e:
            raise e

    async def create_order(self, payload: CreateOrderRequest, customer_id: str) -> OrderResponse:
        try:
            return await self.service.create_order(payload, customer_id)
        except Exception as e:
            raise e

    async def create_optimization_order(self, payload: CreateOptimizationOrderRequest, customer_id: str) -> OrderGroupResponse:
        try:
            return await self.service.create_optimization_order(payload, customer_id)
        except Exception as e:
            raise e

    async def cancel_order(self, order_id: int, customer_id: str) -> OrderResponse:
        try:
            return await self.service.cancel_order(order_id, customer_id)
        except Exception as e:
            raise e

    async def update_order_status(self, order_id: int, new_status: str) -> OrderResponse:
        try:
            return await self.service.update_order_status(order_id, new_status)
        except Exception as e:
            raise e

    async def get_order_group(self, order_group_id: int, customer_id: str) -> OrderGroupResponse:
        try:
            return await self.service.get_order_group(order_group_id, customer_id)
        except Exception as e:
            raise e
