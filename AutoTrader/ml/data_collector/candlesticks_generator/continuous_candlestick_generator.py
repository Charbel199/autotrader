from AutoTrader.data.previous_data.data_fetcher import DataFetcher
from AutoTrader.data.data_structures.structure import TickStructure
import collections
import random
from AutoTrader.helper import date_helper, logger
from AutoTrader.ml.data_collector.features_generator.features_generator import FeaturesGenerator
from AutoTrader.ml.data_collector.candlesticks_generator.candlestick_generator import CandlestickGenerator

log = logger.get_logger(__name__)


class CandlestickContinuousGenerator(CandlestickGenerator):
    data_fetcher: DataFetcher
    data_structure: TickStructure
    candlestick_processor: FeaturesGenerator

    def __init__(self,
                 features_generator: FeaturesGenerator,
                 data_fetcher: DataFetcher,
                 data_structure: TickStructure,
                 symbols: list,
                 timeframe: str):
        super().__init__(features_generator, data_fetcher, data_structure, symbols, timeframe)
        self.buffer = collections.deque()

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

        self.buffer.append(self.features_generator.process_candlesticks(candlesticks))

    def get_new_candlesticks(self) -> dict:
        return self.buffer.pop()

    @staticmethod
    def condition(name: str) -> bool:
        return name == 'continuous'
