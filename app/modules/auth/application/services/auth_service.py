from app.modules.auth.infrastructure.auth_repository_supabase import AuthRepositorySupabase
from app.modules.notifications.application.services.notifications_service import NotificationsService
from fastapi import Depends
from app.lib.JWT import jwt_handler
from datetime import timedelta
from app.modules.auth.domain.helpers import normalize_roles, mapRoleNameToRoleId
from app.core.config import settings
class AuthService:
    def __init__(self, auth_repository: AuthRepositorySupabase = Depends(AuthRepositorySupabase), notification_service: NotificationsService = Depends(NotificationsService)):
        self.auth_repository = auth_repository
        self.notification_service = notification_service

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
        await self.notification_service.send_welcome_notification(sign_up_response.user.id)

    async def sign_in_with_password(self, login_data):
        login_response = await self.auth_repository.sign_in_with_password(login_data.dict())
        user_id = login_response.user.id
        raw_user = await self.auth_repository.get_user_by_id(user_id)
        if raw_user["is_active"] is False:
            raise ValueError("User account is suspended. Please contact support.")
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
        redirect_url = f"{settings.WEB_URL}/auth/reset-password" if platform == "web" else f"{settings.MOBILE_URL}reset-password"
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

    async def get_all_users(self, current_user, role: str | None = None, status: str | None = None, page: int = 1, page_size: int = 10):
        if "admin" not in current_user.get("roles", []):
            raise PermissionError("You do not have permission to view users.")

        if page < 1:
            raise ValueError("page must be greater than or equal to 1.")
        if page_size < 1:
            raise ValueError("page_size must be greater than or equal to 1.")

        is_active = None
        if status is not None:
            status = status.lower()
            if status == "active":
                is_active = True
            elif status == "suspended":
                is_active = False
            else:
                raise ValueError("Invalid status filter. Use 'active' or 'suspended'.")

        raw_users = await self.auth_repository.get_all_users(is_active=is_active)

        users = []
        for raw_user in raw_users:
            roles = normalize_roles(raw_user.get("roles", []))
            # Exclude admins from the results
            if "admin" in roles and role != "admin":
                continue
            # Optional filter by role (e.g. customer, vendor, delivery)
            if role is not None and role not in roles:
                continue
            users.append({
                "id": raw_user["id"],
                "email": raw_user["email"],
                "phone": raw_user["phone_number"],
                "full_name": raw_user["full_name"],
                "roles": roles,
                "is_active": raw_user.get("is_active", True),
            })

        total = len(users)
        total_pages = (total + page_size - 1) // page_size
        start = (page - 1) * page_size
        end = start + page_size

        return {
            "items": users[start:end],
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
        }

    # async def get_user_by_id(self, user_id: str, current_user):
    #     if "admin" not in current_user.get("roles", []) or "vendor" not in current_user.get("roles", []):
    #         raise PermissionError("You do not have permission to view user details.")

    #     raw_user = await self.auth_repository.get_user_by_id(user_id)
    #     if not raw_user:
    #         raise ValueError("User not found")

    #     roles = normalize_roles(raw_user.get("roles", []))
    #     return {
    #         "id": raw_user["id"],
    #         "email": raw_user["email"],
    #         "phone": raw_user["phone_number"],
    #         "full_name": raw_user["full_name"],
    #         "roles": roles,
    #         "is_active": raw_user.get("is_active", True),
    #     }

    async def suspend_user_account(self, user_id: str, current_user):
        if "admin" not in current_user.get("roles", []):
            raise PermissionError("You do not have permission to suspend user accounts.")
        user_to_suspend = await self.auth_repository.get_user_by_id(user_id)
        if not user_to_suspend:
            raise ValueError("User not found")
        await self.auth_repository.suspend_user_account(user_id)

    async def activate_user_account(self, user_id: str, current_user):
        if "admin" not in current_user.get("roles", []):
            raise PermissionError("You do not have permission to activate user accounts.")
        user_to_activate = await self.auth_repository.get_user_by_id(user_id)
        if not user_to_activate:
            raise ValueError("User not found")
        await self.auth_repository.activate_user_account(user_id)