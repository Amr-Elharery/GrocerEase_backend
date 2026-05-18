from pydantic import BaseModel


class CreateProductRequest(BaseModel):
    product_name: str
    category_id: int
    sub_category_id: int | None = None
    description: str | None = None
    brand: str | None = None
    unit: str | None = None


class UpdateProductRequest(CreateProductRequest):
    pass


class ProductResponse(BaseModel):
    product_name: str
    category_id: int


class ProductListResponse(BaseModel):
    pass

class SuccessResponse(BaseModel):
    success: bool | None = False
    message: str | None = None