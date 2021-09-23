from abc import ABC, abstractmethod


class TickStructure(ABC):
    columns = ['Time', 'Open', 'Close', 'High', 'Low', 'Volume', 'OpenTime', 'CloseTime']

    def __init__(self):
        pass

    @abstractmethod
    def add_row(self, row):
        pass

    @abstractmethod
    def add_bulk_rows(self, rows):
        pass

    @abstractmethod
    def set_tick(self, tick):
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

    @abstractmethod
    def get_number_of_rows(self):
        pass

    @abstractmethod
    def get_last_row(self):
        pass

    @abstractmethod
    def get_last_rows(self, n):
        pass
    @abstractmethod
    def get_last_value(self, column_name):
        pass
    @abstractmethod
    def get_before_last_row(self):
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
