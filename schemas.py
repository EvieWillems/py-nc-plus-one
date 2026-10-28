from pydantic import BaseModel, EmailStr
from typing import Optional


class NewUserProfile(BaseModel):
    name: str
    email: EmailStr
    password: str

class LoginDetails(BaseModel):
    email: EmailStr
    password: str