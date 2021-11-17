from AutoTrader.ml.data_collector.generator.candlestick_processor.candlestick_processor import get_candlestick_processor
from AutoTrader.data.previous_data.data_fetcher import get_fetcher
import pandas as pd
from AutoTrader.data.data_structures.structure import get_data_structure
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from AutoTrader.helper import date_helper, logger
from AutoTrader.ml.data_collector.generator.candlestick_generator import CandlestickGenerator
from plotly.graph_objs import Figure

log = logger.get_logger(__name__)


class DataCollectorAuto(object):
    def __init__(self,
                 symbols: list,
                 timeframe: str,
                 data_fetcher_provider: str,
                 data_structure_provider: str,
                 candlestick_auto_processor_provider: str,
                 start_date: str):
        self.data = {}
        self.start_date = start_date
        data_fetcher = get_fetcher(data_fetcher_provider)
        data_structure = get_data_structure(data_structure_provider)
        candlestick_generator_processor = get_candlestick_processor(candlestick_auto_processor_provider, data_structure)
        self.generator = CandlestickGenerator(candlestick_generator_processor, data_fetcher, data_structure, symbols, timeframe)
        self.generator.fetch_new_candlesticks(date_helper.get_random_timestamp(date_helper.from_binance_date_to_timestamp(start_date)), 8)

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
