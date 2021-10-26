from AutoTrader.trading.accounts.account import Account
import plotly.graph_objects as go
from AutoTrader.data.data_logger import logger

log = logger.get_logger(__name__)


class TestAccount(Account):

    def __init__(self, balance: float):
        super().__init__(balance)

    def get_position(self) -> dict:
        return self.position

    def buy(self,
            time: int,
            symbol: str,
            price: float,
            amount: float = 0) -> None:
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
        self.list.append({
            'Time': time,
            'Action': 'Buy',
            'Amount': amount,
            'Symbol': symbol,
            'Price': price
        })

    def sell(self,
             time: int,
             symbol: str,
             price: float,
             amount: float = 0) -> None:
        if self.position['Time'] != time:
            if amount == 0:
                amount = self.position['Amount']
            self.balance += amount * price
            log.info(f"{time} - Sold - {amount} of {symbol} at {price}")
            log.info(f"New balance: {self.balance}")
            self.position = {}
            self.list.append({
                'Time': time,
                'Action': 'Sell',
                'Amount': amount,
                'Symbol': symbol,
                'Price': price
            })

    def get_plot(self) -> go:
        buys = [d for d in self.list if d["Action"] == "Buy"]
        sells = [d for d in self.list if d["Action"] == "Sell"]
        return go.Scatter(
            x=[d["Time"] for d in buys],
            y=[d["Price"] for d in buys],
            marker=dict(color="gold", size=13, symbol=46),
            mode="markers",
            name="Buy"
        ), go.Scatter(
            x=[d["Time"] for d in sells],
            y=[d["Price"] for d in sells],
            marker=dict(color="silver", size=13, symbol=45),
            mode="markers",
            name="Sell"
        )

    @staticmethod
    def condition(name: str) -> bool:
        return name == "testAccount"
