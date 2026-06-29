from fastapi import APIRouter, Depends, status

from app.core.dependencies import require_admin
from app.modules.areas.presentation.controller import AreasController
from app.modules.areas.presentation.schemas import AreaResponse, CreateAreaRequest

router = APIRouter(prefix="/areas", tags=["areas"])


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[AreaResponse])
async def get_all_areas(controller: AreasController = Depends(AreasController)):
    return await controller.get_all_areas()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=AreaResponse)
async def create_area(
    payload: CreateAreaRequest,
    controller: AreasController = Depends(AreasController),
    user=Depends(require_admin),
):
    return await controller.create_area(payload)


@router.delete("/{area_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_area(
    area_id: int,
    controller: AreasController = Depends(AreasController),
    user=Depends(require_admin),
):
    await controller.delete_area(area_id)
