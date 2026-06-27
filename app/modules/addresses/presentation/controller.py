from fastapi import Depends

from app.modules.addresses.application.services.addresses_service import AddressesService
from app.modules.addresses.presentation.schemas import CreateAddressRequest, UpdateAddressRequest


class AddressesController:
    def __init__(self, service: AddressesService = Depends(AddressesService)) -> None:
        self.service = service

    async def get_all_addresses(self, user_id: str):
        try:
            return await self.service.get_all_addresses(user_id)
        except Exception as e:
            raise e

    async def get_address(self, address_id: int, user_id: str):
        try:
            return await self.service.get_address(address_id, user_id)
        except Exception as e:
            raise e

    async def create_address(self, payload: CreateAddressRequest, user_id: str):
        try:
            return await self.service.create_address(payload, user_id)
        except Exception as e:
            raise e

    async def update_address(self, address_id: int, payload: UpdateAddressRequest, user_id: str):
        try:
            return await self.service.update_address(address_id, payload, user_id)
        except Exception as e:
            raise e

    async def delete_address(self, address_id: int, user_id: str):
        try:
            await self.service.delete_address(address_id, user_id)
        except Exception as e:
            raise e
