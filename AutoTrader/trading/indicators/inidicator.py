from abc import ABC, abstractmethod
from AutoTrader.data.data_structures.candlesticks import Candlesticks


class Indicator(ABC):
    def __init__(self, candlesticks: Candlesticks):
        self.list = []
        self.candlesticks = candlesticks

    @abstractmethod
    def process_new_candlestick(self) -> None:
        pass

    @abstractmethod
    def process_new_tick(self):
        pass

    def get_last_values(self, n: int = 1) -> list:
        return self.list[-n:]

    def get_all_values(self) -> list:
        return self.list

    @abstractmethod
    def delete_data(self) -> None:
        pass

    @abstractmethod
    def get_plot(self):
        pass
