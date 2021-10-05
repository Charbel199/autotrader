from dotenv import load_dotenv
load_dotenv()
import time
from live_trader import LiveTraderRunner
from backtester import BackTesterRunner
start_date = "5 Oct, 2021"

# runner = BackTesterRunner()
# backtester1 = runner.prepare_backtester(symbol="DOGEUSDT", timeframe="15m", account_provider="testAccount",
#                                         strategy_provider="quickStrategy", data_structure_provider="pandas", data_fetcher_provider="binance",
#                                         start_date=start_date)
# backtester2 = runner.prepare_backtester(symbol="BTCUSDT", timeframe="15m", account_provider="testAccount",
#                                         strategy_provider="quickStrategy", data_structure_provider="pandas", data_fetcher_provider="binance",
#                                         start_date=start_date)
# backtester3 = runner.prepare_backtester(symbol="LTCUSDT", timeframe="15m", account_provider="testAccount",
#                                         strategy_provider="quickStrategy", data_structure_provider="pandas", data_fetcher_provider="binance",
#                                         start_date=start_date)
# backtester4 = runner.prepare_backtester(symbol="ADAUSDT", timeframe="15m", account_provider="testAccount",
#                                         strategy_provider="quickStrategy", data_structure_provider="pandas", data_fetcher_provider="binance",
#                                         start_date=start_date)
# backtester5 = runner.prepare_backtester(symbol="ETHUSDT", timeframe="15m", account_provider="testAccount",
#                                         strategy_provider="quickStrategy", data_structure_provider="pandas", data_fetcher_provider="binance",
#                                         start_date=start_date)
# runner.launch()
# fig = backtester1.strategy.get_figure()
# fig.show()
# fig2 = backtester2.strategy.get_figure()
# fig2.show()
#
# account1 = backtester2.account
# print(account1.df.to_string())



live_runner = LiveTraderRunner('binance')

live_trader1 = live_runner.prepare_live_trader(symbol="BTCUSDT", timeframe="15m", account_provider="testAccount",
                                               strategy_provider="quickStrategy", data_structure_provider="pandas", data_fetcher_provider="binance",
                                               back_date=start_date)
live_trader2 = live_runner.prepare_live_trader(symbol="DOGEUSDT", timeframe="15m", account_provider="testAccount",
                                               strategy_provider="quickStrategy", data_structure_provider="pandas", data_fetcher_provider="binance",
                                               back_date=start_date)
live_trader3 = live_runner.prepare_live_trader(symbol="LTCUSDT", timeframe="15m", account_provider="testAccount",
                                               strategy_provider="quickStrategy", data_structure_provider="pandas", data_fetcher_provider="binance",
                                               back_date=start_date)
live_runner.start_all_live_traders()
print('start')
time.sleep(60)
live_runner.stop_all_live_traders()
print('stop')
fig = live_trader1.strategy.get_figure()
fig.show()
fig2 = live_trader2.strategy.get_figure()
fig2.show()
fig3 = live_trader3.strategy.get_figure()
fig3.show()

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
# from plot_test.candlesticks import show_candlesticks
# show_candlesticks(data_structure.get_data())
# df_merged.to_excel("output.xlsx")
