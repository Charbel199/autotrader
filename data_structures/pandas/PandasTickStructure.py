from data_structures.structure import TickStructure
import pandas as pd


class PandasTickStructure(TickStructure):

    def __init__(self):
        super().__init__()
        self.df = pd.DataFrame(columns=self.columns)
        self.tick = {}

    def add_row(self, row):
        self.df.loc[len(self.df.index)] = row

    def add_bulk_rows(self, rows):
        self.df = self.df.append(pd.DataFrame(rows), ignore_index=True)

    def set_tick(self, tick):
        self.tick = tick

    def change_last_row(self, row):
        self.df.iloc[-1] = row

    def get_data(self):
        return self.df

    def get_tick(self):
        if self.tick:
            return self.tick
        return {}

    @staticmethod
    def condition(name):
        return name == 'pandas'
