from fastapi import APIRouter, Depends, status
from typing import List
from app.core.dependencies import get_current_user
from app.modules.shop_products.presentation.controller import ShopProductsController
from app.modules.shop_products.presentation.schemas import (
    CreateShopProductRequest,
    UpdateShopProductRequest,
    ShopProductResponse,
)
from app.modules.shop_products.domain.errors import ShopProductsError

router = APIRouter(prefix="/shop-products", tags=["shop-products"])


@router.get("/", response_model=List[ShopProductResponse], status_code=status.HTTP_200_OK)
async def get_all_shop_products(shop_id: int, limit: int = 10, offset: int = 0, controller: ShopProductsController = Depends(ShopProductsController)):
    try:
        return await controller.get_all_shop_products(shop_id, is_manager=False, limit=limit, offset=offset)
    except Exception as e:
        raise ShopProductsError(str(e))


@router.get("/manage", response_model=List[ShopProductResponse], status_code=status.HTTP_200_OK)
async def get_shop_products_for_manager(shop_id: int, limit: int = 10, offset: int = 0, controller: ShopProductsController = Depends(ShopProductsController), current_user=Depends(get_current_user)):
    try:
        return await controller.get_all_shop_products(shop_id, is_manager=True, limit=limit, offset=offset)
    except Exception as e:
        raise ShopProductsError(str(e))


@router.get("/{shop_product_id}", response_model=ShopProductResponse, status_code=status.HTTP_200_OK)
async def get_shop_product(shop_product_id: int, controller: ShopProductsController = Depends(ShopProductsController)):
    try:
        return await controller.get_shop_product(shop_product_id)
    except Exception as e:
        raise ShopProductsError(str(e))


@router.post("/", response_model=ShopProductResponse, status_code=status.HTTP_201_CREATED)
async def create_shop_product(payload: CreateShopProductRequest, controller: ShopProductsController = Depends(ShopProductsController), current_user=Depends(get_current_user)):
    try:
        requester_id = current_user.get("id")
        return await controller.create_shop_product(payload, requester_id)
    except Exception as e:
        raise ShopProductsError(str(e))


@router.put("/{shop_product_id}", response_model=ShopProductResponse, status_code=status.HTTP_200_OK)
async def update_shop_product(shop_product_id: int, payload: UpdateShopProductRequest, controller: ShopProductsController = Depends(ShopProductsController), current_user=Depends(get_current_user)):
    try:
        requester_id = current_user.get("id")
        return await controller.update_shop_product(shop_product_id, payload, requester_id)
    except Exception as e:
        raise ShopProductsError(str(e))


@router.patch("/{shop_product_id}/mark-available", response_model=ShopProductResponse, status_code=status.HTTP_200_OK)
async def mark_available(shop_product_id: int, controller: ShopProductsController = Depends(ShopProductsController), current_user=Depends(get_current_user)):
    try:
        requester_id = current_user.get("id")
        return await controller.toggle_availability(shop_product_id, True, requester_id)
    except Exception as e:
        raise ShopProductsError(str(e))


@router.patch("/{shop_product_id}/mark-unavailable", response_model=ShopProductResponse, status_code=status.HTTP_200_OK)
async def mark_unavailable(shop_product_id: int, controller: ShopProductsController = Depends(ShopProductsController), current_user=Depends(get_current_user)):
    try:
        requester_id = current_user.get("id")
        return await controller.toggle_availability(shop_product_id, False, requester_id)
    except Exception as e:
        raise ShopProductsError(str(e))


@router.delete("/{shop_product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_shop_product(shop_product_id: int, controller: ShopProductsController = Depends(ShopProductsController), current_user=Depends(get_current_user)):
    try:
        requester_id = current_user.get("id")
        await controller.delete_shop_product(shop_product_id, requester_id)
        return {"message": "Shop product deleted successfully"}
    except Exception as e:
        raise ShopProductsError(str(e))
