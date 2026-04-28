from starlette import status
from supabase import AsyncClient

from app.core.exceptions import AppException
from app.modules.products.domain.errors import CategoryNameAlreadyExistsError, CategoryNotFoundError, ProductNotFoundError, SubCategoryCannotHaveChildrenError
from app.modules.products.presentation.schemas import (
    CategoryItem,
    CategoryResponse,
    CreateProductRequest,
    CreateShopProductRequest,
    ShopProductItem,
    SuccessResponse,
    UpdateProductRequest,
    ProductResponse,
    ProductListResponse,
    UpdateShopProductRequest,
)


class ProductsService:
    def __init__(self, admin_client: AsyncClient,anon_client:AsyncClient) -> None:
        self.client = admin_client
        self._anon = anon_client



    async def create_category(self,category_name:str)->CategoryResponse:
            existingCategory = await self.client.from_("category").select("id").eq("category_name",category_name).is_("parent_id",None).execute()
            
            if existingCategory.data:
                raise CategoryNameAlreadyExistsError()
            
            try:

                result = await self.client.from_("category").insert({"category_name":category_name,"parent_id":None}).execute()
            
            except Exception as e:
                raise AppException(f"Failed to create category: {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            row = result.data[0]
            return CategoryResponse(id=row["id"],category_name= row["category_name"])
        
    async def get_all_categories(self)->list[CategoryResponse]:
        
        try:
            result = await self.client.from_("category").select("*").order("parent_id").execute()
            
        except Exception as e:
                raise AppException(f"Failed to retrieve categories: {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        categories = result.data
        tree = {}
        for category in categories: #id category_name parent_id
            if category["parent_id"] is None:
                tree[category["id"]] = CategoryResponse(id = category["id"],category_name=category["category_name"])
                
        for category in categories:
            if category["parent_id"] is not None and category["parent_id"] in tree:
                tree[category["parent_id"]].subcategories.append(CategoryItem(id=category["id"],category_name=category["category_name"]))
                
        return list(tree.values())    
    
    async def create_subcategory(self,category_name:str,parent_id:int)->CategoryItem:
        try:
            parent_result = await self.client.from_("category").select("id, parent_id").eq("id",parent_id).execute()
        except Exception as e:
                raise AppException(f"Failed Retrieving the parent {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR)
        if not parent_result.data:
            raise CategoryNotFoundError()
        
        if parent_result.data[0]["parent_id"] is not None:
            raise SubCategoryCannotHaveChildrenError()
        try:
            insert_result = await self.client.from_("category").insert({"category_name":category_name,"parent_id":parent_id}).execute()
        except Exception as e:
                raise AppException(f"Failed inserting the data {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR)
        response = insert_result.data[0]
        return  CategoryItem(id=response["id"],category_name=response["category_name"])
    
    async def delete_category(self,category_id:int)->None:
        try:
            # ToDo : Check if a product is assigned to the deleted category first and raise error if there is
            result = await self.client.from_("category").delete().eq("id",category_id).execute()
        except Exception as e:
            raise AppException(f"Failed deleting category {str(e)}", status.HTTP_500_INTERNAL_SERVER_ERROR)
        if not result.data:
            raise CategoryNotFoundError()
        
       
            
                    
    async def create_product(self, payload: CreateProductRequest) -> ProductResponse:
        pass

    async def get_product(self, product_id: str) -> ProductResponse:
        pass

    async def get_all_products(self) -> ProductListResponse:
        pass

    async def update_product(self, product_id: str, payload: UpdateProductRequest) -> ProductResponse:
        pass

    async def delete_product(self, product_id: str) -> None:
        pass


    async def create_shop_product(self,shop_id:int,payload:CreateShopProductRequest)->ShopProductItem:
        try:
             result = await self.client.from_("shop_product").insert({"shop_id":shop_id,"product_id":payload.product_id,"available_stock":payload.available_stock,"low_stock_threshold":payload.low_stock_threshold,"price":payload.price,"is_active":payload.is_active}).execute()
        except Exception as e:
            raise AppException(f"Failed Inserting shop product {str(e)}",status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        response = result.data[0]
        return ShopProductItem(id=response["id"],shop_id=shop_id,product_id=response["product_id"],available_stock=response["available_stock"],low_stock_threshold=response["low_stock_threshold"],price=response["price"],is_active=response["is_active"])           
    
    async def update_shop_product(self,shop_id:int,product_id,payload:UpdateShopProductRequest)->ShopProductItem:
        try:
            result = await self.client.from_("shop_product").update({"available_stock":payload.available_stock,"low_stock_threshold":payload.low_stock_threshold,"price":payload.price,"is_active":payload.is_active}).eq("shop_id",shop_id).eq("product_id",product_id).execute()
        except Exception as e:
            raise AppException(f"Failed Updating shop product {str(e)}",status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        response = result.data[0]
        return ShopProductItem(id=response["id"],shop_id=shop_id,product_id=response["product_id"],available_stock=response["available_stock"],low_stock_threshold=response["low_stock_threshold"],price=response["price"],is_active=response["is_active"])    
            