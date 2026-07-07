from fastapi import APIRouter, Depends, status
from typing import List

from app.core.dependencies import get_current_user, require_roles, require_admin
from app.modules.deliveries.presentation.controller import DeliveriesController
from app.modules.deliveries.presentation.schemas import (
    CreateDeliveryProfileRequest,
    DeliveryDetailResponse,
    DeliveryGroupResponse,
    DeliveryProfileResponse,
    DeliveryResponse,
    UpdateAvailabilityRequest,
    UpdateLocationRequest,
    UpdateOrderStatusRequest,
)

router = APIRouter(prefix="/deliveries", tags=["deliveries"])


# ---------- Profile ----------

@router.post("/profile", response_model=DeliveryProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_profile(
    payload: CreateDeliveryProfileRequest,
    controller: DeliveriesController = Depends(DeliveriesController),
    current_user=Depends(get_current_user),
    _=Depends(require_roles(["delivery"])),
):
    user_id = current_user.get("id")
    return await controller.create_profile(payload, user_id)


@router.get("/profile/me", response_model=DeliveryProfileResponse, status_code=status.HTTP_200_OK)
async def get_my_profile(
    controller: DeliveriesController = Depends(DeliveriesController),
    current_user=Depends(get_current_user),
    _=Depends(require_roles(["delivery"])),
):
    user_id = current_user.get("id")
    return await controller.get_my_profile(user_id)


@router.patch("/profile/availability", response_model=DeliveryProfileResponse, status_code=status.HTTP_200_OK)
async def update_availability(
    payload: UpdateAvailabilityRequest,
    controller: DeliveriesController = Depends(DeliveriesController),
    current_user=Depends(get_current_user),
    _=Depends(require_roles(["delivery"])),
):
    user_id = current_user.get("id")
    return await controller.update_availability(payload, user_id)


@router.patch("/profile/location", response_model=DeliveryProfileResponse, status_code=status.HTTP_200_OK)
async def update_location(
    payload: UpdateLocationRequest,
    controller: DeliveriesController = Depends(DeliveriesController),
    current_user=Depends(get_current_user),
    _=Depends(require_roles(["delivery"])),
):
    user_id = current_user.get("id")
    return await controller.update_location(payload, user_id)


# ---------- Jobs ----------

@router.get("/available", status_code=status.HTTP_200_OK)
async def get_available_orders(
    limit: int = 10,
    offset: int = 0,
    controller: DeliveriesController = Depends(DeliveriesController),
    current_user=Depends(get_current_user),
    _=Depends(require_roles(["delivery"])),
):
    user_id = current_user.get("id")
    return await controller.get_available_orders(user_id, limit, offset)


@router.post("/accept/{order_id}", response_model=DeliveryResponse, status_code=status.HTTP_201_CREATED)
async def accept_order(
    order_id: int,
    controller: DeliveriesController = Depends(DeliveriesController),
    current_user=Depends(get_current_user),
    _=Depends(require_roles(["delivery"])),
):
    user_id = current_user.get("id")
    return await controller.accept_order(order_id, user_id)


@router.post("/accept-group/{order_group_id}", response_model=DeliveryGroupResponse, status_code=status.HTTP_201_CREATED)
async def accept_group(
    order_group_id: int,
    controller: DeliveriesController = Depends(DeliveriesController),
    current_user=Depends(get_current_user),
    _=Depends(require_roles(["delivery"])),
):
    user_id = current_user.get("id")
    return await controller.accept_group(order_group_id, user_id)


@router.get("/my-assignments", response_model=List[DeliveryDetailResponse], status_code=status.HTTP_200_OK)
async def get_my_deliveries(
    controller: DeliveriesController = Depends(DeliveriesController),
    current_user=Depends(get_current_user),
    _=Depends(require_roles(["delivery"])),
):
    user_id = current_user.get("id")
    return await controller.get_my_deliveries(user_id)


@router.patch("/orders/{order_id}/status", status_code=status.HTTP_200_OK)
async def update_order_status(
    order_id: int,
    payload: UpdateOrderStatusRequest,
    controller: DeliveriesController = Depends(DeliveriesController),
    current_user=Depends(get_current_user),
    _=Depends(require_roles(["delivery"])),
):
    user_id = current_user.get("id")
    return await controller.update_order_status(order_id, payload, user_id)


@router.patch("/groups/{order_group_id}/status", status_code=status.HTTP_200_OK)
async def update_group_status(
    order_group_id: int,
    payload: UpdateOrderStatusRequest,
    controller: DeliveriesController = Depends(DeliveriesController),
    current_user=Depends(get_current_user),
    _=Depends(require_roles(["delivery"])),
):
    user_id = current_user.get("id")
    return await controller.update_group_status(order_group_id, payload, user_id)


# ---------- Admin ----------

@router.delete("/{delivery_id}", status_code=status.HTTP_204_NO_CONTENT)
async def unassign_delivery(
    delivery_id: int,
    controller: DeliveriesController = Depends(DeliveriesController),
    _=Depends(require_admin),
):
    await controller.unassign_delivery(delivery_id)
