from abc import ABC, abstractmethod
import numpy as np


class LiveDataFetcher(ABC):

    def __init__(self):
        pass

    @abstractmethod
    def run(self, symbol, timeframe, process_message):
        pass

    @abstractmethod
    def stop(self):
        pass

    @staticmethod
    @abstractmethod
    def condition(name):
        pass


# Get fetcher based on broker name
def get_live_fetcher(name):
    for fetcher in LiveDataFetcher.__subclasses__():
        if fetcher.condition(name):
            return fetcher()
    return None
