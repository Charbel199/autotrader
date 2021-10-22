import sys

sys.path.append("..")
from dotenv import load_dotenv
from data.data_logger import logger

load_dotenv()
log = logger.setup_applevel_logger(file_name='test_backtester_debug.log')
from trading.backtester import BackTesterRunner
import time
import pandas as pd


def get_info(backtester: BackTesterRunner, show_fig=False):
    account = backtester.account
    strategy = backtester.strategy
    log.info(f"For: {strategy.symbol}")
    account.get_profit()
    trades = pd.DataFrame(account.list)
    log.info(f"Trades: \n{trades.to_string()}")
    log.info(f"Number of trades {strategy.number_of_trades} and number of stop losses {strategy.number_of_stop_losses}")
    if show_fig:
        fig = strategy.get_figure()
        fig.show()
        fig.write_html("test.html")


start = time.time()

start_date = "1 Jul, 2021"
end_date = "1 Oct, 2021"
runner = BackTesterRunner()
backtester1 = runner.prepare_backtester(symbol="ADAUSDT", timeframe="5m", account_provider="testAccount",
                                        strategy_provider="quickStrategy", data_structure_provider="list", data_fetcher_provider="binance",
                                        start_date=start_date, end_date=end_date)
backtester2 = runner.prepare_backtester(symbol="DOTUSDT", timeframe="5m", account_provider="testAccount",
                                        strategy_provider="quickStrategy", data_structure_provider="list", data_fetcher_provider="binance",
                                        start_date=start_date, end_date=end_date)
backtester3 = runner.prepare_backtester(symbol="ETHUSDT", timeframe="5m", account_provider="testAccount",
                                        strategy_provider="quickStrategy", data_structure_provider="list", data_fetcher_provider="binance",
                                        start_date=start_date, end_date=end_date)
backtester4 = runner.prepare_backtester(symbol="SUSHIUSDT", timeframe="5m", account_provider="testAccount",
                                        strategy_provider="quickStrategy", data_structure_provider="list", data_fetcher_provider="binance",
                                        start_date=start_date, end_date=end_date)
backtester5 = runner.prepare_backtester(symbol="LINKUSDT", timeframe="5m", account_provider="testAccount",
                                        strategy_provider="quickStrategy", data_structure_provider="list", data_fetcher_provider="binance",
                                        start_date=start_date, end_date=end_date)
runner.launch()

get_info(backtester1, show_fig=False)
get_info(backtester2, show_fig=False)
get_info(backtester3, show_fig=False)
get_info(backtester4, show_fig=False)
get_info(backtester5, show_fig=False)

end = time.time()
log.info(f"Total duration: {(end - start)}")


