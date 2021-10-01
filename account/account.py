from abc import ABC, abstractmethod
import pandas as pd


class Account(ABC):
    columns = ['Time', 'Action', 'Amount', 'Symbol', 'Price']

    def __init__(self):
        self.position = {}
        self.df = pd.DataFrame(columns=self.columns)

    @abstractmethod
    def get_position(self):
        return self.position

    @abstractmethod
    def buy(self, time, symbol, amount, price):
        pass

    @abstractmethod
    def sell(self, time, symbol, amount, price):
        pass

    @staticmethod
    @abstractmethod
    def condition(name):
        pass


# Get strategy
def get_account(name):
    for account in Account.__subclasses__():
        if account.condition(name):
            return account()
    return None
