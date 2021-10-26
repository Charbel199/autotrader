from AutoTrader.data.data_structures.structure import TickStructure
import numpy as np
import plotly.graph_objects as go
from AutoTrader.trading.indicators.inidicator import Indicator


class BollingerBand(Indicator):
    # columns = ['Time', 'SMA', 'UpperBollingerBand', 'LowerBollingerBand']
    period = 19
    bollinger_band_multiplier = 2
    data_structure: TickStructure

    def __init__(self, data_structure: TickStructure):
        super().__init__(data_structure)
        self.sma_counter = 0

    def process_new_candlestick(self) -> None:

        # Create new row
        self.list.append({'Time': self.data_structure.get_last_time()})

        if self.data_structure.get_number_of_rows() >= self.period:
            self.list[-1]['SMA'] = np.mean(self.data_structure.get_last_rows(self.period, 'Close'))
            self.sma_counter += 1
        if self.sma_counter >= 1:
            deviation = np.std(self.data_structure.get_last_rows(self.period, 'Close'))
            self.list[-1]['UpperBollingerBand'] = self.list[-1]['SMA'] + deviation * self.bollinger_band_multiplier
            self.list[-1]['LowerBollingerBand'] = self.list[-1]['SMA'] - deviation * self.bollinger_band_multiplier

    def process_new_tick(self):
        pass

    def get_plot(self):
        return go.Scatter(x=[d['Time'] for d in self.list], y=[d['UpperBollingerBand'] for d in self.list if 'UpperBollingerBand' in d], name="UpperBollingerBand"), \
               go.Scatter(x=[d['Time'] for d in self.list], y=[d['LowerBollingerBand'] for d in self.list if 'LowerBollingerBand' in d], name="LowerBollingerBand"), \
               go.Scatter(x=[d['Time'] for d in self.list], y=[d['SMA'] for d in self.list if 'SMA' in d], name="SMA")

    def delete_data(self) -> None:
        self.list = []
        self.sma_counter = 0
