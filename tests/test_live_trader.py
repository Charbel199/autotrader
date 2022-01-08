from dotenv import load_dotenv
from AutoTrader.trading.modes.live_trader import LiveTraderRunner, LiveTrader
from AutoTrader.helper import logger
import pandas as pd

load_dotenv()
log = logger.setup_applevel_logger(file_name='test_live_trader_debug.log')
import time


def get_info(live_trader: LiveTrader, show_fig=False):
    account = live_trader.account
    strategy = live_trader.strategy
    log.info(f"For: {strategy.symbol}")
    account.get_profit(symbol=live_trader.symbol, primary_symbol=live_trader.primary_symbol, secondary_symbol=live_trader.secondary_symbol)
    trades = pd.DataFrame(account.lists[live_trader.symbol])
    log.info(f"Trades: \n{trades.to_string()}")
    log.info(f"Number of trades {strategy.number_of_trades} and number of stop losses {strategy.number_of_stop_losses}")
    if show_fig:
        fig = strategy.get_figure()
        fig.show()
        fig.write_html("test.html")


start_date = "25 Dec, 2021"
live_runner = LiveTraderRunner(live_fetcher_provider='binance', account='testAccount')

live_trader1 = live_runner.prepare_live_trader(symbol="BTCUSDT", primary_symbol="BTC", secondary_symbol="USDT", timeframe="1m",
                                               strategy_provider="quickStrategy", data_structure_provider="list", data_fetcher_provider="binance",
                                               back_date=start_date)
# live_trader2 = live_runner.prepare_live_trader(symbol="DOGEUSDT", timeframe="1m",
#                                                strategy_provider="quickStrategy", data_structure_provider="list", data_fetcher_provider="binance",
#                                                back_date=start_date)
# live_trader3 = live_runner.prepare_live_trader(symbol="LTCUSDT", timeframe="1m",
#                                                strategy_provider="quickStrategy", data_structure_provider="list", data_fetcher_provider="binance",
#                                                back_date=start_date)
live_runner.start_all_live_traders()
print('start')
time.sleep(120)
live_runner.stop_all_live_traders()
print('stop')

get_info(live_trader1, show_fig=True)
# get_info(live_trader2, show_fig=True)
# get_info(live_trader3, show_fig=True)
