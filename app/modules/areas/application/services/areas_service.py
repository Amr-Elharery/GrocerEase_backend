from fastapi import Depends
from starlette import status

from app.core.exceptions import AppException
from app.modules.areas.domain.errors import AreaHasShopsError, AreaNameAlreadyExistsError, AreaNotFoundError
from app.modules.areas.infrastructure.areas_repository_supabase import AreasRepositorySupabase


class AreasService:
    def __init__(
        self,
        repository: AreasRepositorySupabase = Depends(AreasRepositorySupabase),
    ) -> None:
        self.repository = repository

    async def get_all_areas(self):
        try:
            return await self.repository.get_all_areas()
        except Exception as e:
            raise AppException(f"Failed to retrieve areas: {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def create_area(self, area_name: str, city_name: str):
        existing = await self.repository.get_area_by_name(area_name)
        if existing:
            raise AreaNameAlreadyExistsError()

        try:
            return await self.repository.create_area(area_name, city_name)
        except Exception as e:
            raise AppException(f"Failed to create area: {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR)

    async def delete_area(self, area_id: int) -> None:
        area = await self.repository.get_area_by_id(area_id)
        if not area:
            raise AreaNotFoundError()

        try:
            shop_count = await self.repository.get_shops_count_for_area(area_id)
            if shop_count > 0:
                raise AreaHasShopsError(shop_count)

            await self.repository.delete_area(area_id)
        except AreaHasShopsError:
            raise
        except Exception as e:
            raise AppException(f"Failed to delete area: {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR)
