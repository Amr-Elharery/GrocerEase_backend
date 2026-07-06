from fastapi import APIRouter, Depends, status
from typing import List
from app.core.dependencies import get_current_user, require_roles, require_admin
from app.modules.orders.presentation.controller import OrdersController
from app.modules.orders.presentation.schemas import (
    CreateOrderRequest,
    CreateOptimizationOrderRequest,
    OrderResponse,
    OrderGroupResponse,
)
from app.modules.orders.domain.errors import OrdersError

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("/admin/all", response_model=List[OrderResponse], status_code=status.HTTP_200_OK)
async def get_all_orders_admin(limit: int = 10, offset: int = 0, controller: OrdersController = Depends(OrdersController), _=Depends(require_roles(["admin"]))):
    try:
        return await controller.get_all_orders_admin(limit, offset)
    except Exception as e:
        raise OrdersError(str(e))


@router.get("/shop", response_model=List[OrderResponse], status_code=status.HTTP_200_OK)
async def get_shop_orders(limit: int = 10, offset: int = 0, controller: OrdersController = Depends(OrdersController), current_user=Depends(get_current_user), _=Depends(require_roles(["vendor"]))):
    try:
        owner_id = current_user.get("id")
        return await controller.get_shop_orders(owner_id, limit, offset)
    except Exception as e:
        raise OrdersError(str(e))


@router.get("/", response_model=List[OrderResponse], status_code=status.HTTP_200_OK)
async def get_all_orders(limit: int = 10, offset: int = 0, controller: OrdersController = Depends(OrdersController), current_user=Depends(get_current_user)):
    try:
        customer_id = current_user.get("id")
        return await controller.get_all_orders(customer_id, limit, offset)
    except Exception as e:
        raise OrdersError(str(e))


@router.get("/groups/{order_group_id}", response_model=OrderGroupResponse, status_code=status.HTTP_200_OK)
async def get_order_group(order_group_id: int, controller: OrdersController = Depends(OrdersController), current_user=Depends(get_current_user)):
    try:
        customer_id = current_user.get("id")
        return await controller.get_order_group(order_group_id, customer_id)
    except Exception as e:
        raise OrdersError(str(e))


@router.get("/{order_id}", response_model=OrderResponse, status_code=status.HTTP_200_OK)
async def get_order(order_id: int, controller: OrdersController = Depends(OrdersController), current_user=Depends(get_current_user)):
    try:
        return await controller.get_order(order_id, current_user)
    except Exception as e:
        raise OrdersError(str(e))


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(payload: CreateOrderRequest, controller: OrdersController = Depends(OrdersController), current_user=Depends(get_current_user)):
    try:
        customer_id = current_user.get("id")
        return await controller.create_order(payload, customer_id)
    except Exception as e:
        raise OrdersError(str(e))


@router.post("/optimization", response_model=OrderGroupResponse, status_code=status.HTTP_201_CREATED)
async def create_optimization_order(payload: CreateOptimizationOrderRequest, controller: OrdersController = Depends(OrdersController), current_user=Depends(get_current_user)):
    try:
        customer_id = current_user.get("id")
        return await controller.create_optimization_order(payload, customer_id)
    except Exception as e:
        raise OrdersError(str(e))


@router.patch("/{order_id}/cancel", response_model=OrderResponse, status_code=status.HTTP_200_OK)
async def cancel_order(order_id: int, controller: OrdersController = Depends(OrdersController), current_user=Depends(get_current_user)):
    try:
        customer_id = current_user.get("id")
        return await controller.cancel_order(order_id, customer_id)
    except Exception as e:
        raise OrdersError(str(e))


@router.patch("/{order_id}/status", response_model=OrderResponse, status_code=status.HTTP_200_OK)
async def update_order_status(order_id: int, new_status: str, controller: OrdersController = Depends(OrdersController), _=Depends(require_roles(["admin"]))):
    try:
        return await controller.update_order_status(order_id, new_status)
    except Exception as e:
        raise OrdersError(str(e))
