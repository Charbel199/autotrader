import sys

from AutoTrader.trading.accounts.account import Account
from AutoTrader.helper import logger
from AutoTrader.models import Order, Trade, Position
from AutoTrader.enums import OrderType, OrderSide, OrderStatus
from AutoTrader.helper.date_helper import from_timestamp_to_date
from typing import Dict
import random

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

        if order_type == OrderType.MARKET:
            self._market_order(
                symbol=symbol,
                source_symbol=source_symbol,
                destination_symbol=destination_symbol,
                order_type=order_type,
                price=price,
                quantity=amount,
                time=time,
                side=side
            )

    def _market_order(self,
                      symbol: str,
                      source_symbol: str,
                      destination_symbol: str,
                      quantity: float,
                      price: float,
                      time: int,
                      order_type: OrderType,
                      side: OrderSide):
        # Launch order
        quote_order_quantity, fees = self._order_logic(source_symbol=source_symbol,
                                                       destination_symbol=destination_symbol,
                                                       quantity=quantity,
                                                       price=price,
                                                       side=side)
        log.info(
            f"{from_timestamp_to_date(time)} -  Market {str(side)} Order - {quantity} of {destination_symbol} for {price}, with a fee of {fees} {destination_symbol}")

        # Record order
        order = Order(
            Time=time,
            Side=side,
            OriginalQuantity=quantity,
            ExecutedQuantity=quantity,
            Symbol=symbol,
            Type=order_type,
            AveragePrice=price,
            Price=price,
            Status=OrderStatus.FILLED,
            CumulativeQuoteQuantity=quote_order_quantity,
            OrderId=str(random.randint(0, sys.maxsize))
        )
        self.add_order(symbol=symbol,
                       order=order)
        # Record trade
        trade = Trade(
            Time=time,
            Symbol=symbol,
            Side=side,
            IsMaker=False,
            Price=price,
            Quantity=quantity,
            QuoteQuantity=quote_order_quantity,
            CommissionSymbol=destination_symbol if side == OrderSide.BUY else source_symbol,
            Commission=fees,
            TradeId=str(random.randint(0, sys.maxsize))
        )
        self.add_trade(symbol=symbol,
                       trade=trade)
        # Update position
        self.set_position(symbol, Position(
            Time=trade.Time,
            AveragePrice=trade.Price,
            Symbol=symbol,
            Quantity=trade.Quantity - trade.Commission
        )) if side == OrderSide.BUY else self.reset_position(symbol)

    def _order_logic(self,
                     source_symbol: str,
                     destination_symbol: str,
                     quantity: float,
                     price: float,
                     side: OrderSide) -> [float, float]:
        if side == OrderSide.BUY:
            # Launch order
            # Subtract the total amount of source symbol spent
            quote_order_quantity = quantity * price
            self.remove_from_balance(source_symbol, quote_order_quantity)
            # Apply transaction fees (Orders are executed immediately as this is a 'test account')
            fees = quantity * self.transaction_percentage + self.transaction_fee
            # Adjusted amount after fees
            quantity_after_fees = quantity - fees
            # Add the total quantity_after_fees of destination symbol bought
            self.add_to_balance(destination_symbol, quantity_after_fees)
            return quote_order_quantity, fees
        elif side == OrderSide.SELL:
            # Launch order
            # Subtract the total amount of destination symbol spent
            self.remove_from_balance(destination_symbol, quantity)
            # Amount of source symbol bought
            quote_order_quantity = quantity * price
            # Apply transaction fees (Orders are executed immediately as this is a 'test account')
            fees = quote_order_quantity * self.transaction_percentage + self.transaction_fee
            # Actual amount that will be held after fees
            quote_order_quantity_after_fees = quote_order_quantity - fees
            self.add_to_balance(source_symbol, quote_order_quantity_after_fees)
            return quote_order_quantity, fees

    def get_current_balance(self) -> Dict[str, float]:
        return self.balance

    def _get_account_initial_balance(self) -> Dict[str, float]:
        return self.account_balance

    @staticmethod
    def condition(name: str) -> bool:
        return name == "testAccount"
