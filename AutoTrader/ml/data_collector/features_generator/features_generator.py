from AutoTrader.data.data_structures.structure import TickStructure
from abc import abstractmethod
from AutoTrader.exceptions import FeaturesGeneratorNotFound


class FeaturesGenerator(object):
    data_structure: TickStructure

    def __init__(self, data_structure: TickStructure):
        self.data_structure = data_structure

    @abstractmethod
    def process_candlesticks(self, candlesticks: list) -> dict:
        pass

    @staticmethod
    @abstractmethod
    def condition(name: str) -> bool:
        pass


# Get fetcher based on broker name
def get_features_generator(name: str, data_structure: TickStructure) -> FeaturesGenerator:
    for features_generator in FeaturesGenerator.__subclasses__():
        if features_generator.condition(name):
            return features_generator(data_structure)
    raise FeaturesGeneratorNotFound(f"Features generator: {name} not found")
