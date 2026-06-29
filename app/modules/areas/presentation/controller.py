from fastapi import Depends

from app.modules.areas.application.services.areas_service import AreasService
from app.modules.areas.presentation.schemas import CreateAreaRequest


class AreasController:
    def __init__(self, service: AreasService = Depends(AreasService)) -> None:
        self.service = service

    async def get_all_areas(self):
        return await self.service.get_all_areas()

    async def create_area(self, payload: CreateAreaRequest):
        return await self.service.create_area(payload.area_name, payload.city_name)

    async def delete_area(self, area_id: int) -> None:
        await self.service.delete_area(area_id)
