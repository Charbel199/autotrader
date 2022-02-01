from AutoTrader.data.data_structures.candlesticks import Candlesticks
import numpy as np
import plotly.graph_objects as go
from AutoTrader.trading.indicators.inidicator import Indicator
from typing import List


class ADX(Indicator):
    # columns = ['Time', 'TrueRange', 'ATR', 'H-pH', 'pL-L', '+DX', '-DX', 'Smooth+DX', 'Smooth-DX', '+DMI', '-DMI', 'DX','ADX']
    candlesticks: Candlesticks

    def __init__(self, candlesticks: Candlesticks, **kwargs):
        super().__init__(candlesticks)
        self.period = kwargs.get('period', 14)
        self.true_range_counter = 0
        self.atr_counter = 0
        self.dx_counter = 0
        self.adx_counter = 0

    def process_new_candlestick(self) -> None:
        # Create new row
        self.list.append({'Time': self.candlesticks.get_last_time()})
        last_candlestick = self.candlesticks.get_last_candlestick()

        if self.candlesticks.get_number_of_rows() >= 2:
            before_last_candlestick = self.candlesticks.get_specific_candlestick(n=-2)
            # Calculate true range
            self.list[-1]['TrueRange'] = max(last_candlestick.High - last_candlestick.Low, last_candlestick.High - before_last_candlestick.Close, before_last_candlestick.Close - last_candlestick.Low)
            self.true_range_counter += 1

            # Calculate H-pH and pL-L
            self.list[-1]['H-pH'] = last_candlestick.High - before_last_candlestick.High
            self.list[-1]['pL-L'] = before_last_candlestick.Low - last_candlestick.Low

            # Calculate +DX and -DX
            self.list[-1]['+DX'] = self.list[-1]['H-pH'] if self.list[-1]['H-pH'] > self.list[-1]['pL-L'] and self.list[-1]['H-pH'] > 0 else 0
            self.list[-1]['-DX'] = self.list[-1]['pL-L'] if self.list[-1]['pL-L'] > self.list[-1]['H-pH'] and self.list[-1]['pL-L'] > 0 else 0

        # Calculate ATR and smooth +DX and -DX
        if self.true_range_counter == self.period and self.atr_counter == 0:
            self.list[-1]['ATR'] = np.mean([d['TrueRange'] for d in self.list[-self.period:]])
            self.atr_counter += 1
            self.list[-1]['Smooth+DX'] = np.mean([d['+DX'] for d in self.list[-self.period:]])
            self.list[-1]['Smooth-DX'] = np.mean([d['-DX'] for d in self.list[-self.period:]])

        elif self.atr_counter > 0:
            self.list[-1]['ATR'] = (self.list[-2]['ATR'] * (self.period - 1) + self.list[-1]['TrueRange']) / self.period
            self.atr_counter += 1
            self.list[-1]['Smooth+DX'] = (self.list[-2]['Smooth+DX'] * (self.period - 1) + self.list[-1]['+DX']) / self.period
            self.list[-1]['Smooth-DX'] = (self.list[-2]['Smooth-DX'] * (self.period - 1) + self.list[-1]['-DX']) / self.period

        # Calculate +DMI and -DMI and DX a
        if self.atr_counter > 0:
            self.list[-1]['+DMI'] = (self.list[-1]['Smooth+DX'] / self.list[-1]['ATR']) * 100
            self.list[-1]['-DMI'] = (self.list[-1]['Smooth-DX'] / self.list[-1]['ATR']) * 100
            self.list[-1]['DX'] = (abs(self.list[-1]['+DMI'] - self.list[-1]['-DMI']) / (self.list[-1]['+DMI'] + self.list[-1]['-DMI'])) * 100
            self.dx_counter += 1
        # Calculate ADX
        if self.dx_counter == self.period and self.adx_counter == 0:
            self.list[-1]['ADX'] = np.mean([d['DX'] for d in self.list[-self.period:]])
            self.adx_counter += 1
        elif self.adx_counter > 0:
            self.list[-1]['ADX'] = (self.list[-2]['ADX'] * (self.period - 1) + self.list[-1]['DX']) / self.period
            self.adx_counter += 1

    def process_new_tick(self) -> None:
        pass

    def get_plot(self) -> List:
        return [go.Scatter(x=[d['Time'] for d in self.list], y=[d['ADX'] if 'ADX' in d else None for d in self.list], name="ADX")]

    def delete_data(self) -> None:
        self.list = []
        self.true_range_counter = 0
        self.atr_counter = 0
        self.dx_counter = 0
        self.adx_counter = 0
