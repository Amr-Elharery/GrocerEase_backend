from fastapi import APIRouter, Depends, status

from app.core.dependencies import require_admin
from app.db.supabase_client import get_admin_client, get_anon_client
from app.modules.categories.application.services.categories_service import CategoriesService
from app.modules.categories.presentation.controller import CategoriesController
from app.modules.categories.presentation.schemas import (
    CategoryResponse,
    CreateCategoryRequest,
    CreateSubCategoryRequest,
)

router = APIRouter(prefix="/categories", tags=["categories"])

async def _get_controller() -> CategoriesController:
    return CategoriesController(CategoriesService(await get_admin_client(), await get_anon_client()))


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CategoryResponse)
async def create_category(payload: CreateCategoryRequest, controller: CategoriesController = Depends(_get_controller), user=Depends(require_admin)):
    return await controller.create_category(payload)


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[CategoryResponse])
async def get_all_categories(controller: CategoriesController = Depends(_get_controller)):
    return await controller.get_all_categories()


@router.post("/{parent_id}/subcategories", status_code=status.HTTP_201_CREATED, response_model=CategoryResponse)
async def create_subcategory(parent_id: int, payload: CreateSubCategoryRequest, controller: CategoriesController = Depends(_get_controller), user=Depends(require_admin)):
    return await controller.create_subcategory(payload, parent_id)


@router.delete("/{category_id}", status_code=status.HTTP_200_OK)
async def delete_category(category_id: int, controller: CategoriesController = Depends(_get_controller), user=Depends(require_admin)):
    await controller.delete_category(category_id)
    return {"message": "Category deleted successfully"}
