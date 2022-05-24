from fastapi import APIRouter

from app.api.api_v1.endpoints import poetry


api_router = APIRouter()
api_router.include_router(poetry.router, prefix="/poetries", tags=["poetries"])
