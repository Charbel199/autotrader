from __future__ import annotations
from abc import ABC, abstractmethod
import plotly.graph_objects as go
from app.AutoTrader.exceptions import DataStructureNotFound
from app.AutoTrader.models import Tick
from typing import List


class Candlesticks(ABC):
    columns = ['Time', 'Open', 'Close', 'High', 'Low', 'Volume', 'OpenTime', 'CloseTime']

    def __init__(self):
        pass

    @abstractmethod
    def add_row(self, row: Tick) -> None:
        pass

    @abstractmethod
    def add_bulk_rows(self, rows: List[Tick]) -> None:
        pass

    @abstractmethod
    def set_tick(self, tick: Tick) -> None:
        pass

    @abstractmethod
    def get_data(self) -> object:
        pass

    @abstractmethod
    def get_specific_candlestick(self, n: int) -> Tick:
        pass

    @abstractmethod
    def get_tick(self) -> Tick:
        pass

    @abstractmethod
    def get_number_of_rows(self) -> int:
        pass

    @abstractmethod
    def get_last_candlesticks(self, n: int) -> List[Tick]:
        pass

    @abstractmethod
    def get_last_candlestick(self) -> Tick:
        pass

    @abstractmethod
    def get_last_time(self) -> int:
        pass

    @abstractmethod
    def get_last_time_tick(self) -> int:
        pass

    @abstractmethod
    def get_plot(self) -> go:
        pass


    @abstractmethod
    def delete_data(self) -> None:
        pass

    @abstractmethod
    def reduce(self, reduced_size: int = 300, trigger_size: int = 500) -> None:
        pass

    @staticmethod
    @abstractmethod
    def condition(name: str) -> bool:
        pass


# Get fetcher based on broker name
def get_data_structure(name) -> Candlesticks:
    for data_structure in Candlesticks.__subclasses__():
        if data_structure.condition(name):
            return data_structure()
    raise DataStructureNotFound(f"Data structure: {name} not found")
