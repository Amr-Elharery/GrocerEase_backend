from fastapi import Depends, HTTPException, status

from app.modules.auth.infrastructure.auth_repository_supabase import AuthRepositorySupabase
from app.modules.deliveries.domain.errors import DeliveryAssignmentNotFoundError, NotAssignedToOrderError, OrderAlreadyAssignedError
from app.modules.deliveries.infrastructure.deliveries_repository_supabase import DeliveriesRepositorySupabase
from app.modules.notifications.application.services.notifications_service import NotificationsService
from app.modules.orders.application.services.orders_service import OrdersService


class DeliveriesService:
    def __init__(
        self,
        repository: DeliveriesRepositorySupabase = Depends(DeliveriesRepositorySupabase),
        orders_service: OrdersService = Depends(OrdersService),
        notifications_service: NotificationsService = Depends(NotificationsService),
        auth_repository: AuthRepositorySupabase = Depends(AuthRepositorySupabase),
    ) -> None:
        self.repository = repository
        self.orders_service = orders_service
        self.notifications_service = notifications_service
        self.auth_repository = auth_repository

    async def get_available_orders(self, limit: int = 10, offset: int = 0):
        all_orders = await self.orders_service.repository.get_available_orders_for_delivery(limit, offset)
        available = []
        for order in all_orders:
            assignment = await self.repository.get_assignment_by_order(order["id"])
            if not assignment:
                available.append(order)
        return available

    async def accept_order(self, order_id: int, delivery_user_id: str):
        order = await self.orders_service.repository.get_order(order_id)
        if not order:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

        if order.get("status") not in ["pending", "ready"]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This order is not available for delivery")

        existing = await self.repository.get_assignment_by_order(order_id)
        if existing:
            raise OrderAlreadyAssignedError()

        assignment = await self.repository.create_assignment(order_id, delivery_user_id)
        await self.orders_service.repository.update_order_status(order_id, "out_for_delivery")
        return assignment

    async def get_my_assignments(self, delivery_user_id: str):
        assignments = await self.repository.get_my_assignments(delivery_user_id)
        result = []
        for assignment in assignments:
            order = await self.orders_service.repository.get_order_for_delivery(assignment["order_id"])
            result.append({
                "id": assignment["id"],
                "order_id": assignment["order_id"],
                "delivery_user_id": assignment["delivery_user_id"],
                "assigned_at": assignment["assigned_at"],
                "order": order,
            })
        return result

    async def update_order_status(self, order_id: int, new_status: str, delivery_user_id: str):
        assignment = await self.repository.get_assignment_by_order(order_id)
        if not assignment:
            raise DeliveryAssignmentNotFoundError()
        if assignment.get("delivery_user_id") != delivery_user_id:
            raise NotAssignedToOrderError()

        allowed_statuses = ["on_the_way", "delivered"]
        if new_status not in allowed_statuses:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Status must be one of: {', '.join(allowed_statuses)}")

        return await self.orders_service.repository.update_order_status(order_id, new_status)

    async def unassign_delivery(self, assignment_id: int):
        assignment = await self.repository.get_assignment(assignment_id)
        if not assignment:
            raise DeliveryAssignmentNotFoundError()
        await self.repository.delete_assignment(assignment_id)

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
