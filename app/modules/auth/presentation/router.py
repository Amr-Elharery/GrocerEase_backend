from fastapi import APIRouter, Depends, status, HTTPException

from app.core.dependencies import get_current_user
from app.db.supabase_client import get_admin_client, get_anon_client
from app.modules.auth.application.services.auth_service import AuthService
from app.modules.auth.presentation.controller import AuthController
from app.modules.auth.domain.errors import AuthenticationError, InvalidCredentialsError
from app.modules.auth.presentation.schemas import (
    ChangePasswordRequest,
    ForgotPasswordRequest,
    LoginRequest,
    RegisterRequest,
    AuthResponse,
    ResetPasswordRequest,
    UpdateProfileRequest,
)

router = APIRouter(prefix="/auth", tags=["auth"])

# @router.get("/me")
# async def get_profile(controller: AuthController = Depends(AuthController)):
#     return {"user_id":user.id,"email":user.email,   "full_name": user.user_metadata.get("full_name"),
#     "created_at": user.created_at,}

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(payload: RegisterRequest, controller: AuthController = Depends(AuthController)):
    try:
        return await controller.register(payload)
    except Exception as e:
        raise AuthenticationError(str(e))

@router.post("/login", status_code=status.HTTP_200_OK)
async def login(payload: LoginRequest, controller: AuthController = Depends(AuthController)):
    try:
        return await controller.sign_in_with_password(payload)
    except Exception as e:
        raise AuthenticationError(str(e))

# @router.post("/change-password", status_code=status.HTTP_200_OK)
# async def change_password(payload: ChangePasswordRequest, controller: AuthController = Depends(_get_controller),user = Depends(get_current_user)):
#     return await controller.change_password(user.id,user.email,payload)


# @router.post("/forgot-password", status_code=status.HTTP_200_OK)
# async def forgot_password(payload: ForgotPasswordRequest, controller: AuthController = Depends(_get_controller)):
#    return await controller.forgot_password(payload)


# @router.post("/reset-password", status_code=status.HTTP_200_OK)
# async def reset_password(payload: ResetPasswordRequest, controller: AuthController = Depends(_get_controller)):
#     return await controller.reset_password(payload)

# @router.put("/profile",status_code=status.HTTP_200_OK)
# async def update_user_profile(payload:UpdateProfileRequest,controller: AuthController = Depends(_get_controller),user= Depends(get_current_user)):
#     return await controller.update_user_profile(user.id,payload)
