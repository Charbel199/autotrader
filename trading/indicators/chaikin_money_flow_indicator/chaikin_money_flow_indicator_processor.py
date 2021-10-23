from data.data_structures.structure import TickStructure
import numpy as np
import plotly.graph_objects as go
from trading.indicators.inidicator import Indicator


class ChaikinMoneyFlow(Indicator):
    # columns = ['Time', 'ChaikinMultiplier', 'MoneyFlowVolume', 'ChaikinMoneyFlow']
    period = 21
    data_structure: TickStructure

    def __init__(self, data_structure):
        super().__init__(data_structure)
        self.money_flow_volume_counter = 0

    def process_new_candlestick(self):

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
        return go.Scatter(x=[d['Time'] for d in self.list], y=[d['ChaikinMoneyFlow'] for d in self.list if 'ChaikinMoneyFlow' in d], name="ChaikinMoneyFlow")

# import pandas as pd
# from data.data_structures.structure import TickStructure
# import numpy as np
# import plotly.graph_objects as go
# from helper import data_structure_helper
#
#
# class ChaikinMoneyFlow(object):
#     columns = ['Time', 'ChaikinMultiplier', 'MoneyFlowVolume', 'ChaikinMoneyFlow']
#     period = 21
#     number_of_ticks_needed = 21
#     data_structure: TickStructure
#     temp_data_structure: TickStructure
#
#     def __init__(self, data_structure):
#         self.df = pd.DataFrame(columns=self.columns)
#         self.data_structure = data_structure
#
#     def process_new_candlestick(self):
#         self.df = data_structure_helper.reduce_df(self.df)
#         # Create temporary data structures
#         temp_df = data_structure_helper.get_temp_df(self.df, self.period)
#         self.temp_data_structure = data_structure_helper.get_temp_tick_data_structure(self.data_structure, self.number_of_ticks_needed)
#
#         # Create new row
#         temp_df.loc[len(self.df.index)] = {'Time': self.temp_data_structure.get_last_time()}
#         if self.temp_data_structure.get_number_of_rows() >= 1:
#             temp_df['ChaikinMultiplier'].iloc[-1] = ((self.temp_data_structure.get_last_value('Close') - self.temp_data_structure.get_last_value('Low')) - (
#                     self.temp_data_structure.get_last_value('High') - self.temp_data_structure.get_last_value('Close'))) / (
#                                                             self.temp_data_structure.get_last_value('High') - self.temp_data_structure.get_last_value('Low'))
#             temp_df['MoneyFlowVolume'].iloc[-1] = temp_df['ChaikinMultiplier'].iloc[-1] * self.temp_data_structure.get_last_value('Volume')
#         if temp_df['MoneyFlowVolume'].count() >= self.period:
#             volume_average = np.mean(self.temp_data_structure.get_last_rows(self.period,'Volume'))
#             money_flow_average = np.mean(temp_df['MoneyFlowVolume'].tail(self.period).tolist())
#             temp_df['ChaikinMoneyFlow'].iloc[-1] = money_flow_average / volume_average
#
#         # Update CMF dataframe
#         self.df = self.df.append(temp_df.tail(1))
#
#     def get_last_cmf_values(self, n=1):
#         # Gets last BollingerBands by default
#         return self.df[['Time', 'ChaikinMoneyFlow']].tail(n)
#
#     def get_all_cmf_values(self):
#         return self.df[['Time', 'ChaikinMoneyFlow']]
#
#     def delete_data(self):
#         self.df = pd.DataFrame(columns=self.columns)
#
#     def get_plot(self):
#         return go.Scatter(x=self.df['Time'].tolist(), y=self.df['ChaikinMoneyFlow'].tolist(), name="ChaikinMoneyFlow")
