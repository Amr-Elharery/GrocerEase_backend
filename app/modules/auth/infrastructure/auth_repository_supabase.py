from supabase import AsyncClient
from fastapi import Depends
from app.db.supabase_client import get_admin_client

class AuthRepositorySupabase:
    def __init__(self, supabase_client: AsyncClient = Depends(get_admin_client)) -> None:
        self.supabase_client = supabase_client

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

    async def sign_up(self, registration_data):
        response = await self.supabase_client.auth.sign_up(registration_data)
        return response

    async def sign_in_with_password(self, login_data):
      response = await self.supabase_client.auth.sign_in_with_password(login_data)
      return response.user.id

    async def sign_out(self):
        response = await self.supabase_client.auth.sign_out()
        return response

    # async def forgot_password(self, email: str):
    #     response = await self.supabase_client.auth.api.reset_password_for_email(email)
    #     return response

    # async def reset_password(self, access_token: str, new_password: str):
    #     response = await self.supabase_client.auth.api.update_user(access_token=access_token, password=new_password)
    #     return response