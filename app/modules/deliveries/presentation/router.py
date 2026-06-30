from fastapi import APIRouter, Depends, status
from typing import List

from app.core.dependencies import get_current_user, require_roles, require_admin
from app.modules.deliveries.presentation.controller import DeliveriesController
from app.modules.deliveries.presentation.schemas import (
    DeliveryAssignmentResponse,
    DeliveryAssignmentDetailResponse,
    UpdateOrderStatusRequest,
)

router = APIRouter(prefix="/deliveries", tags=["deliveries"])


@router.get("/available", status_code=status.HTTP_200_OK)
async def get_available_orders(
    limit: int = 10,
    offset: int = 0,
    controller: DeliveriesController = Depends(DeliveriesController),
    _=Depends(require_roles(["delivery"])),
):
    try:
        return await controller.get_available_orders(limit, offset)
    except Exception as e:
        raise e


@router.post("/accept/{order_id}", response_model=DeliveryAssignmentResponse, status_code=status.HTTP_201_CREATED)
async def accept_order(
    order_id: int,
    controller: DeliveriesController = Depends(DeliveriesController),
    current_user=Depends(get_current_user),
    _=Depends(require_roles(["delivery"])),
):
    try:
        delivery_user_id = current_user.get("id")
        return await controller.accept_order(order_id, delivery_user_id)
    except Exception as e:
        raise e


@router.get("/my-assignments", response_model=List[DeliveryAssignmentDetailResponse], status_code=status.HTTP_200_OK)
async def get_my_assignments(
    controller: DeliveriesController = Depends(DeliveriesController),
    current_user=Depends(get_current_user),
    _=Depends(require_roles(["delivery"])),
):
    try:
        delivery_user_id = current_user.get("id")
        return await controller.get_my_assignments(delivery_user_id)
    except Exception as e:
        raise e


@router.patch("/orders/{order_id}/status", status_code=status.HTTP_200_OK)
async def update_order_status(
    order_id: int,
    payload: UpdateOrderStatusRequest,
    controller: DeliveriesController = Depends(DeliveriesController),
    current_user=Depends(get_current_user),
    _=Depends(require_roles(["delivery"])),
):
    try:
        delivery_user_id = current_user.get("id")
        return await controller.update_order_status(order_id, payload, delivery_user_id)
    except Exception as e:
        raise e


@router.delete("/assignments/{assignment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def unassign_delivery(
    assignment_id: int,
    controller: DeliveriesController = Depends(DeliveriesController),
    _=Depends(require_admin),
):
    try:
        await controller.unassign_delivery(assignment_id)
    except Exception as e:
        raise e
