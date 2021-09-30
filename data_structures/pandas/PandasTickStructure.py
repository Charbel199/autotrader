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

    def get_last_value(self, column_name):
        return float(self.df[column_name].iloc[-1])

    def get_before_last_value(self, column_name):
        return float(self.df[column_name].iloc[-2])

    def get_specific_value(self, column_name, n):
        return float(self.df[column_name].iloc[n])

    def get_data(self):
        return self.df

    def get_tick(self):
        if self.tick:
            return self.tick
        return {}

    def get_copy(self):
        return self.df.copy()

    def get_last_row(self):
        return self.df.tail(1)

    def get_last_rows(self, n):
        return self.df.tail(n)

    def get_last_rows_copy(self, n):
        return self.df.tail(n).copy()

    def get_before_last_row(self):
        return self.df.iloc[-2]

    def get_number_of_rows(self):
        return len(self.df.index)

    def set_data_structure_content(self, data_structure_content):
        self.df = data_structure_content

    def get_tick_structure_copy(self, n=0):
        new_data_structure = PandasTickStructure()
        if n == 0:
            new_data_structure.set_data_structure_content(self.df.copy())
        else:
            new_data_structure.set_data_structure_content(self.df.tail(n).copy())
        return new_data_structure

    @staticmethod
    def condition(name):
        return name == 'pandas'
