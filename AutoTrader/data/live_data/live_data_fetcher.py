from abc import ABC, abstractmethod
from typing import Callable


class LiveDataFetcher(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def run(self, symbol: str, timeframe: str, process_message: Callable[[dict], None]) -> None:
        pass

    @abstractmethod
    def stop(self) -> None:
        pass

    @staticmethod
    @abstractmethod
    def condition(name: str) -> bool:
        pass


# Get fetcher based on broker name
def get_live_fetcher(name: str) -> LiveDataFetcher:
    for fetcher in LiveDataFetcher.__subclasses__():
        if fetcher.condition(name):
            return fetcher()
    raise Exception('Live fetcher not found.')
