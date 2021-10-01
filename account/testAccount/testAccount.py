from account.account import Account


class TestAccount(Account):
    columns = ['Time', 'Action', 'Amount', 'Symbol', 'Price']

    def __init__(self):
        super().__init__()

    def get_position(self):
        return self.position

    def buy(self, time, symbol, amount, price):
        print(time, "  -  Bought ", amount, " of: ", symbol, " at ", price)
        print("New position ", self.position)
        self.df.loc[len(self.df.index)] = {
            'Time': time,
            'Action': 'Buy',
            'Amount': amount,
            'Symbol': symbol,
            'Price': price
        }

    def sell(self, time, symbol, amount, price):
        print(time, "  -  Sold ", amount, " of: ", symbol, " at ", price)
        print("New position ", self.position)
        self.df.loc[len(self.df.index)] = {
            'Time': time,
            'Action': 'Sell',
            'Amount': amount,
            'Symbol': symbol,
            'Price': price
        }

    @staticmethod
    def condition(name):
        return name == "testAccount"
