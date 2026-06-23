from supabase import AsyncClient
from fastapi import Depends
from app.db.supabase_client import get_admin_client, get_anon_client

class AuthRepositorySupabase:
    def __init__(self, supabase_client: AsyncClient = Depends(get_anon_client), supabase_admin_client: AsyncClient = Depends(get_admin_client)) -> None:
        self.supabase_client = supabase_client
        self.supabase_admin_client = supabase_admin_client

    async def get_user_by_id(self, user_id: str):
        response = await self.supabase_client.from_("users").select("""
                          id,
                          email,
                          phone_number,
                          full_name,

                          roles:users_roles(
                            role:roles(
                                role_name
                            )
                          )
        """).eq("id", user_id).single().execute()
        return response.data

    async def add_role_to_user(self, user_id: str, role_id: int):
        response = await self.supabase_client.from_("users_roles").insert({
            "user_id": user_id,
            "role_id": role_id
        }).execute()
        return response.data

    async def sign_up(self, registration_data):
        response = await self.supabase_client.auth.sign_up(registration_data)
        return response

    async def sign_in_with_password(self, login_data):
        response = await self.supabase_client.auth.sign_in_with_password(login_data)
        return response

    async def sign_out(self):
        response = await self.supabase_client.auth.sign_out()
        return response

    async def change_password(self, user_id: str, new_password: str):
        response = await self.supabase_admin_client.auth.admin.update_user_by_id(user_id, {"password": new_password})
        return response

    async def forgot_password(self, email: str, redirect_url: str):
        response = await self.supabase_client.auth.reset_password_email(email, {
            "redirect_to": redirect_url
        })
        return response

    async def reset_password(self, access_token: str, refresh_token: str, new_password: str):
        await self.supabase_client.auth.set_session(access_token, refresh_token)
        response = await self.supabase_client.auth.update_user({"password": new_password})
        return response

    async def update_user_profile(self, user_id: str, profile_data: dict):
        await self.supabase_admin_client.auth.admin.update_user_by_id(
            user_id,
            {
                "user_metadata": {
                    "full_name": profile_data["full_name"],
                    "phone": profile_data["phone_number"]
                    }
            })
        await self.supabase_client.from_("users").update({
            "full_name": profile_data["full_name"],
            "phone_number": profile_data["phone_number"]
            }).eq("id", user_id).execute()
