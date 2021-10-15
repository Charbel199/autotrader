from dotenv import load_dotenv
from trading.live_trader import LiveTraderRunner
from data.data_logger import logger
load_dotenv()
log = logger.setup_applevel_logger(file_name = 'test_live_trader_debug.log')
import time
start_date = "12 Oct, 2021"
live_runner = LiveTraderRunner('binance')

# live_trader1 = live_runner.prepare_live_trader(symbol="BTCUSDT", timeframe="1m", account_provider="testAccount",
#                                                strategy_provider="quickStrategy", data_structure_provider="pandas", data_fetcher_provider="binance",
#                                                back_date=start_date)
# live_trader2 = live_runner.prepare_live_trader(symbol="DOGEUSDT", timeframe="1m", account_provider="testAccount",
#                                                strategy_provider="quickStrategy", data_structure_provider="pandas", data_fetcher_provider="binance",
#                                                back_date=start_date)
live_trader3 = live_runner.prepare_live_trader(symbol="LTCUSDT", timeframe="1m", account_provider="testAccount",
                                               strategy_provider="quickStrategy", data_structure_provider="pandas", data_fetcher_provider="binance",
                                               back_date=start_date)
live_runner.start_all_live_traders()
print('start')
time.sleep(20)
live_runner.stop_all_live_traders()
print('stop')
# fig = live_trader1.strategy.get_figure()
# fig.show()
# fig2 = live_trader2.strategy.get_figure()
# fig2.show()
fig3 = live_trader3.strategy.get_figure()
fig3.show()