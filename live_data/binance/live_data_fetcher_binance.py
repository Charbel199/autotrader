from live_data.live_data_fetcher import LiveDataFetcher
from data_structures.structure import TickStructure
import websocket
from binance import ThreadedWebsocketManager


class LiveDataFetcherBinance(LiveDataFetcher):

    data_structure: TickStructure

    def __init__(self):
        self.twm = ThreadedWebsocketManager()
        self.twm.start()

    def run(self,symbol, timeframe, data_structure):
        self.data_structure = data_structure
        self.twm.start_kline_socket(callback=self.map_message, symbol=symbol, interval=timeframe)

    def stop(self):
        self.twm.stop()

    def map_message(self, message):
        tick = {
            "Time": message["E"],
            "Open": message["k"]["o"],
            "Close": message["k"]["c"],
            "High": message["k"]["h"],
            "Low": message["k"]["l"],
            "Volume": message["k"]["v"],
            "OpenTime": message["k"]["t"],
            "CloseTime": message["k"]["T"],
        }
        if self.data_structure:
            self.data_structure.add_tick(tick)


    @staticmethod
    def condition(name):
        return name == 'binance'

