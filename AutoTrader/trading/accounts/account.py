from abc import ABC, abstractmethod
from AutoTrader.helper import logger
import plotly.graph_objects as go
from AutoTrader.exceptions import AccountNotFound
from AutoTrader.services.summary import get_trades_summary, print_summary
from typing import Dict, List
from AutoTrader.models import Transaction, Position, Order
from AutoTrader.enums import *
import copy

log = logger.get_logger(__name__)


class Account(ABC):
    columns = ['Time', 'Action', 'Amount', 'Symbol', 'Price']
    transaction_percentage = NotImplemented
    transaction_fee = NotImplemented

    def __init__(self):
        balance = self._get_balance()
        self.balance: Dict[str, float] = balance
        self.initial_balance: Dict[str, float] = copy.deepcopy(balance)
        self.orders: Dict[str, List[Order]] = {}
        self.open_orders: Dict[str, List[Order]] = {}
        self.positions: Dict[str, Order] = {}

    def get_position(self, symbol: str) -> Order:
        return self.positions.get(symbol, Order())

    @abstractmethod
    def place_order(self,
                    time: int,
                    symbol: str,
                    source_symbol: str,
                    destination_symbol: str,
                    type: OrderType,
                    price: float,
                    side: OrderSide,
                    source_symbol_total_amount: float = 0,
                    destination_symbol_amount: float = 0) -> None:
        pass

    def get_profit(self, symbol: str, primary_symbol: str, secondary_symbol: str, undo_last_position=True) -> float:
        # If in position when calculating profit, revert last buy
        if undo_last_position:
            self._undo_last_position(symbol, primary_symbol, secondary_symbol)

        # Get summary
        summary = get_trades_summary(self.orders[symbol], self.initial_balance[primary_symbol])
        log.info(print_summary(summary))
        return summary['PercentageChange'] if summary != {} else 0

    def get_all_trades(self, symbol: str, primary_symbol: str, secondary_symbol: str, undo_last_position=True) -> list:
        # If in position when getting all trades, revert last buy
        if undo_last_position:
            self._undo_last_position(symbol, primary_symbol, secondary_symbol)

        summary = get_trades_summary(self.orders[symbol], self.initial_balance[primary_symbol])
        return summary['AllTrades']

    @abstractmethod
    def get_plot(self, symbol: str) -> go:
        pass

    @abstractmethod
    def _get_balance(self) -> Dict[str, float]:
        pass

    def _undo_last_position(self, symbol: str, primary_symbol: str, secondary_symbol: str) -> None:
        # If no position found with this symbol, return
        if symbol not in self.positions:
            return

        if self.positions[symbol].is_valid():
            # Remove last transaction
            self.orders[symbol] = self.orders[symbol][:-1]
            # Refund balance
            self.balance[primary_symbol] += self.positions[symbol].Price * self.positions[symbol].ExecutedQuantity
            # Empty position
            self.positions[symbol] = Order()

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
