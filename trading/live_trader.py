from trading.strategies.strategy import Strategy
from data.data_structures.structure import TickStructure
from data.previous_data.data_fetcher import DataFetcher
from data.live_data.live_data_fetcher import LiveDataFetcher
from trading.accounts.account import Account


class LiveTrader(object):
    strategy: Strategy
    data_structure: TickStructure
    data_fetcher: DataFetcher
    live_data_fetcher: LiveDataFetcher
    account: Account

    def __init__(self, symbol, timeframe, live_data_fetcher, data_fetcher, data_structure, strategy, account, back_date=None):
        self.data_structure = data_structure
        self.live_data_fetcher = live_data_fetcher
        self.strategy = strategy
        self.symbol = symbol
        self.timeframe = timeframe
        self.data_fetcher = data_fetcher
        self.back_date = back_date
        self.account = account

    def run_live_trader(self):
        if self.back_date:
            candlesticks = self.data_fetcher.get_candlesticks(
                self.symbol, self.timeframe, self.back_date
            )
            self.strategy.disable_transactions()
            for candlestick in candlesticks:
                if self.data_structure:
                    self.data_structure.set_tick(candlestick)
                    self.data_structure.add_row(candlestick)
                    self.strategy.process_new_candlestick()
            self.strategy.enable_transactions()
        self.live_data_fetcher.run(self.symbol, self.timeframe, self.process_message)

    def stop_live_trader(self):
        self.live_data_fetcher.stop()

    def process_message(self, tick):
        if self.data_structure:
            # Only add to rows if it's a new candlestick
            if self.data_structure.get_tick() != {} and tick["CloseTime"] != self.data_structure.get_tick()["CloseTime"]:
                self.data_structure.add_row(self.data_structure.get_tick())
                self.strategy.process_new_candlestick()

            self.data_structure.set_tick(tick)
            self.strategy.process_new_tick()


from data.previous_data.data_fetcher import get_fetcher
from data.data_structures.structure import get_data_structure
from trading.strategies.strategy import get_strategy
from trading.accounts.account import get_account
from data.live_data.live_data_fetcher import get_live_fetcher


class LiveTraderRunner(object):
    live_traders = []

    def __init__(self, live_fetcher_provider):
        self.live_data_fetcher = get_live_fetcher(live_fetcher_provider)

    def prepare_live_trader(self, symbol, timeframe, account_provider, data_fetcher_provider, data_structure_provider, strategy_provider, back_date=None):
        account = get_account(account_provider)
        data_fetcher = get_fetcher(data_fetcher_provider)
        data_structure = get_data_structure(data_structure_provider)
        strategy = get_strategy(strategy_provider, data_structure, account, symbol)
        live_trader_instance = LiveTrader(symbol, timeframe, self.live_data_fetcher, data_fetcher, data_structure, strategy, account, back_date)
        self.live_traders.append(live_trader_instance)
        return live_trader_instance

    def start_all_live_traders(self):
        for live_trader in self.live_traders:
            live_trader.run_live_trader()

    def stop_all_live_traders(self):
        self.live_data_fetcher.stop()
