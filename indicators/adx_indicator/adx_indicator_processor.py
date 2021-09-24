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
        # Create new row
        self.df.loc[len(self.df.index)] = {'Time': self.data_structure.get_last_value('Time')}

        if self.data_structure.get_number_of_rows() >= 2:
            # Calculate true range
            self.df['TrueRange'].iloc[-1] = max(
                self.data_structure.get_last_value('High') - self.data_structure.get_last_value('Low'),
                self.data_structure.get_last_value('High') - self.data_structure.get_before_last_value('Close'),
                self.data_structure.get_before_last_value('Close') - self.data_structure.get_last_value('Low')
            )
            # Calculate H-pH and pL-L
            self.df['H-pH'].iloc[-1] = self.data_structure.get_last_value('High') - self.data_structure.get_before_last_value('High')
            self.df['pL-L'].iloc[-1] = self.data_structure.get_before_last_value('Low') - self.data_structure.get_last_value('Low')

            # Calculate +DX and -DX
            self.df['+DX'].iloc[-1] = self.df['H-pH'].iloc[-1] if self.df['H-pH'].iloc[-1] > self.df['pL-L'].iloc[-1] and self.df['H-pH'].iloc[-1] > 0 else 0
            self.df['-DX'].iloc[-1] = self.df['pL-L'].iloc[-1] if self.df['pL-L'].iloc[-1] > self.df['H-pH'].iloc[-1] and self.df['pL-L'].iloc[-1] > 0 else 0

        # Calculate ATR and smooth +DX and -DX
        if self.df['TrueRange'].count() == self.period and self.df['ATR'].count() == 0:
            self.df['ATR'].iloc[-1] = np.mean(self.df['TrueRange'].tail(self.period).tolist())
            self.df['Smooth+DX'].iloc[-1] = np.mean(self.df['+DX'].tail(self.period).tolist())
            self.df['Smooth-DX'].iloc[-1] = np.mean(self.df['-DX'].tail(self.period).tolist())

        elif self.df['ATR'].count() > 0:
            self.df['ATR'].iloc[-1] = (self.df['ATR'].iloc[-2] * (self.period - 1) + self.df['TrueRange'].iloc[-1]) / self.period
            self.df['Smooth+DX'].iloc[-1] = (self.df['Smooth+DX'].iloc[-2] * (self.period - 1) + self.df['+DX'].iloc[-1]) / self.period
            self.df['Smooth-DX'].iloc[-1] = (self.df['Smooth-DX'].iloc[-2] * (self.period - 1) + self.df['-DX'].iloc[-1]) / self.period

        # Calculate +DMI and -DMI and DX a
        if self.df['ATR'].count() > 0:
            self.df['+DMI'].iloc[-1] = (self.df['Smooth+DX'].iloc[-1] / self.df['ATR'].iloc[-1]) * 100
            self.df['-DMI'].iloc[-1] = (self.df['Smooth-DX'].iloc[-1] / self.df['ATR'].iloc[-1]) * 100
            self.df['DX'].iloc[-1] = (abs(self.df['+DMI'].iloc[-1] - self.df['-DMI'].iloc[-1]) / (self.df['+DMI'].iloc[-1] + self.df['-DMI'].iloc[-1]))*100

        # Calculate ADX
        if self.df['DX'].count() == self.period and self.df['ADX'].count() == 0:
            self.df['ADX'].iloc[-1] = np.mean(self.df['DX'].tail(self.period).tolist())
        elif self.df['DX'].count() > 0:
            self.df['ADX'].iloc[-1] = (self.df['ADX'].iloc[-2] * (self.period - 1) + self.df['DX'].iloc[-1]) / self.period



    def get_last_adx_values(self, n=1):
        # Gets last ADX by default
        return self.df[['Time', 'ADX']].tail(n)
