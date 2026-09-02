import uuid
from typing import Callable, List, Optional
import jwt
from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.security import oauth2_scheme, decode_token
from app.core.exceptions import UnauthorizedException, ForbiddenException
from app.db.session import get_db
from app.models.user import User


async def get_current_user(
    token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    """Extract and validate current authenticated staff user from OAuth2 Bearer token."""
    if not token:
        raise UnauthorizedException(
            message="Not authenticated", code="NOT_AUTHENTICATED"
        )

    try:
        payload = decode_token(token)
        user_id_str = payload.get("sub")
        token_type = payload.get("type")

        if not user_id_str or token_type != "access":
            raise UnauthorizedException(
                message="Invalid token payload", code="INVALID_TOKEN"
            )

        user_id = uuid.UUID(user_id_str)
    except (jwt.PyJWTError, ValueError):
        raise UnauthorizedException(
            message="Invalid or expired token", code="INVALID_TOKEN"
        )

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise UnauthorizedException(
            message="User not found", code="USER_NOT_FOUND"
        )
    if not user.is_active:
        raise ForbiddenException(
            message="User account is inactive", code="USER_INACTIVE"
        )

    return user


def require_roles(*allowed_roles: str) -> Callable:
    """Dependency factory that validates current user has one of the allowed roles."""
    async def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles:
            raise ForbiddenException(
                message=f"Role '{current_user.role}' is not authorized to access this resource",
                code="FORBIDDEN_ROLE",
                details={"required_roles": list(allowed_roles), "user_role": current_user.role},
            )
        return current_user

    return role_checker


async def get_optional_current_user(
    token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> Optional[User]:
    """Extract current user if valid token present, otherwise None."""
    if not token:
        return None
    try:
        return await get_current_user(token=token, db=db)
    except UnauthorizedException:
        return None
