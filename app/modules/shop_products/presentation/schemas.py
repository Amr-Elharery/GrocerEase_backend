from pydantic import BaseModel
from typing import List


class ShopProductBase(BaseModel):
    price: float
    available_stock: int | None = None
    low_stock_threshold: int | None = None


class CreateShopProductRequest(ShopProductBase):
    shop_id: int
    product_id: int


class UpdateShopProductRequest(ShopProductBase):
    price: float | None = None


class ProductImageResponse(BaseModel):
    id: int | None = None
    image_url: str | None = None
    is_primary: bool | None = None


class ProductResponse(BaseModel):
    id: int
    product_name: str
    description: str | None = None
    brand: str | None = None
    unit: str | None = None
    product_images: List[ProductImageResponse] | None = None


class ShopProductResponse(ShopProductBase):
    id: int
    shop_id: int
    product_id: int
    is_active: bool | None = None
    product: ProductResponse | None = None
