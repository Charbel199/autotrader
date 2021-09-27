import pandas as pd
from data_structures.structure import TickStructure
import numpy as np


class ADX(object):
    columns = ['Time', 'TrueRange', 'ATR', 'H-pH', 'pL-L', '+DX', '-DX', 'Smooth+DX', 'Smooth-DX', '+DMI', '-DMI', 'DX',
               'ADX']
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
        if self.data_structure.get_number_of_rows() >= 2:
            # Calculate true range
            temp_df['TrueRange'].iloc[-1] = max(
                self.data_structure.get_last_value('High') - self.data_structure.get_last_value('Low'),
                self.data_structure.get_last_value('High') - self.data_structure.get_before_last_value('Close'),
                self.data_structure.get_before_last_value('Close') - self.data_structure.get_last_value('Low')
            )
            # Calculate H-pH and pL-L
            temp_df['H-pH'].iloc[-1] = self.data_structure.get_last_value('High') - self.data_structure.get_before_last_value('High')
            temp_df['pL-L'].iloc[-1] = self.data_structure.get_before_last_value('Low') - self.data_structure.get_last_value('Low')

            # Calculate +DX and -DX
            temp_df['+DX'].iloc[-1] = temp_df['H-pH'].iloc[-1] if temp_df['H-pH'].iloc[-1] > temp_df['pL-L'].iloc[-1] and temp_df['H-pH'].iloc[-1] > 0 else 0
            temp_df['-DX'].iloc[-1] = temp_df['pL-L'].iloc[-1] if temp_df['pL-L'].iloc[-1] > temp_df['H-pH'].iloc[-1] and temp_df['pL-L'].iloc[-1] > 0 else 0

        # Calculate ATR and smooth +DX and -DX
        if temp_df['TrueRange'].count() == self.period and temp_df['ATR'].count() == 0:
            temp_df['ATR'].iloc[-1] = np.mean(temp_df['TrueRange'].tail(self.period).tolist())
            temp_df['Smooth+DX'].iloc[-1] = np.mean(temp_df['+DX'].tail(self.period).tolist())
            temp_df['Smooth-DX'].iloc[-1] = np.mean(temp_df['-DX'].tail(self.period).tolist())

        elif temp_df['ATR'].count() > 0:
            temp_df['ATR'].iloc[-1] = (temp_df['ATR'].iloc[-2] * (self.period - 1) + temp_df['TrueRange'].iloc[-1]) / self.period
            temp_df['Smooth+DX'].iloc[-1] = (temp_df['Smooth+DX'].iloc[-2] * (self.period - 1) + temp_df['+DX'].iloc[-1]) / self.period
            temp_df['Smooth-DX'].iloc[-1] = (temp_df['Smooth-DX'].iloc[-2] * (self.period - 1) + temp_df['-DX'].iloc[-1]) / self.period

        # Calculate +DMI and -DMI and DX a
        if temp_df['ATR'].count() > 0:
            temp_df['+DMI'].iloc[-1] = (temp_df['Smooth+DX'].iloc[-1] / temp_df['ATR'].iloc[-1]) * 100
            temp_df['-DMI'].iloc[-1] = (temp_df['Smooth-DX'].iloc[-1] / temp_df['ATR'].iloc[-1]) * 100
            temp_df['DX'].iloc[-1] = (abs(temp_df['+DMI'].iloc[-1] - temp_df['-DMI'].iloc[-1]) / (temp_df['+DMI'].iloc[-1] + temp_df['-DMI'].iloc[-1])) * 100

        # Calculate ADX
        if temp_df['DX'].count() == self.period and temp_df['ADX'].count() == 0:
            temp_df['ADX'].iloc[-1] = np.mean(temp_df['DX'].tail(self.period).tolist())
        elif temp_df['DX'].count() > 0:
            temp_df['ADX'].iloc[-1] = (temp_df['ADX'].iloc[-2] * (self.period - 1) + temp_df['DX'].iloc[-1]) / self.period

        # Update ADX dataframe
        self.df = self.df.append(temp_df.tail(1))

    def get_last_adx_values(self, n=1):
        # Gets last ADX by default
        return self.df[['Time', 'ADX']].tail(n)
