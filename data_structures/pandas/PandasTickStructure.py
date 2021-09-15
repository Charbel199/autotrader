from data_structures.structure import TickStructure
import pandas as pd


class PandasTickStructure(TickStructure):

    def __init__(self, ):
        self.df = pd.DataFrame(columns=self.columns)

    def add_row(self, row):
        self.df.loc[len(self.df.index)] = row
        print('DF NOW')
        print(self.df)

    def change_last_row(self, row):
        self.df.iloc[-1] = row
