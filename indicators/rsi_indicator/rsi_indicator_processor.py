import pandas as pd
from data_structures.structure import TickStructure
import numpy as np


class RSI(object):
    columns = ['Time', 'Gain', 'Loss', 'AverageGain', 'AverageLoss', 'RS', 'RSI']
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

        # Compute gain and loss
        if self.data_structure.get_number_of_rows() >= 2:
            change = self.data_structure.get_last_value('Close') - self.data_structure.get_before_last_value('Close')
            if change > 0:
                temp_df['Gain'].iloc[-1] = change
                temp_df['Loss'].iloc[-1] = 0
            else:
                temp_df['Loss'].iloc[-1] = -change
                temp_df['Gain'].iloc[-1] = 0

        # Compute RSI
        if temp_df['Gain'].count() >= self.period:
            temp_df['AverageGain'].iloc[-1] = np.mean(temp_df['Gain'].tail(self.period).tolist())
            temp_df['AverageLoss'].iloc[-1] = np.mean(temp_df['Loss'].tail(self.period).tolist())
            temp_df['RS'].iloc[-1] = temp_df['AverageGain'].iloc[-1] / temp_df['AverageLoss'].iloc[-1]
            temp_df['RSI'].iloc[-1] = 100 - (100 / (1 + temp_df['RS'].iloc[-1]))

        # Update RSI dataframe
        self.df = self.df.append(temp_df.tail(1))

    def get_last_rsi_values(self, n=1):
        # Gets last ADX by default
        return self.df[['Time', 'RSI']].tail(n)
