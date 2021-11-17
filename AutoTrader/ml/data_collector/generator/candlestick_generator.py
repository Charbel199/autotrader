from AutoTrader.data.previous_data.data_fetcher import DataFetcher
from AutoTrader.data.data_structures.structure import TickStructure
import collections
import random
from AutoTrader.helper import date_helper, logger
from AutoTrader.ml.data_collector.generator.candlestick_processor.candlestick_processor import CandlestickProcessor

log = logger.get_logger(__name__)


class CandlestickGenerator(object):
    data_fetcher: DataFetcher
    data_structure: TickStructure
    candlestick_processor: CandlestickProcessor

    def __init__(self,
                 candlestick_generator_processor: CandlestickProcessor,
                 data_fetcher: DataFetcher,
                 data_structure: TickStructure,
                 symbols: list,
                 timeframe: str):
        self.buffer = collections.deque()
        self.symbols = symbols
        self.data_fetcher = data_fetcher
        self.data_structure = data_structure
        self.candlestick_generator_processor = candlestick_generator_processor
        self.timeframe = timeframe

    def fetch_new_candlesticks(self, start_timestamp: int, duration: int) -> None:
        log.info(date_helper.from_timestamp_to_binance_date(start_timestamp))
        log.info(date_helper.from_timestamp_to_binance_date(
            date_helper.get_next_timestamp(start_timestamp, hours=duration)))

        candlesticks = self.data_fetcher.get_candlesticks(
            random.choice(self.symbols),
            self.timeframe,
            date_helper.from_timestamp_to_binance_date(start_timestamp),
            date_helper.from_timestamp_to_binance_date(
                date_helper.get_next_timestamp(start_timestamp, hours=duration))
        )

        self.buffer.append(self.candlestick_generator_processor.process_candlesticks(candlesticks))

    def get_new_candlesticks(self) -> dict:
        return self.buffer.pop()
