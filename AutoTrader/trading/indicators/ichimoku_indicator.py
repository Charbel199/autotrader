from AutoTrader.data.data_structures.structure import TickStructure
import plotly.graph_objects as go
from AutoTrader.trading.indicators.inidicator import Indicator


class Ichimoku(Indicator):
    # columns = ['Time', 'HighestHigh1', 'LowestLow1', 'TenkanSen', 'HighestHigh2', 'LowestLow2', 'KijunSen', 'ChikouSpan', 'SenkouSpanA', 'HighestHigh3', 'LowestLow3', 'SenkouSpanB']
    period_1 = 9
    period_2 = 26
    period_3 = 52
    shift_period1 = 26
    shift_period2 = 26
    data_structure: TickStructure

    def __init__(self, data_structure: TickStructure):
        super().__init__(data_structure)

    def process_new_candlestick(self) -> None:
        # Create new row
        self.list.append({'Time': self.data_structure.get_last_time()})
        last_candlestick = self.data_structure.get_last_candlestick()

        if self.data_structure.get_number_of_rows() >= self.period_1:
            # Calculate highest high and lowest low
            self.list[-1]['HighestHigh1'] = max(
                [c.Close for c in self.data_structure.get_last_candlesticks(self.period_1)])
            self.list[-1]['LowestLow1'] = min(
                [c.Close for c in self.data_structure.get_last_candlesticks(self.period_1)])

            # Calculate TekanSen
            self.list[-1]['TenkanSen'] = (self.list[-1]['HighestHigh1'] + self.list[-1]['LowestLow1']) / 2
        if self.data_structure.get_number_of_rows() >= self.period_2:
            # Calculate highest high and lowest low
            self.list[-1]['HighestHigh2'] = max(
                [c.Close for c in self.data_structure.get_last_candlesticks(self.period_2)])
            self.list[-1]['LowestLow2'] = min(
                [c.Close for c in self.data_structure.get_last_candlesticks(self.period_2)])

            # Calculate KijunSen
            self.list[-1]['KijunSen'] = (self.list[-1]['HighestHigh2'] + self.list[-1]['LowestLow2']) / 2

            # Calculate ChikouSpan
            if len(self.list) >= self.period_2:
                self.list[-self.period_2]['ChikouSpan'] = self.data_structure.get_last_candlestick().Close

        if self.data_structure.get_number_of_rows() >= self.period_2 + self.shift_period1:
            # Calculate SenkouSpanA
            self.list[-1]['SenkouSpanA'] = (self.list[-self.shift_period1]['TenkanSen'] + self.list[-self.shift_period1][
                'KijunSen']) / 2

        if self.data_structure.get_number_of_rows() >= self.period_3:
            # Calculate highest high and lowest low
            self.list[-1]['HighestHigh3'] = max(
                [c.Close for c in self.data_structure.get_last_candlesticks(self.period_3)])
            self.list[-1]['LowestLow3'] = min(
                [c.Close for c in self.data_structure.get_last_candlesticks(self.period_3)])

        if self.data_structure.get_number_of_rows() >= self.period_3 + self.shift_period2:
            # Calculate SenkouSpanB
            self.list[-1]['SenkouSpanB'] = (self.list[-self.shift_period2]['HighestHigh3'] + self.list[-self.shift_period2][
                'LowestLow3']) / 2

    def process_new_tick(self):
        pass

    def get_plot(self):
        return go.Scatter(x=[d['Time'] for d in self.list],
                          y=[d['TenkanSen'] if 'TenkanSen' in d else None for d in self.list],
                          name="TenkanSen"), \
               go.Scatter(x=[d['Time'] for d in self.list],
                          y=[d['KijunSen'] if 'KijunSen' in d else None for d in self.list],
                          name="KijunSen"), \
               go.Scatter(x=[d['Time'] for d in self.list],
                          y=[d['ChikouSpan'] if 'ChikouSpan' in d else None for d in self.list],
                          name="ChikouSpan"), \
               go.Scatter(x=[d['Time'] for d in self.list],
                          y=[d['SenkouSpanA'] if 'SenkouSpanA' in d else None for d in self.list],
                          name="SenkouSpanA"), \
               go.Scatter(x=[d['Time'] for d in self.list],
                          y=[d['SenkouSpanB'] if 'SenkouSpanB' in d else None for d in self.list],
                          name="SenkouSpanB",fill='tonexty')

    def delete_data(self) -> None:
        self.list = []
