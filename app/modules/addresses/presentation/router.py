from fastapi import APIRouter, Depends, status
from typing import List

from app.core.dependencies import get_current_user
from app.modules.addresses.presentation.controller import AddressesController
from app.modules.addresses.presentation.schemas import AddressResponse, CreateAddressRequest, UpdateAddressRequest
from app.modules.addresses.domain.errors import AddressNotFoundError, AddressNotOwnedError

router = APIRouter(prefix="/addresses", tags=["addresses"])


@router.get("/", response_model=List[AddressResponse], status_code=status.HTTP_200_OK)
async def get_all_addresses(controller: AddressesController = Depends(AddressesController), current_user=Depends(get_current_user)):
    try:
        user_id = current_user.get("id")
        return await controller.get_all_addresses(user_id)
    except Exception as e:
        raise e


@router.get("/{address_id}", response_model=AddressResponse, status_code=status.HTTP_200_OK)
async def get_address(address_id: int, controller: AddressesController = Depends(AddressesController), current_user=Depends(get_current_user)):
    try:
        user_id = current_user.get("id")
        return await controller.get_address(address_id, user_id)
    except Exception as e:
        raise e


@router.post("/", response_model=AddressResponse, status_code=status.HTTP_201_CREATED)
async def create_address(payload: CreateAddressRequest, controller: AddressesController = Depends(AddressesController), current_user=Depends(get_current_user)):
    try:
        user_id = current_user.get("id")
        return await controller.create_address(payload, user_id)
    except Exception as e:
        raise e


@router.put("/{address_id}", response_model=AddressResponse, status_code=status.HTTP_200_OK)
async def update_address(address_id: int, payload: UpdateAddressRequest, controller: AddressesController = Depends(AddressesController), current_user=Depends(get_current_user)):
    try:
        user_id = current_user.get("id")
        return await controller.update_address(address_id, payload, user_id)
    except Exception as e:
        raise e


@router.delete("/{address_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_address(address_id: int, controller: AddressesController = Depends(AddressesController), current_user=Depends(get_current_user)):
    try:
        user_id = current_user.get("id")
        await controller.delete_address(address_id, user_id)
    except Exception as e:
        raise e
