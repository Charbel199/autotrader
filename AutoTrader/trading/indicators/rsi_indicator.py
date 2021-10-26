from AutoTrader.data.data_structures.structure import TickStructure
import numpy as np
import plotly.graph_objects as go
from AutoTrader.trading.indicators.inidicator import Indicator


class RSI(Indicator):
    # columns = ['Time', 'Gain', 'Loss', 'AverageGain', 'AverageLoss', 'RS', 'RSI']
    period = 14
    data_structure: TickStructure

    def __init__(self, data_structure: TickStructure):
        super().__init__(data_structure)
        self.gain_counter = 0

    def process_new_candlestick(self) -> None:
        # Create new row
        self.list.append({'Time': self.data_structure.get_last_time()})

        # Compute gain and loss
        if self.data_structure.get_number_of_rows() >= 2:
            change = self.data_structure.get_last_value('Close') - self.data_structure.get_before_last_value('Close')
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

    def process_new_tick(self):
        pass

    def get_plot(self):
        return go.Scatter(x=[d['Time'] for d in self.list], y=[d['RSI'] for d in self.list if 'RSI' in d], name="RSI")

    def delete_data(self) -> None:
        self.list = []
        self.gain_counter = 0
