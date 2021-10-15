from data.live_data.live_data_fetcher import LiveDataFetcher
from trading.strategies.strategy import Strategy
from data.data_structures.structure import TickStructure
from binance import ThreadedWebsocketManager
from data.data_logger import logger

log = logger.get_logger(__name__)


class LiveDataFetcherBinance(LiveDataFetcher):
    strategy: Strategy
    data_structure: TickStructure

    def __init__(self):
        super().__init__()
        self.twm = ThreadedWebsocketManager()
        self.twm.start()

    def run(self, symbol, timeframe, process_message):
        log.info(f'Live fetching candlesticks for {symbol}, timeframe of {timeframe}')
        self.process_message = process_message
        self.twm.start_kline_socket(callback=self.map_message, symbol=symbol, interval=timeframe)

    def stop(self):
        log.info(f'Stopping live fetching')
        self.twm.stop()

    def map_message(self, message):
        tick = {
            "Time": message["E"],
            "Open": float(message["k"]["o"]),
            "Close": float(message["k"]["c"]),
            "High": float(message["k"]["h"]),
            "Low": float(message["k"]["l"]),
            "Volume": float(message["k"]["v"]),
            "OpenTime": message["k"]["t"],
            "CloseTime": message["k"]["T"],
        }
        self.process_message(tick)

    @staticmethod
    def condition(name):
        return name == 'binance'
