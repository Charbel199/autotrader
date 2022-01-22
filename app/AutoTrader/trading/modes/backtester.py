from app.AutoTrader.trading.strategies.strategy import Strategy
from app.AutoTrader.data.data_structures.candlesticks import Candlesticks
from app.AutoTrader.data.previous_data.data_fetcher import DataFetcher
from app.AutoTrader.trading.accounts.account import Account
import time
from app.AutoTrader.helper import logger

log = logger.get_logger(__name__)


class BackTester(object):
    strategy: Strategy
    candlesticks: Candlesticks
    data_fetcher: DataFetcher
    account: Account

    def __init__(self,
                 symbol: str,
                 primary_symbol: str,
                 secondary_symbol: str,
                 timeframe: str,
                 data_fetcher: DataFetcher,
                 data_structure: Candlesticks,
                 strategy: Strategy,
                 account: Account,
                 start_date: str,
                 end_date: str = None):
        self.candlesticks = data_structure
        self.strategy = strategy
        self.symbol = symbol
        self.primary_symbol = primary_symbol
        self.secondary_symbol = secondary_symbol
        self.timeframe = timeframe
        self.data_fetcher = data_fetcher
        self.account = account
        self.start_date = start_date
        self.end_date = end_date

    def run_backtester(self) -> None:
        start = time.time()
        candlesticks = self.data_fetcher.get_candlesticks(self.symbol, self.timeframe, self.start_date, self.end_date)
        end = time.time()
        log.info(f"Candlestick fetching duration: {(end - start)}")

        start = time.time()
        for candlestick in candlesticks:
            if self.candlesticks:
                self.candlesticks.set_tick(candlestick)
                self.strategy.process_new_tick()

                self.candlesticks.add_row(candlestick)
                self.strategy.process_new_candlestick()

        end = time.time()
        log.info(f"Candlestick processing duration: {(end - start)}")

    def backtester_performance(self,
                               show_fig=False,
                               show_trades=False):
        trades_summary = self.account.get_trades_summary(symbol=self.symbol, primary_symbol=self.primary_symbol, secondary_symbol=self.secondary_symbol)
        print(trades_summary.get_text_summary(show_trades=show_trades))
        if show_fig:
            fig = self.strategy.get_figure()
            fig.show()
            fig.write_html("test.html")


from app.AutoTrader.data.previous_data.data_fetcher import get_fetcher
from app.AutoTrader.data.data_structures.candlesticks import get_data_structure
from app.AutoTrader.trading.strategies.strategy import get_strategy
from app.AutoTrader.trading.accounts.account import get_account
import threading


class BackTesterRunner(object):
    threads = []

    def __init__(self, account: str):
        self.account = get_account(account)

    def prepare_backtester(self,
                           symbol: str,
                           primary_symbol: str,
                           secondary_symbol: str,
                           timeframe: str,
                           data_fetcher_provider: str,
                           candlesticks_provider: str,
                           strategy_provider: str,
                           start_date: str,
                           end_date: str = None) -> BackTester:
        data_fetcher = get_fetcher(data_fetcher_provider)
        data_structure = get_data_structure(candlesticks_provider)
        strategy = get_strategy(strategy_provider, data_structure, self.account, symbol, primary_symbol, secondary_symbol)
        backtester_instance = BackTester(symbol, primary_symbol, secondary_symbol, timeframe, data_fetcher, data_structure, strategy, self.account, start_date, end_date)
        # backtester_instance.run_backtester()
        thread = threading.Thread(target=backtester_instance.run_backtester)
        thread.start()
        self.threads.append(thread)
        return backtester_instance

    def launch(self) -> None:
        for thread in self.threads:
            thread.join()
        # pass
