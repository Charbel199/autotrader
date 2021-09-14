from data.data_fetcher import DataFetcher


class DataFetcherBinance(DataFetcher):
    def __init__(self, symbol, timeframe):
        super().__init__(symbol, timeframe)

    def get_candlesticks(self, start_date, end_date=None):
        print('in binance')

    @staticmethod
    def condition(name):
        return name == 'binance'
