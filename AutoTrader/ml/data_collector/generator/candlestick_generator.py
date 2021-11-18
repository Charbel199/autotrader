from AutoTrader.data.previous_data.data_fetcher import DataFetcher
from AutoTrader.data.data_structures.structure import TickStructure
from AutoTrader.ml.data_collector.features_generator.features_generator import FeaturesGenerator
from abc import abstractmethod
from AutoTrader.exceptions import CandlestickGeneratorException


class CandlestickGenerator(object):
    data_fetcher: DataFetcher
    data_structure: TickStructure
    features_generator: FeaturesGenerator

    def __init__(self,
                 features_generator: FeaturesGenerator,
                 data_fetcher: DataFetcher,
                 data_structure: TickStructure,
                 symbols: list,
                 timeframe: str):
        self.symbols = symbols
        self.data_fetcher = data_fetcher
        self.data_structure = data_structure
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
                              data_structure: TickStructure,
                              symbols: list,
                              timeframe: str) -> CandlestickGenerator:
    for candlestick_generator in CandlestickGenerator.__subclasses__():
        if candlestick_generator.condition(name):
            return candlestick_generator(features_generator, data_fetcher,
                                         data_structure,
                                         symbols,
                                         timeframe)
    raise CandlestickGeneratorException(f"Candlestick generator: {name} not found")
