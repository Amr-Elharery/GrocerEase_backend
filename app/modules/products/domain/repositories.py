from abc import ABC, abstractmethod
from typing import List, Optional, Any

class ProductRepository(ABC):
    @abstractmethod
    async def create(self, data: dict[str, Any]) -> dict[str, Any]:
        pass

    @abstractmethod
    async def get_by_id(self, product_id: str) -> Optional[dict[str, Any]]:
        pass

    @abstractmethod
    async def get_all(self) -> List[dict[str, Any]]:
        pass

    @abstractmethod
    async def update(self, product_id: str, data: dict[str, Any]) -> Optional[dict[str, Any]]:
        pass

    @abstractmethod
    async def delete(self, product_id: str) -> bool:
        pass