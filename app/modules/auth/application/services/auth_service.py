from supabase_auth.errors import AuthApiError
from supabase import AsyncClient

from app.modules.auth.domain.errors import EmailAlreadyRegisteredError, EmailNotVerifiedError, InvalidCredentialsError, InvalidTokenError, PhoneAlreadyInUseError
from app.modules.auth.presentation.schemas import AuthResponse,GeneralResponse, UpdateProfileResponse


class AuthService:

    def __init__(self, admin_client: AsyncClient, anon_client: AsyncClient) -> None:
        self.client = admin_client
        self._anon = anon_client

    async def register(self, email: str, password: str, full_name: str) -> AuthResponse:
        try:
            response = await self.client.auth.sign_up(
            {"email": email, "password": password, "options": {"data": {"full_name": full_name}}}
            )
        except AuthApiError as e:    
            if "already registered" in str(e).lower():
                raise EmailAlreadyRegisteredError()
            raise

        session = response.session
        if session:
            return AuthResponse(
            message="Registration successful",
            access_token=session.access_token,
            refresh_token=session.refresh_token,
        )
        return AuthResponse(message="Registration successful. Please verify your email.")

    async def login(self,email:str,password:str)->AuthResponse:
       try:
        response = await self.client.auth.sign_in_with_password({"email":email,"password":password})
        
       except AuthApiError as e:
           if "Email not confirmed" in str(e):
               raise EmailNotVerifiedError()
           raise InvalidCredentialsError()
               
       if response.user is None:
            raise InvalidCredentialsError()
        
       session = response.session
       if session:
            return AuthResponse(
                message="Login Successful",
                access_token=session.access_token,
                refresh_token=session.refresh_token
            )
       raise  EmailNotVerifiedError()   
            
        
    async def change_password(self, user_id: str, user_email: str, current_password: str, new_password: str) -> GeneralResponse:
        try:
            sign_in_response = await self._anon.auth.sign_in_with_password({"email": user_email, "password": current_password})
        except AuthApiError:
            raise InvalidCredentialsError()

        access_token = sign_in_response.session.access_token
        await self._anon.auth.set_session(access_token, sign_in_response.session.refresh_token)
        await self._anon.auth.update_user({"password": new_password})
        try:
            await self._anon.auth.sign_in_with_password({"email": user_email, "password": new_password})
            return GeneralResponse(message="Password changed Successfully")
        except AuthApiError:
            raise InvalidCredentialsError()

    async def forgot_password(self, email: str) -> None:
        await self.client.auth.reset_password_for_email(email)
        return GeneralResponse(message="Check your email for password reset")

    async def reset_password(self, access_token: str, new_password: str) -> None:
        try:
            user_response = await self.client.auth.get_user(access_token)
        except AuthApiError:
            raise InvalidTokenError()

        await self.client.auth.admin.update_user_by_id(user_response.user.id, {"password": new_password})
        return GeneralResponse(message="Password reseted Successfully")
            
    async def update_user_profile(self,user_id:str,user_full_name:str |None ,user_phone:str | None)->UpdateProfileResponse:
        payload = {}
        if user_full_name is not None:
            payload["user_metadata"] = {"full_name": user_full_name}
        if user_phone is not None:
            payload["phone"] = user_phone
        try:
            
            response = await self.client.auth.admin.update_user_by_id(user_id,payload)
        
        except AuthApiError as e:
            if "already" in str(e).lower() or "phone" in str(e).lower():
                raise PhoneAlreadyInUseError
            raise    
        
        return UpdateProfileResponse(full_name=response.user.user_metadata.get("full_name"),
        phone= response.user.phone)
        