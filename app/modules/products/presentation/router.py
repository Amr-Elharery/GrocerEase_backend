from fastapi import APIRouter, Depends, status, File, UploadFile
from typing import List
from app.core.dependencies import get_current_user
from app.db.supabase_client import get_admin_client, get_anon_client
from app.modules.products.application.services.products_service import ProductsService
from app.modules.products.presentation.controller import ProductsController
from app.modules.products.presentation.schemas import (
    CreateProductRequest,
    CreateProductRequestAsForm,
    UpdateProductRequest,
    ProductResponse,
)
from app.modules.products.domain.errors import ProductsError

router = APIRouter(prefix="/products", tags=["products"])

# TODO: Remove
def _get_controller() -> ProductsController:
    return ProductsController()

@router.get("/", response_model=List[ProductResponse], status_code=status.HTTP_200_OK)
async def get_all_products(limit: int = 10, offset: int = 0, search: str = None ,controller: ProductsController = Depends(ProductsController)):
    try:
        return await controller.get_all_products(limit, offset, search)
    except Exception as e:
        raise ProductsError(str(e))

@router.get("/{product_id}", response_model=ProductResponse, status_code=status.HTTP_200_OK)
async def get_product(product_id: str, controller: ProductsController = Depends(ProductsController)):
    try:
        return await controller.get_product(product_id)
    except Exception as e:
        raise ProductsError(str(e))


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(file: UploadFile = File(), payload: CreateProductRequest = Depends(CreateProductRequestAsForm), controller: ProductsController = Depends(ProductsController)):
    try:
        return await controller.create_product(payload, file)
    except Exception as e:
        raise ProductsError(str(e))


@router.put("/{product_id}", response_model=ProductResponse, status_code=status.HTTP_200_OK)
async def update_product(product_id: str, payload: UpdateProductRequest, controller: ProductsController = Depends(_get_controller), user=Depends(get_current_user)):
    try:
        return await controller.update_product(product_id, payload)
    except Exception as e:
        raise ProductsError(str(e))


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: str, controller: ProductsController = Depends(ProductsController)):
    try:
        await controller.delete_product(product_id)
    except Exception as e:
        raise ProductsError(str(e))
