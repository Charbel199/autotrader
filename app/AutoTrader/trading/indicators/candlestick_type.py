from app.AutoTrader.data.data_structures.candlesticks import Candlesticks
from app.AutoTrader.trading.indicators.inidicator import Indicator
from typing import List


class CandlestickType(Indicator):
    # columns = ['Time', 'Type']
    candlesticks: Candlesticks

    def __init__(self, candlesticks: Candlesticks):
        super().__init__(candlesticks)

    def process_new_candlestick(self) -> None:

        # Create new row
        self.list.append({'Time': self.candlesticks.get_last_time()})
        candlestick_type = ''
        last_candlestick = self.candlesticks.get_last_candlestick()
        last_close = last_candlestick.Close
        last_open = last_candlestick.Open
        last_high = last_candlestick.High
        last_low = last_candlestick.Low

        # Get candlestick info
        real_body = abs(last_close - last_open)
        candle_range = last_high - last_low

        # Get type
        if self.candlesticks.get_number_of_rows() >= 2:
            before_last_candlestick = self.candlesticks.get_last_candlestick()
            before_last_high = before_last_candlestick.High
            before_last_low = before_last_candlestick.Low

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

        if self.candlesticks.get_number_of_rows() >= 3:
            # Bullish swing
            if last_low > before_last_low and \
                    before_last_low < self.candlesticks.get_specific_value('Low', -3):
                candlestick_type = 'BullishSwing'
            # Bearish swing
            if last_high < before_last_high and \
                    before_last_high > self.candlesticks.get_specific_value('High', -3):
                candlestick_type = 'BearishSwing'

        self.list[-1]['Type'] = candlestick_type

    def process_new_tick(self) -> None:
        pass

    def get_plot(self) -> List:
        pass

    def delete_data(self) -> None:
        self.list = []
