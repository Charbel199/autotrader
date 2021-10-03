from account.account import Account
import plotly.graph_objects as go


class TestAccount(Account):

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

    def get_plot(self):
        buy_df = self.df[(self.df['Action'] == 'Buy')]
        sell_df = self.df[(self.df['Action'] == 'Sell')]
        return go.Scatter(
            x=buy_df['Time'],
            y=buy_df['Price'],
            marker=dict(color="gold", size=13, symbol=46),
            mode="markers",
            name="Buy"
        ), go.Scatter(
            x=sell_df['Time'],
            y=sell_df['Price'],
            marker=dict(color="gold", size=13, symbol=46),
            mode="markers",
            name="Sell"
        )

    @staticmethod
    def condition(name):
        return name == "testAccount"
