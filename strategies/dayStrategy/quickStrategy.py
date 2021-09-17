from strategies.strategy import Strategy


class QuickStrategy(Strategy):

    def __init__(self, data_structure):
        super().__init__(data_structure)

    def process_new_candlestick(self):
        #print('Got a new candlestick strat ',self.data_structure.get_data())
        pass

    def process_new_tick(self):
        print('Got new tick in strat ', self.data_structure.get_tick())
        pass

    @staticmethod
    def condition(name):
        return name == 'quickStrategy'
