from app.modules.auth.infrastructure.auth_repository_supabase import AuthRepositorySupabase
from fastapi import Depends
from app.lib.JWT import jwt_handler
from datetime import timedelta
from app.modules.auth.domain.helpers import normalize_roles, mapRoleNameToRoleId
from app.core.config import settings
class AuthService:
    def __init__(self, auth_repository: AuthRepositorySupabase = Depends(AuthRepositorySupabase)):
        self.auth_repository = auth_repository

    async def register_user(self, registration_data, role: str = "customer"):
        registration_data = registration_data.dict().copy()
        registration_data["options"] = {
            "data": {
                "full_name": registration_data.get("full_name"),
                "phone": registration_data.get("phone"),
            }
        }
        sign_up_response = await self.auth_repository.sign_up(registration_data)
        await self.auth_repository.add_role_to_user(sign_up_response.user.id, mapRoleNameToRoleId(role))

    async def sign_in_with_password(self, login_data):
        login_response = await self.auth_repository.sign_in_with_password(login_data.dict())
        user_id = login_response.user.id
        raw_user = await self.auth_repository.get_user_by_id(user_id)
        user_data = {
            "id": raw_user["id"],
            "email": raw_user["email"],
            "phone": raw_user["phone_number"],
            "full_name": raw_user["full_name"],
            "roles": normalize_roles(raw_user.get("roles", [])),
        }
        token = jwt_handler.encode(
            user_data=user_data,
            expiry=timedelta(hours=1),
            refresh=False
        )

        refresh_token = jwt_handler.encode(
            user_data=user_data,
            expiry=timedelta(days=2),
            refresh=True
        )
        return {"user_data": user_data,"access_token": token, "refresh_token": refresh_token}

    async def logout(self):
        return await self.auth_repository.sign_out()

    async def refresh_token(self, user_data):
        token = jwt_handler.encode(
            user_data=user_data,
            expiry=timedelta(hours=1),
            refresh=False
        )

        return {"new_access_token": token}

    async def change_password(self, payload, user):
        sign_in_data = {
            "email": user.get("email"),
            "password": payload.current_password
        }
        login_response = await self.auth_repository.sign_in_with_password(sign_in_data)
        user_id = login_response.user.id
        if not user_id:
            raise ValueError("Current password is incorrect")
        await self.auth_repository.change_password(user_id, payload.new_password)

    def forgot_password(self, email, platform: str = "mobile"):
        # Need confirmation #
        redirect_url = f"{settings.WEB_URL}/reset-password" if platform == "web" else f"{settings.MOBILE_URL}reset-password"
        return self.auth_repository.forgot_password(email, redirect_url)

    def reset_password(self, reset_data):
        access_token = reset_data.access_token
        refresh_token = reset_data.refresh_token
        new_password = reset_data.new_password
        return self.auth_repository.reset_password(access_token, refresh_token, new_password)

    async def update_user_profile(self, user_id: str, payload):
        current_user = await self.auth_repository.get_user_by_id(user_id)
        if not current_user:
            raise ValueError("User not found")

        updated_data = {
            "full_name": payload.full_name,
            "phone_number": payload.phone,
        }

        # Update the user profile in the database
        response = await self.auth_repository.supabase_admin_client.from_("users").update(updated_data).eq("id", user_id).execute()
        if not response.data:
            raise ValueError("Failed to update user profile")

        return response.data[0]