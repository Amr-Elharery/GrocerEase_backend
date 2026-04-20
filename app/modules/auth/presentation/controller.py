from app.modules.auth.application.services.auth_service import AuthService
from app.modules.auth.presentation.schemas import (
    ChangePasswordRequest,
    ForgotPasswordRequest,
    GeneralResponse,
    RegisterRequest,
    RegisterResponse,
    ResetPasswordRequest,
)


class AuthController:
    def __init__(self, service: AuthService) -> None:
        self.service = service

    def register(self, payload: RegisterRequest) -> RegisterResponse:
        return self.service.register(payload.email, payload.password, payload.full_name)

    def change_password(self, payload: ChangePasswordRequest) -> GeneralResponse:
       return  self.service.change_password(payload.user_id, payload.user_email, payload.current_password, payload.new_password)

    def forgot_password(self, payload: ForgotPasswordRequest) -> GeneralResponse:
       return  self.service.forgot_password(payload.email)

    def reset_password(self, payload: ResetPasswordRequest) -> GeneralResponse:
      return self.service.reset_password(payload.access_token, payload.new_password)
