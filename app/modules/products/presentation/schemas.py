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
    
class CreateShopProductRequest(BaseModel):
    product_id:int
    available_stock:int
    low_stock_threshold: int
    price:float
    is_active:bool | None = True
    
class UpdateShopProductRequest(BaseModel):
    available_stock:int
    low_stock_threshold: int
    price:float
    is_active:bool
        
class ShopProductItem(BaseModel):
    id:int
    shop_id:int
    product_id:int
    available_stock:int
    low_stock_threshold: int
    price:float
    is_active:bool