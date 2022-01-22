from dataclasses import dataclass


@dataclass
class Tick(object):
    """
    Candlestick/Tick data
    """

    Time: int = 0
    Open: float = 0
    Close: float = 0
    High: float = 0
    Low: float = 0
    Volume: float = 0
    OpenTime: int = 0
    CloseTime: int = 0

    def is_valid(self):
        return self.Time != 0
