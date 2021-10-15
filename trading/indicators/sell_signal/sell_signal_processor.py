import pandas as pd
from data.data_structures.structure import TickStructure
import sys
from helper import data_structure_helper
from data.data_logger import logger

log = logger.get_logger(__name__)


class SellSignal(object):
    columns = ['Time', 'SellSignal']
    data_structure: TickStructure

    def __init__(self, data_structure, sell_below_max_percentage):
        self.df = pd.DataFrame(columns=self.columns)
        self.data_structure = data_structure
        self.target = sys.maxsize
        self.max_price_reached_in_position = 0
        self.in_sell_zone = False
        self.sell_below_max_percentage = sell_below_max_percentage

    def process_new_tick(self):
        self.df = data_structure_helper.reduce_df(self.df)

        sell_signal = ''
        last_tick = self.data_structure.get_tick()
        if last_tick == {}:
            return
        last_tick_price = float(last_tick['Close'])

        # Check if reached sell zone
        if last_tick_price >= self.target:
            self.in_sell_zone = True

        if self.in_sell_zone:
            self.df.loc[len(self.df.index)] = {'Time': self.data_structure.get_last_time_tick()}
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

            self.df.loc[self.df.index[-1], 'SellSignal'] = sell_signal
            return sell_signal == 'Sell'

    def get_last_sell_signal_values(self, n=1):
        # Gets last SellSignal by default
        return self.df[['Time', 'SellSignal']].tail(n)

    def get_all_sell_signal_values(self):
        return self.df[['Time', 'SellSignal']]

    def delete_data(self):
        self.df = pd.DataFrame(columns=self.columns)

    def set_sell_target(self, price):
        self.target = price
        log.info(f"Target set to {price}")

    def reset_target(self):
        self.in_sell_zone = False
        self.target = sys.maxsize
        self.max_price_reached_in_position = 0

    def get_plot(self):
        coordinates = []
        coordinate = {}
        for index, row in self.df.iterrows():
            if row['SellSignal'] == "SellZone" and coordinate == {}:
                coordinate["x0"] = row['Time']
            elif row['SellSignal'] == "Sell":
                if "x0" in coordinate:
                    coordinate["x1"] = row['Time']
                    coordinates.append(coordinate)
                    coordinate = {}
        return coordinates
