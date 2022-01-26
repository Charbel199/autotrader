
from dotenv import load_dotenv
from app.AutoTrader.helper import logger
load_dotenv()
log = logger.setup_applevel_logger(file_name='test_backtester_debug.log')
from app.AutoTrader.trading.modes.backtester import BackTesterRunner
import time



start = time.time()

start_date = "21 Dec, 2021"
# start_date = "1 Oct, 2020"
end_date = "1 Jan, 2022"
runner = BackTesterRunner('testAccount')
strategy_name = 'HAS_strategy'
backtester1 = runner.prepare_backtester(symbol="ADAUSDT", primary_symbol='USDT',
                                        secondary_symbol='ADA', timeframe="5m",
                                        strategy_provider=strategy_name, candlesticks_provider="list", data_fetcher_provider="binance",
                                        start_date=start_date, end_date=end_date)

# backtester2 = runner.prepare_backtester(symbol="XRPBUSD", primary_symbol='BUSD',
#                                         secondary_symbol='XRP', timeframe="1m",
#                                         strategy_provider=strategy_name, candlesticks_provider="list", data_fetcher_provider="binance",
#                                         start_date=start_date, end_date=end_date)
#
# backtester3 = runner.prepare_backtester(symbol="LINKBTC", primary_symbol='BTC',
#                                         secondary_symbol='LINK', timeframe="1m",
#                                         strategy_provider=strategy_name, candlesticks_provider="list", data_fetcher_provider="binance",
#                                         start_date=start_date, end_date=end_date)


runner.launch()

backtester1.backtester_performance(show_fig=True, show_trades=False)
# backtester2.backtester_performance(show_fig=False, show_trades=False)
# backtester3.backtester_performance(show_fig=False, show_trades=False)


end = time.time()
log.info(f"Total duration: {(end - start)}")
log.info(f"End balance: {runner.account.balance}")
