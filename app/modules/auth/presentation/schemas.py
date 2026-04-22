from pydantic import BaseModel, EmailStr, model_validator, field_validator
import re

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
    current_password: str
    new_password: str

    
class ForgotPasswordRequest(BaseModel):
    email: EmailStr

class GeneralResponse(BaseModel):
    message:str

class ResetPasswordRequest(BaseModel):
    access_token: str
    new_password: str
    
class UpdateProfileRequest(BaseModel):
    full_name:str | None
    phone:str | None
    

    @field_validator("phone")
    @classmethod
    def validate_phone(cls,v:str|None)->str|None:
        if v is not None and not re.match(r"^\+[1-9]\d{7,14}$",v):
            raise ValueError("Phone must be in E.164 format (e.g. +201231255122)")    
        return v
    
class UpdateProfileResponse(BaseModel):
    full_name:str | None
    phone:str | None      
