from app.modules.auth.application.services.auth_service import AuthService
from app.modules.auth.presentation.schemas import RegisterRequest, RegisterResponse


class AuthController:
    def __init__(self, service: AuthService) -> None:
        self.service = service

    def register(self, payload: RegisterRequest) -> RegisterResponse:
        return self.service.register(payload.email, payload.password, payload.full_name)
