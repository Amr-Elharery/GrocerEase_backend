from fastapi import Depends, HTTPException, UploadFile, status
from app.modules.product_requests.infrastructure.product_requests_repository_supabase import ProductRequestsRepositorySupabase
from app.modules.product_requests.infrastructure.storage_supabase import SupabaseImageStorage
from app.modules.products.application.services.products_service import ProductsService
from app.modules.products.presentation.schemas import CreateProductRequest
from app.modules.shops.application.services.shops_service import ShopsService
from app.core.ports import ImageStorage


class ProductRequestsService:
    def __init__(
        self,
        repository: ProductRequestsRepositorySupabase = Depends(ProductRequestsRepositorySupabase),
        storage: ImageStorage = Depends(SupabaseImageStorage),
        products_service: ProductsService = Depends(ProductsService),
        shops_service: ShopsService = Depends(ShopsService),
    ) -> None:
        self.repository = repository
        self.storage = storage
        self.products_service = products_service
        self.shops_service = shops_service

    async def get_all_requests(self, status: str = None, shop_id: int = None, limit: int = 10, offset: int = 0):
        try:
            return await self.repository.get_all_requests(status, shop_id, limit, offset)
        except Exception as e:
            raise e

    async def get_request(self, request_id: int):
        try:
            request = await self.repository.get_request(request_id)
            if not request:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product request not found")
            return request
        except Exception as e:
            raise e

    async def create_request(self, payload, requester_id: str, image: UploadFile = None):
        try:
            shop = await self.shops_service.get_shop(payload.shop_id)
            if not shop:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shop not found")
            if shop.get("owner_id") != requester_id:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not the owner of this shop")

            data = payload.dict()
            data["requested_by"] = requester_id
            data["status"] = "pending"

            if image:
                image_url = await self.storage.save(image)
                data["image_url"] = image_url

            return await self.repository.create_request(data)
        except Exception as e:
            raise e

    async def approve_request(self, request_id: int):
        try:
            request = await self.repository.get_request(request_id)
            if not request:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product request not found")
            if request.get("status") != "pending":
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only pending requests can be approved")

            product_payload = CreateProductRequest(
                product_name=request["name"],
                description=request["description"],
                brand=request["brand"],
                unit=request["unit"],
                category_id=request["category_id"],
                sub_category_id=request.get("subcategory_id"),
            )
            product = await self.products_service.create_product(product_payload, files=None)

            if product and request.get("image_url"):
                await self.products_service.repository.create_product_image(
                    product_id=product["id"],
                    image_url=request["image_url"],
                    is_primary=True,
                )

            return await self.repository.update_request_status(request_id, "approved")
        except Exception as e:
            raise e

    async def reject_request(self, request_id: int):
        try:
            request = await self.repository.get_request(request_id)
            if not request:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product request not found")
            if request.get("status") != "pending":
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only pending requests can be rejected")
            return await self.repository.update_request_status(request_id, "rejected")
        except Exception as e:
            raise e
