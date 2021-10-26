from AutoTrader.data.data_structures.structure import TickStructure
from AutoTrader.trading.indicators.inidicator import Indicator


class CandlestickType(Indicator):
    # columns = ['Time', 'Type']
    data_structure: TickStructure

    def __init__(self, data_structure: TickStructure):
        super().__init__(data_structure)
        self.list = []
        self.data_structure = data_structure

    def process_new_candlestick(self) -> None:

        # Create new row
        self.list.append({'Time': self.data_structure.get_last_time()})
        candlestick_type = ''

        last_close = self.data_structure.get_last_value('Close')
        last_open = self.data_structure.get_last_value('Open')
        last_high = self.data_structure.get_last_value('High')
        last_low = self.data_structure.get_last_value('Low')
        # Get candlestick info
        real_body = abs(last_close - last_open)
        candle_range = last_high - last_low

        # Get type
        if self.data_structure.get_number_of_rows() >= 2:

            before_last_high = self.data_structure.get_before_last_value('High')
            before_last_low = self.data_structure.get_before_last_value('Low')

            # Bullish pinbar
            if real_body <= candle_range / 3 and \
                    min(last_close, last_open) > (
                    last_high + last_low) / 2 and \
                    last_low < before_last_low:
                candlestick_type = 'BullishPinbar'

            # Bearish pinbar
            if real_body <= candle_range / 3 and \
                    max(last_close, last_open) < (
                    last_high + last_low) / 2 and \
                    last_high > before_last_high:
                candlestick_type = 'BearishPinbar'

            # Inside bar
            if last_high < before_last_high and \
                    last_low > before_last_low:
                candlestick_type = 'InsideBar'

            # Outside bar
            if last_high > before_last_high and \
                    last_low < before_last_low:
                candlestick_type = 'OutsideBar'

            # Bullish engulfing
            if last_high > before_last_high and \
                    last_low < before_last_low and \
                    real_body >= 0.8 * candle_range and \
                    last_close > last_open:
                candlestick_type = 'BullishEngulfing'

            # Bearish engulfing
            if last_high > before_last_high and \
                    last_low < before_last_low and \
                    real_body >= 0.8 * candle_range and \
                    last_close < last_open:
                candlestick_type = 'BearishEngulfing'

        if self.data_structure.get_number_of_rows() >= 3:
            # Bullish swing
            if last_low > before_last_low and \
                    before_last_low < self.data_structure.get_specific_value('Low', -3):
                candlestick_type = 'BullishSwing'
            # Bearish swing
            if last_high < before_last_high and \
                    before_last_high > self.data_structure.get_specific_value('High', -3):
                candlestick_type = 'BearishSwing'

        self.list[-1]['Type'] = candlestick_type

    def process_new_tick(self):
        pass

    def get_plot(self):
        pass

    def delete_data(self) -> None:
        self.list = []
# from data.data_structures.structure import TickStructure
# import pandas as pd
# from helper import data_structure_helper
#
#
# class CandlestickType(object):
#     columns = ['Time', 'Type']
#     number_of_ticks_needed = 3
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
#         self.temp_data_structure = data_structure_helper.get_temp_tick_data_structure(self.data_structure, self.number_of_ticks_needed)
#
#         # Create new row
#         self.df.loc[len(self.df.index)] = {'Time': self.temp_data_structure.get_last_time()}
#         candlestick_type = ''
#
#         # Get candlestick info
#         real_body = abs(self.temp_data_structure.get_last_value('Close') - self.temp_data_structure.get_last_value('Open'))
#         candle_range = self.temp_data_structure.get_last_value('High') - self.temp_data_structure.get_last_value('Low')
#
#         # Get type
#         if self.temp_data_structure.get_number_of_rows() >= 2:
#             # Bullish pinbar
#             if real_body <= candle_range / 3 and \
#                     min(self.temp_data_structure.get_last_value('Close'), self.temp_data_structure.get_last_value('Open')) > (
#                     self.temp_data_structure.get_last_value('High') + self.temp_data_structure.get_last_value('Low')) / 2 and \
#                     self.temp_data_structure.get_last_value('Low') < self.temp_data_structure.get_before_last_value('Low'):
#                 candlestick_type = 'BullishPinbar'
#
#             # Bearish pinbar
#             if real_body <= candle_range / 3 and \
#                     max(self.temp_data_structure.get_last_value('Close'), self.temp_data_structure.get_last_value('Open')) < (
#                     self.temp_data_structure.get_last_value('High') + self.temp_data_structure.get_last_value('Low')) / 2 and \
#                     self.temp_data_structure.get_last_value('High') > self.temp_data_structure.get_before_last_value('High'):
#                 candlestick_type = 'BearishPinbar'
#
#             # Inside bar
#             if self.temp_data_structure.get_last_value('High') < self.temp_data_structure.get_before_last_value('High') and \
#                     self.temp_data_structure.get_last_value('Low') > self.temp_data_structure.get_before_last_value('Low'):
#                 candlestick_type = 'InsideBar'
#
#             # Outside bar
#             if self.temp_data_structure.get_last_value('High') > self.temp_data_structure.get_before_last_value('High') and \
#                     self.temp_data_structure.get_last_value('Low') < self.temp_data_structure.get_before_last_value('Low'):
#                 candlestick_type = 'OutsideBar'
#
#             # Bullish engulfing
#             if self.temp_data_structure.get_last_value('High') > self.temp_data_structure.get_before_last_value('High') and \
#                     self.temp_data_structure.get_last_value('Low') < self.temp_data_structure.get_before_last_value('Low') and \
#                     real_body >= 0.8 * candle_range and \
#                     self.temp_data_structure.get_last_value('Close') > self.temp_data_structure.get_last_value('Open'):
#                 candlestick_type = 'BullishEngulfing'
#
#             # Bearish engulfing
#             if self.temp_data_structure.get_last_value('High') > self.temp_data_structure.get_before_last_value('High') and \
#                     self.temp_data_structure.get_last_value('Low') < self.temp_data_structure.get_before_last_value('Low') and \
#                     real_body >= 0.8 * candle_range and \
#                     self.temp_data_structure.get_last_value('Close') < self.temp_data_structure.get_last_value('Open'):
#                 candlestick_type = 'BearishEngulfing'
#
#         if self.temp_data_structure.get_number_of_rows() >= 3:
#             # Bullish swing
#             if self.temp_data_structure.get_last_value('Low') > self.temp_data_structure.get_before_last_value('Low') and \
#                     self.temp_data_structure.get_before_last_value('Low') < self.temp_data_structure.get_specific_value('Low', -3):
#                 candlestick_type = 'BullishSwing'
#             # Bearish swing
#             if self.temp_data_structure.get_last_value('High') < self.temp_data_structure.get_before_last_value('High') and \
#                     self.temp_data_structure.get_before_last_value('High') > self.temp_data_structure.get_specific_value('High', -3):
#                 candlestick_type = 'BearishSwing'
#
#         self.df.loc[self.df.index[-1], 'Type'] = candlestick_type
#
#     def get_last_candlestick_type_values(self, n=1):
#         # Gets last ADX by default
#         return self.df[['Time', 'Type']].tail(n)
#
#     def get_all_candlestick_type_values(self):
#         return self.df[['Time', 'Type']]
#
#     def delete_data(self):
#         self.df = pd.DataFrame(columns=self.columns)
