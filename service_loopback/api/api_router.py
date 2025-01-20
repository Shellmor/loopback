from fastapi import APIRouter
from api.v1 import users_sellers, health
from core.config import settings
api_router = APIRouter()

api_router.include_router(users_sellers.router, prefix=settings.API_V1_STR, tags=["Пользователи продавцы"])
api_router.include_router(health.router, prefix=settings.API_V1_STR, tags=["Health"])