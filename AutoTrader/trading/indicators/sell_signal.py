from AutoTrader.data.data_structures.structure import TickStructure
import sys
from AutoTrader.helper import logger
from AutoTrader.trading.indicators.inidicator import Indicator

log = logger.get_logger(__name__)


class SellSignal(Indicator):
    # columns = ['Time', 'SellSignal']
    data_structure: TickStructure

    def __init__(self, data_structure: TickStructure, sell_below_max_percentage: float):
        super().__init__(data_structure)
        self.target = sys.maxsize
        self.max_price_reached_in_position = 0
        self.in_sell_zone = False
        self.sell_below_max_percentage = sell_below_max_percentage

    def process_new_candlestick(self) -> None:
        pass

    def process_new_tick(self):
        sell_signal = ''
        last_tick = self.data_structure.get_tick()
        if last_tick == {}:
            return
        last_tick_price = last_tick['Close']

        # Check if reached sell zone
        if last_tick_price >= self.target:
            self.in_sell_zone = True

        if self.in_sell_zone:
            self.list.append({'Time': self.data_structure.get_last_time()})
            # Set max price reached
            if last_tick_price > self.max_price_reached_in_position:
                sell_signal = 'SellZone'
                log.info(f"Sell zone at {last_tick_price}")
                self.max_price_reached_in_position = last_tick_price

            if last_tick_price < (self.max_price_reached_in_position * self.sell_below_max_percentage):
                # Sell
                sell_signal = 'Sell'
                log.info(f"Sell at {last_tick_price} last max was {self.max_price_reached_in_position}")
                # Reset target and max
                self.reset_target()

            self.list[-1]['SellSignal'] = sell_signal
            return sell_signal == 'Sell'

    def set_sell_target(self, price: float) -> None:
        self.target = price
        log.info(f"Target set to {price}")

    def reset_target(self) -> None:
        self.in_sell_zone = False
        self.target = sys.maxsize
        self.max_price_reached_in_position = 0

    def get_plot(self):
        coordinates = []
        coordinate = {}
        for row in self.list:
            if row['SellSignal'] == "SellZone" and coordinate == {}:
                coordinate["x0"] = row['Time']
            elif row['SellSignal'] == "Sell":
                if "x0" in coordinate:
                    coordinate["x1"] = row['Time']
                    coordinates.append(coordinate)
                    coordinate = {}
        return coordinates

    def delete_data(self) -> None:
        self.list = []
        self.target = sys.maxsize
        self.max_price_reached_in_position = 0
        self.in_sell_zone = False
