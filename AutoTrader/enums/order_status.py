from enum import Enum


class OrderStatus(Enum):
    FILLED = 1
    OPEN = 2
    CANCELED = 3

    def __str__(self):
        return f"{self.name.lower()}"
