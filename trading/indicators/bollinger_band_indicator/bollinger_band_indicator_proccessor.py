import pandas as pd
from data.data_structures.structure import TickStructure
import numpy as np
import plotly.graph_objects as go
from helper import data_structure_helper


class BollingerBand(object):
    columns = ['Time', 'SMA', 'UpperBollingerBand', 'LowerBollingerBand']
    period = 19
    number_of_ticks_needed = 19
    bollinger_band_multiplier = 2
    data_structure: TickStructure
    temp_data_structure: TickStructure

    def __init__(self, data_structure):
        self.df = pd.DataFrame(columns=self.columns)
        self.data_structure = data_structure

    def process_new_candlestick(self):
        # Create temporary data structures
        temp_df = data_structure_helper.get_temp_df(self.df, self.period)
        self.temp_data_structure = data_structure_helper.get_temp_tick_data_structure(self.data_structure, self.number_of_ticks_needed)

        # Create new row
        temp_df.loc[len(self.df.index)] = {'Time': self.temp_data_structure.get_last_time()}
        if self.temp_data_structure.get_number_of_rows() >= self.period:
            temp_df['SMA'].iloc[-1] = np.mean(self.temp_data_structure.get_last_rows(self.period)['Close'].tolist())
        if temp_df['SMA'].count() >= 1:
            deviation = np.std(self.temp_data_structure.get_last_rows(self.period)['Close'].tolist())
            temp_df['UpperBollingerBand'].iloc[-1] = temp_df['SMA'].iloc[-1] + deviation * self.bollinger_band_multiplier
            temp_df['LowerBollingerBand'].iloc[-1] = temp_df['SMA'].iloc[-1] - deviation * self.bollinger_band_multiplier
        self.df = self.df.append(temp_df.tail(1))

    def get_last_bollinger_bands_values(self, n=1):
        # Gets last BollingerBands by default
        return self.df[['Time', 'UpperBollingerBand', 'LowerBollingerBand', 'SMA']].tail(n)

    def get_all_bollinger_bands_values(self):
        return self.df[['Time', 'UpperBollingerBand', 'LowerBollingerBand', 'SMA']]

    def delete_data(self):
        self.df = pd.DataFrame(columns=self.columns)

    def get_plot(self):
        return go.Scatter(x=self.df['Time'].tolist(), y=self.df['UpperBollingerBand'].tolist(), name="UpperBollingerBand"), \
               go.Scatter(x=self.df['Time'].tolist(), y=self.df['LowerBollingerBand'].tolist(), name="LowerBollingerBand"), \
               go.Scatter(x=self.df['Time'].tolist(), y=self.df['SMA'].tolist(), name="SMA")
