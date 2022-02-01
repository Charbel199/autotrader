from AutoTrader.data.data_structures.candlesticks import Candlesticks
import numpy as np
import plotly.graph_objects as go
from AutoTrader.trading.indicators.inidicator import Indicator
from typing import List


class BollingerBand(Indicator):
    # columns = ['Time', 'SMA', 'UpperBollingerBand', 'LowerBollingerBand']
    candlesticks: Candlesticks

    def __init__(self, candlesticks: Candlesticks, **kwargs):
        super().__init__(candlesticks)
        self.period = kwargs.get('period', 19)
        self.bollinger_band_multiplier = kwargs.get('bollinger_band_multiplier', 2)
        self.sma_counter = 0

    def process_new_candlestick(self) -> None:

        # Create new row
        self.list.append({'Time': self.candlesticks.get_last_time()})

        if self.candlesticks.get_number_of_rows() >= self.period:
            last_closes = [c.Close for c in self.candlesticks.get_last_candlesticks(self.period)]
            self.list[-1]['SMA'] = np.mean(last_closes)
            self.sma_counter += 1
            if self.sma_counter >= 1:
                deviation = np.std(last_closes)
                self.list[-1]['UpperBollingerBand'] = self.list[-1]['SMA'] + deviation * self.bollinger_band_multiplier
                self.list[-1]['LowerBollingerBand'] = self.list[-1]['SMA'] - deviation * self.bollinger_band_multiplier

    def process_new_tick(self) -> None:
        pass

    def get_plot(self) -> List:
        return [go.Scatter(x=[d['Time'] for d in self.list], y=[d['UpperBollingerBand'] if 'UpperBollingerBand' in d else None for d in self.list], name="UpperBollingerBand"), \
                go.Scatter(x=[d['Time'] for d in self.list], y=[d['LowerBollingerBand'] if 'LowerBollingerBand' in d else None for d in self.list], name="LowerBollingerBand"), \
                go.Scatter(x=[d['Time'] for d in self.list], y=[d['SMA'] if 'SMA' in d else None for d in self.list], name="SMA")]

    def delete_data(self) -> None:
        self.list = []
        self.sma_counter = 0
