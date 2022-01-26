from dotenv import load_dotenv
from AutoTrader.trading.modes.live_trader import LiveTraderRunner
from AutoTrader.helper import logger

load_dotenv()
log = logger.setup_applevel_logger(file_name='test_live_trader_debug.log')
import time


start_date = "25 Dec, 2021"
live_runner = LiveTraderRunner(live_fetcher_provider='binance', account='testAccount')

live_trader1 = live_runner.prepare_live_trader(symbol="BTCUSDT", primary_symbol="BTC", secondary_symbol="USDT", timeframe="1m",
                                               strategy_provider="quickStrategy", data_structure_provider="list", candlesticks_provider="binance",
                                               back_date=start_date)
# live_trader2 = live_runner.prepare_live_trader(symbol="DOGEUSDT", timeframe="1m",
#                                                strategy_provider="quickStrategy", data_structure_provider="list", data_fetcher_provider="binance",
#                                                back_date=start_date)
# live_trader3 = live_runner.prepare_live_trader(symbol="LTCUSDT", timeframe="1m",
#                                                strategy_provider="quickStrategy", data_structure_provider="list", data_fetcher_provider="binance",
#                                                back_date=start_date)
live_runner.start_all_live_traders()
print('start')
time.sleep(120)
live_runner.stop_all_live_traders()
print('stop')

