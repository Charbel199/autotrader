from abc import ABC, abstractmethod
from data_structures.structure import TickStructure
from account.account import Account


class Strategy(ABC):
    data_structure: TickStructure
    account: Account

    def __init__(self, data_structure, account):
        self.data_structure = data_structure
        self.account = account

    # Happens AFTER updating the tick in the data structure
    @abstractmethod
    def process_new_tick(self):
        pass

    # Happens AFTER adding the new candlestick in the data structure
    @abstractmethod
    def process_new_candlestick(self):
        pass

    @abstractmethod
    def get_figure(self):
        pass

    @staticmethod
    @abstractmethod
    def condition(name):
        pass


# Get strategy
def get_strategy(name, data_structure, account):
    for strategy in Strategy.__subclasses__():
        if strategy.condition(name):
            return strategy(data_structure, account)
    return None
