from abc import ABC, abstractmethod
import pandas as pd


class Account(ABC):
    columns = ['Time', 'Action', 'Amount', 'Symbol', 'Price']

    def __init__(self):
        self.position = {}
        self.df = pd.DataFrame(columns=self.columns)

    @abstractmethod
    def get_position(self):
        return self.position

    @abstractmethod
    def buy(self, time, symbol, amount, price):
        pass

    @abstractmethod
    def sell(self, time, symbol, amount, price):
        pass

    def get_profit(self):
        if self.df["Action"].iloc[-1] == "Buy":
            self.df = self.df[:-1]
        sells = self.df[self.df["Action"] == "Sell"]
        buys = self.df[self.df["Action"] == "Buy"]
        total_buy_price = (buys["Price"] * buys["Amount"]).sum()
        total_sell_price = (sells["Price"] * sells["Amount"]).sum()
        profit = total_sell_price - total_buy_price
        if total_buy_price != 0:
            percentage = ((total_sell_price - total_buy_price) / total_buy_price) * 100
        else:
            percentage = 0
        print("Buy ", total_buy_price)
        print("Sell ", total_sell_price)
        print("Percentage gain: ", percentage)
        return profit

    @abstractmethod
    def get_plot(self):
        pass

    @staticmethod
    @abstractmethod
    def condition(name):
        pass


# Get strategy
def get_account(name):
    for account in Account.__subclasses__():
        if account.condition(name):
            return account()
    return None
