from AutoTrader.data.data_structures.candlesticks import Candlesticks
import plotly.graph_objects as go
from AutoTrader.trading.indicators.inidicator import Indicator
import numpy as np
from typing import List


class EMA(Indicator):
    # columns = ['Time', 'EMA']
    ema_counter = 0
    candlesticks: Candlesticks

    def __init__(self, candlesticks: Candlesticks, **kwargs):
        super().__init__(candlesticks)
        self.period = kwargs.get('period', 12)
        self.multiplier = 2 / (self.period + 1)

    def process_new_candlestick(self) -> None:
        # Create new row
        self.list.append({'Time': self.candlesticks.get_last_time()})
        number_of_rows = self.candlesticks.get_number_of_rows()

        if number_of_rows >= self.period:
            if self.ema_counter == 0:
                self.list[-1]['EMA'] = np.mean([d.Close for d in self.candlesticks.get_last_candlesticks(self.period)])
            else:
                self.list[-1]['EMA'] = ((self.candlesticks.get_last_candlestick().Close - self.list[-2]['EMA']) * self.multiplier) + self.list[-2]['EMA']
            self.ema_counter += 1

    def process_new_tick(self) -> None:
        pass

    def get_plot(self) -> List:
        return [go.Scatter(x=[d['Time'] for d in self.list],
                           y=[d['EMA'] if 'EMA' in d else None for d in self.list],
                           name="EMA")]

    def delete_data(self) -> None:
        self.list = []
        ema_counter = 0
