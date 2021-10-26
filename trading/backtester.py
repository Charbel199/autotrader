from trading.strategies.strategy import Strategy
from data.data_structures.structure import TickStructure
from data.previous_data.data_fetcher import DataFetcher
from trading.accounts.account import Account
import time
from data.data_logger import logger

log = logger.get_logger(__name__)


class BackTester(object):
    strategy: Strategy
    data_structure: TickStructure
    data_fetcher: DataFetcher
    account: Account

    def __init__(self,
                 symbol: str,
                 timeframe: str,
                 data_fetcher: DataFetcher,
                 data_structure: TickStructure,
                 strategy: Strategy,
                 account: Account,
                 start_date: str,
                 end_date: str = None):
        self.data_structure = data_structure
        self.strategy = strategy
        self.symbol = symbol
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
            if self.data_structure:
                self.data_structure.set_tick(candlestick)
                self.strategy.process_new_tick()

                self.data_structure.add_row(candlestick)
                self.strategy.process_new_candlestick()

        end = time.time()
        log.info(f"Candlestick processing duration: {(end - start)}")


from data.previous_data.data_fetcher import get_fetcher
from data.data_structures.structure import get_data_structure
from trading.strategies.strategy import get_strategy
from trading.accounts.account import get_account
import threading


class BackTesterRunner(object):
    threads = []

    def __init__(self):
        pass

    def prepare_backtester(self,
                           symbol: str,
                           timeframe: str,
                           account_provider: str,
                           data_fetcher_provider: str,
                           data_structure_provider: str,
                           strategy_provider: str,
                           start_date: str,
                           balance: float = 100,
                           end_date: str = None) -> BackTester:
        account = get_account(account_provider, balance)
        data_fetcher = get_fetcher(data_fetcher_provider)
        data_structure = get_data_structure(data_structure_provider)
        strategy = get_strategy(strategy_provider, data_structure, account, symbol)
        backtester_instance = BackTester(symbol, timeframe, data_fetcher, data_structure, strategy, account, start_date, end_date)
        # backtester_instance.run_backtester()
        thread = threading.Thread(target=backtester_instance.run_backtester)
        thread.start()
        self.threads.append(thread)
        return backtester_instance

    def launch(self) -> None:
        for thread in self.threads:
            thread.join()
        # pass
