from AutoTrader.data.previous_data.data_fetcher import DataFetcher
from AutoTrader.data.data_structures.structure import TickStructure
import collections
import random
from AutoTrader.helper import date_helper
from AutoTrader.ml.candlestick_processor.candlestick_processor import CandlestickProcessor
from AutoTrader.data.data_logger import logger
from plotly.graph_objs import Figure

log = logger.get_logger(__name__)


class CandlestickGenerator(object):
    data_fetcher: DataFetcher
    data_structure: TickStructure
    candlestick_processor: CandlestickProcessor

    def __init__(self,
                 candlestick_generator_processor: CandlestickProcessor,
                 data_fetcher: DataFetcher,
                 data_structure: TickStructure,
                 symbols: str,
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


from AutoTrader.ml.candlestick_processor.candlestick_processor import get_candlestick_processor
from AutoTrader.data.previous_data.data_fetcher import get_fetcher
import pandas as pd
from AutoTrader.data.data_structures.structure import get_data_structure
from plotly.subplots import make_subplots
import plotly.graph_objects as go


class CandlestickGeneratorRunner(object):

    def __init__(self,
                 symbols: list,
                 timeframe: str,
                 data_fetcher_provider: str,
                 data_structure_provider: str,
                 candlestick_processor_provider: str,
                 start_date: str):
        self.data = {}
        self.fig = make_subplots(rows=1, cols=1)
        self.clicked_candlesticks = []
        self.start_date = start_date
        data_fetcher = get_fetcher(data_fetcher_provider)
        data_structure = get_data_structure(data_structure_provider)
        candlestick_generator_processor = get_candlestick_processor(candlestick_processor_provider, data_structure)
        self.generator = CandlestickGenerator(candlestick_generator_processor, data_fetcher, data_structure, symbols, timeframe)
        self.generator.fetch_new_candlesticks(date_helper.get_random_timestamp(date_helper.from_binance_date_to_timestamp(start_date)), 8)

    def get_new_candlesticks(self) -> None:
        # Save old data
        if len(self.clicked_candlesticks) > 0:
            print('candlesticks ', self.clicked_candlesticks)
            # print(self.data['ADX'].to_string())

        self.clicked_candlesticks = []
        self.data = self.generator.get_new_candlesticks()
        candlesticks = self.data['Ticks']
        df = pd.DataFrame(candlesticks)
        self.fig = make_subplots(rows=1, cols=1)
        self.fig.append_trace(go.Candlestick(x=df['Time'],
                                             open=df['Open'],
                                             high=df['High'],
                                             low=df['Low'],
                                             close=df['Close'], name="Candlesticks"), row=1, col=1)
        self.fig.update_layout(xaxis_rangeslider_visible=False)
        self.generator.fetch_new_candlesticks(date_helper.get_random_timestamp(date_helper.from_binance_date_to_timestamp(self.start_date)), 8)

    def click_candlestick(self, click: dict) -> None:
        if len(self.clicked_candlesticks) < 2:
            log.info(f"Candlestick clicked {click}")
            time = click['x']
            close = click['close']
            self.clicked_candlesticks.append({
                'Time': time,
                'Close': close
            })
            if len(self.clicked_candlesticks) == 1:
                self.fig.append_trace(go.Scatter(
                    x=[time],
                    y=[close],
                    marker=dict(color="gold", size=13, symbol=46),
                    mode="markers",
                    name="Buy"
                ), row=1, col=1)
            elif len(self.clicked_candlesticks) == 2:
                self.fig.append_trace(go.Scatter(
                    x=[time],
                    y=[close],
                    marker=dict(color="silver", size=13, symbol=45),
                    mode="markers",
                    name="Sell"), row=1, col=1)

    def get_fig(self) -> Figure:
        return self.fig


class CandlestickGeneratorAutoRunner(object):

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
        self.generator.fetch_new_candlesticks(date_helper.get_random_timestamp(date_helper.from_binance_date_to_timestamp(self.start_date)), 8)
