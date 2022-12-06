from fastapi import APIRouter

from project.app import image

api_router = APIRouter()

api_router.include_router(image.router, prefix="/image")