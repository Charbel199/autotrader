from dataclasses import dataclass

@dataclass
class Transaction(object):
    """
    Transaction
    """

    Time: int = 0
    Symbol: str = ''
    Quantity: float = 0
    Price: float = 0
    Type: str = ''
    Side: str = ''

    def is_valid(self):
        return self.Time != 0