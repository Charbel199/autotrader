from AutoTrader.data.data_structures.candlesticks import Candlesticks
from abc import abstractmethod
from AutoTrader.exceptions import FeaturesGeneratorNotFound


class FeaturesGenerator(object):
    candlesticks: Candlesticks

    def __init__(self, candlesticks: Candlesticks):
        self.candlesticks = candlesticks

    @abstractmethod
    def process_candlesticks(self, candlesticks: list) -> dict:
        pass

    @staticmethod
    @abstractmethod
    def condition(name: str) -> bool:
        pass


# Get fetcher based on broker name
def get_features_generator(name: str, data_structure: Candlesticks) -> FeaturesGenerator:
    for features_generator in FeaturesGenerator.__subclasses__():
        if features_generator.condition(name):
            return features_generator(data_structure)
    raise FeaturesGeneratorNotFound(f"Features generator: {name} not found")
