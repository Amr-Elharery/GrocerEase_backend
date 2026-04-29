from typing import List, Optional, Any, cast
from supabase import AsyncClient
from app.modules.products.domain.repositories import ProductRepository

class SupabaseProductRepository(ProductRepository):
    def __init__(self, client: AsyncClient):
        self.table = client.table("product")

    async def create(self, data: dict[str, Any]) -> dict[str, Any]:
        response = await self.table.insert(data).execute()
        return cast(dict[str, Any], response.data[0])

    async def get_by_id(self, product_id: str) -> Optional[dict[str, Any]]:
        response = await self.table.select("*").eq("id", product_id).execute()
        return cast(dict[str, Any], response.data[0]) if response.data else None

    async def get_all(self) -> List[dict[str, Any]]:
        response = await self.table.select("*").order("created_at").execute()
        return cast(List[dict[str, Any]], response.data)

    async def update(self, product_id: str, data: dict[str, Any]) -> Optional[dict[str, Any]]:
        update_data = {k: v for k, v in data.items() if v is not None}
        response = await self.table.update(update_data).eq("id", product_id).execute()
        return cast(dict[str, Any], response.data[0]) if response.data else None

    async def delete(self, product_id: str) -> bool:
        response = await self.table.delete().eq("id", product_id).execute()
        return len(response.data) > 0