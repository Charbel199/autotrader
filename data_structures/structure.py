from abc import ABC, abstractmethod


class TickStructure(ABC):
    columns = ['Time', 'Open', 'Close', 'High', 'Low', 'Volume', 'OpenTime', 'CloseTime']
    def __init__(self):
        pass

    @abstractmethod
    def add_row(self, row):
        pass

    @abstractmethod
    def add_tick(self, tick):
        pass

    @abstractmethod
    def change_last_row(self, row):
        pass

    @abstractmethod
    def get_data(self):
        pass

    @abstractmethod
    def get_tick(self):
        pass

    @staticmethod
    @abstractmethod
    def condition(name):
        pass


# Get fetcher based on broker name
def get_data_structure(name):
    for data_structure in TickStructure.__subclasses__():
        if data_structure.condition(name):
            return data_structure()
    return None
