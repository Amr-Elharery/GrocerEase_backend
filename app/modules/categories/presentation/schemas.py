from pydantic import BaseModel, Field


class CreateCategoryRequest(BaseModel):
    category_name: str


class CreateSubCategoryRequest(BaseModel):
    category_name: str


class CategoryItem(BaseModel):
    id: int
    category_name: str


class CategoryResponse(BaseModel):
    id: int
    category_name: str
    subcategories: list[CategoryItem] = Field(default_factory=list)
