from fastapi import Depends, UploadFile
from app.modules.product_requests.application.services.product_requests_service import ProductRequestsService
from app.modules.product_requests.presentation.schemas import CreateProductRequestRequest, ProductRequestResponse


class ProductRequestsController:
    def __init__(self, service: ProductRequestsService = Depends(ProductRequestsService)) -> None:
        self.service = service

    async def get_all_requests(self, status: str = None, shop_id: int = None, limit: int = 10, offset: int = 0):
        try:
            return await self.service.get_all_requests(status, shop_id, limit, offset)
        except Exception as e:
            raise e

    async def get_request(self, request_id: int) -> ProductRequestResponse:
        try:
            return await self.service.get_request(request_id)
        except Exception as e:
            raise e

    async def create_request(self, payload: CreateProductRequestRequest, requester_id: str, image: UploadFile = None) -> ProductRequestResponse:
        try:
            return await self.service.create_request(payload, requester_id, image)
        except Exception as e:
            raise e

    async def approve_request(self, request_id: int) -> ProductRequestResponse:
        try:
            return await self.service.approve_request(request_id)
        except Exception as e:
            raise e

    async def reject_request(self, request_id: int) -> ProductRequestResponse:
        try:
            return await self.service.reject_request(request_id)
        except Exception as e:
            raise e
