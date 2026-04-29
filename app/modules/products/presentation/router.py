from fastapi import APIRouter, Depends, status
from app.core.dependencies import get_current_user
from app.db.supabase_client import get_admin_client
from app.modules.products.application.services.products_service import ProductsService
from app.modules.products.presentation.controller import ProductsController
from app.modules.products.presentation.schemas import (
    CreateProductRequest,
    UpdateProductRequest,
    ProductResponse,
    ProductListResponse,
)

router = APIRouter(prefix="/products", tags=["products"])

async def _get_controller() -> ProductsController:
    client = await get_admin_client()
    return ProductsController(ProductsService(client))

@router.get("/", response_model=ProductListResponse)
async def get_all_products(controller: ProductsController = Depends(_get_controller)):
    return await controller.get_all_products()

@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: str, controller: ProductsController = Depends(_get_controller)):
    return await controller.get_product(product_id)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ProductResponse)
async def create_product(
    payload: CreateProductRequest, 
    controller: ProductsController = Depends(_get_controller), 
    user=Depends(get_current_user)
):
    return await controller.create_product(payload)

@router.put("/{product_id}", status_code=status.HTTP_200_OK, response_model=ProductResponse)
async def update_product(
    product_id: str, 
    payload: UpdateProductRequest, 
    controller: ProductsController = Depends(_get_controller), 
    user=Depends(get_current_user)
):
    return await controller.update_product(product_id, payload)

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: str, 
    controller: ProductsController = Depends(_get_controller), 
    user=Depends(get_current_user)
):
    await controller.delete_product(product_id)