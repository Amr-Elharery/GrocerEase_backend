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