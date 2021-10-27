from abc import ABC, abstractmethod
from AutoTrader.helper import date_helper, logger
import plotly.graph_objects as go
from AutoTrader.exceptions import AccountNotFound
from AutoTrader.services.summary import get_trades_summary,print_summary
log = logger.get_logger(__name__)


class Account(ABC):
    columns = ['Time', 'Action', 'Amount', 'Symbol', 'Price']

    def __init__(self, balance: float):
        self.position = {}
        self.initial_balance = balance
        self.balance = balance
        self.list = []

    @abstractmethod
    def get_position(self) -> dict:
        return self.position

    @abstractmethod
    def buy(self,
            time: int,
            symbol: str,
            price: float,
            amount: float = 0) -> None:
        pass

    @abstractmethod
    def sell(self,
             time: int,
             symbol: str,
             price: float,
             amount: float = 0) -> None:
        pass

    def get_profit(self) -> float:
        # If in position when calculating profit, revert last buy
        if self.position != {}:
            self.list = self.list[:-1]
            self.balance += self.position['Price'] * self.position['Amount']
            self.position = {}
        summary = get_trades_summary(self.list, self.initial_balance)
        log.info(print_summary(summary))
        return summary['PercentageChange']

    @abstractmethod
    def get_plot(self) -> go:
        pass

    def get_all_trades(self) -> list:
        if self.position != {}:
            self.list = self.list[:-1]
            self.balance += self.position['Price'] * self.position['Amount']
            self.position = {}
        summary = get_trades_summary(self.list, self.initial_balance)
        return summary['AllTrades']

    @staticmethod
    @abstractmethod
    def condition(name: str) -> bool:
        pass


# Get strategy
def get_account(name: str, balance: float) -> Account:
    for account in Account.__subclasses__():
        if account.condition(name):
            return account(balance)
    raise AccountNotFound(f"Account type: {name} not found")
