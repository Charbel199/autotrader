import sys

sys.path.append("..")
from dotenv import load_dotenv
from AutoTrader.helper import logger

load_dotenv()
log = logger.setup_applevel_logger(file_name='test_backtester_debug.log')
from AutoTrader.trading.modes.backtester import BackTesterRunner, BackTester
import time
import pandas as pd


def get_info(backtester: BackTester, show_fig=False):
    account = backtester.account
    strategy = backtester.strategy
    log.info(f"For: {strategy.symbol}")
    trades = pd.DataFrame(account.get_all_trades(symbol=backtester.symbol, primary_symbol=backtester.primary_symbol, secondary_symbol=backtester.secondary_symbol))
    log.info(f"Trades: \n{trades.to_string()}")
    log.info(f"Number of trades {strategy.number_of_trades} and number of stop losses {strategy.number_of_stop_losses}")
    account.get_profit(symbol=backtester.symbol, primary_symbol=backtester.primary_symbol, secondary_symbol=backtester.secondary_symbol)
    if show_fig:
        fig = strategy.get_figure()
        fig.show()
        fig.write_html("test.html")


start = time.time()

start_date = "21 Dec, 2021"
# start_date = "1 Oct, 2020"
end_date = "1 Jan, 2022"
runner = BackTesterRunner('testAccount')
backtester1 = runner.prepare_backtester(symbol="ADAUSDT", primary_symbol='USDT',
                                        secondary_symbol='ADA', timeframe="5m",
                                        strategy_provider="quickStrategy", candlesticks_provider="list", data_fetcher_provider="binance",
                                        start_date=start_date, end_date=end_date)

backtester2 = runner.prepare_backtester(symbol="XRPBUSD", primary_symbol='BUSD',
                                        secondary_symbol='XRP', timeframe="5m",
                                        strategy_provider="quickStrategy", candlesticks_provider="list", data_fetcher_provider="binance",
                                        start_date=start_date, end_date=end_date)
# backtester2 = runner.prepare_backtester(symbol="GBPUSDT", timeframe="5m", account_provider="testAccount",
#                                         strategy_provider="quickStrategy", data_structure_provider="list", data_fetcher_provider="binance",
#                                         start_date=start_date, end_date=end_date)
# backtester3 = runner.prepare_backtester(symbol="JPYUSDT", timeframe="5m", account_provider="testAccount",
#                                         strategy_provider="quickStrategy", data_structure_provider="list", data_fetcher_provider="binance",
#                                         start_date=start_date, end_date=end_date)
# backtester4 = runner.prepare_backtester(symbol="SUSHIUSDT", timeframe="5m", account_provider="testAccount",
#                                         strategy_provider="quickStrategy", data_structure_provider="list", data_fetcher_provider="binance",
#                                         start_date=start_date, end_date=end_date)
# backtester5 = runner.prepare_backtester(symbol="LINKUSDT", timeframe="5m", account_provider="testAccount",
#                                         strategy_provider="quickStrategy", data_structure_provider="list", data_fetcher_provider="binance",
#                                         start_date=start_date, end_date=end_date)
runner.launch()

get_info(backtester1, show_fig=True)
# get_info(backtester2, show_fig=True)
# get_info(backtester3, show_fig=False)
# get_info(backtester4, show_fig=False)
# get_info(backtester5, show_fig=False)

end = time.time()
log.info(f"Total duration: {(end - start)}")
log.info(f"End balance: {runner.account.balance}")
transactions = runner.account.transactions

for transaction in transactions["ADAUSDT"]:
    log.info(f"{transaction}")