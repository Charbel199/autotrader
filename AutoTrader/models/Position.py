from dataclasses import dataclass


@dataclass
class Position(object):
    """
    Trade position
    """

    Time: int = 0
    Symbol: str = ''
    Amount: float = 0
    Price: float = 0

    def is_valid(self):
        return self.Time != 0
