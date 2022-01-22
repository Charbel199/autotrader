from abc import abstractmethod
from app.AutoTrader.exceptions import OrdersGeneratorException


class OrdersGenerator(object):
    def __init__(self):
        pass

    def get_orders(self, candlesticks) -> None:
        pass

    @staticmethod
    @abstractmethod
    def condition(name: str) -> bool:
        pass


# Get candlestick generator
def get_orders_generator(name: str) -> OrdersGenerator:
    for orders_generator in OrdersGenerator.__subclasses__():
        if orders_generator.condition(name):
            return orders_generator()
    raise OrdersGeneratorException(f"Orders generator: {name} not found")
