from abc import ABC, abstractmethod
import pandas as pd
from data.data_logger import logger

log = logger.get_logger(__name__)


class Account(ABC):
    columns = ['Time', 'Action', 'Amount', 'Symbol', 'Price']

    def __init__(self, balance):
        self.position = {}
        self.initial_balance = balance
        self.balance = balance
        self.df = pd.DataFrame(columns=self.columns)

    @abstractmethod
    def get_position(self):
        return self.position

    @abstractmethod
    def buy(self, time, symbol, price, amount=0):
        pass

    @abstractmethod
    def sell(self, time, symbol, price, amount=0):
        pass

    def get_profit(self):
        # If in position when calculating profit, revert last buy
        if self.position != {}:
            self.df = self.df[:-1]
            self.balance += self.position['Price'] * self.position['Amount']

        sells = self.df[self.df["Action"] == "Sell"]
        buys = self.df[self.df["Action"] == "Buy"]
        total_buy_price = (buys["Price"] * buys["Amount"]).sum()
        total_sell_price = (sells["Price"] * sells["Amount"]).sum()
        profit = total_sell_price - total_buy_price
        # if total_buy_price != 0:
        #     percentage = ((total_sell_price - total_buy_price) / total_buy_price) * 100
        # else:
        #     percentage = 0
        percentage = (self.balance / self.initial_balance) * 100
        # log.info(f"Buy {total_buy_price}")
        # log.info(f"Sell {total_sell_price}")
        log.info(f"Initial balance {self.initial_balance}")
        log.info(f"End balance {self.balance}")
        log.info(f"Percentage gain: {percentage}")
        return profit

    @abstractmethod
    def get_plot(self):
        pass

    @staticmethod
    @abstractmethod
    def condition(name):
        pass


# Get strategy
def get_account(name, balance):
    for account in Account.__subclasses__():
        if account.condition(name):
            return account(balance)
    return None
