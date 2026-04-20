from pydantic import BaseModel, EmailStr, model_validator


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    confirmPassword: str
    full_name: str

    @model_validator(mode="after") # Used Model Validator for checking the matching between password and confirmpassword
    def passwords_match(self) -> "RegisterRequest":
        if self.password != self.confirmPassword:
            raise ValueError("Passwords do not match")
        return self

class LoginRequest(BaseModel):
        email:EmailStr
        password:str



class AuthResponse(BaseModel):
    message: str
    access_token: str | None = None
    refresh_token: str | None = None


class ChangePasswordRequest(BaseModel):
    user_id: str
    user_email: EmailStr
    current_password: str
    new_password: str


    
class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class GeneralResponse(BaseModel):
    message:str

class ResetPasswordRequest(BaseModel):
    access_token: str
    new_password: str
