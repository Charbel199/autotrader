from data.data_structures.structure import TickStructure
from abc import abstractmethod


class CandlestickProcessor(object):
    data_structure: TickStructure

    def __init__(self, data_structure):
        self.data_structure = data_structure

    @abstractmethod
    def process_candlesticks(self, candlesticks):
        pass

    @staticmethod
    @abstractmethod
    def condition(name):
        pass


# Get fetcher based on broker name
def get_candlestick_processor(name, data_structure):
    for candlestick_processor in CandlestickProcessor.__subclasses__():
        if candlestick_processor.condition(name):
            return candlestick_processor(data_structure)
    return None
