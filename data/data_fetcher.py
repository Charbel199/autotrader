from abc import ABC, abstractmethod


class DataFetcher(ABC):

    def __init__(self, symbol, timeframe):
        self.symbol = symbol
        self.timeframe = timeframe

    @abstractmethod
    def get_candlesticks(self, start_date, end_date=None):
        pass

    @staticmethod
    @abstractmethod
    def condition(name):
        pass


def get_fetcher(name):
    for fetcher in DataFetcher.__subclasses__():
        if fetcher.condition(name):
            return fetcher
    return None