from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.db.supabase_client import get_admin_client

_bearer = HTTPBearer()

async def get_current_user(credentials:HTTPAuthorizationCredentials = Depends(_bearer)):
    token = credentials.credentials
    try:
        client = await get_admin_client()
        response = await client.auth.get_user(token)
        if response.user is None:
          raise ValueError
    except Exception:
        raise HTTPException(status_code=401,detail="Invalid or expired token")
    return response.user


# from core.database import SessionLocal
# from models.user import User
# from fastapi import HTTPException, Depends

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
        
# def get_current_user(db=Depends(get_db)):
#     #(mock auth) return the first user just to test
#     user = db.query(User).first()
#     if not user:
#         raise HTTPException(status_code=401, detail="User not found")
#     return user


# from core.database import SessionLocal
# from models.user import User
# from fastapi import HTTPException, Depends

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
        
# def get_current_user(db=Depends(get_db)):
#     #(mock auth) return the first user just to test
#     user = db.query(User).first()
#     if not user:
#         raise HTTPException(status_code=401, detail="User not found")
#     return user