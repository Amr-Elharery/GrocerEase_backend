from supabase import AsyncClient
from fastapi import Depends
from app.db.supabase_client import get_admin_client

SELECT_FIELDS = """
    id,
    shop_id,
    requested_by,
    name,
    description,
    brand,
    unit,
    category_id,
    subcategory_id,
    status,
    image_url,
    created_at
"""

class ProductRequestsRepositorySupabase:
    def __init__(self, admin_client: AsyncClient = Depends(get_admin_client)) -> None:
        self.client = admin_client

    async def get_all_requests(self, status: str = None, shop_id: int = None, limit: int = 10, offset: int = 0):
        try:
            query = self.client.from_("product_requests").select(SELECT_FIELDS)
            if status:
                query = query.eq("status", status)
            if shop_id:
                query = query.eq("shop_id", shop_id)
            response = await query.range(offset, offset + limit - 1).execute()
            return response.data
        except Exception as e:
            print(f"Error fetching product requests: {e}")
            raise e

    async def get_request(self, request_id: int):
        try:
            response = await self.client.from_("product_requests").select(SELECT_FIELDS).eq("id", request_id).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            print(f"Error fetching product request: {e}")
            raise e

    async def create_request(self, payload: dict):
        try:
            response = await self.client.from_("product_requests").insert(payload).execute()
            if response.data:
                return await self.get_request(response.data[0]["id"])
            return None
        except Exception as e:
            print(f"Error creating product request: {e}")
            raise e

    async def update_request_status(self, request_id: int, status: str):
        try:
            response = await self.client.from_("product_requests").update({"status": status}).eq("id", request_id).execute()
            if response.data:
                return await self.get_request(request_id)
            return None
        except Exception as e:
            print(f"Error updating product request status: {e}")
            raise e

