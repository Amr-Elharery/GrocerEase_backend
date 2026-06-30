from fastapi import Depends

from app.modules.deliveries.application.services.deliveries_service import DeliveriesService
from app.modules.deliveries.presentation.schemas import UpdateOrderStatusRequest


class DeliveriesController:
    def __init__(self, service: DeliveriesService = Depends(DeliveriesService)) -> None:
        self.service = service

    async def get_available_orders(self, limit: int = 10, offset: int = 0):
        try:
            return await self.service.get_available_orders(limit, offset)
        except Exception as e:
            raise e

    async def accept_order(self, order_id: int, delivery_user_id: str):
        try:
            return await self.service.accept_order(order_id, delivery_user_id)
        except Exception as e:
            raise e

    async def get_my_assignments(self, delivery_user_id: str):
        try:
            return await self.service.get_my_assignments(delivery_user_id)
        except Exception as e:
            raise e

    async def update_order_status(self, order_id: int, payload: UpdateOrderStatusRequest, delivery_user_id: str):
        try:
            return await self.service.update_order_status(order_id, payload.new_status, delivery_user_id)
        except Exception as e:
            raise e

    async def unassign_delivery(self, assignment_id: int):
        try:
            await self.service.unassign_delivery(assignment_id)
        except Exception as e:
            raise e
