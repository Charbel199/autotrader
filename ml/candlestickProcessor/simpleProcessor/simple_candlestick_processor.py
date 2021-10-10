from trading.indicators.adx_indicator.adx_indicator_processor import ADX
from trading.indicators.rsi_indicator.rsi_indicator_processor import RSI
from ml.candlestickProcessor.candlestick_processor import CandlestickProcessor


class SimpleCandlestickProcessor(CandlestickProcessor):
    def __init__(self, data_structure):
        super().__init__(data_structure)
        self.ADX = ADX(data_structure)
        self.RSI = RSI(data_structure)

    def process_candlesticks(self, candlesticks):
        for candlestick in candlesticks:
            if self.data_structure:
                self.data_structure.add_row(candlestick)
                self.ADX.process_new_candlestick()
                self.RSI.process_new_candlestick()
                self.data_structure.set_tick(candlestick)
        data = {
            'Ticks': self.data_structure.get_data(),
            'ADX': self.ADX.df,
            'RSI': self.RSI.df
        }

        # Empty data
        self.data_structure.delete_data()
        self.ADX.delete_data()
        self.RSI.delete_data()
        return data

    @staticmethod
    def condition(name):
        return name == 'simple'