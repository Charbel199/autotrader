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
import time

start = time.time()
symbol = "DOGEUSDT"
timeframe = "15m"
account = get_account("testAccount")
data_fetcher = get_fetcher('binance')
data_structure = get_data_structure('pandas')
strategy = get_strategy('quickStrategy', data_structure, account, symbol)
start_date = "5 Oct, 2021"

# backtester_instance = BackTester(symbol, timeframe, data_fetcher, data_structure, strategy,account, start_date)
# backtester_instance.run_backtester()
symbol2 = "BTCUSDT"
account2 = get_account("testAccount")
data_fetcher2 = get_fetcher('binance')
data_structure2 = get_data_structure('pandas')
strategy2 = get_strategy('quickStrategy', data_structure2, account2, symbol2)
start_date2 = "5 Oct, 2021"

# backtester_instance2 = BackTester(symbol2, timeframe, data_fetcher2, data_structure2, strategy2,account2, start_date)
# backtester_instance2.run_backtester()

from backtester import BackTesterRunner

runner = BackTesterRunner()
backtester1 = runner.prepare_backtester(symbol="DOGEUSDT", timeframe="15m", account_provider="testAccount",
                                        strategy_provider="quickStrategy", data_structure_provider="pandas", data_fetcher_provider="binance",
                                        start_date=start_date)
backtester2 = runner.prepare_backtester(symbol="BTCUSDT", timeframe="15m", account_provider="testAccount",
                                        strategy_provider="quickStrategy", data_structure_provider="pandas", data_fetcher_provider="binance",
                                        start_date=start_date)
runner.launch()
fig = backtester1.strategy.get_figure()
fig.show()
fig2 = backtester2.strategy.get_figure()
fig2.show()

account1 = backtester2.account
print(account1.df.to_string())

# live_data_fetcher = get_live_fetcher('binance')
# live_trader_instance = LiveTrader(symbol, timeframe, live_data_fetcher, data_fetcher, data_structure, strategy, start_date)
# live_trader_instance.run_live_trader()
# print('start')
# time.sleep(60)
# live_trader_instance.stop_live_trader()
# print('stop')
import pandas as pd

# from functools import reduce
#
# dfs = [data_structure.get_data(),
#        strategy.ADX.get_all_adx_values(),
#        strategy.CandlestickType.get_all_candlestick_type_values(),
#        strategy.RSI.get_all_rsi_values(),
#        account.df]
# df_merged = reduce(lambda left, right: pd.merge(left, right, on=['Time'],
#                                                 how='outer'), dfs)
# print('First')
# print(df_merged.to_string())
#
# fig = strategy.get_figure()
# fig.show()
# fig2 = strategy2.get_figure()
# fig2.show()
# from plot_test.candlesticks import show_candlesticks
# show_candlesticks(data_structure.get_data())
# df_merged.to_excel("output.xlsx")
