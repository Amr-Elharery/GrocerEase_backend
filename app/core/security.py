import bcrypt
import secrets
from datetime import datetime, timedelta

def hash_password(password: str):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain, hashed):
    return bcrypt.checkpw(plain.encode('utf-8'), hashed.encode('utf-8'))

def generate_reset_token():
    return secrets.token_urlsafe(32)

def get_token_expiry():
    return datetime.utcnow() + timedelta(hours=1)