from abc import ABC, abstractmethod


class Indicator(ABC):
    def __init__(self, data_structure):
        self.list = []
        self.data_structure = data_structure

    @abstractmethod
    def process_new_candlestick(self):
        pass

    @abstractmethod
    def process_new_tick(self):
        pass

    def get_last_values(self, n=1):
        return self.list[-n:]

    def get_all_values(self):
        return self.list

    def delete_data(self):
        self.list = []

    @abstractmethod
    def get_plot(self):
        pass
