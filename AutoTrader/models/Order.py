from dataclasses import dataclass
from AutoTrader.enums import OrderSide, OrderType, OrderStatus

@dataclass
class Order(object):
    """
    Order
    """

    Time: int = 0
    Symbol: str = ''
    Side: OrderSide = OrderSide.BUY
    Type: OrderType = OrderType.LIMIT
    Price: float = 0
    AveragePrice: float = 0
    OriginalQuantity: float = 0
    ExecutedQuantity: float = 0
    CumulativeQuoteQuantity: float = 0
    Status: OrderStatus = OrderStatus.OPEN
    OrderId: str = ''

    def is_valid(self):
        return self.Time != 0
