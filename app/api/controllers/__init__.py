from fastapi import APIRouter
from .health_check_controller import router as health_router
from .authentication_controller import router as auth_router
main_router = APIRouter()

main_router.include_router(health_router,
                           prefix="/health",
                           tags=["health"],
                           responses={404: {"description": "Not found"}})
main_router.include_router(auth_router,
                           prefix="",
                           tags=["auth"],
                           responses={404: {"description": "Not found"}})