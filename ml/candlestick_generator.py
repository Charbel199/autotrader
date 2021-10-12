from data.previous_data.data_fetcher import DataFetcher
from data.data_structures.structure import TickStructure
import collections
import random
from helper import date_helper
from ml.candlestick_processor.candlestick_processor import CandlestickProcessor
from data.data_logger import logger

log = logger.get_logger(__name__)


class CandlestickGenerator(object):
    data_fetcher: DataFetcher
    data_structure: TickStructure
    candlestick_processor: CandlestickProcessor

    def __init__(self, candlestick_generator_processor, data_fetcher, data_structure, symbols, timeframe):
        self.buffer = collections.deque()
        self.symbols = symbols
        self.data_fetcher = data_fetcher
        self.data_structure = data_structure
        self.candlestick_generator_processor = candlestick_generator_processor
        self.timeframe = timeframe

    def fetch_new_candlesticks(self, start_date, duration):
        log.info(date_helper.from_timestamp_to_binance_date(start_date))
        log.info(date_helper.from_timestamp_to_binance_date(
            date_helper.get_next_timestamp(start_date, hours=duration)))


        candlesticks = self.data_fetcher.get_candlesticks(
            random.choice(self.symbols),
            self.timeframe,
            date_helper.from_timestamp_to_binance_date(start_date),
            date_helper.from_timestamp_to_binance_date(
                date_helper.get_next_timestamp(start_date, hours=duration))
        )

        self.buffer.append(self.candlestick_generator_processor.process_candlesticks(candlesticks))

    def get_new_candlesticks(self):
        return self.buffer.pop()
