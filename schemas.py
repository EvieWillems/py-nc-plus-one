from pydantic import BaseModel, EmailStr
from typing import Optional
from fastapi.security import HTTPBearer

class NewUserProfile(BaseModel):
    name: str
    email: EmailStr
    password: str

class LoginDetails(BaseModel):
    email: EmailStr
    password: str

user_auth_scheme = HTTPBearer(auto_error=False)