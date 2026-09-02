import uuid
from datetime import datetime, timezone
import jwt
from sqlalchemy.orm import Session

from app.core.exceptions import UnauthorizedException, ConflictException, NotFoundException
from app.core.security import verify_password, hash_password, create_access_token, create_refresh_token, decode_token
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.auth import LoginRequest, LoginResponse, RefreshTokenResponse, UserCreate


class AuthService:
    @staticmethod
    def authenticate(db: Session, login_data: LoginRequest) -> LoginResponse:
        user = UserRepository.get_by_email(db, login_data.email)
        if not user or not verify_password(login_data.password, user.hashed_password):
            raise UnauthorizedException(
                message="Invalid email or password",
                code="INVALID_CREDENTIALS",
            )

        if not user.is_active:
            raise UnauthorizedException(
                message="Account is inactive",
                code="USER_INACTIVE",
            )

        # Update last login
        user.last_login = datetime.now(timezone.utc)
        UserRepository.update(db, user)

        # Generate tokens
        token_payload = {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role,
            "authority_id": str(user.authority_id) if user.authority_id else None,
        }

        access_token = create_access_token(token_payload)
        refresh_token = create_refresh_token(token_payload)

        return LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            role=user.role,
            token_type="bearer",
        )

    @staticmethod
    def refresh_token(db: Session, refresh_token_str: str) -> RefreshTokenResponse:
        try:
            payload = decode_token(refresh_token_str)
            user_id_str = payload.get("sub")
            token_type = payload.get("type")

            if not user_id_str or token_type != "refresh":
                raise UnauthorizedException(
                    message="Invalid refresh token",
                    code="INVALID_REFRESH_TOKEN",
                )

            user_id = uuid.UUID(user_id_str)
        except (jwt.PyJWTError, ValueError):
            raise UnauthorizedException(
                message="Expired or invalid refresh token",
                code="INVALID_REFRESH_TOKEN",
            )

        user = UserRepository.get_by_id(db, user_id)
        if not user or not user.is_active:
            raise UnauthorizedException(
                message="User not found or inactive",
                code="USER_INACTIVE",
            )

        token_payload = {
            "sub": str(user.id),
            "email": user.email,
            "role": user.role,
            "authority_id": str(user.authority_id) if user.authority_id else None,
        }
        new_access_token = create_access_token(token_payload)

        return RefreshTokenResponse(
            access_token=new_access_token,
            token_type="bearer",
        )

    @staticmethod
    def create_user(db: Session, user_in: UserCreate) -> User:
        existing = UserRepository.get_by_email(db, user_in.email)
        if existing:
            raise ConflictException(
                message=f"User with email '{user_in.email}' already exists",
                code="USER_ALREADY_EXISTS",
            )

        user = User(
            full_name=user_in.full_name,
            email=user_in.email.strip().lower(),
            hashed_password=hash_password(user_in.password),
            role=user_in.role,
            authority_id=user_in.authority_id,
        )
        return UserRepository.create(db, user)
