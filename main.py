from data.data_fetcher import DataFetcher
from data.binance.data_fetcher_binance import DataFetcherBinance


def get_fetcher(name):
    for subclass in DataFetcher.__subclasses__():
        if subclass.condition(name):
            return subclass
    return None


subclass = get_fetcher('binance')
if subclass:
    data_fetcher_obj = subclass('DOGE', '5m')
    data_fetcher_obj.get_candlesticks('test')
