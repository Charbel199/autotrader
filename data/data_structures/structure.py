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
    def get_data(self):
        pass

    @abstractmethod
    def get_specific_value(self, column_name, n):
        pass

    @abstractmethod
    def get_tick(self):
        pass

    @abstractmethod
    def get_number_of_rows(self):
        pass

    @abstractmethod
    def get_last_rows(self, n, column_name):
        pass

    @abstractmethod
    def get_last_value(self, column_name):
        pass

    @abstractmethod
    def get_before_last_value(self, column_name):
        pass

    @abstractmethod
    def set_data_structure_content(self, data_structure_content):
        pass

    @abstractmethod
    def get_tick_structure_copy(self, n=0):
        pass

    @abstractmethod
    def get_last_time(self):
        pass

    @abstractmethod
    def get_last_time_tick(self):
        pass

    @abstractmethod
    def get_plot(self):
        pass

    @abstractmethod
    def get_tick_close(self):
        pass

    @abstractmethod
    def delete_data(self):
        pass

    @abstractmethod
    def reduce(self, reduced_size=300, trigger_size=500):
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
