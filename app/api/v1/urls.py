from fastapi import APIRouter
from .endpoints.auth import router as auth_router
from .endpoints.user import router as user_router
from .endpoints.health import router as health_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(auth_router)
api_router.include_router(user_router)
