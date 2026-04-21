from fastapi import APIRouter, Depends, status

from app.core.dependencies import get_current_user
from app.db.supabase_client import get_admin_client, get_anon_client
from app.modules.auth.application.services.auth_service import AuthService
from app.modules.auth.presentation.controller import AuthController
from app.modules.auth.presentation.schemas import (
    ChangePasswordRequest,
    ForgotPasswordRequest,
    LoginRequest,
    RegisterRequest,
    AuthResponse,
    ResetPasswordRequest,
)

router = APIRouter(prefix="/auth", tags=["auth"])


def _get_controller() -> AuthController:
    return AuthController(AuthService(get_admin_client(), get_anon_client()))

@router.get("/me")
def get_profile(user = Depends(get_current_user)):
    return {"user_id":user.id,"email":user.email,   "full_name": user.user_metadata.get("full_name"),
    "created_at": user.created_at,}

@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, controller: AuthController = Depends(_get_controller)):
    return controller.register(payload)

@router.post("/login",response_model=AuthResponse,status_code=status.HTTP_200_OK)
def login(payload:LoginRequest,controller: AuthController = Depends(_get_controller)):
    return controller.login(payload)

@router.post("/change-password", status_code=status.HTTP_200_OK)
def change_password(payload: ChangePasswordRequest, controller: AuthController = Depends(_get_controller),user = Depends(get_current_user)):
    return controller.change_password(user.id,user.email,payload)


@router.post("/forgot-password", status_code=status.HTTP_200_OK)
def forgot_password(payload: ForgotPasswordRequest, controller: AuthController = Depends(_get_controller)):
   return controller.forgot_password(payload)


@router.post("/reset-password", status_code=status.HTTP_200_OK)
def reset_password(payload: ResetPasswordRequest, controller: AuthController = Depends(_get_controller)):
    return controller.reset_password(payload)
