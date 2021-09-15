from abc import ABC, abstractmethod


class TickStructure(ABC):
    columns = ['Time', 'Open', 'Close', 'High', 'Low', 'Volume', 'OpenTime', 'CloseTime']

    def __init__(self):
        pass

    @abstractmethod
    def add_row(self, row):
        pass

    @abstractmethod
    def change_last_row(self, row):
        pass
