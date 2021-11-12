from AutoTrader.data.data_structures.structure import TickStructure
import plotly.graph_objects as go
from AutoTrader.trading.indicators.inidicator import Indicator


class VWAP(Indicator):
    # columns = ['Time', 'VolumeClose', 'VWAP']
    period = 288
    data_structure: TickStructure

    def __init__(self, data_structure: TickStructure):
        super().__init__(data_structure)

    def process_new_candlestick(self) -> None:
        # Create new row
        self.list.append({'Time': self.data_structure.get_last_time()})

        self.list[-1]['VolumeClose'] = self.data_structure.get_last_candlestick().Close * self.data_structure.get_last_candlestick().Volume
        if self.data_structure.get_number_of_rows() >= self.period:
            volume_sum = sum([c.Volume for c in self.data_structure.get_last_candlesticks(self.period)])
            if volume_sum > 0:
                self.list[-1]['VWAP'] = sum([d['VolumeClose'] for d in self.list[-self.period:]]) / volume_sum

    def process_new_tick(self):
        pass

    def get_plot(self):
        return go.Scatter(x=[d['Time'] for d in self.list], y=[d['VWAP'] if 'VWAP' in d else None for d in self.list], name="VWAP")

    def delete_data(self) -> None:
        self.list = []
