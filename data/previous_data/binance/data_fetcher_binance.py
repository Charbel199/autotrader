from data.previous_data.data_fetcher import DataFetcher
from binance.client import Client
import os
from data.data_logger import logger
from helper import date_helper
import pickle
import os

log = logger.get_logger(__name__)


class DataFetcherBinance(DataFetcher):
    binance_timeframes = {
        "1m": Client.KLINE_INTERVAL_1MINUTE,
        "5m": Client.KLINE_INTERVAL_5MINUTE,
        "15m": Client.KLINE_INTERVAL_15MINUTE,
        "1h": Client.KLINE_INTERVAL_1HOUR,
        "2h": Client.KLINE_INTERVAL_2HOUR
    }

    def __init__(self):
        super().__init__()

    def get_candlesticks(self, symbol, timeframe, start_date, end_date=None):
        log.info(f'Fetching candlesticks for {symbol}, timeframe of {timeframe} and a start date of {start_date} and an end date of {end_date}')
        try:
            candlesticks = load_candlesticks(symbol, timeframe, start_date, end_date)
            if len(candlesticks) == 0:
                client = Client(os.getenv('API_KEY'), os.getenv('API_SECRET'))

                # Format timeframe
                if timeframe in self.binance_timeframes:
                    binance_timeframe = self.binance_timeframes[timeframe]
                else:
                    binance_timeframe = None

                # Get candlesticks
                if binance_timeframe:
                    if end_date:
                        candlesticks = client.get_historical_klines(symbol, binance_timeframe, start_date, end_date)
                    else:
                        candlesticks = client.get_historical_klines(symbol, binance_timeframe, start_date)
                else:
                    return []
                candlesticks = list(map(format_tick, candlesticks))
                save_candlesticks(symbol, timeframe, start_date, end_date, candlesticks)
                # Close connection
                client.close_connection()

            log.info('Finished fetching candlesticks')
            return candlesticks
        except Exception:
            log.error('Ran into an error while fetching candlesticks')
            return []

    @staticmethod
    def condition(name):
        return name == 'binance'


def format_tick(tick):
    candlestick = {
        # "Time": date_helper.from_timestamp_to_date(int(tick[0])/1000),
        "Time": tick[0],
        "Open": float(tick[1]),
        "Close": float(tick[4]),
        "High": float(tick[2]),
        "Low": float(tick[3]),
        "Volume": float(tick[5]),
        "OpenTime": tick[0],
        "CloseTime": tick[6]
    }
    return candlestick


def load_candlesticks(symbol, timeframe, start_date, end_date):
    try:
        if end_date is not None:
            directory = "saved_data"
            existing_files = [f for f in os.listdir(directory) if f.endswith('.pkl')]
            file_name = f"{symbol}_{timeframe}_{start_date}_{end_date}.pkl"
            if file_name in existing_files:
                with open(f"{directory}/{file_name}", 'rb') as f:
                    return pickle.load(f)
            else:
                return []
    except Exception:
        return []


def save_candlesticks(symbol, timeframe, start_date, end_date, list):
    try:
        if end_date is not None:
            directory = "saved_data"
            existing_files = [f for f in os.listdir(directory) if f.endswith('.pkl')]
            file_name = f"{symbol}_{timeframe}_{start_date}_{end_date}.pkl"
            if file_name not in existing_files:
                with open(f"{directory}/{file_name}", 'wb') as f:
                    pickle.dump(list, f)
    except Exception:
        return
