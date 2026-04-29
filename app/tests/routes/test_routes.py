from fastapi import APIRouter
from app.db.supabase_client import get_anon_client

router = APIRouter()

@router.get("/test-supabase")
async def test_supabase():
    try:
        client = await get_anon_client()
        response = await client.table("users").select("*").limit(1).execute()

        return {
            "status": "connected",
            "data": response.data
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }