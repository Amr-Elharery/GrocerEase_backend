from app.core.exceptions import AppException, UnauthorizedException
from fastapi import status


class InvalidCredentialsError(UnauthorizedException):
    def __init__(self) -> None:
        super().__init__("Invalid email or password")


class EmailAlreadyRegisteredError(AppException):
    def __init__(self) -> None:
        super().__init__("Email is already registered", status.HTTP_409_CONFLICT)

class EmailNotVerifiedError(AppException):
    def __init__(self) -> None:
        super().__init__("Email is not verified", status.HTTP_403_FORBIDDEN)

class InvalidRefreshTokenError(UnauthorizedException):
    def __init__(self) -> None:
        super().__init__("Invalid or expired refresh token")


class InvalidTokenError(UnauthorizedException):
    def __init__(self) -> None:
        super().__init__("Invalid or expired reset token")

class PhoneAlreadyInUseError(AppException):
        def __init__(self)->None:
            super().__init__("Phone already used before")