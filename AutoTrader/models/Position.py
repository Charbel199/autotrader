from dataclasses import dataclass


@dataclass
class Position(object):
    """
    Trade position
    """

    Time: int = 0
    Symbol: str = ''
    AveragePrice: float = 0
    Quantity: float = 0

    def is_valid(self):
        return self.Time != 0
