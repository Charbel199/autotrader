from dataclasses import dataclass
from AutoTrader.enums import *


@dataclass
class Order(object):
    """
    Trade
    """

    Time: int = 0
    Symbol: str = ''
    Side: OrderSide = OrderSide.BUY
    IsMaker: bool = False
    Price: float = 0
    Quantity: float = 0
    QuoteQuantity: float = 0
    CommissionSymbol: str = ''
    Commission: float = 0
    OrderId: str = ''

    def is_valid(self):
        return self.Time != 0
