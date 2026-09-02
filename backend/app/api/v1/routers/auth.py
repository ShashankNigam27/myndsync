from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    RefreshTokenRequest,
    RefreshTokenResponse,
    UserRead,
)
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/token",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    summary="OAuth2 Password Token Flow (for Swagger UI / Form Auth)",
)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> LoginResponse:
    """OAuth2 password flow token endpoint. Used automatically by Swagger UI's Authorize dialog."""
    login_data = LoginRequest(email=form_data.username, password=form_data.password)
    return AuthService.authenticate(db, login_data)


@router.post(
    "/login",
    response_model=LoginResponse,
    status_code=status.HTTP_200_OK,
    summary="Authenticate Staff User (JSON API)",
)
async def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db),
) -> LoginResponse:
    """Authenticate a staff member (Counsellor, District/State/National official, Admin) using JSON body."""
    return AuthService.authenticate(db, login_data)


@router.post(
    "/refresh",
    response_model=RefreshTokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Refresh Access Token",
)
async def refresh_token(
    refresh_data: RefreshTokenRequest,
    db: Session = Depends(get_db),
) -> RefreshTokenResponse:
    """Issue a new short-lived access token using a valid refresh token."""
    return AuthService.refresh_token(db, refresh_data.refresh_token)


@router.get(
    "/me",
    response_model=UserRead,
    status_code=status.HTTP_200_OK,
    summary="Get Current Authenticated Staff User",
)
async def get_me(
    current_user: User = Depends(get_current_user),
) -> UserRead:
    """Return the profile and role details of the currently authenticated staff user."""
    return UserRead.model_validate(current_user)
