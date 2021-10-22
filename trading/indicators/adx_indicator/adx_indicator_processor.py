from data.data_structures.structure import TickStructure
import numpy as np
import plotly.graph_objects as go


class ADX(object):
    columns = ['Time', 'TrueRange', 'ATR', 'H-pH', 'pL-L', '+DX', '-DX', 'Smooth+DX', 'Smooth-DX', '+DMI', '-DMI', 'DX',
               'ADX']
    period = 14
    number_of_ticks_needed = 2
    data_structure: TickStructure

    def __init__(self, data_structure):
        self.list = []
        self.data_structure = data_structure
        self.true_range_counter = 0
        self.atr_counter = 0
        self.dx_counter = 0
        self.adx_counter = 0

    def process_new_candlestick(self):
        # Create new row
        self.list.append({'Time': self.data_structure.get_last_time()})

        if self.data_structure.get_number_of_rows() >= 2:
            # Calculate true range
            self.list[-1]['TrueRange'] = max(
                self.data_structure.get_last_value('High') - self.data_structure.get_last_value('Low'),
                self.data_structure.get_last_value('High') - self.data_structure.get_before_last_value('Close'),
                self.data_structure.get_before_last_value('Close') - self.data_structure.get_last_value('Low')
            )
            self.true_range_counter += 1

            # Calculate H-pH and pL-L
            self.list[-1]['H-pH'] = self.data_structure.get_last_value('High') - self.data_structure.get_before_last_value('High')
            self.list[-1]['pL-L'] = self.data_structure.get_before_last_value('Low') - self.data_structure.get_last_value('Low')

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

    def get_last_adx_values(self, n=1):
        # Gets last ADX by default
        return self.list[-n:]

    def get_all_adx_values(self):
        return self.list

    def delete_data(self):
        self.list = []

    def get_plot(self):
        return go.Scatter(x=[d['Time'] for d in self.list], y=[d['ADX'] for d in self.list], name="ADX")

# import pandas as pd
# from data.data_structures.structure import TickStructure
# import numpy as np
# import plotly.graph_objects as go
# from helper import data_structure_helper
#
#
# class ADX(object):
#     columns = ['Time', 'TrueRange', 'ATR', 'H-pH', 'pL-L', '+DX', '-DX', 'Smooth+DX', 'Smooth-DX', '+DMI', '-DMI', 'DX',
#                'ADX']
#     period = 14
#     number_of_ticks_needed = 2
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
#         if self.temp_data_structure.get_number_of_rows() >= 2:
#             # Calculate true range
#             temp_df['TrueRange'].iloc[-1] = max(
#                 self.temp_data_structure.get_last_value('High') - self.temp_data_structure.get_last_value('Low'),
#                 self.temp_data_structure.get_last_value('High') - self.temp_data_structure.get_before_last_value('Close'),
#                 self.temp_data_structure.get_before_last_value('Close') - self.temp_data_structure.get_last_value('Low')
#             )
#             # Calculate H-pH and pL-L
#             temp_df['H-pH'].iloc[-1] = self.temp_data_structure.get_last_value('High') - self.temp_data_structure.get_before_last_value('High')
#             temp_df['pL-L'].iloc[-1] = self.temp_data_structure.get_before_last_value('Low') - self.temp_data_structure.get_last_value('Low')
#
#             # Calculate +DX and -DX
#             temp_df['+DX'].iloc[-1] = temp_df['H-pH'].iloc[-1] if temp_df['H-pH'].iloc[-1] > temp_df['pL-L'].iloc[-1] and temp_df['H-pH'].iloc[-1] > 0 else 0
#             temp_df['-DX'].iloc[-1] = temp_df['pL-L'].iloc[-1] if temp_df['pL-L'].iloc[-1] > temp_df['H-pH'].iloc[-1] and temp_df['pL-L'].iloc[-1] > 0 else 0
#
#         # Calculate ATR and smooth +DX and -DX
#         if temp_df['TrueRange'].count() == self.period and temp_df['ATR'].count() == 0:
#             temp_df['ATR'].iloc[-1] = np.mean(temp_df['TrueRange'].tail(self.period).tolist())
#             temp_df['Smooth+DX'].iloc[-1] = np.mean(temp_df['+DX'].tail(self.period).tolist())
#             temp_df['Smooth-DX'].iloc[-1] = np.mean(temp_df['-DX'].tail(self.period).tolist())
#
#         elif temp_df['ATR'].count() > 0:
#             temp_df['ATR'].iloc[-1] = (temp_df['ATR'].iloc[-2] * (self.period - 1) + temp_df['TrueRange'].iloc[-1]) / self.period
#             temp_df['Smooth+DX'].iloc[-1] = (temp_df['Smooth+DX'].iloc[-2] * (self.period - 1) + temp_df['+DX'].iloc[-1]) / self.period
#             temp_df['Smooth-DX'].iloc[-1] = (temp_df['Smooth-DX'].iloc[-2] * (self.period - 1) + temp_df['-DX'].iloc[-1]) / self.period
#
#         # Calculate +DMI and -DMI and DX a
#         if temp_df['ATR'].count() > 0:
#             temp_df['+DMI'].iloc[-1] = (temp_df['Smooth+DX'].iloc[-1] / temp_df['ATR'].iloc[-1]) * 100
#             temp_df['-DMI'].iloc[-1] = (temp_df['Smooth-DX'].iloc[-1] / temp_df['ATR'].iloc[-1]) * 100
#             temp_df['DX'].iloc[-1] = (abs(temp_df['+DMI'].iloc[-1] - temp_df['-DMI'].iloc[-1]) / (temp_df['+DMI'].iloc[-1] + temp_df['-DMI'].iloc[-1])) * 100
#
#         # Calculate ADX
#         if temp_df['DX'].count() == self.period and temp_df['ADX'].count() == 0:
#             temp_df['ADX'].iloc[-1] = np.mean(temp_df['DX'].tail(self.period).tolist())
#         elif temp_df['DX'].count() > 0:
#             temp_df['ADX'].iloc[-1] = (temp_df['ADX'].iloc[-2] * (self.period - 1) + temp_df['DX'].iloc[-1]) / self.period
#
#         # Update ADX dataframe
#         self.df = self.df.append(temp_df.tail(1))
#
#     def get_last_adx_values(self, n=1):
#         # Gets last ADX by default
#         return self.df[['Time', 'ADX']].tail(n)
#
#     def get_all_adx_values(self):
#         return self.df[['Time', 'ADX']]
#
#     def delete_data(self):
#         self.df = pd.DataFrame(columns=self.columns)
#
#     def get_plot(self):
#         return go.Scatter(x=self.df['Time'].tolist(), y=self.df['ADX'].tolist(), name="ADX")
