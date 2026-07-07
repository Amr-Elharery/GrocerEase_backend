from app.modules.auth.application.services.auth_service import AuthService
from fastapi import Depends

class AuthController:
    def __init__(self, auth_service: AuthService = Depends(AuthService)):
        self.auth_service = auth_service

    async def register(self, registration_data, role: str = "customer"):
        return await self.auth_service.register_user(registration_data, role=role)

    async def sign_in_with_password(self, login_data):
        return await self.auth_service.sign_in_with_password(login_data)

    async def logout(self):
        return await self.auth_service.logout()

    async def refresh_token(self, user_data):
        return await self.auth_service.refresh_token(user_data)

    async def change_password(self, payload, user):
        return await self.auth_service.change_password(payload, user)

    async def forgot_password(self, payload, platform: str = "mobile"):
        return await self.auth_service.forgot_password(payload.email, platform)

    async def reset_password(self, payload):
        return await self.auth_service.reset_password(payload)

    async def update_user_profile(self, user_id: str, payload):
        return await self.auth_service.update_user_profile(user_id, payload)

    async def get_all_users(self, current_user, role: str | None = None, status: str | None = None, page: int = 1, page_size: int = 10):
        return await self.auth_service.get_all_users(current_user, role=role, status=status, page=page, page_size=page_size)

    # async def get_user_by_id(self, user_id: str, current_user):
    #     return await self.auth_service.get_user_by_id(user_id, current_user)

    async def suspend_user_account(self, user_id: str, current_user):
        return await self.auth_service.suspend_user_account(user_id, current_user)

    async def activate_user_account(self, user_id: str, current_user):
        return await self.auth_service.activate_user_account(user_id, current_user)