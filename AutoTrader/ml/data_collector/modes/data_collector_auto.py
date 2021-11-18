from AutoTrader.ml.data_collector.features_generator.features_generator import get_features_generator
from AutoTrader.data.previous_data.data_fetcher import get_fetcher
from AutoTrader.data.data_structures.structure import get_data_structure
from AutoTrader.helper import date_helper, logger
from AutoTrader.ml.data_collector.generator.candlestick_generator import get_candlestick_generator

log = logger.get_logger(__name__)


class DataCollectorAuto(object):
    def __init__(self,
                 symbols: list,
                 timeframe: str,
                 data_fetcher_provider: str,
                 data_structure_provider: str,
                 features_generator_provider: str,
                 candlestick_generator_processor_provider: str,
                 start_date: str):
        self.data = {}
        self.start_date = start_date
        data_fetcher = get_fetcher(data_fetcher_provider)
        data_structure = get_data_structure(data_structure_provider)
        candlestick_generator_processor = get_features_generator(features_generator_provider, data_structure)
        self.generator = get_candlestick_generator(candlestick_generator_processor_provider, candlestick_generator_processor, data_fetcher, data_structure, symbols, timeframe)
        self.generator.fetch_new_candlesticks(date_helper.get_random_timestamp(date_helper.from_binance_date_to_timestamp(start_date)), 8)

    def process_collected_data(self) -> None:
        # Save old data
        pass

    def get_new_candlesticks(self) -> None:
        self.data = self.generator.get_new_candlesticks()
        if self.data != {}:
            candlesticks = self.data['Ticks']
            # print(candlesticks)
            # Set Buy and Sell
            # Store results

        self.generator.fetch_new_candlesticks(date_helper.get_random_timestamp(date_helper.from_binance_date_to_timestamp(self.start_date)), 8)

    def launch_auto_collector(self):
        for i in range(30):
            self.get_new_candlesticks()
