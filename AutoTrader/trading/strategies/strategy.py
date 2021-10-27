from abc import ABC, abstractmethod
from AutoTrader.data.data_structures.structure import TickStructure
from AutoTrader.trading.accounts.account import Account
from plotly.graph_objs import Figure
from AutoTrader.exceptions import StrategyNotFound


class Strategy(ABC):
    data_structure: TickStructure
    account: Account

    def __init__(self,
                 data_structure: TickStructure,
                 account: Account,
                 symbol: str):
        self.data_structure = data_structure
        self.account = account
        self.symbol = symbol
        self.transactions_allowed = True
        self.number_of_trades = 0
        self.number_of_stop_losses = 0

    # Happens AFTER updating the tick in the previous_data structure
    @abstractmethod
    def process_new_tick(self) -> None:
        pass

    # Happens AFTER adding the new candlestick in the previous_data structure
    @abstractmethod
    def process_new_candlestick(self) -> None:
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
def get_strategy(name: str, data_structure: TickStructure, account: Account, symbol: str) -> Strategy:
    for strategy in Strategy.__subclasses__():
        if strategy.condition(name):
            return strategy(data_structure, account, symbol)
    raise StrategyNotFound(f"Strategy: {name} not found")
