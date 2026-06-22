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


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_product(files: List[UploadFile] = File(), payload: CreateProductRequest = Depends(CreateProductRequestAsForm), controller: ProductsController = Depends(ProductsController)):
    try:
        return await controller.create_product(payload, files)
    except Exception as e:
        raise ProductsError(str(e))


@router.put("/{product_id}", response_model=ProductResponse, status_code=status.HTTP_200_OK)
async def update_product(product_id: int, files: List[UploadFile] = File(None), payload: UpdateProductRequest = Depends(CreateProductRequestAsForm), controller: ProductsController = Depends(ProductsController)):
    try:
        return await controller.update_product(product_id, payload, files)
    except Exception as e:
        raise ProductsError(str(e))

@router.delete("/{product_id}/images/{image_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product_image(product_id: int, image_id: int, controller: ProductsController = Depends(ProductsController)):
    try:
        await controller.delete_product_image(product_id, image_id)
        return {"message": "Image deleted successfully"}
    except Exception as e:
        raise ProductsError(str(e))

@router.post("/{product_id}/images/{image_id}/make-primary", status_code=status.HTTP_204_NO_CONTENT)
async def make_primary_image(product_id: int, image_id: int, controller: ProductsController = Depends(ProductsController)):
    try:
        await controller.make_primary_image(product_id, image_id)
        return {"message": "Primary image updated successfully"}
    except Exception as e:
        raise ProductsError(str(e))

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: str, controller: ProductsController = Depends(ProductsController)):
    try:
        await controller.delete_product(product_id)
        return {"message": "Product deleted successfully"}
    except Exception as e:
        raise ProductsError(str(e))
