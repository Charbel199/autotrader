from live_data.live_data_fetcher import LiveDataFetcher
import websocket
from binance import ThreadedWebsocketManager


class LiveDataFetcherBinance(LiveDataFetcher):

    def __init__(self):
        self.twm = ThreadedWebsocketManager()
        self.twm.start()

    def run(self,symbol, timeframe, handle_socket_message):
        self.twm.start_kline_socket(callback=handle_socket_message, symbol=symbol, interval=timeframe)

    def stop(self):
        self.twm.stop()




    @staticmethod
    def condition(name):
        return name == 'binance'
