from data.data_fetcher import get_fetcher
from dotenv import load_dotenv
from live_trader import LiveTrader
from data_structures.structure import get_data_structure
load_dotenv()
import time
from backtester import BackTester
from live_data.live_data_fetcher import get_live_fetcher
from strategies.strategy import get_strategy
from account.account import get_account
import datetime


symbol = "DOGEUSDT"
timeframe = "15m"
account = get_account("testAccount")
data_fetcher = get_fetcher('binance')
data_structure = get_data_structure('pandas')
live_data_fetcher = get_live_fetcher('binance')
strategy = get_strategy('quickStrategy', data_structure, account)
start_date = "30 Sep, 2021"

start_time = datetime.datetime.now()


backtester_instance = BackTester(symbol, timeframe, data_fetcher, data_structure, strategy, start_date)
backtester_instance.run_backtester()

#live_trader_instance = LiveTrader(symbol, timeframe, live_data_fetcher, data_fetcher, data_structure, strategy, start_date)
#live_trader_instance.run_live_trader()
#print('start')
#time.sleep(90)
#live_trader_instance.stop_live_trader()
#print('stop')
import pandas as pd

end_time = datetime.datetime.now()
print(end_time - start_time)
from functools import reduce
dfs = [data_structure.get_data(),strategy.ADX.get_all_adx_values(),strategy.CandlestickType.get_all_candlestick_type_values(),strategy.RSI.get_all_rsi_values()]

df_merged = reduce(lambda  left,right: pd.merge(left,right,on=['Time'],
                                            how='outer'), dfs)
print(df_merged.to_string())