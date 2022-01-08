from AutoTrader.trading.strategies.strategy import Strategy
from AutoTrader.data.data_structures.structure import TickStructure
from AutoTrader.data.previous_data.data_fetcher import DataFetcher
from AutoTrader.data.live_data.live_data_fetcher import LiveDataFetcher
from AutoTrader.trading.accounts.account import Account
from AutoTrader.data.models import Tick


class LiveTrader(object):
    strategy: Strategy
    data_structure: TickStructure
    data_fetcher: DataFetcher
    live_data_fetcher: LiveDataFetcher
    account: Account

    def __init__(self,
                 symbol: str,
                 primary_symbol: str,
                 secondary_symbol: str,
                 timeframe: str,
                 live_data_fetcher: LiveDataFetcher,
                 data_fetcher: DataFetcher,
                 data_structure: TickStructure,
                 strategy: Strategy,
                 account: Account,
                 back_date: str = None):
        self.data_structure = data_structure
        self.live_data_fetcher = live_data_fetcher
        self.strategy = strategy
        self.symbol = symbol
        self.primary_symbol = primary_symbol
        self.secondary_symbol = secondary_symbol
        self.timeframe = timeframe
        self.data_fetcher = data_fetcher
        self.back_date = back_date
        self.account = account

    def run_live_trader(self) -> None:
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

    def stop_live_trader(self) -> None:
        self.live_data_fetcher.stop()

    def process_message(self, tick: Tick) -> None:
        if self.data_structure:
            previous_tick = self.data_structure.get_tick()
            self.data_structure.set_tick(tick)
            self.strategy.process_new_tick()

            # Only add to rows if it's a new candlestick
            if previous_tick.is_valid() and tick.CloseTime != previous_tick.CloseTime:
                self.data_structure.add_row(previous_tick)
                self.strategy.process_new_candlestick()


from AutoTrader.data.previous_data.data_fetcher import get_fetcher
from AutoTrader.data.data_structures.structure import get_data_structure
from AutoTrader.trading.strategies.strategy import get_strategy
from AutoTrader.trading.accounts.account import get_account
from AutoTrader.data.live_data.live_data_fetcher import get_live_fetcher


class LiveTraderRunner(object):
    live_traders = []

    def __init__(self, live_fetcher_provider: str, account: str):
        self.live_data_fetcher = get_live_fetcher(live_fetcher_provider)
        self.account = get_account(account)

    def prepare_live_trader(self,
                            symbol: str,
                            primary_symbol: str,
                            secondary_symbol: str,
                            timeframe: str,
                            data_fetcher_provider: str,
                            data_structure_provider: str,
                            strategy_provider: str,
                            back_date: str = None) -> LiveTrader:

        data_fetcher = get_fetcher(data_fetcher_provider)
        data_structure = get_data_structure(data_structure_provider)
        strategy = get_strategy(strategy_provider, data_structure, self.account, symbol, primary_symbol, secondary_symbol)
        live_trader_instance = LiveTrader(symbol, primary_symbol, secondary_symbol, timeframe, self.live_data_fetcher, data_fetcher, data_structure, strategy, self.account, back_date)
        self.live_traders.append(live_trader_instance)
        return live_trader_instance

    def start_all_live_traders(self) -> None:
        for live_trader in self.live_traders:
            live_trader.run_live_trader()

    def stop_all_live_traders(self) -> None:
        self.live_data_fetcher.stop()
