from data_structures.structure import TickStructure
import pandas as pd


class PandasTickStructure(TickStructure):

    def __init__(self):
        self.df = pd.DataFrame(columns=self.columns)
        self.tick = {}

    def add_row(self, row):
        self.df.loc[len(self.df.index)] = row

    def add_tick(self, tick):
        self.tick = tick
        self.add_row(tick)

    def change_last_row(self, row):
        self.df.iloc[-1] = row

    def get_data(self):
        return self.df

    def get_tick(self):
        if self.tick:
            return self.tick

    @staticmethod
    def condition(name):
        return name == 'pandas'
