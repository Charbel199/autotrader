from data.data_fetcher import DataFetcher
from binance.client import Client
import numpy as np
import os


class DataFetcherBinance(DataFetcher):
    binance_timeframes = {
        "1m": Client.KLINE_INTERVAL_1MINUTE,
        "5m": Client.KLINE_INTERVAL_5MINUTE,
        "15m": Client.KLINE_INTERVAL_15MINUTE,
        "1h": Client.KLINE_INTERVAL_1HOUR,
        "2h": Client.KLINE_INTERVAL_2HOUR
    }

    def __init__(self, symbol, timeframe):
        super().__init__(symbol, timeframe)

    def get_candlesticks(self, start_date, end_date=None) -> np.ndarray:
        try:
            client = Client(os.getenv('API_KEY'), os.getenv('API_SECRET'))

            # Format timeframe
            if self.timeframe in self.binance_timeframes:
                binance_timeframe = self.binance_timeframes[self.timeframe]
            else:
                binance_timeframe = None

            # Get candlesticks
            if binance_timeframe:
                if end_date:
                    candlesticks = client.get_historical_klines(self.symbol, binance_timeframe, start_date, end_date)
                else:
                    candlesticks = client.get_historical_klines(self.symbol, binance_timeframe, start_date)
            else:
                return np.array([])
            candlesticks = list(map(format_tick, candlesticks))
            return np.array(candlesticks)
        except Exception:
            return np.array([])

    @staticmethod
    def condition(name):
        return name == 'binance'


def format_tick(tick):
    candlestick = {
        "Time": tick[0],
        "Open": tick[1],
        "Close": tick[4],
        "High": tick[2],
        "Low": tick[3],
        "Volume": tick[5],
        "OpenTime": tick[0],
        "CloseTime": tick[6]
    }
    return candlestick
