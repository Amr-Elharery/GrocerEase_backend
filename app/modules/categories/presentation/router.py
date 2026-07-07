from fastapi import APIRouter, Depends, status

from app.core.dependencies import require_admin
from app.modules.categories.application.services.categories_service import CategoriesService
from app.modules.categories.presentation.controller import CategoriesController
from app.modules.categories.presentation.schemas import (
    CategoryItem,
    CategoryResponse,
    CreateCategoryRequest,
    CreateSubCategoryRequest,
)

router = APIRouter(prefix="/categories", tags=["categories"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CategoryResponse)
async def create_category(
    payload: CreateCategoryRequest,
    controller: CategoriesController = Depends(CategoriesController),
    user=Depends(require_admin),
):
    return await controller.create_category(payload)


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[CategoryResponse])
async def get_all_categories(controller: CategoriesController = Depends(CategoriesController)):
    return await controller.get_all_categories()


@router.post("/{parent_id}/subcategories", status_code=status.HTTP_201_CREATED, response_model=CategoryItem)
async def create_subcategory(
    parent_id: int,
    payload: CreateSubCategoryRequest,
    controller: CategoriesController = Depends(CategoriesController),
    user=Depends(require_admin),
):
    return await controller.create_subcategory(payload, parent_id)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int,
    controller: CategoriesController = Depends(CategoriesController),
    user=Depends(require_admin),
):
    await controller.delete_category(category_id)
