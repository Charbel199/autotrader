from data.previous_data.data_fetcher import DataFetcher
import collections
import random
from helper import date_helper


class CandlestickGenerator(object):
    data_fetcher: DataFetcher

    def __init__(self, data_fetcher, symbols, timeframe):
        self.buffer = collections.deque()
        self.symbols = symbols
        self.data_fetcher = data_fetcher
        self.timeframe = timeframe
        pass

    def fetch_new_candlesticks(self, start_date, duration):
        print(date_helper.from_timestamp_to_binance_date(start_date))
        print( date_helper.from_timestamp_to_binance_date(
                date_helper.get_next_timestamp(start_date, hours=duration)))
        candlesticks = self.data_fetcher.get_candlesticks(
            random.choice(self.symbols),
            self.timeframe,
            date_helper.from_timestamp_to_binance_date(start_date),
            date_helper.from_timestamp_to_binance_date(
                date_helper.get_next_timestamp(start_date, hours=duration))
        )
        self.buffer.append(candlesticks)
        print("Deque ",self.buffer)
        print("len of dq ",len(self.buffer) )
    def get_new_candlesticks(self):
        return self.buffer.pop()