from app.AutoTrader.trading.indicators.adx_indicator import ADX
from app.AutoTrader.trading.indicators.rsi_indicator import RSI
from app.AutoTrader.ml.data_collector.features_generator.features_generator import FeaturesGenerator
from app.AutoTrader.data.data_structures.candlesticks import Candlesticks


class SimpleFeaturesGenerator(FeaturesGenerator):
    def __init__(self, candlesticks: Candlesticks):
        super().__init__(candlesticks)
        self.ADX = ADX(candlesticks)
        self.RSI = RSI(candlesticks)

    def process_candlesticks(self, candlesticks: list) -> dict:
        for candlestick in candlesticks:
            if self.candlesticks:
                self.candlesticks.add_row(candlestick)
                self.ADX.process_new_candlestick()
                self.RSI.process_new_candlestick()
                self.candlesticks.set_tick(candlestick)
        data = {
            'Ticks': self.candlesticks.get_data(),
            'ADX': self.ADX.get_all_values(),
            'RSI': self.RSI.get_all_values()
        }

        # Empty data
        self.candlesticks.delete_data()
        self.ADX.delete_data()
        self.RSI.delete_data()
        return data

    @staticmethod
    def condition(name: str) -> bool:
        return name == 'simple'
