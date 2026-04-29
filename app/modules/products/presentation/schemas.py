from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import List, Optional

class ProductBase(BaseModel):
    product_name: str = Field(..., min_length=1)
    description: Optional[str] = None
    brand: Optional[str] = None
    unit: Optional[str] = None
    category_id: int
    sub_category_id: Optional[int] = None

class CreateProductRequest(ProductBase):
    pass

class UpdateProductRequest(BaseModel):
    product_name: Optional[str] = None
    description: Optional[str] = None
    brand: Optional[str] = None
    unit: Optional[str] = None
    category_id: Optional[int] = None
    sub_category_id: Optional[int] = None

class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ProductListResponse(BaseModel):
    products: List[ProductResponse]