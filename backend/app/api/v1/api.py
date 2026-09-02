from fastapi import APIRouter
from app.api.v1.routers import health, auth, victims, interactions, cases, debug

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(victims.router)
api_router.include_router(interactions.router)
api_router.include_router(cases.router)
api_router.include_router(debug.router)
