from supabase import Client

from app.modules.auth.domain.errors import EmailAlreadyRegisteredError
from app.modules.auth.presentation.schemas import RegisterResponse


class AuthService:

    def __init__(self, client: Client) -> None:
        self.client = client

    def register(self, email: str, password: str, full_name: str) -> RegisterResponse:
        response = self.client.auth.sign_up(
            {"email": email, "password": password, "options": {"data": {"full_name": full_name}}}
        )
        if response.user is None:
            raise EmailAlreadyRegisteredError()

        session = response.session
        if session:
            return RegisterResponse(
                message="Registration successful",
                access_token=session.access_token,
                refresh_token=session.refresh_token,
            )
        return RegisterResponse(message="Registration successful. Please verify your email.")
