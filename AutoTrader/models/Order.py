from dataclasses import dataclass
from AutoTrader.enums import *


@dataclass
class Order(object):
    """
    Order
    """

    Time: int = 0
    Symbol: str = ''
    Side: Side = Side.BUY
    Type: OrderType = OrderType.LIMIT
    Price: float = 0
    OriginalQuantity: float = 0
    ExecutedQuantity: float = 0
    Total: float = 0
    Status: Status = Status.OPEN
    OrderId: str = ''

    def is_valid(self):
        return self.Time != 0
