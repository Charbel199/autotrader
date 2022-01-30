from fastapi import APIRouter
from .health_check_controller import router as health_router
from .user_controller import router as auth_router
from .bot_controller import router as bot_router
from .bot_instance_controller import router as bot_instance_router
from .exchange_controller import router as exchange_router
from .exchange_instance_controller import router as exchange_instance_router
from .symbol_pair_controller import router as symbol_pair_controller

main_router = APIRouter()

main_router.include_router(health_router,
                           prefix="/health",
                           tags=["health"],
                           responses={404: {"description": "Not found"}})
main_router.include_router(auth_router,
                           prefix="",
                           tags=["auth"],
                           responses={404: {"description": "Not found"}})

main_router.include_router(bot_router,
                           prefix="/bot",
                           tags=["bot"],
                           responses={404: {"description": "Not found"}})

main_router.include_router(bot_instance_router,
                           prefix="/bot_instance",
                           tags=["bot_instance"],
                           responses={404: {"description": "Not found"}})

main_router.include_router(exchange_router,
                           prefix="/exchange",
                           tags=["exchange"],
                           responses={404: {"description": "Not found"}})

main_router.include_router(exchange_instance_router,
                           prefix="/exchange_instance",
                           tags=["exchange_instance"],
                           responses={404: {"description": "Not found"}})

main_router.include_router(symbol_pair_controller,
                           prefix="/symbol_pair",
                           tags=["symbol_pair"],
                           responses={404: {"description": "Not found"}})
