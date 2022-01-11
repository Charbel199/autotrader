from AutoTrader.trading.indicators.adx_indicator import ADX
from AutoTrader.trading.indicators.rsi_indicator import RSI
from AutoTrader.ml.data_collector.features_generator.features_generator import FeaturesGenerator
from AutoTrader.data.data_structures.candlesticks import Candlesticks


class AutoFeaturesGenerator(FeaturesGenerator):
    def __init__(self, candlesticks: Candlesticks):
        super().__init__(candlesticks)
        self.ADX = ADX(candlesticks)
        self.RSI = RSI(candlesticks)

    def process_candlesticks(self, candlesticks: list) -> dict:
        if len(candlesticks) != 0:
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
            closes = [d.Close for d in self.candlesticks.get_last_candlesticks(self.candlesticks.get_number_of_rows())]
            print(max(closes))
            # Empty data
            self.candlesticks.delete_data()
            self.ADX.delete_data()
            self.RSI.delete_data()
            return data
        else:
            return {}

    @staticmethod
    def condition(name: str) -> bool:
        return name == 'auto'
