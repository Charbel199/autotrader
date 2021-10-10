from dotenv import load_dotenv

load_dotenv()
from trading.backtester import BackTesterRunner
start_date = "10 Oct, 2021"

runner = BackTesterRunner()
backtester1 = runner.prepare_backtester(symbol="DOGEUSDT", timeframe="15m", account_provider="testAccount",
                                        strategy_provider="quickStrategy", data_structure_provider="pandas", data_fetcher_provider="binance",
                                        start_date=start_date)
backtester2 = runner.prepare_backtester(symbol="BTCUSDT", timeframe="15m", account_provider="testAccount",
                                        strategy_provider="quickStrategy", data_structure_provider="pandas", data_fetcher_provider="binance",
                                        start_date=start_date)
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
fig2 = backtester2.strategy.get_figure()
fig2.show()

account1 = backtester2.account
print(account1.df.to_string())