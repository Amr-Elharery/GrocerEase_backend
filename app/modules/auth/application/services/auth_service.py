from app.modules.auth.infrastructure.auth_repository_supabase import AuthRepositorySupabase
from fastapi import Depends
from app.lib.JWT import jwt_handler
from datetime import timedelta
from app.modules.auth.domain.helpers import normalize_roles, mapRoleNameToRoleId
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
        user_id = await self.auth_repository.sign_in_with_password(login_data.dict())
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

    async def refresh_token(self, user_data):
        token = jwt_handler.encode(
            user_data=user_data,
            expiry=timedelta(hours=1),
            refresh=False
        )

        return {"new_access_token": token}

    # def forgot_password(self, email):
    #     return self.auth_repository.forgot_password(email)

    # def reset_password(self, reset_data):
    #     return self.auth_repository.reset_password(reset_data)