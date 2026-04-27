from fastapi import APIRouter, Depends, status

from app.core.dependencies import get_current_user, require_admin
from app.db.supabase_client import get_admin_client,get_anon_client
from app.modules.products.application.services.products_service import ProductsService
from app.modules.products.presentation.controller import ProductsController
from app.modules.products.presentation.schemas import (
    CategoryResponse,
    CreateCategoryRequest,
    CreateProductRequest,
    CreateSubCategoryRequest,
    UpdateProductRequest,
)

router = APIRouter(prefix="/products", tags=["products"])
categories_router = APIRouter(prefix="/categories",tags=["categories"])

async def _get_controller() -> ProductsController:
    return ProductsController(ProductsService(await get_admin_client(),await get_anon_client()))


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

@categories_router.post("/", status_code=status.HTTP_201_CREATED, response_model=CategoryResponse)
async def create_category(payload: CreateCategoryRequest, controller: ProductsController = Depends(_get_controller), user=Depends(require_admin)):
    return await controller.create_category(payload)

@categories_router.get("/",status_code=status.HTTP_200_OK,response_model=list[CategoryResponse])
async def get_all_categories(controller:ProductsController=Depends(_get_controller)):
    return await controller.get_all_categories()

@categories_router.post("/{parent_id}/subcategories",status_code=status.HTTP_201_CREATED,response_model=CategoryResponse)
async def create_subcategory(parent_id:int,payload:CreateCategoryRequest,controller:ProductsController=Depends(_get_controller),user=Depends(require_admin)):
    return await controller.create_subcategory(payload,parent_id)

@categories_router.delete("/{category_id}",status_code=status.HTTP_200_OK)
async def creat_subcategory(category_id:int,controller:ProductsController=Depends(_get_controller),user=Depends(require_admin)):
    await controller.delete_category(category_id)
    return {"message": "Category deleted successfully"}