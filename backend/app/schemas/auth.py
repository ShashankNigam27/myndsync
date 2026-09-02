import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    email: str = Field(..., description="Staff user email address")
    password: str = Field(..., min_length=6, description="Staff user password")


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    role: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class RefreshTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserRead(BaseModel):
    id: uuid.UUID
    full_name: str
    email: str
    role: str
    authority_id: Optional[uuid.UUID] = None
    auth_provider: str = "local"
    is_active: bool
    last_login: Optional[datetime] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class UserCreate(BaseModel):
    full_name: str
    email: str
    password: str
    role: str
    authority_id: Optional[uuid.UUID] = None
