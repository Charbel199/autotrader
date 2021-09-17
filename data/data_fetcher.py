from abc import ABC, abstractmethod
import numpy as np


class DataFetcher(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def get_candlesticks(self, symbol, timeframe, start_date, end_date=None):
        pass

    @staticmethod
    @abstractmethod
    def condition(name):
        pass


# Get fetcher based on broker name
def get_fetcher(name):
    for fetcher in DataFetcher.__subclasses__():
        if fetcher.condition(name):
            return fetcher()
    return None
