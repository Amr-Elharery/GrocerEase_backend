from fastapi import APIRouter, Depends, status, File, UploadFile
from typing import List
from app.core.dependencies import get_current_user
from app.modules.shops.presentation.controller import ShopsController
from app.modules.shops.presentation.schemas import (
    CreateShopRequest,
    CreateShopRequestAsForm,
    UpdateShopRequest,
    UpdateShopRequestAsForm,
    ShopResponse,
)
from app.modules.shops.domain.errors import ShopsError

router = APIRouter(prefix="/shops", tags=["shops"])


@router.get("/", response_model=List[ShopResponse], status_code=status.HTTP_200_OK)
async def get_all_shops(limit: int = 10, offset: int = 0, search: str = None, area_id: int = None, controller: ShopsController = Depends(ShopsController)):
    try:
        return await controller.get_all_shops(limit, offset, search, area_id)
    except Exception as e:
        raise ShopsError(str(e))


@router.get("/{shop_id}", response_model=ShopResponse, status_code=status.HTTP_200_OK)
async def get_shop(shop_id: int, controller: ShopsController = Depends(ShopsController)):
    try:
        return await controller.get_shop(shop_id)
    except Exception as e:
        raise ShopsError(str(e))


@router.post("/", response_model=ShopResponse, status_code=status.HTTP_201_CREATED)
async def create_shop(logo: UploadFile = File(None), payload: CreateShopRequest = Depends(CreateShopRequestAsForm), controller: ShopsController = Depends(ShopsController), current_user=Depends(get_current_user)):
    try:
        owner_id = current_user.get("id")
        return await controller.create_shop(payload, owner_id, logo)
    except Exception as e:
        raise ShopsError(str(e))


@router.put("/{shop_id}", response_model=ShopResponse, status_code=status.HTTP_200_OK)
async def update_shop(shop_id: int, logo: UploadFile = File(None), payload: UpdateShopRequest = Depends(UpdateShopRequestAsForm), controller: ShopsController = Depends(ShopsController), current_user=Depends(get_current_user)):
    try:
        requester_id = current_user.get("id")
        return await controller.update_shop(shop_id, payload, requester_id, logo)
    except Exception as e:
        raise ShopsError(str(e))


@router.delete("/{shop_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_shop(shop_id: int, controller: ShopsController = Depends(ShopsController), current_user=Depends(get_current_user)):
    try:
        requester_id = current_user.get("id")
        await controller.delete_shop(shop_id, requester_id)
        return {"message": "Shop deleted successfully"}
    except Exception as e:
        raise ShopsError(str(e))

