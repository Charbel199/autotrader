from abc import ABC, abstractmethod
from AutoTrader.helper import logger
from AutoTrader.data.models import Position
import plotly.graph_objects as go
from AutoTrader.exceptions import AccountNotFound
from AutoTrader.services.summary import get_trades_summary, print_summary
from typing import Dict, List
import copy

log = logger.get_logger(__name__)


class Account(ABC):
    columns = ['Time', 'Action', 'Amount', 'Symbol', 'Price']
    transaction_percentage = NotImplemented
    transaction_fee = NotImplemented

    def __init__(self):
        self.positions: Dict[str, Position] = {}
        balance = self._get_balance()
        self.balance: Dict[str, float] = balance
        self.initial_balance: Dict[str, float] = copy.deepcopy(balance)
        self.lists: Dict[str, List[dict]] = {}

    def get_position(self, symbol: str) -> Position:
        return self.positions[symbol] if symbol in self.positions else Position()

    @abstractmethod
    def transaction(self,
                    time: int,
                    symbol: str,
                    source_symbol: str,
                    destination_symbol: str,
                    source_symbol_amount: float,
                    transaction_type: str,
                    destination_symbol_amount: float = 0) -> None:
        pass

    def get_profit(self, symbol: str, primary_symbol: str, secondary_symbol: str) -> float:
        # If in position when calculating profit, revert last buy
        self._undo_last_position(symbol, primary_symbol, secondary_symbol)

        summary = get_trades_summary(self.lists[symbol], self.initial_balance[primary_symbol])
        log.info(print_summary(summary))
        return summary['PercentageChange'] if summary != {} else 0

    @abstractmethod
    def get_plot(self, symbol: str) -> go:
        pass

    @abstractmethod
    def _get_balance(self) -> Dict[str, float]:
        pass

    def _undo_last_position(self, symbol: str, primary_symbol: str, secondary_symbol: str) -> None:
        self.positions[secondary_symbol] = Position() if secondary_symbol not in self.positions else self.positions[secondary_symbol]
        if self.positions[secondary_symbol].is_valid():
            self.lists[symbol] = self.lists[symbol][:-1]
            self.balance[primary_symbol] += self.positions[secondary_symbol].Price * self.positions[secondary_symbol].Amount
            self.positions[secondary_symbol] = Position()

    def get_all_trades(self, symbol: str, primary_symbol: str, secondary_symbol: str) -> list:
        # If in position when getting all trades, revert last buy
        self._undo_last_position(symbol, primary_symbol, secondary_symbol)

        summary = get_trades_summary(self.lists[symbol], self.initial_balance[primary_symbol])
        return summary['AllTrades']

    @staticmethod
    @abstractmethod
    def condition(name: str) -> bool:
        pass


# Get strategy
def get_account(name: str) -> Account:
    for account in Account.__subclasses__():
        if account.condition(name):
            return account()
    raise AccountNotFound(f"Account type: {name} not found")
