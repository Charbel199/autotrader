from AutoTrader.data.data_structures.candlesticks import Candlesticks
import sys
from AutoTrader.helper import logger
from AutoTrader.trading.indicators.inidicator import Indicator
from typing import List

log = logger.get_logger(__name__)


class SellSignal(Indicator):
    # columns = ['Time', 'SellSignal']
    candlesticks: Candlesticks

    def __init__(self, candlesticks: Candlesticks, **kwargs):
        super().__init__(candlesticks)
        self.target = sys.maxsize
        self.max_price_reached_in_position = 0
        self.in_sell_zone = False
        self.sell_below_max_percentage = kwargs.get('sell_below_max_percentage', 1)

    def process_new_candlestick(self) -> None:
        pass

    def process_new_tick(self) -> None:
        # Create new row
        self.list.append({'Time': self.candlesticks.get_last_time_tick()})

        sell_signal = ''
        last_tick = self.candlesticks.get_tick()
        if last_tick == {}:
            self.list[-1]['SellSignal'] = sell_signal
            return
        last_tick_price = last_tick.Close

        # Check if reached sell zone
        if last_tick_price >= self.target:
            self.in_sell_zone = True

        if self.in_sell_zone:
            sell_signal = 'SellZone'
            # Set max price reached
            if last_tick_price > self.max_price_reached_in_position:
                log.info(f"New Sell zone at {last_tick_price}")
                self.max_price_reached_in_position = last_tick_price

            if last_tick_price <= (self.max_price_reached_in_position * self.sell_below_max_percentage):
                # Sell
                sell_signal = 'Sell'
                log.info(f"Sell at {last_tick_price} last max was {self.max_price_reached_in_position}")
                # Reset target and max
                self._reset_target()

        self.list[-1]['SellSignal'] = sell_signal

    def set_sell_target(self, price: float) -> None:
        self.target = price
        log.info(f"Target set to {price}")

    def _reset_target(self) -> None:
        self.in_sell_zone = False
        self.target = sys.maxsize
        self.max_price_reached_in_position = 0

    def get_plot(self) -> List:
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
