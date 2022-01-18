from AutoTrader.data.data_structures.candlesticks import Candlesticks
import plotly.graph_objects as go
from AutoTrader.trading.indicators.inidicator import Indicator
import numpy as np
from typing import List


class MACD(Indicator):
    # columns = ['Time', 'EMA1', 'EMA2', 'MACD', 'Signal']
    period_1 = 12
    period_2 = 26
    period_3 = 9
    multiplier_1 = 2 / (period_1 + 1)
    multiplier_2 = 2 / (period_2 + 1)
    multiplier_3 = 2 / (period_3 + 1)

    ema_counter_1 = 0
    ema_counter_2 = 0
    signal_counter = 0

    candlesticks: Candlesticks

    def __init__(self, candlesticks: Candlesticks):
        super().__init__(candlesticks)

    def process_new_candlestick(self) -> None:
        # Create new row
        self.list.append({'Time': self.candlesticks.get_last_time()})
        number_of_rows = self.candlesticks.get_number_of_rows()

        if number_of_rows >= self.period_1:
            if self.ema_counter_1 == 0:
                self.list[-1]['EMA1'] = np.mean([d.Close for d in self.candlesticks.get_last_candlesticks(self.period_1)])
            else:
                self.list[-1]['EMA1'] = ((self.candlesticks.get_last_candlestick().Close - self.list[-2]['EMA1']) * self.multiplier_1) + self.list[-2]['EMA1']
            self.ema_counter_1 += 1

        if number_of_rows >= self.period_2:
            if self.ema_counter_2 == 0:
                self.list[-1]['EMA2'] = np.mean([d.Close for d in self.candlesticks.get_last_candlesticks(self.period_2)])
            else:
                self.list[-1]['EMA2'] = ((self.candlesticks.get_last_candlestick().Close - self.list[-2]['EMA2']) * self.multiplier_2) + self.list[-2]['EMA2']
            self.ema_counter_2 += 1

            self.list[-1]['MACD'] = self.list[-1]['EMA1'] - self.list[-1]['EMA2']

        if self.ema_counter_2 > self.period_3:
            if self.signal_counter == 0:
                self.list[-1]['Signal'] = np.mean([d['MACD'] for d in self.list[-self.period_3:]])
            else:
                self.list[-1]['Signal'] = ((self.list[-1]['MACD'] - self.list[-2][
                    'Signal']) * self.multiplier_3) + self.list[-2]['Signal']
            self.signal_counter += 1

    def process_new_tick(self) -> None:
        pass

    def get_plot(self) -> List:
        return [go.Scatter(x=[d['Time'] for d in self.list],
                           y=[d['MACD'] if 'MACD' in d else None for d in self.list],
                           name="MACD"), \
                go.Scatter(x=[d['Time'] for d in self.list],
                           y=[d['Signal'] if 'Signal' in d else None for d in self.list],
                           name="Signal")]

    def delete_data(self) -> None:
        self.list = []
        self.ema_counter_1 = 0
        self.ema_counter_2 = 0
        self.signal_counter = 0
