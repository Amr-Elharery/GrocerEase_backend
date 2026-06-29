from pydantic import BaseModel
from fastapi import Form
from typing import Annotated
from datetime import datetime


class CreateProductRequestRequest(BaseModel):
    shop_id: int
    name: str
    description: str
    brand: str
    unit: str
    category_id: int
    subcategory_id: int | None = None


def CreateProductRequestAsForm(
    shop_id: Annotated[int, Form()],
    name: Annotated[str, Form()],
    description: Annotated[str, Form()],
    brand: Annotated[str, Form()],
    unit: Annotated[str, Form()],
    category_id: Annotated[int, Form()],
    subcategory_id: Annotated[int | None, Form()] = None,
) -> CreateProductRequestRequest:
    return CreateProductRequestRequest(
        shop_id=shop_id,
        name=name,
        description=description,
        brand=brand,
        unit=unit,
        category_id=category_id,
        subcategory_id=subcategory_id,
    )


class ProductRequestResponse(BaseModel):
    id: int
    shop_id: int
    requested_by: str
    name: str
    description: str
    brand: str
    unit: str
    category_id: int
    subcategory_id: int | None = None
    status: str
    image_url: str | None = None
    created_at: datetime | None = None
