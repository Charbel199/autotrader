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
