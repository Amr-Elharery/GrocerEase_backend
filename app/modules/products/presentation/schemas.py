from pydantic import BaseModel
from fastapi import Form
from typing import Annotated, List

class ProductBase(BaseModel):
    product_name: str
    description: str | None = None
    brand: str | None = None
    unit: str | None = None
class CreateProductRequest(ProductBase):
    category_id: int
    sub_category_id: int | None = None

def CreateProductRequestAsForm(
    product_name: Annotated[str, Form()],
    category_id: Annotated[int, Form()],
    sub_category_id: Annotated[int | None, Form()] = None,
    description: Annotated[str | None, Form()] = None,
    brand: Annotated[str | None, Form()] = None,
    unit: Annotated[str | None, Form()] = None) -> CreateProductRequest:
    return CreateProductRequest(
        product_name=product_name,
        category_id=category_id,
        sub_category_id=sub_category_id,
        description=description,
        brand=brand,
        unit=unit
    )

class UpdateProductRequest(CreateProductRequest):
    pass

class ProductImageResponse(BaseModel):
    id: int | None = None
    image_url: str | None = None
    is_primary: bool | None = None
    variant: str | None = None

class CategoryResponse(BaseModel):
    id: int
    category_name: str

class SubCategoryResponse(BaseModel):
    id: int | None = None
    category_name: str | None = None

class ProductsResponse(ProductBase):
    id: int
    category: CategoryResponse
    sub_category: SubCategoryResponse | None = None
    product_images: List[ProductImageResponse]

class shopResponse(BaseModel):
    id: int | None = None
    shop_name: str | None = None
    logo_url: str | None = None

class ShopProductResponse(BaseModel):
    available_stock: int | None = None
    price: float | None = None
    is_active: bool | None = None
    is_available: bool | None = None
    shop: shopResponse | None = None

class ProductResponse(ProductBase):
    id: int
    category: CategoryResponse
    sub_category: SubCategoryResponse | None = None
    product_images: List[ProductImageResponse]
    shops: List[ShopProductResponse] | None = None