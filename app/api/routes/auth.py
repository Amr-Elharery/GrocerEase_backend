from fastapi import APIRouter, Depends, HTTPException
from schemas.auth_schema import *
from services.auth_service import AuthService
from core.dependencies import get_db
from core.dependencies import get_current_user
from repositories.user_repo import UserRepository

user_repo = UserRepository()
router = APIRouter(prefix="/auth")
auth_service = AuthService()

@router.put("/change-password")
def change_password(data: ChangePasswordRequest,
                    db=Depends(get_db),
                    current_user=Depends(get_current_user)):

    try:
        auth_service.change_password(db, current_user, data.current_password, data.new_password)
        return {"message": "Password updated successfully"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/forgot-password")
def forgot_password(data: ForgotPasswordRequest, db=Depends(get_db)):

    token = auth_service.forgot_password(db, data.email, user_repo)

    if token is None:
        return {"message": "If the email exists, a reset link will be sent"}
    
    # In production, send this token via email
    # For development, return it in the response
    return {"message": "a reset link has been sent", "reset_token": token}


@router.post("/reset-password")
def reset_password(data: ResetPasswordRequest, db=Depends(get_db)):

    try:
        auth_service.reset_password(db, data.token, data.new_password, user_repo)
        return {"message": "Password reset successful"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    