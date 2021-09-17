from data.data_fetcher import get_fetcher
from dotenv import load_dotenv
from live_trader import LiveTrader
from data_structures.structure import get_data_structure
load_dotenv()
import time
from live_data.live_data_fetcher import get_live_fetcher
from strategies.strategy import get_strategy

symbol = "DOGEUSDT"
timeframe = "1m"
data_fetcher = get_fetcher('binance')
data_structure = get_data_structure('pandas')
live_data_fetcher = get_live_fetcher('binance')
strategy = get_strategy('quickStrategy', data_structure)
start_date = "17 Sep, 2021"

# backtester_instance = BackTester(symbol, timeframe, data_fetcher, data_structure, strategy, start_date)
# backtester_instance.run_backtester()

live_trader_instance = LiveTrader(symbol, timeframe, live_data_fetcher, data_fetcher, data_structure, strategy,
                                  start_date)
live_trader_instance.run_live_trader()
print('start')
time.sleep(30)
live_trader_instance.stop_live_trader()
print('stop')


print(data_structure.get_data())
