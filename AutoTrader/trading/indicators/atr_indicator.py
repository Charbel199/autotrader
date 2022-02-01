from AutoTrader.data.data_structures.candlesticks import Candlesticks
import numpy as np
import plotly.graph_objects as go
from AutoTrader.trading.indicators.inidicator import Indicator
from typing import List


class ATR(Indicator):
    # columns = ['Time', 'TrueRange', 'ATR']

    true_range_counter = 0
    candlesticks: Candlesticks

    def __init__(self, candlesticks: Candlesticks, **kwargs):
        super().__init__(candlesticks)
        self.period = kwargs.get('period', 14)

    def process_new_candlestick(self) -> None:

        # Create new row
        self.list.append({'Time': self.candlesticks.get_last_time()})
        number_of_rows = self.candlesticks.get_number_of_rows()

        if number_of_rows >= 2:
            current_candlestick = self.candlesticks.get_last_candlestick()
            current_high = current_candlestick.High
            current_low = current_candlestick.Low
            previous_close = self.candlesticks.get_last_candlesticks(n=2)[-2].Close
            self.list[-1]['TrueRange'] = max((current_high - current_low), abs(current_high - previous_close),
                                             abs(current_low - previous_close))
            self.true_range_counter += 1
            if self.true_range_counter >= self.period:
                self.list[-1]['ATR'] = np.mean([d['TrueRange'] for d in self.list[-self.period:]])
        # TODO: Add more weight to recent data

    def process_new_tick(self) -> None:
        pass

    def get_plot(self) -> List:
        return [go.Scatter(x=[d['Time'] for d in self.list],
                           y=[d['ATR'] if 'ATR' in d else None for d in self.list],
                           name="ATR")]

    def delete_data(self) -> None:
        self.list = []
        self.true_range_counter = 0
