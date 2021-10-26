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
# import pandas as pd
# from data.data_structures.structure import TickStructure
# import numpy as np
# import plotly.graph_objects as go
# from helper import data_structure_helper
#
#
# class RSI(object):
#     columns = ['Time', 'Gain', 'Loss', 'AverageGain', 'AverageLoss', 'RS', 'RSI']
#     period = 14
#
#     data_structure: TickStructure
#
#     def __init__(self, data_structure):
#         self.df = pd.DataFrame(columns=self.columns)
#         self.data_structure = data_structure
#
#     def process_new_candlestick(self):
#         self.df = data_structure_helper.reduce_df(self.df)
#         # Create temporary data structures
#         temp_df = data_structure_helper.get_temp_df(self.df, self.period)
#
#         # Create new row
#         temp_df.loc[len(self.df.index)] = {'Time': self.data_structure.get_last_time()}
#
#         # Compute gain and loss
#         if self.data_structure.get_number_of_rows() >= 2:
#             change = self.data_structure.get_last_value('Close') - self.data_structure.get_before_last_value('Close')
#             if change > 0:
#                 temp_df['Gain'].iloc[-1] = change
#                 temp_df['Loss'].iloc[-1] = 0
#             else:
#                 temp_df['Loss'].iloc[-1] = -change
#                 temp_df['Gain'].iloc[-1] = 0
#
#         # Compute RSI
#         if temp_df['Gain'].count() >= self.period:
#             temp_df['AverageGain'].iloc[-1] = np.mean(temp_df['Gain'].tail(self.period).tolist())
#             temp_df['AverageLoss'].iloc[-1] = np.mean(temp_df['Loss'].tail(self.period).tolist())
#             if temp_df['AverageLoss'].iloc[-1] != 0:
#                 temp_df['RS'].iloc[-1] = temp_df['AverageGain'].iloc[-1] / temp_df['AverageLoss'].iloc[-1]
#                 temp_df['RSI'].iloc[-1] = 100 - (100 / (1 + temp_df['RS'].iloc[-1]))
#             else:
#                 temp_df['RS'].iloc[-1] = 100
#                 temp_df['RSI'].iloc[-1] = 100
#
#         # Update RSI dataframe
#         self.df = self.df.append(temp_df.tail(1))
#
#     def get_last_rsi_values(self, n=1):
#         # Gets last ADX by default
#         return self.df[['Time', 'RSI']].tail(n)
#
#     def get_all_rsi_values(self):
#         return self.df[['Time', 'RSI']]
#
#     def delete_data(self):
#         self.df = pd.DataFrame(columns=self.columns)
#
#     def get_plot(self):
#         return go.Scatter(x=self.df['Time'].tolist(), y=self.df['RSI'].tolist(), name="RSI")
