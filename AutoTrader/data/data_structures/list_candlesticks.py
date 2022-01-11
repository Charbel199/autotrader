from AutoTrader.data.data_structures.candlesticks import Candlesticks
import plotly.graph_objects as go
from AutoTrader.models import Tick
from typing import List


class ListCandlesticks(Candlesticks):

    def __init__(self):
        super().__init__()
        self.candlesticks: List[Tick] = []
        self.tick: Tick = Tick()

    def add_row(self, row: Tick) -> None:
        self.candlesticks.append(row)

    def add_bulk_rows(self, rows: List[Tick]) -> None:
        self.candlesticks.extend(rows)

    def set_tick(self, tick: Tick) -> None:
        self.tick = tick

    def get_last_time(self) -> int:
        return self.candlesticks[-1].Time

    def get_last_time_tick(self) -> int:
        if self.tick:
            return self.tick.Time
        return 0

    def get_last_candlestick(self) -> Tick:
        return self.candlesticks[-1]

    def get_specific_candlestick(self, n: int) -> Tick:
        return self.candlesticks[n]

    def get_data(self) -> object:
        return self.candlesticks

    def get_tick(self) -> Tick:
        if self.tick:
            return self.tick
        return Tick()

    def get_last_candlesticks(self, n: int) -> List[Tick]:
        return self.candlesticks[-n:]

    def reduce(self, reduced_size: int = 300, trigger_size: int = 500) -> None:
        if len(self.candlesticks) >= trigger_size:
            self.candlesticks = self.candlesticks[-reduced_size:]

    def get_number_of_rows(self) -> int:
        return len(self.candlesticks)

    def set_data_structure_content(self, data_structure_content: List[Tick]) -> None:
        self.candlesticks = data_structure_content

    def get_plot(self) -> go:
        return go.Candlestick(x=[d.Time for d in self.candlesticks],
                              open=[d.Open for d in self.candlesticks],
                              high=[d.High for d in self.candlesticks],
                              low=[d.Low for d in self.candlesticks],
                              close=[d.Close for d in self.candlesticks], name="Candlesticks")

    def delete_data(self) -> None:
        self.candlesticks = []
        self.tick = Tick()

    @staticmethod
    def condition(name: str) -> bool:
        return name == 'list'
