from data.data_structures.structure import TickStructure
import plotly.graph_objects as go


class ListTickStructure(TickStructure):

    def __init__(self):
        super().__init__()
        self.list = []
        self.tick = {}

    def add_row(self, row: dict) -> None:
        self.list.append(row)

    def add_bulk_rows(self, rows: list) -> None:
        self.list.extend(rows)

    def set_tick(self, tick: dict) -> None:
        self.tick = tick

    def get_last_time(self) -> int:
        return self.list[-1]['Time']

    def get_last_time_tick(self) -> int:
        if self.tick:
            return self.tick['Time']
        return 0

    def get_last_value(self, column_name: str) -> float:
        return self.list[-1][column_name]

    def get_before_last_value(self, column_name: str) -> float:
        return self.list[-2][column_name]

    def get_specific_value(self, column_name: str, n: int):
        return self.list[n][column_name]

    def get_data(self) -> object:
        return self.list

    def get_tick(self) -> dict:
        if self.tick:
            return self.tick
        return {}

    def get_last_rows(self, n: int, column_name: str) -> list:
        return [d[column_name] for d in self.list[-n:]]

    def reduce(self, reduced_size: int = 300, trigger_size: int = 500) -> None:
        if len(self.list) >= trigger_size:
            self.list = self.list[-reduced_size:]

    def get_number_of_rows(self) -> int:
        return len(self.list)

    def set_data_structure_content(self, data_structure_content: list) -> None:
        self.list = data_structure_content

    def get_tick_structure_copy(self, n: int = 0) -> TickStructure:
        new_data_structure = TickStructure()
        if n == 0:
            new_data_structure.set_data_structure_content(self.list.copy())
        else:
            new_data_structure.set_data_structure_content(self.list[-n:])
        return new_data_structure

    def get_tick_close(self) -> float:
        return float(self.tick['Close'])

    def get_plot(self) -> go:
        return go.Candlestick(x=[d['Time'] for d in self.list],
                              open=[d['Open'] for d in self.list],
                              high=[d['High'] for d in self.list],
                              low=[d['Low'] for d in self.list],
                              close=[d['Close'] for d in self.list], name="Candlesticks")

    def delete_data(self) -> None:
        self.list = []
        self.tick = {}

    @staticmethod
    def condition(name: str) -> bool:
        return name == 'list'
