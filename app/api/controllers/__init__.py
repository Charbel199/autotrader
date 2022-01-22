from fastapi import APIRouter
from .health_check_controller import router as health_router

main_router = APIRouter()

main_router.include_router(health_router,
                           prefix="/health",
                           tags=["health"],
                           responses={404: {"description": "Not found"}})
