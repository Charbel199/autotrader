from trading.strategies.strategy import Strategy
from trading.indicators.adx_indicator.adx_indicator_processor import ADX
from trading.indicators.candlestick_type.candlestick_type_processor import CandlestickType
from trading.indicators.rsi_indicator.rsi_indicator_processor import RSI
from trading.indicators.sell_signal.sell_signal_processor import SellSignal
from plotly.subplots import make_subplots


class QuickStrategy(Strategy):
    def __init__(self, data_structure, account, symbol):
        super().__init__(data_structure, account, symbol)
        self.ADX = ADX(data_structure)
        self.CandlestickType = CandlestickType(data_structure)
        self.RSI = RSI(data_structure)
        self.SellSignal = SellSignal(data_structure, sell_below_max_percentage=0.995)

    def process_new_candlestick(self):
        # Process ADX
        self.ADX.process_new_candlestick()
        self.CandlestickType.process_new_candlestick()
        self.RSI.process_new_candlestick()
        # print(self.RSI.get_last_rsi_values())
        # print(self.CandlestickType.get_last_candlestick_type_values())
        # print(self.ADX.get_last_adx_values())
        # print('Got a new candlestick strat ', self.data_structure.get_data())
        if self.transactions_allowed:
            if self.RSI.get_all_rsi_values()['RSI'].iloc[-1] < 20 and self.account.get_position() == {}:
                self.SellSignal.set_sell_target(self.data_structure.get_tick_close() * 1.01)
                self.account.buy(self.ADX.get_last_adx_values()['Time'].iloc[-1], self.symbol, 10, self.data_structure.get_tick_close())

    def process_new_tick(self):
        # print('Got new tick in strat ', self.data_structure.get_tick())
        if self.transactions_allowed:
            if self.account.get_position() != {}:
                if self.SellSignal.process_new_tick():
                    self.account.sell(self.ADX.get_last_adx_values()['Time'].iloc[-1], self.symbol, 10, self.data_structure.get_tick_close())
                elif float(self.account.get_position()['Price']) * 0.98 >= self.data_structure.get_tick_close():
                    print("Hit stoploss of", float(self.account.get_position()['Price']) * 0.98, ", at ", self.data_structure.get_tick_close())
                    self.account.sell(self.ADX.get_last_adx_values()['Time'].iloc[-1], self.symbol, 10, self.data_structure.get_tick_close())

    def get_figure(self):
        fig = make_subplots(rows=3, cols=1)
        fig.append_trace(self.data_structure.get_plot(), row=1, col=1)
        buy_plot, sell_plot = self.account.get_plot()
        fig.append_trace(buy_plot, row=1, col=1)
        fig.append_trace(sell_plot, row=1, col=1)
        fig.append_trace(self.ADX.get_plot(), row=2, col=1)
        fig.append_trace(self.RSI.get_plot(), row=3, col=1)
        coordinates = self.SellSignal.get_plot()
        for coordinate in coordinates:
            fig.add_vrect(
                x0=coordinate["x0"], x1=coordinate["x1"],
                fillcolor="LightSalmon", opacity=0.5,
                layer="below", line_width=0, row=1, col=1
            )

        fig.update_layout(xaxis_rangeslider_visible=False)
        fig.update_xaxes(matches='x')
        return fig

    @staticmethod
    def condition(name):
        return name == 'quickStrategy'
