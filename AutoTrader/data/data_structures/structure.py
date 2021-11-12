from __future__ import annotations
from abc import ABC, abstractmethod
import plotly.graph_objects as go
from AutoTrader.exceptions import DataStructureNotFound
from AutoTrader.data.models import Tick
from typing import List

class TickStructure(ABC):
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
    def get_before_last_candlestick(self) -> Tick:
        pass

    @abstractmethod
    def get_tick_structure_copy(self, n: int = 0) -> TickStructure:
        pass

    @abstractmethod
    def set_data_structure_content(self, data_structure_content: List[Tick]) -> None:
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
    def get_tick_close(self) -> float:
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
def get_data_structure(name) -> TickStructure:
    for data_structure in TickStructure.__subclasses__():
        if data_structure.condition(name):
            return data_structure()
    raise DataStructureNotFound(f"Data structure: {name} not found")
