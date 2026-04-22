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

    def register(self, payload: RegisterRequest) -> AuthResponse:
        return self.service.register(payload.email, payload.password, payload.full_name)

    def login(self,payload:LoginRequest)->AuthResponse:
        return self.service.login(payload.email,payload.password)
    
    def change_password(self, user_id: str, user_email: str,payload: ChangePasswordRequest) -> GeneralResponse:
       return  self.service.change_password(user_id, user_email, payload.current_password, payload.new_password)

    def forgot_password(self, payload: ForgotPasswordRequest) -> GeneralResponse:
       return  self.service.forgot_password(payload.email)

    def reset_password(self, payload: ResetPasswordRequest) -> GeneralResponse:
      return self.service.reset_password(payload.access_token, payload.new_password)
  
    def update_user_profile(self,user_id:str,payload:UpdateProfileRequest)->UpdateProfileResponse:
        return self.service.update_user_profile(user_id,payload.full_name,payload.phone)
