from data.data_fetcher import DataFetcher
from binance.client import Client
import os


class DataFetcherBinance(DataFetcher):
    def __init__(self, symbol, timeframe):
        super().__init__(symbol, timeframe)

    def get_candlesticks(self, start_date, end_date=None):
        try:
            client = Client(os.getenv('API_KEY'), os.getenv('API_SECRET'))

            if self.timeframe == "1m":
                binance_timeframe = Client.KLINE_INTERVAL_1MINUTE
            elif self.timeframe == "5m":
                binance_timeframe = Client.KLINE_INTERVAL_5MINUTE
            elif self.timeframe == "15m":
                binance_timeframe = Client.KLINE_INTERVAL_15MINUTE
            elif self.timeframe == "1h":
                binance_timeframe = Client.KLINE_INTERVAL_1HOUR
            elif self.timeframe == "2h":
                binance_timeframe = Client.KLINE_INTERVAL_2HOUR
            else:
                binance_timeframe = None

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
