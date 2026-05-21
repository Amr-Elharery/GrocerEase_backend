from abc import ABC, abstractmethod
from fastapi import UploadFile


class ImageStorage(ABC):
    @abstractmethod
    async def save(self, file: UploadFile) -> str:
        """Save the provided UploadFile and return a public path/URL."""

    @abstractmethod
    async def delete(self, path: str) -> None:
        """Delete a previously saved file by path/URL."""
