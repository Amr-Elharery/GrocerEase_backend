from supabase_auth.errors import AuthApiError
from supabase import Client

from app.modules.auth.domain.errors import EmailAlreadyRegisteredError, EmailNotVerifiedError, InvalidCredentialsError, InvalidTokenError, PhoneAlreadyInUseError
from app.modules.auth.presentation.schemas import AuthResponse,GeneralResponse, UpdateProfileResponse


class AuthService:

    def __init__(self, admin_client: Client, anon_client: Client) -> None:
        self.client = admin_client
        self._anon = anon_client

    def register(self, email: str, password: str, full_name: str) -> AuthResponse:
        response = self.client.auth.sign_up(
            {"email": email, "password": password, "options": {"data": {"full_name": full_name}}}
        )
        if response.user is None:
            raise EmailAlreadyRegisteredError()

        session = response.session
        if session:
            return AuthResponse(
                message="Registration successful",
                access_token=session.access_token,
                refresh_token=session.refresh_token,
            )
        return AuthResponse(message="Registration successful. Please verify your email.")

    def login(self,email:str,password:str)->AuthResponse:
       try:
        response = self.client.auth.sign_in_with_password({"email":email,"password":password})
        
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
            
        
    def change_password(self, user_id: str, user_email: str, current_password: str, new_password: str) -> GeneralResponse:
        try:
            sign_in_response = self._anon.auth.sign_in_with_password({"email": user_email, "password": current_password})
        except AuthApiError:
            raise InvalidCredentialsError()

        access_token = sign_in_response.session.access_token
        self._anon.auth.set_session(access_token, sign_in_response.session.refresh_token)
        self._anon.auth.update_user({"password": new_password})
        try:
            self._anon.auth.sign_in_with_password({"email": user_email, "password": new_password})
            return GeneralResponse(message="Password changed Successfully")
        except AuthApiError:
            raise InvalidCredentialsError()


    def forgot_password(self, email: str) -> None:
        self.client.auth.reset_password_for_email(email)
        return GeneralResponse(message="Check your email for password reset")

    def reset_password(self, access_token: str, new_password: str) -> None:
        try:
            user_response = self.client.auth.get_user(access_token)
        except AuthApiError:
            raise InvalidTokenError()

        self.client.auth.admin.update_user_by_id(user_response.user.id, {"password": new_password})
        return GeneralResponse(message="Password reseted Successfully")
            

    def update_user_profile(self,user_id:str,user_full_name:str |None ,user_phone:str | None)->UpdateProfileResponse:
        payload = {}
        if user_full_name is not None:
            payload["user_metadata"] = {"full_name": user_full_name}
        if user_phone is not None:
            payload["phone"] = user_phone
        try:
            
            response = self.client.auth.admin.update_user_by_id(user_id,payload)
        
        except AuthApiError as e:
            if "already" in str(e).lower() or "phone" in str(e).lower():
                raise PhoneAlreadyInUseError
            raise    
        
        return UpdateProfileResponse(full_name=response.user.user_metadata.get("full_name"),
        phone= response.user.phone)
        