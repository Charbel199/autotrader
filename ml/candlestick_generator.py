from data.previous_data.data_fetcher import DataFetcher
import collections


class CandlestickGenerator(object):
    data_fetcher: DataFetcher

    def __init__(self, data_fetcher, symbols):
        self.buffer = collections.deque()
        self.symbols = symbols
        self.data_fetcher = data_fetcher
        pass

    def fetch_new_candlesticks(self):
        pass

    def get_new_candlesticks(self):
        pass
