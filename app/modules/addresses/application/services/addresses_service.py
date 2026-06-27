from fastapi import Depends

from app.modules.addresses.domain.errors import AddressNotFoundError, AddressNotOwnedError
from app.modules.addresses.infrastructure.addresses_repository_supabase import AddressesRepositorySupabase


class AddressesService:
    def __init__(
        self,
        repository: AddressesRepositorySupabase = Depends(AddressesRepositorySupabase),
    ) -> None:
        self.repository = repository

    async def get_all_addresses(self, user_id: str):
        return await self.repository.get_all_addresses(user_id)

    async def get_address(self, address_id: int, user_id: str):
        address = await self.repository.get_address(address_id)
        if not address:
            raise AddressNotFoundError()
        if address.get("user_id") != user_id:
            raise AddressNotOwnedError()
        return address

    async def create_address(self, payload, user_id: str):
        data = payload.dict()
        data["user_id"] = user_id
        return await self.repository.create_address(data)

    async def update_address(self, address_id: int, payload, user_id: str):
        address = await self.repository.get_address(address_id)
        if not address:
            raise AddressNotFoundError()
        if address.get("user_id") != user_id:
            raise AddressNotOwnedError()
        data = {k: v for k, v in payload.dict().items() if v is not None}
        return await self.repository.update_address(address_id, data)

    async def delete_address(self, address_id: int, user_id: str):
        address = await self.repository.get_address(address_id)
        if not address:
            raise AddressNotFoundError()
        if address.get("user_id") != user_id:
            raise AddressNotOwnedError()
        await self.repository.delete_address(address_id)
