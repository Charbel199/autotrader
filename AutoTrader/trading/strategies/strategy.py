from abc import ABC, abstractmethod
from AutoTrader.data.data_structures.candlesticks import Candlesticks
from AutoTrader.trading.accounts.account import Account
from plotly.graph_objs import Figure
from AutoTrader.exceptions import StrategyNotFound
from AutoTrader.trading.indicators import Indicator
from typing import List


class Strategy(ABC):
    candlesticks: Candlesticks
    account: Account

    def __init__(self,
                 candlesticks: Candlesticks,
                 account: Account,
                 symbol: str,
                 primary_symbol: str,
                 secondary_symbol: str):

        self.candlesticks = candlesticks
        self.account = account
        self.symbol = symbol
        self.primary_symbol = primary_symbol
        self.secondary_symbol = secondary_symbol
        self.transactions_allowed = True

        self.initialize_variables()
        # Add indicators
        self.indicators = []
        for key, value in vars(self).items():
            if isinstance(value, Indicator):
                self.indicators.append(value)

    # Happens AFTER updating the tick
    def process_new_tick(self) -> None:
        for indicator in self.indicators:
            indicator.process_new_tick()
        self.new_tick_logic()

    # Happens AFTER adding a new candlestick
    def process_new_candlestick(self) -> None:
        for indicator in self.indicators:
            indicator.process_new_candlestick()
        self.new_candlestick_logic()

    @abstractmethod
    def initialize_variables(self):
        pass

    @abstractmethod
    def new_candlestick_logic(self) -> None:
        pass

    @abstractmethod
    def new_tick_logic(self) -> None:
        pass

    def enable_transactions(self) -> None:
        self.transactions_allowed = True

    def disable_transactions(self) -> None:
        self.transactions_allowed = False

    @abstractmethod
    def get_figure(self) -> Figure:
        pass

    @staticmethod
    @abstractmethod
    def condition(name: str) -> bool:
        pass


# Get strategy
def get_strategy(name: str, data_structure: Candlesticks, account: Account, symbol: str, primary_symbol: str, secondary_symbol: str) -> Strategy:
    for strategy in Strategy.__subclasses__():
        if strategy.condition(name):
            return strategy(data_structure, account, symbol, primary_symbol, secondary_symbol)
    raise StrategyNotFound(f"Strategy: {name} not found")
