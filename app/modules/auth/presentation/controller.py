from app.modules.auth.application.services.auth_service import AuthService
from fastapi import Depends

class AuthController:
    def __init__(self, auth_service: AuthService = Depends(AuthService)):
        self.auth_service = auth_service

    async def register(self, registration_data, role: str = "customer"):
        return await self.auth_service.register_user(registration_data, role=role)

    async def sign_in_with_password(self, login_data):
        return await self.auth_service.sign_in_with_password(login_data)

    async def refresh_token(self, user_data):
        return await self.auth_service.refresh_token(user_data)

    # async def forgot_password(self, payload):
    #     return await self.auth_service.forgot_password(payload.email)

    # async def reset_password(self, payload):
    #     return await self.auth_service.reset_password(payload)