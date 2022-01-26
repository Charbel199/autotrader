from AutoTrader.data.data_structures.candlesticks import Candlesticks
import numpy as np
import plotly.graph_objects as go
from AutoTrader.trading.indicators.inidicator import Indicator
from typing import List


class ChaikinMoneyFlow(Indicator):
    # columns = ['Time', 'ChaikinMultiplier', 'MoneyFlowVolume', 'ChaikinMoneyFlow']
    period = 21
    candlesticks: Candlesticks

    def __init__(self, candlesticks: Candlesticks):
        super().__init__(candlesticks)
        self.money_flow_volume_counter = 0

    def process_new_candlestick(self) -> None:

        # Create new row
        self.list.append({'Time': self.candlesticks.get_last_time()})
        last_candlestick = self.candlesticks.get_last_candlestick()
        if self.candlesticks.get_number_of_rows() >= 1:
            if (last_candlestick.High - last_candlestick.Low) != 0:
                self.list[-1]['ChaikinMultiplier'] = ((last_candlestick.Close - last_candlestick.Low) - (
                        last_candlestick.High - last_candlestick.Close)) / (last_candlestick.High - last_candlestick.Low)
            else:
                self.list[-1]['ChaikinMultiplier'] = 0
            self.list[-1]['MoneyFlowVolume'] = self.list[-1]['ChaikinMultiplier'] * last_candlestick.Volume
            self.money_flow_volume_counter += 1
        if self.money_flow_volume_counter >= self.period:
            volume_average = np.mean([c.Volume for c in self.candlesticks.get_last_candlesticks(self.period)])
            money_flow_average = np.mean([d['MoneyFlowVolume'] for d in self.list[-self.period:]])
            self.list[-1]['ChaikinMoneyFlow'] = money_flow_average / volume_average

    def process_new_tick(self) -> None:
        pass

    def get_plot(self) -> List:
        return [go.Scatter(x=[d['Time'] for d in self.list], y=[d['ChaikinMoneyFlow'] if 'ChaikinMoneyFlow' in d else None for d in self.list], name="ChaikinMoneyFlow")]

    def delete_data(self) -> None:
        self.list = []
        self.money_flow_volume_counter = 0
