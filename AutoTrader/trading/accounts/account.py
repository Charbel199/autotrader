from abc import ABC, abstractmethod
from AutoTrader.helper import logger
import plotly.graph_objects as go
from AutoTrader.exceptions import AccountNotFound
from AutoTrader.services.summary import get_trades_summary
from typing import Dict, List
from AutoTrader.models import Order, Trade, Position, TradesSummary
from AutoTrader.enums import OrderSide, OrderType
import copy

log = logger.get_logger(__name__)


class Account(ABC):
    # columns = ['Time', 'Action', 'Amount', 'Symbol', 'Price']
    transaction_percentage = NotImplemented
    transaction_fee = NotImplemented

    def __init__(self):
        balance = self._get_account_initial_balance()
        self.balance: Dict[str, float] = balance
        self.initial_balance: Dict[str, float] = copy.deepcopy(balance)
        self.trades: Dict[str, List[Trade]] = {}
        self.orders: Dict[str, List[Order]] = {}
        self.open_orders: Dict[str, List[Order]] = {}
        self.positions: Dict[str, Position] = {}

    def get_position(self, symbol: str) -> Position:
        return self.positions.get(symbol, Position())

    def get_orders(self, symbol: str) -> List[Order]:
        return self.orders.get(symbol, [])

    def get_trades(self, symbol: str) -> List[Trade]:
        return self.trades.get(symbol, [])

    def get_open_orders(self, symbol: str) -> List[Order]:
        return self.open_orders.get(symbol, [])

    def add_order(self, symbol: str, order: Order) -> None:
        self.orders[symbol] = [] if symbol not in self.orders else self.orders[symbol]
        self.orders[symbol].append(order)

    def add_trade(self, symbol: str, trade: Trade) -> None:
        self.trades[symbol] = [] if symbol not in self.trades else self.trades[symbol]
        self.trades[symbol].append(trade)

    def add_open_order(self, symbol: str, order: Order) -> None:
        self.open_orders[symbol] = [] if symbol not in self.open_orders else self.open_orders[symbol]
        self.open_orders[symbol].append(order)

    def set_position(self, symbol: str, position: Position) -> None:
        self.positions[symbol] = position

    def add_to_balance(self, symbol: str, amount: float) -> None:
        self.balance[symbol] = self.balance.get(symbol, 0) + amount

    def remove_from_balance(self, symbol: str, amount: float) -> None:
        self.balance[symbol] = self.balance.get(symbol) - amount

    def reset_position(self, symbol: str) -> None:
        self.positions[symbol] = Position()

    def get_symbol_balance(self, symbol: str) -> None:
        self.get_current_balance().get(symbol, 0)

    def refresh_balance(self) -> None:
        self.balance = self.get_current_balance()

    def get_trades_summary(self, symbol: str, primary_symbol: str, secondary_symbol: str, undo_last_position=True) -> TradesSummary:
        # If in position when getting all trades, revert last buy
        if undo_last_position:
            self._undo_last_position(symbol, primary_symbol, secondary_symbol)

        trades_summary = get_trades_summary(symbol=symbol,
                                            source_symbol=primary_symbol,
                                            destination_symbol=secondary_symbol,
                                            initial_balance= self.initial_balance[primary_symbol],
                                            end_balance=self.balance[primary_symbol],
                                            trades= self.trades[symbol])
        return trades_summary

    def get_plot(self, symbol: str) -> go:
        buys = [d for d in self.orders[symbol] if d.Side == OrderSide.BUY]
        sells = [d for d in self.orders[symbol] if d.Side == OrderSide.SELL]
        return go.Scatter(
            x=[d.Time for d in buys],
            y=[d.Price for d in buys],
            marker=dict(color="gold", size=13, symbol=46),
            mode="markers",
            name="Buy"
        ), go.Scatter(
            x=[d.Time for d in sells],
            y=[d.Price for d in sells],
            marker=dict(color="silver", size=13, symbol=45),
            mode="markers",
            name="Sell"
        )

    def _undo_last_position(self, symbol: str, primary_symbol: str, secondary_symbol: str) -> None:
        # If no position found with this symbol, return
        if symbol not in self.positions:
            return

        position = self.get_position(symbol)
        if position.is_valid():
            # Remove last transaction
            self.orders[symbol] = self.orders[symbol][:-1]
            # Remove last BUY Trades ? Maybe reverse pass through list and remove all buys until reaching a sell and breaking SAME WITH ORDERS
            self.trades[symbol] = self.trades[symbol][:-1]

            # Refund balance
            self.balance[primary_symbol] += position.AveragePrice * position.Quantity
            # Empty position
            self.reset_position(symbol)

    @abstractmethod
    def get_current_balance(self) -> Dict[str, float]:
        pass

    @abstractmethod
    def _get_account_initial_balance(self) -> Dict[str, float]:
        pass

    @abstractmethod
    def place_order(self,
                    time: int,
                    symbol: str,
                    source_symbol: str,
                    destination_symbol: str,
                    order_type: OrderType,
                    price: float,
                    side: OrderSide,
                    amount: float
                    ) -> None:
        pass

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
