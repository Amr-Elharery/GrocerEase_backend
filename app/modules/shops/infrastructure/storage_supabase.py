from uuid import uuid4
from pathlib import Path
from fastapi import UploadFile, Depends
from supabase import AsyncClient
from app.db.supabase_client import get_admin_client
from app.core.ports import ImageStorage


class SupabaseImageStorage(ImageStorage):
    def __init__(self, admin_client: AsyncClient = Depends(get_admin_client)) -> None:
        self.client = admin_client
        self.bucket = "files"

    async def save(self, file: UploadFile) -> str:
        ext = Path(file.filename).suffix
        filename = f"{uuid4()}{ext}"
        path = f"shops/{filename}"
        content = await file.read()
        try:
            await self.client.storage.from_(self.bucket).upload(path, content)
        except Exception:
            print(f"Error uploading file to Supabase: {file.filename}")
            return f"{self.bucket}/{path}"

        try:
            public = await self.client.storage.from_(self.bucket).get_public_url(path)
            return public
        except Exception:
            return f"{self.bucket}/{path}"

    async def delete(self, path: str) -> None:
        try:
            await self.client.storage.from_(self.bucket).remove([path])
        except Exception:
            print(f"Error deleting file from Supabase: {path}")
