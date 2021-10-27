from AutoTrader.data.data_structures.structure import TickStructure
import numpy as np
import plotly.graph_objects as go
from AutoTrader.trading.indicators.inidicator import Indicator


class ChaikinMoneyFlow(Indicator):
    # columns = ['Time', 'ChaikinMultiplier', 'MoneyFlowVolume', 'ChaikinMoneyFlow']
    period = 21
    data_structure: TickStructure

    def __init__(self, data_structure: TickStructure):
        super().__init__(data_structure)
        self.money_flow_volume_counter = 0

    def process_new_candlestick(self) -> None:

        # Create new row
        self.list.append({'Time': self.data_structure.get_last_time()})

        if self.data_structure.get_number_of_rows() >= 1:
            if (self.data_structure.get_last_value('High') - self.data_structure.get_last_value('Low')) != 0:
                self.list[-1]['ChaikinMultiplier'] = ((self.data_structure.get_last_value('Close') - self.data_structure.get_last_value('Low')) - (
                        self.data_structure.get_last_value('High') - self.data_structure.get_last_value('Close'))) / (
                                                             self.data_structure.get_last_value('High') - self.data_structure.get_last_value('Low'))
            else:
                self.list[-1]['ChaikinMultiplier'] = 0
            self.list[-1]['MoneyFlowVolume'] = self.list[-1]['ChaikinMultiplier'] * self.data_structure.get_last_value('Volume')
            self.money_flow_volume_counter += 1
        if self.money_flow_volume_counter >= self.period:
            volume_average = np.mean(self.data_structure.get_last_rows(self.period, 'Volume'))
            money_flow_average = np.mean([d['MoneyFlowVolume'] for d in self.list[-self.period:]])
            self.list[-1]['ChaikinMoneyFlow'] = money_flow_average / volume_average

    def process_new_tick(self):
        pass

    def get_plot(self):
        return go.Scatter(x=[d['Time'] for d in self.list], y=[d['ChaikinMoneyFlow'] if 'ChaikinMoneyFlow' in d else None for d in self.list], name="ChaikinMoneyFlow")

    def delete_data(self) -> None:
        self.list = []
        self.money_flow_volume_counter = 0
