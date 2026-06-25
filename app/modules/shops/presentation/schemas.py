from pydantic import BaseModel
from fastapi import Form
from typing import Annotated
from datetime import datetime


class ShopBase(BaseModel):
    shop_name: str
    description: str | None = None
    address: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    phone_number: str | None = None
    area_id: int | None = None


class CreateShopRequest(ShopBase):
    pass


def CreateShopRequestAsForm(
    shop_name: Annotated[str, Form()],
    description: Annotated[str | None, Form()] = None,
    address: Annotated[str | None, Form()] = None,
    latitude: Annotated[float | None, Form()] = None,
    longitude: Annotated[float | None, Form()] = None,
    phone_number: Annotated[str | None, Form()] = None,
    area_id: Annotated[int | None, Form()] = None,
) -> CreateShopRequest:
    return CreateShopRequest(
        shop_name=shop_name,
        description=description,
        address=address,
        latitude=latitude,
        longitude=longitude,
        phone_number=phone_number,
        area_id=area_id,
    )


class UpdateShopRequest(ShopBase):
    shop_name: str | None = None


def UpdateShopRequestAsForm(
    shop_name: Annotated[str | None, Form()] = None,
    description: Annotated[str | None, Form()] = None,
    address: Annotated[str | None, Form()] = None,
    latitude: Annotated[float | None, Form()] = None,
    longitude: Annotated[float | None, Form()] = None,
    phone_number: Annotated[str | None, Form()] = None,
    area_id: Annotated[int | None, Form()] = None,
) -> UpdateShopRequest:
    return UpdateShopRequest(
        shop_name=shop_name,
        description=description,
        address=address,
        latitude=latitude,
        longitude=longitude,
        phone_number=phone_number,
        area_id=area_id,
    )


class ShopResponse(ShopBase):
    id: int
    owner_id: str
    logo_url: str | None = None
    is_active: bool | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
