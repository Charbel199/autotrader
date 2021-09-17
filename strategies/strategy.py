from abc import ABC, abstractmethod
from data_structures.structure import TickStructure


class Strategy(ABC):
    df: TickStructure

    def __init__(self, data_structure):
        self.data_structure = data_structure

    @abstractmethod
    def process_new_tick(self):
        pass

    @abstractmethod
    def process_new_candlestick(self):
        pass

    @staticmethod
    @abstractmethod
    def condition(name):
        pass


# Get strategy
def get_strategy(name, data_structure):
    for strategy in Strategy.__subclasses__():
        if strategy.condition(name):
            return strategy(data_structure)
    return None
