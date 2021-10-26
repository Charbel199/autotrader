from AutoTrader.trading.indicators.adx_indicator_processor import ADX
from AutoTrader.trading.indicators.rsi_indicator_processor import RSI
from AutoTrader.ml.candlestick_processor.candlestick_processor import CandlestickProcessor
from AutoTrader.data.data_structures.structure import TickStructure


class SimpleCandlestickProcessor(CandlestickProcessor):
    def __init__(self, data_structure: TickStructure):
        super().__init__(data_structure)
        self.ADX = ADX(data_structure)
        self.RSI = RSI(data_structure)

    def process_candlesticks(self, candlesticks: list) -> dict:
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

        # Empty data
        self.data_structure.delete_data()
        self.ADX.delete_data()
        self.RSI.delete_data()
        return data

    @staticmethod
    def condition(name: str) -> bool:
        return name == 'simple'
