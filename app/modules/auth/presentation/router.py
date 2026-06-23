from fastapi import APIRouter, Depends, status

from app.core.dependencies import verify_bearer_token, verify_refresh_token, get_current_user, require_roles

from app.modules.auth.application.services.auth_service import AuthService
from app.modules.auth.presentation.controller import AuthController
from app.modules.auth.domain.errors import AuthenticationError
from app.modules.auth.presentation.schemas import (
    ChangePasswordRequest,
    ForgotPasswordRequest,
    LoginRequest,
    UserProfileOut,
    LoginResponse,
    RegisterRequest,
    ResetPasswordRequest,
    UpdateProfileRequest,
)

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/me", response_model=UserProfileOut, status_code=status.HTTP_200_OK)
async def get_profile(current_user=Depends(get_current_user)):
    return current_user

@router.post("/customer/register", status_code=status.HTTP_201_CREATED)
async def register(payload: RegisterRequest, controller: AuthController = Depends(AuthController)):
    try:
        await controller.register(payload)
        return {"message": "User registered successfully"}
    except Exception as e:
        raise AuthenticationError(str(e))

@router.post("/vendor/register", status_code=status.HTTP_201_CREATED)
async def register(payload: RegisterRequest, controller: AuthController = Depends(AuthController)):
    try:
        await controller.register(payload, role="vendor")
        return {"message": "User registered successfully"}
    except Exception as e:
        raise AuthenticationError(str(e))

@router.post("/admin/register", status_code=status.HTTP_201_CREATED)
async def register(payload: RegisterRequest, controller: AuthController = Depends(AuthController)):
    try:
        await controller.register(payload, role="admin")
        return {"message": "User registered successfully"}
    except Exception as e:
        raise AuthenticationError(str(e))

@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def login(payload: LoginRequest, controller: AuthController = Depends(AuthController)):
    try:
        return await controller.sign_in_with_password(payload)
    except Exception as e:
        raise AuthenticationError(str(e))

@router.post("/refresh-token", status_code=status.HTTP_200_OK)
async def refresh_token(payload = Depends(verify_refresh_token), controller: AuthController = Depends(AuthController)):
    try:
        user_data = payload.get("user")
        new_token = await controller.refresh_token(user_data)
        return new_token
    except Exception as e:
        raise AuthenticationError(str(e))

# For Development and Testing purposes only
# @router.post("/check-token", status_code=status.HTTP_200_OK)
# async def check_token(current_user=Depends(get_current_user)):
#     return {"message": "Token is valid"}

# # For Development and Testing purposes only
# @router.post("/check-admin", status_code=status.HTTP_200_OK)
# async def check_admin(is_admin=Depends(require_roles(["admin"]))):
#     return {"message": "User is an admin"}

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
