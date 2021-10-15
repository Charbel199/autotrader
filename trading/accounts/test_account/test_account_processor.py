from trading.accounts.account import Account
import plotly.graph_objects as go
from data.data_logger import logger

log = logger.get_logger(__name__)


class TestAccount(Account):

    def __init__(self, balance):
        super().__init__(balance)

    def get_position(self):
        return self.position

    def buy(self, time, symbol, price, amount=0):
        if amount == 0:
            amount = self.balance / price
        self.balance -= amount * price
        log.info(f"{time} - Bought - {amount} of {symbol} at {price}")
        self.position = {
            "Time": time,
            "Symbol": symbol,
            "Amount": amount,
            "Price": price
        }
        log.info(f"New position {self.position}")
        self.df.loc[len(self.df.index)] = {
            'Time': time,
            'Action': 'Buy',
            'Amount': amount,
            'Symbol': symbol,
            'Price': price
        }

    def sell(self, time, symbol, price, amount=0):
        if self.position['Time'] != time:
            if amount == 0:
                amount = self.position['Amount']
            self.balance += amount * price
            log.info(f"{time} - Sold - {amount} of {symbol} at {price}")
            log.info(f"New balance: {self.balance}")
            self.position = {}
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
            marker=dict(color="silver", size=13, symbol=45),
            mode="markers",
            name="Sell"
        )

    @staticmethod
    def condition(name):
        return name == "testAccount"
