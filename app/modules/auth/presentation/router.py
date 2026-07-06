from fastapi import APIRouter, Depends, Query, status

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
    UpdateProfileResponse,
    UsersListItemOut,
    PaginatedUsersOut
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

@router.post("/delivery/register", status_code=status.HTTP_201_CREATED)
async def register(payload: RegisterRequest, controller: AuthController = Depends(AuthController)):
    try:
        await controller.register(payload, role="delivery")
        return {"message": "User registered successfully"}
    except Exception as e:
        raise AuthenticationError(str(e))

@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def login(payload: LoginRequest, controller: AuthController = Depends(AuthController)):
    try:
        return await controller.sign_in_with_password(payload)
    except Exception as e:
        raise AuthenticationError(str(e))

@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout(controller: AuthController = Depends(AuthController)):
    try:
        await controller.logout()
        return {"message": "User logged out successfully"}
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

@router.post("/change-password", status_code=status.HTTP_200_OK)
async def change_password(payload: ChangePasswordRequest, user = Depends(get_current_user), controller: AuthController = Depends(AuthController)):
    try:
        await controller.change_password(payload, user)
        return {"message": "Password changed successfully"}
    except Exception as e:
        raise AuthenticationError(str(e))

# Tested and working
@router.post("/web/forgot-password", status_code=status.HTTP_200_OK)
async def forgot_password(payload: ForgotPasswordRequest, controller: AuthController = Depends(AuthController)):
    return await controller.forgot_password(payload, platform="web")

# Deprecated, use /web/forgot-password
@router.post("/mobile/forgot-password", status_code=status.HTTP_200_OK)
async def forgot_password(payload: ForgotPasswordRequest, controller: AuthController = Depends(AuthController)):
    return await controller.forgot_password(payload)

# Working
@router.post("/reset-password", status_code=status.HTTP_200_OK)
async def reset_password(payload: ResetPasswordRequest, controller: AuthController = Depends(AuthController)):
    return await controller.reset_password(payload)

@router.put("/profile", response_model = UpdateProfileResponse, status_code=status.HTTP_200_OK)
async def update_user_profile(payload: UpdateProfileRequest, controller: AuthController = Depends(AuthController), user = Depends(get_current_user)):
    updated_user = await controller.update_user_profile(user.get("id"), payload)
    return {"message": "User profile updated successfully", "user": updated_user}


# Get All Users (except admins) - admin only, with optional role/status filters and pagination
@router.get("/users", response_model=PaginatedUsersOut, status_code=status.HTTP_200_OK)
async def get_all_users(
    role: str | None = None,
    status: str | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    controller: AuthController = Depends(AuthController),
    user = Depends(get_current_user),
):
    try:
        return await controller.get_all_users(user, role=role, status=status, page=page, page_size=page_size)
    except Exception as e:
        raise AuthenticationError(str(e))

@router.get("/users/{user_id}", response_model=UsersListItemOut, status_code=status.HTTP_200_OK)
async def get_user_by_id(user_id: str, controller: AuthController = Depends(AuthController), user = Depends(get_current_user)):
    try:
        return await controller.get_user_by_id(user_id, user)
    except Exception as e:
        raise AuthenticationError(str(e))

# Suspend user account
@router.post("/suspend/{user_id}", status_code=status.HTTP_200_OK)
async def suspend_user_account(user_id: str, controller: AuthController = Depends(AuthController), user = Depends(get_current_user)):
    try:
        await controller.suspend_user_account(user_id, user)
        return {"message": "User account suspended successfully"}
    except Exception as e:
        raise AuthenticationError(str(e))

# Activate user account
@router.post("/activate/{user_id}", status_code=status.HTTP_200_OK)
async def activate_user_account(user_id: str, controller: AuthController = Depends(AuthController), user = Depends(get_current_user)):
    try:
        await controller.activate_user_account(user_id, user)
        return {"message": "User account activated successfully"}
    except Exception as e:
        raise AuthenticationError(str(e))