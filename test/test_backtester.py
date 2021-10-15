from dotenv import load_dotenv
from data.data_logger import logger

load_dotenv()
log = logger.setup_applevel_logger(file_name='test_backtester_debug.log')
from trading.backtester import BackTesterRunner

start_date = "30 Sep, 2021"
end_date = "1 Oct, 2021"
runner = BackTesterRunner()
backtester1 = runner.prepare_backtester(symbol="ADAUSDT", timeframe="5m", account_provider="testAccount",
                                        strategy_provider="quickStrategy", data_structure_provider="pandas", data_fetcher_provider="binance",
                                        start_date=start_date, end_date=end_date)
backtester2 = runner.prepare_backtester(symbol="DOTUSDT", timeframe="5m", account_provider="testAccount",
                                        strategy_provider="quickStrategy", data_structure_provider="pandas", data_fetcher_provider="binance",
                                        start_date=start_date, end_date=end_date)
backtester3 = runner.prepare_backtester(symbol="ETHUSDT", timeframe="5m", account_provider="testAccount",
                                        strategy_provider="quickStrategy", data_structure_provider="pandas", data_fetcher_provider="binance",
                                        start_date=start_date, end_date=end_date)
backtester4 = runner.prepare_backtester(symbol="SUSHIUSDT", timeframe="5m", account_provider="testAccount",
                                        strategy_provider="quickStrategy", data_structure_provider="pandas", data_fetcher_provider="binance",
                                        start_date=start_date, end_date=end_date)
backtester5 = runner.prepare_backtester(symbol="LINKUSDT", timeframe="5m", account_provider="testAccount",
                                        strategy_provider="quickStrategy", data_structure_provider="pandas", data_fetcher_provider="binance",
                                        start_date=start_date, end_date=end_date)
runner.launch()

account1 = backtester1.account
account2 = backtester2.account
account3 = backtester3.account
account4 = backtester4.account
account5 = backtester5.account

strategy1 = backtester1.strategy
strategy2 = backtester2.strategy
strategy3 = backtester3.strategy
strategy4 = backtester4.strategy
strategy5 = backtester5.strategy

log.info(f"For: {strategy1.symbol}")
account1.get_profit()
log.info(f"Trades: \n{account1.df.to_string()}")
log.info(f"Number of trades {strategy1.number_of_trades} and number of stop losses {strategy1.number_of_stop_losses}")

log.info(f"For: {strategy2.symbol}")
account2.get_profit()
log.info(f"Trades: \n{account2.df.to_string()}")
log.info(f"Number of trades {strategy2.number_of_trades} and number of stop losses {strategy2.number_of_stop_losses}")

log.info(f"For: {strategy3.symbol}")
account3.get_profit()
log.info(f"Trades: \n{account3.df.to_string()}")
log.info(f"Number of trades {strategy3.number_of_trades} and number of stop losses {strategy3.number_of_stop_losses}")

log.info(f"For: {strategy4.symbol}")
account4.get_profit()
log.info(f"Trades: \n{account4.df.to_string()}")
log.info(f"Number of trades {strategy4.number_of_trades} and number of stop losses {strategy4.number_of_stop_losses}")

log.info(f"For: {strategy5.symbol}")
account5.get_profit()
log.info(f"Trades: \n{account5.df.to_string()}")
log.info(f"Number of trades {strategy5.number_of_trades} and number of stop losses {strategy5.number_of_stop_losses}")
