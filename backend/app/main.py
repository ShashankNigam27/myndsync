from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.api import api_router
from app.core.config import settings
from app.core.exceptions import AppException


def create_application() -> FastAPI:
    application = FastAPI(
        title=settings.APP_NAME,
        openapi_url="/openapi.json",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Set up CORS middleware
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Restrict in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Centralized exception handling matching Section 11 format:
    # { "error": { "code": "STRING_CODE", "message": "human-readable", "details": {} } }
    @application.exception_handler(AppException)
    async def app_exception_handler(request: Request, exc: AppException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": exc.code,
                    "message": exc.message,
                    "details": exc.details,
                }
            },
        )

    @application.exception_handler(RequestValidationError)
    async def validation_exception_handler(request: Request, exc: RequestValidationError):
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Validation failed for request data",
                    "details": {"errors": exc.errors()},
                }
            },
        )

    # Root welcome route
    @application.get("/", tags=["Root"])
    async def root():
        return {
            "app": settings.APP_NAME,
            "docs": "/docs",
            "health": f"{settings.API_V1_STR}/health",
        }

    # Include API v1 router
    application.include_router(api_router, prefix=settings.API_V1_STR)

    return application


app = create_application()
