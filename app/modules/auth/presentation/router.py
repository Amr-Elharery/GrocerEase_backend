from fastapi import APIRouter, Depends, status

from app.db.supabase_client import get_admin_client
from app.modules.auth.application.services.auth_service import AuthService
from app.modules.auth.presentation.controller import AuthController
from app.modules.auth.presentation.schemas import RegisterRequest, RegisterResponse

router = APIRouter(prefix="/auth", tags=["auth"])


def _get_controller() -> AuthController:
    return AuthController(AuthService(get_admin_client()))


@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, controller: AuthController = Depends(_get_controller)):
    return controller.register(payload)
