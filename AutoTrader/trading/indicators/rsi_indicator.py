from AutoTrader.data.data_structures.candlesticks import Candlesticks
import numpy as np
import plotly.graph_objects as go
from AutoTrader.trading.indicators.inidicator import Indicator
from typing import List


class RSI(Indicator):
    # columns = ['Time', 'Gain', 'Loss', 'AverageGain', 'AverageLoss', 'RS', 'RSI']
    period = 14
    candlesticks: Candlesticks

    def __init__(self, candlesticks: Candlesticks):
        super().__init__(candlesticks)
        self.gain_counter = 0

    def process_new_candlestick(self) -> None:
        # Create new row
        self.list.append({'Time': self.candlesticks.get_last_time()})

        # Compute gain and loss
        if self.candlesticks.get_number_of_rows() >= 2:
            change = self.candlesticks.get_last_candlestick().Close - self.candlesticks.get_specific_candlestick(n=-2).Close
            if change > 0:
                self.list[-1]['Gain'] = change
                self.list[-1]['Loss'] = 0
            else:
                self.list[-1]['Loss'] = -change
                self.list[-1]['Gain'] = 0
            self.gain_counter += 1
        # Compute RSI
        if self.gain_counter >= self.period:
            self.list[-1]['AverageGain'] = np.mean([d['Gain'] for d in self.list[-self.period:]])
            self.list[-1]['AverageLoss'] = np.mean([d['Loss'] for d in self.list[-self.period:]])
            if self.list[-1]['AverageLoss'] != 0:
                self.list[-1]['RS'] = self.list[-1]['AverageGain'] / self.list[-1]['AverageLoss']
                self.list[-1]['RSI'] = 100 - (100 / (1 + self.list[-1]['RS']))
            else:
                self.list[-1]['RS'] = 100
                self.list[-1]['RSI'] = 100

    def process_new_tick(self) -> None:
        pass

    def get_plot(self) -> List:
        return [go.Scatter(x=[d['Time'] for d in self.list], y=[d['RSI'] if 'RSI' in d else None for d in self.list], name="RSI")]

    def delete_data(self) -> None:
        self.list = []
        self.gain_counter = 0
