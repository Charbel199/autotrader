from AutoTrader.data.data_structures.structure import TickStructure
import plotly.graph_objects as go
from AutoTrader.data.models import Tick
from typing import List


class ListTickStructure(TickStructure):

    def __init__(self):
        super().__init__()
        self.list: List[Tick] = []
        self.tick: Tick = Tick()

    def add_row(self, row: Tick) -> None:
        self.list.append(row)

    def add_bulk_rows(self, rows: List[Tick]) -> None:
        self.list.extend(rows)

    def set_tick(self, tick: Tick) -> None:
        self.tick = tick

    def get_last_time(self) -> int:
        return self.list[-1].Time

    def get_last_time_tick(self) -> int:
        if self.tick:
            return self.tick.Time
        return 0

    def get_last_candlestick(self) -> Tick:
        return self.list[-1]

    def get_before_last_candlestick(self) -> Tick:
        return self.list[-2]

    def get_specific_candlestick(self, n: int) -> Tick:
        return self.list[n]

    def get_data(self) -> object:
        return self.list

    def get_tick(self) -> Tick:
        if self.tick:
            return self.tick
        return Tick()

    def get_last_candlesticks(self, n: int) -> List[Tick]:
        return self.list[-n:]

    def reduce(self, reduced_size: int = 300, trigger_size: int = 500) -> None:
        if len(self.list) >= trigger_size:
            self.list = self.list[-reduced_size:]

    def get_number_of_rows(self) -> int:
        return len(self.list)

    def set_data_structure_content(self, data_structure_content: List[Tick]) -> None:
        self.list = data_structure_content

    def get_tick_structure_copy(self, n: int = 0) -> TickStructure:
        new_data_structure = TickStructure()
        if n == 0:
            new_data_structure.set_data_structure_content(self.list.copy())
        else:
            new_data_structure.set_data_structure_content(self.list[-n:])
        return new_data_structure

    def get_tick_close(self) -> float:
        return float(self.tick.Close)

    def get_plot(self) -> go:
        return go.Candlestick(x=[d.Time for d in self.list],
                              open=[d.Open for d in self.list],
                              high=[d.High for d in self.list],
                              low=[d.Low for d in self.list],
                              close=[d.Close for d in self.list], name="Candlesticks")

    def delete_data(self) -> None:
        self.list = []
        self.tick = {}

    @staticmethod
    def condition(name: str) -> bool:
        return name == 'list'
