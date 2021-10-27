from AutoTrader.data.data_structures.structure import TickStructure
import plotly.graph_objects as go
from AutoTrader.trading.indicators.inidicator import Indicator


class VWAP(Indicator):
    # columns = ['Time', 'VolumeClose', 'VWAP']
    period = 13
    data_structure: TickStructure

    def __init__(self, data_structure: TickStructure):
        super().__init__(data_structure)

    def process_new_candlestick(self) -> None:
        # Create new row
        self.list.append({'Time': self.data_structure.get_last_time()})

        self.list[-1]['VolumeClose'] = self.data_structure.get_last_value('Close') * self.data_structure.get_last_value('Volume')
        if self.data_structure.get_number_of_rows() >= self.period:
            self.list[-1]['VWAP'] = sum([d['VolumeClose'] for d in self.list[-self.period:]]) / sum(self.data_structure.get_last_rows(self.period, 'Volume'))

    def process_new_tick(self):
        pass

    def get_plot(self):
        return go.Scatter(x=[d['Time'] for d in self.list], y=[d['VWAP'] if 'VWAP' in d else None for d in self.list], name="VWAP")

    def delete_data(self) -> None:
        self.list = []
