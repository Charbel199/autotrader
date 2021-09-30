import pandas as pd
from data_structures.structure import TickStructure
import pandas as pd


class CandlestickType(object):
    columns = ['Time', 'Type']
    maxNumberOfPreviousCandlesticks = 4
    data_structure: TickStructure
    temp_data_structure: TickStructure

    def __init__(self, data_structure):
        self.df = pd.DataFrame(columns=self.columns)
        self.data_structure = data_structure

    def process_new_candlestick(self):
        # Create temporary dataframe (We only need a couple of the last data points)
        if self.data_structure.get_number_of_rows() > self.maxNumberOfPreviousCandlesticks:
            self.temp_data_structure = self.data_structure.get_last_rows_copy(self.maxNumberOfPreviousCandlesticks)
        else:
            self.temp_data_structure = self.data_structure.get_copy()

        # Create new row
        self.df.loc[len(self.df.index)] = {'Time': self.data_structure.get_last_value('Time')}
        candlestick_type = ''

        # Get candlestick info
        real_body = abs(self.data_structure.get_last_value('Close') - self.data_structure.get_last_value('Open'))
        candle_range = self.data_structure.get_last_value('High') - self.data_structure.get_last_value('Low')

        # Get type
        if self.data_structure.get_number_of_rows() >= 2:
            # Bullish pinbar
            if real_body <= candle_range / 3 and \
                    min(self.data_structure.get_last_value('Close'), self.data_structure.get_last_value('Open')) > (
                    self.data_structure.get_last_value('High') + self.data_structure.get_last_value('Low')) / 2 and \
                    self.data_structure.get_last_value('Low') < self.data_structure.get_before_last_value('Low'):
                candlestick_type = 'BullishPinbar'

            # Bearish pinbar
            if real_body <= candle_range / 3 and \
                    max(self.data_structure.get_last_value('Close'), self.data_structure.get_last_value('Open')) < (
                    self.data_structure.get_last_value('High') + self.data_structure.get_last_value('Low')) / 2 and \
                    self.data_structure.get_last_value('High') > self.data_structure.get_before_last_value('High'):
                candlestick_type = 'BearishPinbar'

            # Inside bar
            if self.data_structure.get_last_value('High') < self.data_structure.get_before_last_value('High') and \
                    self.data_structure.get_last_value('Low') > self.data_structure.get_before_last_value('Low'):
                candlestick_type = 'InsideBar'

            # Outside bar
            if self.data_structure.get_last_value('High') > self.data_structure.get_before_last_value('High') and \
                    self.data_structure.get_last_value('Low') < self.data_structure.get_before_last_value('Low'):
                candlestick_type = 'OutsideBar'

            # Bullish engulfing
            if self.data_structure.get_last_value('High') > self.data_structure.get_before_last_value('High') and \
                    self.data_structure.get_last_value('Low') < self.data_structure.get_before_last_value('Low') and \
                    real_body >= 0.8 * candle_range and \
                    self.data_structure.get_last_value('Close') > self.data_structure.get_last_value('Open'):
                candlestick_type = 'BullishEngulfing'

            # Bearish engulfing
            if self.data_structure.get_last_value('High') > self.data_structure.get_before_last_value('High') and \
                    self.data_structure.get_last_value('Low') < self.data_structure.get_before_last_value('Low') and \
                    real_body >= 0.8 * candle_range and \
                    self.data_structure.get_last_value('Close') < self.data_structure.get_last_value('Open'):
                candlestick_type = 'BearishEngulfing'

        if self.data_structure.get_number_of_rows() >= 3:
            # Bullish swing
            if self.data_structure.get_last_value('Low') > self.data_structure.get_before_last_value('Low') and \
                    self.data_structure.get_before_last_value('Low') < self.data_structure.get_specific_value('Low', -3):
                candlestick_type = 'BullishSwing'
            # Bearish swing
            if self.data_structure.get_last_value('High') < self.data_structure.get_before_last_value('High') and \
                    self.data_structure.get_before_last_value('High') > self.data_structure.get_specific_value('High', -3):
                candlestick_type = 'BearishSwing'

        self.df.loc[self.df.index[-1], 'Type'] = candlestick_type

    def get_last_candlestick_type_values(self, n=1):
        # Gets last ADX by default
        return self.df[['Time', 'Type']].tail(n)
