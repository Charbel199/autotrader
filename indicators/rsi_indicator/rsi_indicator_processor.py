import pandas as pd
from data_structures.structure import TickStructure


class RSI(object):
    columns = ['Time', 'RSI']
    period = 14

    data_structure: TickStructure

    def __init__(self, data_structure):
        self.df = pd.DataFrame(columns=self.columns)
        self.data_structure = data_structure

    def process_new_candlestick(self):
        # Create temporary dataframe (We only need the last {period} data points)
        if len(self.df.index) > self.period:
            temp_df = self.df.tail(self.period).copy()
        else:
            temp_df = self.df.copy()

        # Create new row
        temp_df.loc[len(self.df.index)] = {'Time': self.data_structure.get_last_value('Time')}

        # Update ADX dataframe
        self.df = self.df.append(temp_df.tail(1))

    def get_last_rsi_values(self, n=1):
        # Gets last ADX by default
        return self.df[['Time', 'RSI']].tail(n)
