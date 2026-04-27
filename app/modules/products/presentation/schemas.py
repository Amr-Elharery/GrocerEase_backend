from pydantic import BaseModel


class CreateProductRequest(BaseModel):
    pass


class UpdateProductRequest(BaseModel):
    pass


class ProductResponse(BaseModel):
    pass


class ProductListResponse(BaseModel):
    pass

class CreateCategoryRequest(BaseModel):
        category_name:str

class CreateSubCategoryRequest(BaseModel):
        category_name:str
        
class CategoryItem(BaseModel):
    id:int
    category_name:str        
class CategoryResponse(BaseModel):
    id:int
    category_name:str
    subcategories:list[CategoryItem] = []
    

    
class SuccessResponse(BaseModel):
    success:bool | None = False
    message:str | None=None   