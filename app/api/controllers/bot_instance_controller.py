from fastapi import Depends, APIRouter
from app.application.models import user_model
from app.application.application_dependency_injection import Services
from app.application.services.interfaces.abstract_bot_instance_service import AbstractBotInstanceService
from app.api.dependencies.user_dependency import get_current_active_user
from app.application.models import bot_instance_model
from typing import List

router = APIRouter()
bot_instance_service: AbstractBotInstanceService = Services.bot_instance_service()


@router.get("/instances", response_model=List[bot_instance_model.BotInstance])
async def get_all_bot_instances(current_user: user_model.UserToken = Depends(get_current_active_user)):
    bot_instances = await bot_instance_service.get_bot_instances(current_user)
    return bot_instances


@router.post("/add", response_model=bot_instance_model.BotInstanceCreateResponse)
async def add_bot(bot_instance: bot_instance_model.BotInstanceCreate,
                  current_user: user_model.UserToken = Depends(get_current_active_user)):
    bot_instance = await bot_instance_service.add_bot_instance(current_user, bot_instance)
    return bot_instance


@router.post("/remove", response_model=bot_instance_model.BotInstance)
async def remove_bot(bot_instance_id: int,
                     current_user: user_model.UserToken = Depends(get_current_active_user)):
    bot_instance = await bot_instance_service.remove_bot_instance(current_user, bot_instance_id)
    return bot_instance


@router.get("/instance", response_model=bot_instance_model.BotInstance)
async def get_bot(bot_instance_id: int,
                  current_user: user_model.UserToken = Depends(get_current_active_user)):
    bot_instance = await bot_instance_service.get_bot_instance(current_user, bot_instance_id)
    return bot_instance

from AutoTrader.trading.modes.live_trader import LiveTraderRunner

@router.get("/launch")
async def launch_bot():
    import time

    start_date = "2 Feb, 2022"
    global live_runner
    live_runner = LiveTraderRunner(live_fetcher_provider='binance', account='testAccount')

    live_trader1 = live_runner.prepare_live_trader(symbol="BTCUSDT", primary_symbol="BTC", secondary_symbol="USDT", timeframe="1m",
                                                   strategy_provider="SHEA_strategy", data_structure_provider="list", candlesticks_provider="binance",
                                                   back_date=start_date)
    print("STARTING")
    live_runner.start_all_live_traders()

@router.get("/stop")
async def stop_bot():
    global live_runner
    live_runner.stop_all_live_traders()
    print('stop')


