from supabase import AsyncClient, acreate_client
from app.core.config import settings

_admin_client: AsyncClient | None = None
_anon_client: AsyncClient | None = None

async def get_admin_client() -> AsyncClient:
    global _admin_client
    if _admin_client is None:
        _admin_client = await acreate_client(settings.SUPABASE_URL, settings.SUPABASE_SERVICE_ROLE_KEY)
    return _admin_client 



async def get_anon_client() -> AsyncClient:
    global _anon_client
    if _anon_client is None:
        _anon_client = await acreate_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)
    return _anon_client    
   


async def get_user_client(jwt_token: str) -> AsyncClient:
    client = await acreate_client(settings.SUPABASE_URL, settings.SUPABASE_ANON_KEY)
    client.postgrest.auth(jwt_token)
    return client
