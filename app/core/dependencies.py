from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.db.supabase_client import get_admin_client
from app.lib.JWT import jwt_handler

_bearer = HTTPBearer(auto_error=False)


async def verify_bearer_token(credentials: HTTPAuthorizationCredentials = Depends(_bearer)):
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Bearer token is missing")

    token = credentials.credentials
    try:
        decoded = jwt_handler.decode(token)
        return {"payload": decoded, "token": token}
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc))

async def verify_refresh_token(token_info = Depends(verify_bearer_token)):
    payload = token_info.get("payload")
    if not payload.get("refresh"):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token: not a refresh token")
    return payload

async def get_current_user(token_info = Depends(verify_bearer_token)):
    try:
        payload = token_info.get("payload")
        if payload.get("refresh"):
            raise HTTPException(status_code=401, detail="Refresh tokens cannot be used to access resources")

        user = payload.get("user")
        if not user:
            raise HTTPException(status_code=401, detail="Invalid token payload: missing user")
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

def require_roles(required_roles: list[str]):
    def _dependency(user = Depends(get_current_user)):
        user_roles = user.get("roles", [])
        for role in required_roles:
            if role in user_roles:
              return True
        raise HTTPException(status_code=403, detail="Forbidden: insufficient permissions")

    return _dependency

# TODO: Remove
async def require_admin(user=Depends(get_current_user)):
    client = await get_admin_client()
    user_id = user.get("id") if isinstance(user, dict) else getattr(user, "id", None)
    result = await client.from_("users_roles").select("roles(role_name)").eq("user_id", user_id).execute()

    roles = [r["roles"]["role_name"] for r in result.data if r.get("roles")]
    if "admin" not in roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return user
