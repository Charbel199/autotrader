from AutoTrader.data.data_structures.structure import TickStructure
import plotly.graph_objects as go
from AutoTrader.trading.indicators.inidicator import Indicator


class FibonacciRetracement(Indicator):
    # columns = ['Time', 'RecentHigh', 'RecentLow', percentages ...]
    period = 1000
    percentages = [0, 0.236, 0.382, 0.5, 0.618, 1]
    data_structure: TickStructure

    counter = 0

    def __init__(self, data_structure: TickStructure):
        super().__init__(data_structure)

    def process_new_candlestick(self) -> None:
        # Create new row
        self.list.append({'Time': self.data_structure.get_last_time()})
        number_of_rows = self.data_structure.get_number_of_rows()

        if number_of_rows >= self.period:
            if True:
                self.list[-1]['RecentHigh'] = max(
                    [c.High for c in self.data_structure.get_last_candlesticks(self.period)])
                self.list[-1]['RecentLow'] = min(
                    [c.Low for c in self.data_structure.get_last_candlesticks(self.period)])
            # else:
            #     if self.data_structure.get_last_candlestick().Close > self.list[-2]['RecentHigh']:
            #         self.list[-1]['RecentHigh'] = self.data_structure.get_last_candlestick().Close
            #     else:
            #         self.list[-1]['RecentHigh'] = self.list[-2]['RecentHigh']
            #
            #     if self.data_structure.get_last_candlestick().Close < self.list[-2]['RecentLow']:
            #         self.list[-1]['RecentLow'] = self.data_structure.get_last_candlestick().Close
            #     else:
            #         self.list[-1]['RecentLow'] = self.list[-2]['RecentLow']

            # TODO: Add logic for downtrend

            self.counter += 1

            high = self.list[-1]['RecentHigh']
            low = self.list[-1]['RecentLow']
            difference = high - low

            for percentage in self.percentages:
                self.list[-1][str(round(percentage, 3))] = high - difference * percentage

    def process_new_tick(self):
        pass

    def get_plot(self):
        plot_list = []
        for percentage in self.percentages:
            percentage_text = str(round(percentage, 3))
            plot_list.append(go.Scatter(x=[d['Time'] for d in self.list],
                          y=[d[percentage_text] if percentage_text in d else None for d in self.list],
                          name=percentage_text))
        return plot_list

    def delete_data(self) -> None:
        self.list = []
        self.counter = 0
