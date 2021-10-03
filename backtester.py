from strategies.strategy import Strategy
from data_structures.structure import TickStructure
from data.data_fetcher import DataFetcher


class BackTester(object):
    strategy: Strategy
    data_structure: TickStructure
    data_fetcher: DataFetcher

    def __init__(self, symbol, timeframe, data_fetcher, data_structure, strategy, start_date, end_date=None):
        self.data_structure = data_structure
        self.strategy = strategy
        self.symbol = symbol
        self.timeframe = timeframe
        self.data_fetcher = data_fetcher
        self.start_date = start_date
        self.end_date = end_date

    def run_backtester(self):
        candlesticks = self.data_fetcher.get_candlesticks(self.symbol, self.timeframe, self.start_date, self.end_date)
        for candlestick in candlesticks:
            if self.data_structure:
                self.data_structure.add_row(candlestick)
                self.strategy.process_new_candlestick()
                self.data_structure.set_tick(candlestick)
                # self.strategy.process_new_tick()
