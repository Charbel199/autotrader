from data.data_fetcher import DataFetcher
from binance.client import Client
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

    def get_candlesticks(self, start_date, end_date=None):
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
                return []
            return candlesticks
        except Exception:
            return []

    @staticmethod
    def condition(name):
        return name == 'binance'
