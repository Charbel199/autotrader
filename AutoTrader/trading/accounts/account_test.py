from AutoTrader.trading.accounts.account import Account
from AutoTrader.helper import logger
from AutoTrader.models import  Order
from AutoTrader.enums import OrderType, OrderSide
from AutoTrader.helper.date_helper import from_timestamp_to_date
from typing import Dict

log = logger.get_logger(__name__)


class AccountTest(Account):
    transaction_percentage = 0.1 / 100
    transaction_fee = 0
    account_balance = {
        'USDT': 100,
        'ADA': 0,
        'BUSD': 200,
        'XRP': 0,
        'BTC': 0
    }

    def __init__(self):
        super().__init__()

    def place_order(self,
                    time: int,
                    symbol: str,
                    source_symbol: str,
                    destination_symbol: str,
                    order_type: OrderType,
                    price: float,
                    side: OrderSide,
                    amount: float) -> None:

        if side == OrderSide.BUY:
            # Subtract the total amount of source symbol spent
            source_symbol_total_amount = amount * price
            self.remove_from_balance(source_symbol, source_symbol_total_amount)

            # Apply transaction fees (Orders are executed immediately as this is a 'test account')
            fees = source_symbol_total_amount * self.transaction_percentage + self.transaction_fee
            # Adjusted amount after fees
            amount = (source_symbol_total_amount - fees) / price

            # Add the total amount of destination symbol bought
            self.add_to_balance(destination_symbol, amount)

            log.info(
                f"{from_timestamp_to_date(time)} - Buy Order - {amount} of {destination_symbol} for {source_symbol_total_amount} of {source_symbol}, {price} per token  - Fee - {fees}")
            # Add transaction
            self.add_order(symbol=symbol,
                           order=Order(
                               Time=time,
                               Side=side,
                               OriginalQuantity=amount,
                               ExecutedQuantity=amount,
                               Symbol=symbol,
                               Type=order_type,
                               Price=price
                           ))
            self.set_position(symbol=symbol, order=self.orders[symbol][-1])
            log.info(f"New position {self.positions[symbol]}")

        if side == OrderSide.SELL:
            # Subtract the total amount of destination symbol spent
            self.remove_from_balance(destination_symbol, amount)

            # Apply transaction fees (Orders are executed immediately as this is a 'test account')
            fees = amount * self.transaction_percentage + self.transaction_fee
            # Actual amount that will be sold
            amount -= fees

            # Amount of source symbol bought
            source_symbol_total_amount = amount * price

            self.add_to_balance(source_symbol, source_symbol_total_amount)

            log.info(
                f"{from_timestamp_to_date(time)} - Sell Order - {amount} of {destination_symbol} for {source_symbol_total_amount} of {source_symbol}, {price} per token  - Fee - {fees}")

            self.add_order(symbol=symbol,
                           order=Order(
                               Time=time,
                               Side=side,
                               OriginalQuantity=amount,
                               ExecutedQuantity=amount,
                               Symbol=symbol,
                               Type=order_type,
                               Price=price
                           ))

            self.reset_position(symbol)
            log.info(f"New balance: {self.get_symbol_balance(source_symbol)}")

    def get_current_balance(self) -> Dict[str, float]:
        return self.balance

    def _get_account_initial_balance(self) -> Dict[str, float]:
        return self.account_balance

    @staticmethod
    def condition(name: str) -> bool:
        return name == "testAccount"
