from abc import ABC, abstractmethod
from app.AutoTrader.exceptions import DataFetcherNotFound


class DataFetcher(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def get_candlesticks(self, symbol: str, timeframe: str, start_date: str, end_date: str = None) -> list:
        pass

    @staticmethod
    @abstractmethod
    def condition(name: str) -> bool:
        pass


# Get fetcher based on broker name
def get_fetcher(name: str) -> DataFetcher:
    for fetcher in DataFetcher.__subclasses__():
        if fetcher.condition(name):
            return fetcher()
    raise DataFetcherNotFound(f"Data fetcher: {name} not found")
