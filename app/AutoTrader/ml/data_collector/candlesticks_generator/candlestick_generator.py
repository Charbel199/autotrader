from app.AutoTrader.data.previous_data.data_fetcher import DataFetcher
from app.AutoTrader.data.data_structures.candlesticks import Candlesticks
from app.AutoTrader.ml.data_collector.features_generator.features_generator import FeaturesGenerator
from abc import abstractmethod
from app.AutoTrader.exceptions import CandlestickGeneratorException


class CandlestickGenerator(object):
    data_fetcher: DataFetcher
    candlesticks: Candlesticks
    features_generator: FeaturesGenerator

    def __init__(self,
                 features_generator: FeaturesGenerator,
                 data_fetcher: DataFetcher,
                 candlesticks: Candlesticks,
                 symbols: list,
                 timeframe: str):
        self.symbols = symbols
        self.data_fetcher = data_fetcher
        self.candlesticks = candlesticks
        self.features_generator = features_generator
        self.timeframe = timeframe

    def fetch_new_candlesticks(self, start_timestamp: int, duration: int) -> None:
        pass

    def get_new_candlesticks(self) -> dict:
        pass

    @staticmethod
    @abstractmethod
    def condition(name: str) -> bool:
        pass


# Get candlestick generator
def get_candlestick_generator(name: str,
                              features_generator: FeaturesGenerator,
                              data_fetcher: DataFetcher,
                              candlesticks: Candlesticks,
                              symbols: list,
                              timeframe: str) -> CandlestickGenerator:
    for candlestick_generator in CandlestickGenerator.__subclasses__():
        if candlestick_generator.condition(name):
            return candlestick_generator(features_generator, data_fetcher,
                                         candlesticks,
                                         symbols,
                                         timeframe)
    raise CandlestickGeneratorException(f"Candlestick generator: {name} not found")
