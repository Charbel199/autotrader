from app.AutoTrader.data.data_structures.candlesticks import Candlesticks
import plotly.graph_objects as go
from app.AutoTrader.trading.indicators.inidicator import Indicator
from typing import List


class VWAP(Indicator):
    # columns = ['Time', 'VolumeClose', 'VWAP']
    period = 288
    candlesticks: Candlesticks

    def __init__(self, candlesticks: Candlesticks):
        super().__init__(candlesticks)

    def process_new_candlestick(self) -> None:
        # Create new row
        self.list.append({'Time': self.candlesticks.get_last_time()})

        self.list[-1]['VolumeClose'] = self.candlesticks.get_last_candlestick().Close * self.candlesticks.get_last_candlestick().Volume
        if self.candlesticks.get_number_of_rows() >= self.period:
            volume_sum = sum([c.Volume for c in self.candlesticks.get_last_candlesticks(self.period)])
            if volume_sum > 0:
                self.list[-1]['VWAP'] = sum([d['VolumeClose'] for d in self.list[-self.period:]]) / volume_sum

    def process_new_tick(self) -> None:
        pass

    def get_plot(self) -> List:
        return [go.Scatter(x=[d['Time'] for d in self.list], y=[d['VWAP'] if 'VWAP' in d else None for d in self.list], name="VWAP")]

    def delete_data(self) -> None:
        self.list = []
