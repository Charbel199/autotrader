from dataclasses import dataclass


@dataclass
class Tick(object):
    """
    Candlestick/Tick data
    """

    Time: int
    Open: float
    Close: float
    High: float
    Low: float
    Volume: float
    OpenTime: int
    CloseTime: int


@dataclass
class Position(object):
    """
    Trade position
    """

    Time: int
    Symbol: str
    Amount: float
    Price: float
