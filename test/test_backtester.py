from dotenv import load_dotenv
from data.data_logger import logger
load_dotenv()
log = logger.setup_applevel_logger(file_name = 'test_backtester_debug.log')
from trading.backtester import BackTesterRunner
start_date = "7 Oct, 2021"

runner = BackTesterRunner()
backtester1 = runner.prepare_backtester(symbol="AVAXUSDT", timeframe="1m", account_provider="testAccount",
                                        strategy_provider="quickStrategy", data_structure_provider="pandas", data_fetcher_provider="binance",
                                        start_date=start_date)
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
runner.launch()
fig = backtester1.strategy.get_figure()
fig.show()

account1 = backtester1.account
#print(account1.df.to_string())
account1.get_profit()
print(account1.df.to_string())

sellSignal1 = backtester1.strategy.SellSignal
#print(sellSignal1.get_all_sell_signal_values().to_string())