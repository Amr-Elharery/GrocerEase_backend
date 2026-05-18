from pydantic import BaseModel


class CreateProductRequest(BaseModel):
    product_name: str
    category_id: int
    description: str | None = None


class UpdateProductRequest(BaseModel):
    pass


class ProductResponse(BaseModel):
    pass


class ProductListResponse(BaseModel):
    pass

class SuccessResponse(BaseModel):
    success: bool | None = False
    message: str | None = None