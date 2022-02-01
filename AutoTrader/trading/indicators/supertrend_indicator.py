from AutoTrader.data.data_structures.candlesticks import Candlesticks
import numpy as np
import plotly.graph_objects as go
from AutoTrader.trading.indicators.inidicator import Indicator
from typing import List


class SuperTrend(Indicator):
    # columns = ['Time', 'TrueRange', 'ATR','BasicUpperBand','BasicLowerBand','FinalUpperBand','FinalLowerBand','Supertrend','IsUpper']

    true_range_counter = 0
    basic_band_counter = 0

    candlesticks: Candlesticks

    def __init__(self, candlesticks: Candlesticks, **kwargs):
        super().__init__(candlesticks)
        self.period = kwargs.get('period', 10)
        self.multiplier = kwargs.get('multiplier', 3)

    def process_new_candlestick(self) -> None:

        # Create new row
        self.list.append({'Time': self.candlesticks.get_last_time()})
        number_of_rows = self.candlesticks.get_number_of_rows()

        if number_of_rows >= 2:
            current_candlestick = self.candlesticks.get_last_candlestick()
            current_high = current_candlestick.High
            current_low = current_candlestick.Low
            current_close = current_candlestick.Close
            previous_close = self.candlesticks.get_last_candlesticks(n=2)[-2].Close
            self.list[-1]['TrueRange'] = max((current_high - current_low), abs(current_high - previous_close),
                                             abs(current_low - previous_close))
            self.true_range_counter += 1
            if self.true_range_counter >= self.period:
                self.list[-1]['ATR'] = np.mean([d['TrueRange'] for d in self.list[-self.period:]])
                self.list[-1]['BasicUpperBand'] = ((current_high + current_low) / 2) + self.multiplier * self.list[-1]['ATR']
                self.list[-1]['BasicLowerBand'] = ((current_high + current_low) / 2) - self.multiplier * self.list[-1]['ATR']
                self.basic_band_counter += 1
                if self.basic_band_counter == 1:
                    self.list[-1]['FinalUpperBand'] = 0
                    self.list[-1]['FinalLowerBand'] = 0
                elif self.basic_band_counter >= 2:
                    self.list[-1]['FinalUpperBand'] = self.list[-1]['BasicUpperBand'] if self.list[-1]['BasicUpperBand'] < self.list[-2]['FinalUpperBand'] or previous_close > self.list[-2][
                        'FinalUpperBand'] else self.list[-2]['FinalUpperBand']
                    self.list[-1]['FinalLowerBand'] = self.list[-1]['BasicLowerBand'] if self.list[-1]['BasicLowerBand'] > self.list[-2]['FinalLowerBand'] or previous_close < self.list[-2][
                        'FinalLowerBand'] else self.list[-2]['FinalLowerBand']

                    if 'Supertrend' not in self.list[-2]:
                        self.list[-2]['Supertrend'] = 0
                        self.list[-1]['IsUpper'] = False

                    previous_supertrend = self.list[-2]['Supertrend']

                    if previous_supertrend == self.list[-2]['FinalUpperBand'] and current_close < self.list[-1]['FinalUpperBand']:
                        self.list[-1]['Supertrend'] = self.list[-1]['FinalUpperBand']
                        self.list[-1]['IsUpper'] = True

                    elif previous_supertrend == self.list[-2]['FinalUpperBand'] and current_close > self.list[-1]['FinalUpperBand']:
                        self.list[-1]['Supertrend'] = self.list[-1]['FinalLowerBand']
                        self.list[-1]['IsUpper'] = False

                    elif previous_supertrend == self.list[-2]['FinalLowerBand'] and current_close > self.list[-1]['FinalLowerBand']:
                        self.list[-1]['Supertrend'] = self.list[-1]['FinalLowerBand']
                        self.list[-1]['IsUpper'] = False
                    elif previous_supertrend == self.list[-2]['FinalLowerBand'] and current_close < self.list[-1]['FinalUpperBand']:
                        self.list[-1]['Supertrend'] = self.list[-1]['FinalUpperBand']
                        self.list[-1]['IsUpper'] = True
                    else:
                        self.list[-1]['Supertrend'] = self.list[-1]['FinalUpperBand']
                        self.list[-1]['IsUpper'] = True

    # TODO: Add more weight to recent data

    def process_new_tick(self) -> None:
        pass

    def get_plot(self) -> List:
        return [go.Scatter(x=[d['Time'] for d in self.list[self.period + 1:]],
                           y=[d['Supertrend'] if 'Supertrend' in d else None for d in self.list[self.period + 1:]],
                           name="Supertrend")]

    def delete_data(self) -> None:
        self.list = []
        self.true_range_counter = 0
        self.basic_band_counter = 0
