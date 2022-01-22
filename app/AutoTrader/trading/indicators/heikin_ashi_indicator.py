from app.AutoTrader.data.data_structures.candlesticks import Candlesticks
import plotly.graph_objects as go
from app.AutoTrader.trading.indicators.inidicator import Indicator
from typing import List


class HeikinAshi(Indicator):
    # columns = ['Time', 'Close', 'Open', 'High', 'Low']
    candlesticks: Candlesticks

    def __init__(self, candlesticks: Candlesticks):
        super().__init__(candlesticks)

    def process_new_candlestick(self) -> None:
        # Create new row
        self.list.append({'Time': self.candlesticks.get_last_time()})
        number_of_rows = self.candlesticks.get_number_of_rows()

        if number_of_rows >= 2:
            last_candlestick = self.candlesticks.get_last_candlestick()
            before_last_candlestick = self.candlesticks.get_specific_candlestick(n=-2)
            self.list[-1]['Close'] = 0.25 * (last_candlestick.Close + last_candlestick.High + last_candlestick.Low + last_candlestick.Open)
            self.list[-1]['Open'] = 0.5 * (before_last_candlestick.Open + before_last_candlestick.Close)
            self.list[-1]['High'] = max(last_candlestick.High, self.list[-1]['Close'], self.list[-1]['Open'])
            self.list[-1]['Low'] = min(last_candlestick.Low, self.list[-1]['Close'], self.list[-1]['Open'])

    def process_new_tick(self) -> None:
        pass

    def get_plot(self) -> List:
        return [go.Candlestick(x=[d["Time"] for d in self.list],
                               open=[d["Open"] if 'Open' in d else None for d in self.list],
                               high=[d["High"] if 'High' in d else None for d in self.list],
                               low=[d["Low"] if 'Low' in d else None for d in self.list],
                               close=[d["Close"] if 'Close' in d else None for d in self.list],
                               name="HeikinAshiCandlesticks")]

    def delete_data(self) -> None:
        self.list = []
