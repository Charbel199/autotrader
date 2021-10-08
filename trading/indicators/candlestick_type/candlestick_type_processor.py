from data.data_structures.structure import TickStructure
import pandas as pd


class CandlestickType(object):
    columns = ['Time', 'Type']
    number_of_ticks_needed = 3
    data_structure: TickStructure
    temp_data_structure: TickStructure

    def __init__(self, data_structure):
        self.df = pd.DataFrame(columns=self.columns)
        self.data_structure = data_structure

    def process_new_candlestick(self):
        # Create temporary data_structure
        if self.data_structure.get_number_of_rows() > self.number_of_ticks_needed:
            self.temp_data_structure = self.data_structure.get_tick_structure_copy(self.number_of_ticks_needed)
        else:
            self.temp_data_structure = self.data_structure.get_tick_structure_copy()

        # Create new row
        self.df.loc[len(self.df.index)] = {'Time': self.temp_data_structure.get_last_time()}
        candlestick_type = ''

        # Get candlestick info
        real_body = abs(self.temp_data_structure.get_last_value('Close') - self.temp_data_structure.get_last_value('Open'))
        candle_range = self.temp_data_structure.get_last_value('High') - self.temp_data_structure.get_last_value('Low')

        # Get type
        if self.temp_data_structure.get_number_of_rows() >= 2:
            # Bullish pinbar
            if real_body <= candle_range / 3 and \
                    min(self.temp_data_structure.get_last_value('Close'), self.temp_data_structure.get_last_value('Open')) > (
                    self.temp_data_structure.get_last_value('High') + self.temp_data_structure.get_last_value('Low')) / 2 and \
                    self.temp_data_structure.get_last_value('Low') < self.temp_data_structure.get_before_last_value('Low'):
                candlestick_type = 'BullishPinbar'

            # Bearish pinbar
            if real_body <= candle_range / 3 and \
                    max(self.temp_data_structure.get_last_value('Close'), self.temp_data_structure.get_last_value('Open')) < (
                    self.temp_data_structure.get_last_value('High') + self.temp_data_structure.get_last_value('Low')) / 2 and \
                    self.temp_data_structure.get_last_value('High') > self.temp_data_structure.get_before_last_value('High'):
                candlestick_type = 'BearishPinbar'

            # Inside bar
            if self.temp_data_structure.get_last_value('High') < self.temp_data_structure.get_before_last_value('High') and \
                    self.temp_data_structure.get_last_value('Low') > self.temp_data_structure.get_before_last_value('Low'):
                candlestick_type = 'InsideBar'

            # Outside bar
            if self.temp_data_structure.get_last_value('High') > self.temp_data_structure.get_before_last_value('High') and \
                    self.temp_data_structure.get_last_value('Low') < self.temp_data_structure.get_before_last_value('Low'):
                candlestick_type = 'OutsideBar'

            # Bullish engulfing
            if self.temp_data_structure.get_last_value('High') > self.temp_data_structure.get_before_last_value('High') and \
                    self.temp_data_structure.get_last_value('Low') < self.temp_data_structure.get_before_last_value('Low') and \
                    real_body >= 0.8 * candle_range and \
                    self.temp_data_structure.get_last_value('Close') > self.temp_data_structure.get_last_value('Open'):
                candlestick_type = 'BullishEngulfing'

            # Bearish engulfing
            if self.temp_data_structure.get_last_value('High') > self.temp_data_structure.get_before_last_value('High') and \
                    self.temp_data_structure.get_last_value('Low') < self.temp_data_structure.get_before_last_value('Low') and \
                    real_body >= 0.8 * candle_range and \
                    self.temp_data_structure.get_last_value('Close') < self.temp_data_structure.get_last_value('Open'):
                candlestick_type = 'BearishEngulfing'

        if self.temp_data_structure.get_number_of_rows() >= 3:
            # Bullish swing
            if self.temp_data_structure.get_last_value('Low') > self.temp_data_structure.get_before_last_value('Low') and \
                    self.temp_data_structure.get_before_last_value('Low') < self.temp_data_structure.get_specific_value('Low', -3):
                candlestick_type = 'BullishSwing'
            # Bearish swing
            if self.temp_data_structure.get_last_value('High') < self.temp_data_structure.get_before_last_value('High') and \
                    self.temp_data_structure.get_before_last_value('High') > self.temp_data_structure.get_specific_value('High', -3):
                candlestick_type = 'BearishSwing'

        self.df.loc[self.df.index[-1], 'Type'] = candlestick_type

    def get_last_candlestick_type_values(self, n=1):
        # Gets last ADX by default
        return self.df[['Time', 'Type']].tail(n)

    def get_all_candlestick_type_values(self):
        return self.df[['Time', 'Type']]