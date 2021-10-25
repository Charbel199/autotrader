from trading.indicators.adx_indicator.adx_indicator_processor import ADX
from trading.indicators.rsi_indicator.rsi_indicator_processor import RSI
from ml.candlestick_processor.candlestick_processor import CandlestickProcessor


class AutoCandlestickProcessor(CandlestickProcessor):
    def __init__(self, data_structure):
        super().__init__(data_structure)
        self.ADX = ADX(data_structure)
        self.RSI = RSI(data_structure)

    def process_candlesticks(self, candlesticks):
        if len(candlesticks) !=0:
            for candlestick in candlesticks:
                if self.data_structure:
                    self.data_structure.add_row(candlestick)
                    self.ADX.process_new_candlestick()
                    self.RSI.process_new_candlestick()
                    self.data_structure.set_tick(candlestick)
            data = {
                'Ticks': self.data_structure.get_data(),
                'ADX': self.ADX.get_all_values(),
                'RSI': self.RSI.get_all_values()
            }
            closes = self.data_structure.get_last_rows(self.data_structure.get_number_of_rows(),'Close')
            print(max(closes))
            # Empty data
            self.data_structure.delete_data()
            self.ADX.delete_data()
            self.RSI.delete_data()
            return data
        else:
            return {}

    @staticmethod
    def condition(name):
        return name == 'auto'
