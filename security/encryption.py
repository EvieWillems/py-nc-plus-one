import bcrypt
import os
from datetime import datetime, timezone, timedelta
import jwt

def hash_password(password:str) -> str:
    return bcrypt.hashpw(password.encode(),bcrypt.gensalt(12)).decode()

def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(),hashed_password.encode())

def get_algorithm():
    ALGORITHM = os.getenv('ALGORITHM')
    return ALGORITHM

def get_secret():
    secret = os.getenv('JWT_SECRET')
    return secret

def create_access_token(id: int) -> str:
    payload = {
        'sub': str(id),
        'exp': datetime.now(timezone.utc)+timedelta(hours=1)
    }
    return jwt.encode(payload,get_secret(),algorithm=get_algorithm())