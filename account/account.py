from abc import ABC, abstractmethod


class Account(ABC):

    def __init__(self):
        self.position = {}

    @abstractmethod
    def get_position(self):
        return self.position

    @abstractmethod
    def buy(self, symbol, amount, price):
        pass

    @abstractmethod
    def sold(self, symbol, amount, price):
        pass

    # Sell and buy orders

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
