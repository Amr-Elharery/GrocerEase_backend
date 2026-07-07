from fastapi import APIRouter, Depends, File, UploadFile, status
from typing import List
from app.core.dependencies import get_current_user, require_roles
from app.modules.product_requests.presentation.controller import ProductRequestsController
from app.modules.product_requests.presentation.schemas import (
    CreateProductRequestRequest,
    CreateProductRequestAsForm,
    ProductRequestResponse,
)
from app.modules.product_requests.domain.errors import ProductRequestsError

router = APIRouter(prefix="/product-requests", tags=["product-requests"])


@router.get("/", response_model=List[ProductRequestResponse], status_code=status.HTTP_200_OK)
async def get_all_requests(status: str = None, shop_id: int = None, limit: int = 10, offset: int = 0, controller: ProductRequestsController = Depends(ProductRequestsController), current_user=Depends(get_current_user)):
    try:
        return await controller.get_all_requests(status, shop_id, limit, offset)
    except Exception as e:
        raise ProductRequestsError(str(e))


@router.get("/{request_id}", response_model=ProductRequestResponse, status_code=status.HTTP_200_OK)
async def get_request(request_id: int, controller: ProductRequestsController = Depends(ProductRequestsController), current_user=Depends(get_current_user)):
    try:
        return await controller.get_request(request_id)
    except Exception as e:
        raise ProductRequestsError(str(e))


@router.post("/", response_model=ProductRequestResponse, status_code=status.HTTP_201_CREATED)
async def create_request(image: UploadFile = File(None), payload: CreateProductRequestRequest = Depends(CreateProductRequestAsForm), controller: ProductRequestsController = Depends(ProductRequestsController), current_user=Depends(get_current_user), _=Depends(require_roles(["vendor"]))):
    try:
        requester_id = current_user.get("id")
        return await controller.create_request(payload, requester_id, image)
    except Exception as e:
        raise ProductRequestsError(str(e))


@router.patch("/{request_id}/approve", response_model=ProductRequestResponse, status_code=status.HTTP_200_OK)
async def approve_request(request_id: int, controller: ProductRequestsController = Depends(ProductRequestsController), _=Depends(require_roles(["admin"]))):
    try:
        return await controller.approve_request(request_id)
    except Exception as e:
        raise ProductRequestsError(str(e))


@router.patch("/{request_id}/reject", response_model=ProductRequestResponse, status_code=status.HTTP_200_OK)
async def reject_request(request_id: int, controller: ProductRequestsController = Depends(ProductRequestsController), _=Depends(require_roles(["admin"]))):
    try:
        return await controller.reject_request(request_id)
    except Exception as e:
        raise ProductRequestsError(str(e))
