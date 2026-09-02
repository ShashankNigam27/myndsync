from typing import Any, Dict, Optional


class AppException(Exception):
    """Base application exception supporting standard error format."""

    def __init__(
        self,
        code: str,
        message: str,
        status_code: int = 400,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(message)


class NotFoundException(AppException):
    def __init__(
        self,
        message: str = "Resource not found",
        code: str = "NOT_FOUND",
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            code=code, message=message, status_code=404, details=details
        )


class UnauthorizedException(AppException):
    def __init__(
        self,
        message: str = "Authentication required or invalid credentials",
        code: str = "UNAUTHORIZED",
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            code=code, message=message, status_code=401, details=details
        )


class ForbiddenException(AppException):
    def __init__(
        self,
        message: str = "Permission denied for this action",
        code: str = "FORBIDDEN",
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            code=code, message=message, status_code=403, details=details
        )


class ConflictException(AppException):
    def __init__(
        self,
        message: str = "Resource conflict",
        code: str = "CONFLICT",
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            code=code, message=message, status_code=409, details=details
        )


class BadRequestException(AppException):
    def __init__(
        self,
        message: str = "Bad request",
        code: str = "BAD_REQUEST",
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        super().__init__(
            code=code, message=message, status_code=400, details=details
        )
