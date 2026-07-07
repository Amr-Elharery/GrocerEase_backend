from fastapi import Depends

from app.modules.deliveries.application.services.deliveries_service import DeliveriesService
from app.modules.deliveries.presentation.schemas import (
    CreateDeliveryProfileRequest,
    UpdateAvailabilityRequest,
    UpdateLocationRequest,
    UpdateOrderStatusRequest,
)


class DeliveriesController:
    def __init__(self, service: DeliveriesService = Depends(DeliveriesService)) -> None:
        self.service = service

    # ---------- Profile ----------

    async def create_profile(self, payload: CreateDeliveryProfileRequest, user_id: str):
        return await self.service.create_profile(payload, user_id)

    async def get_my_profile(self, user_id: str):
        return await self.service.get_my_profile(user_id)

    async def update_availability(self, payload: UpdateAvailabilityRequest, user_id: str):
        return await self.service.update_availability(user_id, payload.is_available)

    async def update_location(self, payload: UpdateLocationRequest, user_id: str):
        return await self.service.update_location(user_id, payload.latitude, payload.longitude)

    # ---------- Jobs ----------

    async def get_available_orders(self, user_id: str, limit: int = 10, offset: int = 0):
        return await self.service.get_available_orders(user_id, limit, offset)

    async def accept_order(self, order_id: int, user_id: str):
        return await self.service.accept_order(order_id, user_id)

    async def accept_group(self, order_group_id: int, user_id: str):
        return await self.service.accept_group(order_group_id, user_id)

    async def get_my_deliveries(self, user_id: str):
        return await self.service.get_my_deliveries(user_id)

    async def update_order_status(self, order_id: int, payload: UpdateOrderStatusRequest, user_id: str):
        return await self.service.update_order_status(order_id, payload.new_status, user_id)

    async def update_group_status(self, order_group_id: int, payload: UpdateOrderStatusRequest, user_id: str):
        return await self.service.update_group_status(order_group_id, payload.new_status, user_id)

    # ---------- Admin ----------

    async def unassign_delivery(self, delivery_id: int):
        await self.service.unassign_delivery(delivery_id)
