from AutoTrader.trading.accounts.account import Account
import plotly.graph_objects as go
from AutoTrader.helper import logger
from AutoTrader.models import Position
from typing import Dict
from binance.client import Client
import os
from dotenv import load_dotenv
load_dotenv()
log = logger.get_logger(__name__)


class AccountBinance(Account):
    transaction_percentage = 0.1 / 100
    transaction_fee = 0
    client: Client = Client(os.getenv('API_KEY'), os.getenv('API_SECRET'))

    def __init__(self):
        super().__init__()


    def transaction(self,
                    time: int,
                    symbol: str,
                    source_symbol: str,
                    destination_symbol: str,
                    source_symbol_amount: float,
                    transaction_type: str,
                    destination_symbol_amount: float = 0) -> None:

        if transaction_type == 'buy':
            if destination_symbol_amount == 0:
                destination_symbol_amount = self.balance[source_symbol] / source_symbol_amount

            cost = destination_symbol_amount * source_symbol_amount  # Amount of initial symbol used
            print(self.balance, ' selling ', source_symbol, ' amount ', source_symbol_amount)
            self.balance[source_symbol] -= cost * (1 + self.transaction_percentage) + self.transaction_percentage

            log.info(
                f"{time} - Bought - {destination_symbol_amount} of {destination_symbol} at {source_symbol_amount} of {source_symbol}  - Fee - {self.transaction_fee + cost * self.transaction_percentage}")
            self.positions[destination_symbol] = Position(
                Time=time,
                Symbol=destination_symbol,
                Amount=destination_symbol_amount,
                Price=source_symbol_amount
            )
            log.info(f"New position {self.positions[destination_symbol]}")
            self.transactions[symbol] = [] if symbol not in self.transactions else self.transactions[symbol]
            self.transactions[symbol].append({
                'Time': time,
                'Action': 'Buy',
                'Amount': destination_symbol_amount,
                'Symbol': destination_symbol,
                'Price': source_symbol_amount
            })
        if transaction_type == 'sell':
            if self.positions[destination_symbol].Time != time:
                if destination_symbol_amount == 0:
                    destination_symbol_amount = self.positions[destination_symbol].Amount
                self.balance[source_symbol] += destination_symbol_amount * source_symbol_amount
                log.info(f"{time} - Sold - {destination_symbol_amount} of {destination_symbol} at {source_symbol_amount} of {source_symbol}")
                log.info(f"New balance: {self.balance[source_symbol]}")
                self.positions[destination_symbol] = Position()
                self.transactions[symbol] = [] if symbol not in self.transactions else self.transactions[symbol]

                self.transactions[symbol].append({
                    'Time': time,
                    'Action': 'Sell',
                    'Amount': destination_symbol_amount,
                    'Symbol': destination_symbol,
                    'Price': source_symbol_amount
                })

    def get_plot(self, symbol: str) -> go:
        buys = [d for d in self.transactions[symbol] if d["Action"] == "Buy"]
        sells = [d for d in self.transactions[symbol] if d["Action"] == "Sell"]
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

    def _get_balance(self) -> Dict[str, float]:
        binance_balance = self.client.get_account()['balances']
        balance = {}
        for b in binance_balance:
            balance[b['asset']] = float(b['free'])
        return balance

    @staticmethod
    def condition(name: str) -> bool:
        return name == "binanceAccount"
