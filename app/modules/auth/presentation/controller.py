from app.modules.auth.application.services.auth_service import AuthService
from app.modules.auth.presentation.schemas import (
    ChangePasswordRequest,
    ForgotPasswordRequest,
    GeneralResponse,
    LoginRequest,
    AuthResponse,
    RegisterRequest,
    ResetPasswordRequest,
    UpdateProfileRequest,
    UpdateProfileResponse,
)


class AuthController:
    def __init__(self, service: AuthService) -> None:
        self.service = service

    async def register(self, payload: RegisterRequest) -> AuthResponse:
        return await self.service.register(payload.email, payload.password, payload.full_name)

    async def login(self,payload:LoginRequest)->AuthResponse:
        return await self.service.login(payload.email,payload.password)
    
    async def change_password(self, user_id: str, user_email: str,payload: ChangePasswordRequest) -> GeneralResponse:
       return  await self.service.change_password(user_id, user_email, payload.current_password, payload.new_password)

    async def forgot_password(self, payload: ForgotPasswordRequest) -> GeneralResponse:
       return  await self.service.forgot_password(payload.email)

    async def reset_password(self, payload: ResetPasswordRequest) -> GeneralResponse:
      return await self.service.reset_password(payload.access_token, payload.new_password)
  
    async def update_user_profile(self,user_id:str,payload:UpdateProfileRequest)->UpdateProfileResponse:
        return await self.service.update_user_profile(user_id,payload.full_name,payload.phone)
