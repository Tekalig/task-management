from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    """Schema for user registration requests."""

    username: str
    email: EmailStr
    password: str

class UserUpdate(BaseModel):
    """Schema for updating user information."""

    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

class UserResponse(BaseModel):
    """Schema for user data returned in responses (password is never exposed)."""

    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    """Schema for the JWT token response."""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Internal schema used when decoding JWT claims."""

    username: Optional[str] = None
