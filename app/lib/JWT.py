import jwt
from app.core.config import settings
from datetime import datetime, timedelta
from typing import Optional


class JWT:
  _instance: Optional["JWT"] = None

  @classmethod
  def get_instance(cls) -> "JWT":
    if cls._instance is None:
      cls._instance = cls(secret_key=settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return cls._instance

  def __init__(self, secret_key: str, algorithm: str):
    self.secret_key = secret_key
    self.algorithm = algorithm

  def encode(self, user_data: dict, expiry: timedelta = timedelta(hours=1), refresh: bool = False) -> str:
    payload = {}
    payload["user"] = user_data
    payload["exp"] = datetime.utcnow() + expiry
    payload["refresh"] = refresh
    return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

  def decode(self, token: str) -> dict:
    if not token:
      raise ValueError("Missing token")
    try:
      decoded_payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
      return decoded_payload
    except jwt.ExpiredSignatureError:
      raise ValueError("Token has expired")
    except jwt.InvalidTokenError:
      raise ValueError("Invalid token")


# Singleton instance using application settings
jwt_handler = JWT.get_instance()