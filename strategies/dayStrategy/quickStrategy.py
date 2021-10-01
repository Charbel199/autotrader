from strategies.strategy import Strategy
from indicators.adx_indicator.adx_indicator_processor import ADX
from indicators.candlestick_type.candlestick_type_processor import CandlestickType
from indicators.rsi_indicator.rsi_indicator_processor import RSI


class QuickStrategy(Strategy):
    def __init__(self, data_structure, account):
        super().__init__(data_structure, account)
        self.ADX = ADX(data_structure)
        self.CandlestickType = CandlestickType(data_structure)
        self.RSI = RSI(data_structure)

    def process_new_candlestick(self):
        # Process ADX
        self.ADX.process_new_candlestick()
        self.CandlestickType.process_new_candlestick()
        self.RSI.process_new_candlestick()
        # print(self.RSI.get_last_rsi_values())
        # print(self.CandlestickType.get_last_candlestick_type_values())
        # print(self.ADX.get_last_adx_values())
        # print('Got a new candlestick strat ', self.data_structure.get_data())

        if (self.ADX.get_last_adx_values()['ADX'].iloc[-1] > 26):
            self.account.buy(self.ADX.get_last_adx_values()['Time'].iloc[-1], 'DOGEUSDT', 10, 0.5)
        pass

    def process_new_tick(self):
        print('Got new tick in strat ', self.data_structure.get_tick())
        pass

    @staticmethod
    def condition(name):
        return name == 'quickStrategy'
