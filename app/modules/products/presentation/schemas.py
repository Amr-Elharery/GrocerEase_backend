from pydantic import BaseModel


class CreateProductRequest(BaseModel):
    pass


class UpdateProductRequest(BaseModel):
    pass


class ProductResponse(BaseModel):
    pass


class ProductListResponse(BaseModel):
    pass
