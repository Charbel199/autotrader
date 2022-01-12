from AutoTrader.trading.accounts.account import Account
import plotly.graph_objects as go
from AutoTrader.helper import logger
from AutoTrader.models import Position, Transaction
from AutoTrader.helper.date_helper import from_timestamp_to_date
from typing import Dict
from binance.client import Client
import os
from dotenv import load_dotenv
load_dotenv()
log = logger.get_logger(__name__)


class AccountBinance(Account):
    transaction_percentage = 0.1 / 100
    transaction_fee = 0
    client = Client(os.getenv('API_KEY'), os.getenv('API_SECRET'))

    def __init__(self):
        super().__init__()

    def place_order(self,
                    time: int,
                    symbol: str,
                    source_symbol: str,
                    destination_symbol: str,
                    price: float,
                    side: str,
                    source_symbol_total_amount: float = 0,
                    destination_symbol_amount: float = 0) -> None:

        if side == 'buy':
            # Subtract the total amount of source symbol spent
            self.balance[source_symbol] -= source_symbol_total_amount

            # Apply transaction fees (Orders are executed immediately as this is a 'test account')
            fees = source_symbol_total_amount * self.transaction_percentage + self.transaction_fee
            source_symbol_total_amount -= fees

            # Calculate the amount of destination_symbol that will be bought
            destination_symbol_amount = source_symbol_total_amount / price

            # Add the total amount of destination symbol bought
            self.balance[destination_symbol] += destination_symbol_amount

            log.info(
                f"{from_timestamp_to_date(time)} - Bought - {destination_symbol_amount} of {destination_symbol} for {source_symbol_total_amount} of {source_symbol} per token  - Fee - {fees}")

            self.positions[destination_symbol] = Position(
                Time=time,
                Symbol=destination_symbol,
                Amount=destination_symbol_amount,
                Price=price,
                SourceSymbol=source_symbol
            )

            log.info(f"New position {self.positions[destination_symbol]}")
            # Add transaction
            self.orders[symbol] = [] if symbol not in self.orders else self.orders[symbol]
            self.orders[symbol].append(Transaction(
                Time=time,
                Side='Buy',
                Quantity=destination_symbol_amount,
                Symbol=symbol,
                Type='LIMIT',
                Price=price
            ))

        if side == 'sell':
            # Sell only if position time is different from current time
            if self.positions[destination_symbol].Time == time:
                return

            # Set amount of destination symbol
            destination_symbol_amount = self.positions[destination_symbol].Amount

            # Subtract the total amount of destination symbol spent
            self.balance[destination_symbol] -= destination_symbol_amount

            # Apply transaction fees (Orders are executed immediately as this is a 'test account')
            fees = destination_symbol_amount * self.transaction_percentage + self.transaction_fee
            destination_symbol_amount -= fees

            # Amount of source symbol bought
            source_symbol_total_amount = destination_symbol_amount * price
            self.balance[source_symbol] += source_symbol_total_amount
            log.info(
                f"{from_timestamp_to_date(time)} - Sold - {destination_symbol_amount} of {destination_symbol} for {source_symbol_total_amount} of {source_symbol} per token  - Fee - {fees}")

            self.positions[destination_symbol] = Position()
            log.info(f"New balance: {self.balance[source_symbol]}")

            self.orders[symbol] = [] if symbol not in self.orders else self.orders[symbol]
            self.orders[symbol].append(Transaction(
                Time=time,
                Side='Sell',
                Quantity=destination_symbol_amount,
                Symbol=symbol,
                Type='LIMIT',
                Price=price
            ))
        print(self.balance)

    def get_plot(self, symbol: str) -> go:
        buys = [d for d in self.orders[symbol] if d.Side == "Buy"]
        sells = [d for d in self.orders[symbol] if d.Side == "Sell"]
        return go.Scatter(
            x=[d.Time for d in buys],
            y=[d.Price for d in buys],
            marker=dict(color="gold", size=13, symbol=46),
            mode="markers",
            name="Buy"
        ), go.Scatter(
            x=[d.Time for d in sells],
            y=[d.Price for d in sells],
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

    def _update_balance(self) -> None:
        self.balance = self._get_balance()

    @staticmethod
    def condition(name: str) -> bool:
        return name == "binanceAccount"
