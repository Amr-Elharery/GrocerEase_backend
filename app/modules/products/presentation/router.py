from fastapi import APIRouter, Depends, status

from app.core.dependencies import get_current_user
from app.db.supabase_client import get_admin_client
from app.modules.products.application.services.products_service import ProductsService
from app.modules.products.presentation.controller import ProductsController
from app.modules.products.presentation.schemas import (
    CreateProductRequest,
    UpdateProductRequest,
)

router = APIRouter(prefix="/products", tags=["products"])


async def _get_controller() -> ProductsController:
    return ProductsController(ProductsService(await get_admin_client()))


@router.get("/")
async def get_all_products(controller: ProductsController = Depends(_get_controller)):
    pass


@router.get("/{product_id}")
async def get_product(product_id: str, controller: ProductsController = Depends(_get_controller)):
    pass


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_product(payload: CreateProductRequest, controller: ProductsController = Depends(_get_controller), user=Depends(get_current_user)):
    pass


@router.put("/{product_id}", status_code=status.HTTP_200_OK)
async def update_product(product_id: str, payload: UpdateProductRequest, controller: ProductsController = Depends(_get_controller), user=Depends(get_current_user)):
    pass


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: str, controller: ProductsController = Depends(_get_controller), user=Depends(get_current_user)):
    pass
