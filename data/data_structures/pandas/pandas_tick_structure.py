from data.data_structures.structure import TickStructure
import pandas as pd
import plotly.graph_objects as go


class PandasTickStructure(TickStructure):

    def __init__(self):
        super().__init__()
        self.df = pd.DataFrame(columns=self.columns)
        self.tick = {}

    def add_row(self, row: dict) -> None:
        self.df.loc[len(self.df.index)] = row

    def add_bulk_rows(self, rows: list) -> None:
        self.df = self.df.append(pd.DataFrame(rows), ignore_index=True)

    def set_tick(self, tick: dict) -> None:
        self.tick = tick

    def get_last_time(self) -> int:
        return self.df['Time'].iloc[-1]

    def get_last_time_tick(self) -> int:
        if self.tick:
            return self.tick['Time']
        return 0

    def get_last_value(self, column_name: str) -> float:
        return float(self.df[column_name].iloc[-1])

    def get_before_last_value(self, column_name: str) -> float:
        return float(self.df[column_name].iloc[-2])

    def get_specific_value(self, column_name: str, n: int):
        return float(self.df[column_name].iloc[n])

    def get_data(self) -> object:
        return self.df.values.tolist()

    def get_tick(self) -> dict:
        if self.tick:
            return self.tick
        return {}

    def set_data_structure_content(self, data_structure_content: list) -> None:
        self.df = pd.DataFrame(data_structure_content)

    def get_last_rows(self, n: int, column_name: str) -> list:
        return self.df.tail(n)[column_name].tolist()

    def reduce(self, reduced_size: int = 300, trigger_size: int = 500) -> None:
        if len(self.df) >= trigger_size:
            self.df = self.df.tail(reduced_size)
            self.df = self.df.reset_index(drop=True)

    def get_number_of_rows(self) -> int:
        return len(self.df.index)

    def get_tick_structure_copy(self, n: int = 0) -> TickStructure:
        new_data_structure = PandasTickStructure()
        if n == 0:
            new_data_structure.set_data_structure_content(self.df)
        else:
            new_data_structure.set_data_structure_content(self.df.tail(n))
        return new_data_structure

    def get_tick_close(self) -> float:
        return float(self.tick['Close'])

    def get_plot(self) -> go:
        return go.Candlestick(x=self.df['Time'],
                              open=self.df['Open'],
                              high=self.df['High'],
                              low=self.df['Low'],
                              close=self.df['Close'], name="Candlesticks")

    def delete_data(self) -> None:
        self.df = pd.DataFrame(columns=self.columns)
        self.tick = {}

    @staticmethod
    def condition(name: str) -> bool:
        return name == 'pandas'
