from strategies.strategy import Strategy
from data_structures.structure import TickStructure
from data.data_fetcher import DataFetcher
from live_data.live_data_fetcher import LiveDataFetcher


class LiveTrader(object):
    strategy: Strategy
    data_structure: TickStructure
    data_fetcher: DataFetcher
    live_data_fetcher: LiveDataFetcher

    def __init__(self, symbol, timeframe, live_data_fetcher, data_fetcher, data_structure, strategy, back_date=None):
        self.data_structure = data_structure
        self.live_data_fetcher = live_data_fetcher
        self.strategy = strategy
        self.symbol = symbol
        self.timeframe = timeframe
        self.data_fetcher = data_fetcher
        self.back_date = back_date

    def run_live_trader(self):
        if self.back_date:
            candlesticks = self.data_fetcher.get_candlesticks(
                self.symbol, self.timeframe, self.back_date
            )
            self.strategy.disable_transactions()
            for candlestick in candlesticks:
                if self.data_structure:
                    self.data_structure.set_tick(candlestick)
                    self.data_structure.add_row(candlestick)
                    self.strategy.process_new_candlestick()
            self.strategy.enable_transactions()
        self.live_data_fetcher.run(self.symbol, self.timeframe, self.process_message)

    def stop_live_trader(self):
        self.live_data_fetcher.stop()

    def process_message(self, tick):
        if self.data_structure:
            # Only add to rows if it's a new candlestick
            if self.data_structure.get_tick() != {} and tick["CloseTime"] != self.data_structure.get_tick()["CloseTime"]:
                self.data_structure.add_row(self.data_structure.get_tick())
                self.strategy.process_new_candlestick()

            self.data_structure.set_tick(tick)
            self.strategy.process_new_tick()
