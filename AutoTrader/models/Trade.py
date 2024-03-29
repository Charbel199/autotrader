from dataclasses import dataclass
from AutoTrader.enums import OrderSide

@dataclass
class Trade(object):
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
    TradeId: str = ''

    def is_valid(self):
        return self.Time != 0
