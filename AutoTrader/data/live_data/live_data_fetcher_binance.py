from AutoTrader.data.live_data.live_data_fetcher import LiveDataFetcher
from binance import ThreadedWebsocketManager
from typing import Callable
from AutoTrader.helper import logger
from AutoTrader.data import Tick

log = logger.get_logger(__name__)


class LiveDataFetcherBinance(LiveDataFetcher):

    def __init__(self):
        super().__init__()
        self.twm = ThreadedWebsocketManager()
        self.twm.start()
        self.process_message = None

    def run(self, symbol: str, timeframe: str, process_message: Callable[[dict], None]) -> None:
        log.info(f'Live fetching candlesticks for {symbol}, timeframe of {timeframe}')
        self.process_message = process_message
        self.twm.start_kline_socket(callback=self.map_message, symbol=symbol, interval=timeframe)

    def stop(self) -> None:
        log.info(f'Stopping live fetching')
        self.twm.stop()

    def map_message(self, message) -> None:
        tick = Tick(
            Time=int(int(message["E"]) / 1000),
            Open=float(message["k"]["o"]),
            Close=float(message["k"]["c"]),
            High=float(message["k"]["h"]),
            Low=float(message["k"]["l"]),
            Volume=float(message["k"]["v"]),
            OpenTime=int(message["k"]["t"]),
            CloseTime=int(message["k"]["T"])
        )
        self.process_message(tick)

    @staticmethod
    def condition(name: str) -> bool:
        return name == 'binance'
