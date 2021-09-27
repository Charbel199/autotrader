import pandas as pd
from data_structures.structure import TickStructure

class CandlestickType(object):
    columns = ['Time', 'Type']
    maxNumberOfPreviousCandlesticks = 4
    data_structure: TickStructure

    def __init__(self, data_structure):
        self.df = pd.DataFrame(columns=self.columns)
        self.data_structure = data_structure

    def process_new_candlestick(self):
        # Create temporary dataframe (We only need a couple of the last data points)
        if len(self.df.index) > self.maxNumberOfPreviousCandlesticks:
            temp_df = self.df.tail(self.maxNumberOfPreviousCandlesticks).copy()
        else:
            temp_df = self.df.copy()

        # Create new row
        temp_df.loc[len(self.df.index)] = {'Time': self.data_structure.get_last_value('Time')}

        if self.data_structure.get_number_of_rows() >= 2:
          pass

        # Update candlestickType dataframe
        self.df = self.df.append(temp_df.tail(1))

    def get_last_candlestick_type_values(self, n=1):
        # Gets last ADX by default
        return self.df[['Time', 'Type']].tail(n)
