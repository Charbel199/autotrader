from enum import Enum


class Side(Enum):
    BUY = 1
    SELL = 2


class OrderType(Enum):
    LIMIT = 1
    MARKET = 2


class Status(Enum):
    FILLED = 1
    OPEN = 2
    CANCELED = 3
