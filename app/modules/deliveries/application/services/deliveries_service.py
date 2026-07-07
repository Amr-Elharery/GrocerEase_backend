from fastapi import Depends

from app.modules.auth.infrastructure.auth_repository_supabase import AuthRepositorySupabase
from app.modules.deliveries.domain.errors import (
    DeliveryNotFoundError,
    DeliveryProfileAlreadyExistsError,
    DeliveryProfileNotFoundError,
    NotAssignedToOrderError,
    OrderAlreadyAssignedError,
    OrderGroupAlreadyAssignedError,
    OrderGroupNotFoundError,
)
from app.core.exceptions import AppException
from fastapi import status
from app.modules.deliveries.infrastructure.deliveries_repository_supabase import DeliveriesRepositorySupabase
from app.modules.deliveries.infrastructure.delivery_profiles_repository_supabase import DeliveryProfilesRepositorySupabase
from app.modules.notifications.application.services.notifications_service import NotificationsService
from app.modules.orders.application.services.orders_service import OrdersService

ACTIVE_ORDER_STATUSES = ["pending"]
ALLOWED_STATUS_TRANSITIONS = ["on_the_way", "delivered"]


class DeliveriesService:
    def __init__(
        self,
        repository: DeliveriesRepositorySupabase = Depends(DeliveriesRepositorySupabase),
        profiles_repository: DeliveryProfilesRepositorySupabase = Depends(DeliveryProfilesRepositorySupabase),
        orders_service: OrdersService = Depends(OrdersService),
        notifications_service: NotificationsService = Depends(NotificationsService),
        auth_repository: AuthRepositorySupabase = Depends(AuthRepositorySupabase),
    ) -> None:
        self.repository = repository
        self.profiles_repository = profiles_repository
        self.orders_service = orders_service
        self.notifications_service = notifications_service
        self.auth_repository = auth_repository


    async def create_profile(self, payload, user_id: str):
        existing = await self.profiles_repository.get_profile_by_user(user_id)
        if existing:
            raise DeliveryProfileAlreadyExistsError()
        data = payload.dict()
        data["user_id"] = user_id
        return await self.profiles_repository.create_profile(data)

    async def get_my_profile(self, user_id: str):
        profile = await self.profiles_repository.get_profile_by_user(user_id)
        if not profile:
            raise DeliveryProfileNotFoundError()
        return profile

    async def update_availability(self, user_id: str, is_available: bool):
        profile = await self._get_profile_or_raise(user_id)
        return await self.profiles_repository.update_profile(profile["id"], {"is_available": is_available})

    async def update_location(self, user_id: str, latitude: float, longitude: float):
        profile = await self._get_profile_or_raise(user_id)
        return await self.profiles_repository.update_profile(
            profile["id"], {"current_latitude": latitude, "current_longitude": longitude}
        )

    async def _get_profile_or_raise(self, user_id: str):
        profile = await self.profiles_repository.get_profile_by_user(user_id)
        if not profile:
            raise DeliveryProfileNotFoundError()
        return profile


    async def get_available_orders(self, user_id: str, limit: int = 10, offset: int = 0):
        profile = await self._get_profile_or_raise(user_id)
        driver_area_id = profile.get("area_id")

        all_orders = await self.orders_service.repository.get_available_orders_for_delivery(limit, offset)

        unassigned = []
        for order in all_orders:
            if driver_area_id is not None:
                address = order.get("customer_address") or {}
                area = address.get("area") or {}
                if area.get("id") != driver_area_id:
                    continue
            delivery = await self.repository.get_delivery_by_order(order["id"])
            if not delivery:
                unassigned.append(_format_order_for_delivery(order))

        singles = []
        groups: dict[int, list] = {}
        for order in unassigned:
            group_id = order.get("order_group_id")
            if group_id:
                groups.setdefault(group_id, []).append(order)
            else:
                singles.append({"type": "single", "order": order})

        group_jobs = [
            {"type": "group", "order_group_id": group_id, "orders": orders}
            for group_id, orders in groups.items()
        ]

        return singles + group_jobs


    async def accept_order(self, order_id: int, user_id: str):
        profile = await self._get_profile_or_raise(user_id)

        order = await self.orders_service.repository.get_order(order_id)
        if not order:
            raise AppException("Order not found", status.HTTP_404_NOT_FOUND)

        if order.get("status") not in ACTIVE_ORDER_STATUSES:
            raise AppException("This order is not available for delivery", status.HTTP_400_BAD_REQUEST)

        existing = await self.repository.get_delivery_by_order(order_id)
        if existing:
            raise OrderAlreadyAssignedError()

        delivery = await self.repository.create_delivery(order_id, profile["id"])
        await self.orders_service.repository.update_order_status(order_id, "out_for_delivery")
        return delivery


    async def accept_group(self, order_group_id: int, user_id: str):
        profile = await self._get_profile_or_raise(user_id)

        group = await self.orders_service.repository.get_order_group(order_group_id)
        if not group:
            raise OrderGroupNotFoundError()

        orders = group.get("orders") or []
        if not orders:
            raise OrderGroupNotFoundError()

        order_ids = [o["id"] for o in orders]
        for order in orders:
            if order.get("status") not in ACTIVE_ORDER_STATUSES:
                raise AppException("This order group is not available for delivery", status.HTTP_400_BAD_REQUEST)

        existing_deliveries = await self.repository.get_deliveries_by_orders(order_ids)
        if existing_deliveries:
            raise OrderGroupAlreadyAssignedError()

        deliveries = await self.repository.create_deliveries_bulk(order_ids, profile["id"])
        for order_id in order_ids:
            await self.orders_service.repository.update_order_status(order_id, "out_for_delivery")

        return {"order_group_id": order_group_id, "deliveries": deliveries}


    async def get_my_deliveries(self, user_id: str):
        profile = await self._get_profile_or_raise(user_id)
        deliveries = await self.repository.get_my_deliveries(profile["id"])

        result = []
        for delivery in deliveries:
            order = await self.orders_service.repository.get_order_for_delivery(delivery["order_id"])
            result.append({
                "id": delivery["id"],
                "order_id": delivery["order_id"],
                "delivery_id": delivery["delivery_id"],
                "created_at": delivery.get("created_at"),
                "order": order,
            })
        return result


    async def update_order_status(self, order_id: int, new_status: str, user_id: str):
        profile = await self._get_profile_or_raise(user_id)

        delivery = await self.repository.get_delivery_by_order(order_id)
        if not delivery:
            raise DeliveryNotFoundError()
        if delivery.get("delivery_id") != profile["id"]:
            raise NotAssignedToOrderError()

        if new_status not in ALLOWED_STATUS_TRANSITIONS:
            raise AppException(
                f"Status must be one of: {', '.join(ALLOWED_STATUS_TRANSITIONS)}", status.HTTP_400_BAD_REQUEST
            )

        updated_order = await self.orders_service.repository.update_order_status(order_id, new_status)
        if new_status == "delivered":
            await self.profiles_repository.increment_total_deliveries(profile["id"])
        return updated_order

    async def update_group_status(self, order_group_id: int, new_status: str, user_id: str):
        profile = await self._get_profile_or_raise(user_id)

        group = await self.orders_service.repository.get_order_group(order_group_id)
        if not group:
            raise OrderGroupNotFoundError()

        orders = group.get("orders") or []
        if not orders:
            raise OrderGroupNotFoundError()

        if new_status not in ALLOWED_STATUS_TRANSITIONS:
            raise AppException(
                f"Status must be one of: {', '.join(ALLOWED_STATUS_TRANSITIONS)}", status.HTTP_400_BAD_REQUEST
            )

        updated_orders = []
        for order in orders:
            delivery = await self.repository.get_delivery_by_order(order["id"])
            if not delivery or delivery.get("delivery_id") != profile["id"]:
                raise NotAssignedToOrderError()

        for order in orders:
            updated = await self.orders_service.repository.update_order_status(order["id"], new_status)
            updated_orders.append(updated)

        if new_status == "delivered":
            await self.profiles_repository.increment_total_deliveries(profile["id"])

        return updated_orders


    async def unassign_delivery(self, delivery_id: int):
        delivery = await self.repository.get_delivery(delivery_id)
        if not delivery:
            raise DeliveryNotFoundError()
        await self.repository.delete_delivery(delivery_id)


    async def notify_delivery_users(self, order_id: int):
        delivery_user_ids = await self.auth_repository.get_users_by_role("delivery")
        for user_id in delivery_user_ids:
            try:
                await self.notifications_service.send_to_user(
                    user_id=user_id,
                    title="New Order Available",
                    body="A new order is available for pickup. Open the app to accept it.",
                    data={"order_id": order_id},
                )
            except Exception:
                pass


def _format_order_for_delivery(order: dict) -> dict:
    for item in order.get("order_items") or []:
        shop_product = item.pop("shop_product", None) or {}
        product = shop_product.get("product") or {}
        item["product_name"] = product.get("product_name")
        if item.get("total") is not None:
            item["total"] = round(item["total"], 2)

    if order.get("subtotal") is not None:
        order["subtotal"] = round(order["subtotal"], 2)
    if order.get("delivery_fee") is not None:
        order["delivery_fee"] = round(order["delivery_fee"], 2)

    return order
