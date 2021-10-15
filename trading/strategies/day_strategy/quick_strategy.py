from trading.strategies.strategy import Strategy
from trading.indicators.adx_indicator.adx_indicator_processor import ADX
from trading.indicators.candlestick_type.candlestick_type_processor import CandlestickType
from trading.indicators.rsi_indicator.rsi_indicator_processor import RSI
from trading.indicators.sell_signal.sell_signal_processor import SellSignal
from trading.indicators.bollinger_band_indicator.bollinger_band_indicator_proccessor import BollingerBand
from trading.indicators.chaikin_money_flow_indicator.chaikin_money_flow_indicator_processor import ChaikinMoneyFlow
from plotly.subplots import make_subplots
from data.data_logger import logger

log = logger.get_logger(__name__)


class QuickStrategy(Strategy):
    def __init__(self, data_structure, account, symbol):
        super().__init__(data_structure, account, symbol)
        self.ADX = ADX(data_structure)
        self.CandlestickType = CandlestickType(data_structure)
        self.RSI = RSI(data_structure)
        self.BollingerBand = BollingerBand(data_structure)
        self.ChaikinMoneyFlow = ChaikinMoneyFlow(data_structure)
        self.SellSignal = SellSignal(data_structure, sell_below_max_percentage=0.997)

    def process_new_candlestick(self):
        # Process ADX
        self.ADX.process_new_candlestick()
        self.CandlestickType.process_new_candlestick()
        self.RSI.process_new_candlestick()
        self.BollingerBand.process_new_candlestick()
        self.ChaikinMoneyFlow.process_new_candlestick()

        # if self.transactions_allowed:
        #     if self.RSI.get_all_rsi_values()['RSI'].iloc[-1] < 20 and self.account.get_position() == {}:
        #         self.account.buy(self.ADX.get_last_adx_values()['Time'].iloc[-1], self.symbol, 10, self.data_structure.get_tick_close())
        #         self.SellSignal.set_sell_target(self.data_structure.get_tick_close() * 1.01)

        if self.transactions_allowed and self.account.get_position() == {} and self.data_structure.get_number_of_rows() > 30:
            # Step 1: Price needs to break the middle line of the bollinger band
            if self.data_structure.get_before_last_value('Open') < self.BollingerBand.get_last_bollinger_bands_values(2)['UpperBollingerBand'].tolist()[-2] < self.data_structure.get_before_last_value('Close')\
                    and self.data_structure.get_last_value('Close') > self.BollingerBand.get_last_bollinger_bands_values()['UpperBollingerBand'].tolist()[-1]:
                # Step 2: RSI above 50
                if self.RSI.get_last_rsi_values()['RSI'].tolist()[-1] > 50:
                    # Step 3: CMF Breaks above 0
                    if self.ChaikinMoneyFlow.get_all_cmf_values()['ChaikinMoneyFlow'].tolist()[-1] > 0:
                        self.account.buy(self.ADX.get_last_adx_values()['Time'].iloc[-1], self.symbol, 10, self.data_structure.get_tick_close())

                        self.SellSignal.set_sell_target(self.data_structure.get_tick_close() * 1.015)

    def process_new_tick(self):
        # print('Got new tick in strat ', self.data_structure.get_tick())
        if self.transactions_allowed:
            if self.account.get_position() != {}:
                # Sell logic
                if self.SellSignal.process_new_tick():
                    self.account.sell(self.ADX.get_last_adx_values()['Time'].iloc[-1], self.symbol, 10, self.data_structure.get_tick_close())
                # Stop loss
                elif float(self.account.get_position()['Price']) * 0.98 >= self.data_structure.get_tick_close():
                    log.warn(f"Hit stoploss of {float(self.account.get_position()['Price']) * 0.98}  at {self.data_structure.get_tick_close()}")
                    self.account.sell(self.ADX.get_last_adx_values()['Time'].iloc[-1], self.symbol, 10, self.data_structure.get_tick_close())

    def get_figure(self):
        fig = make_subplots(rows=2, cols=1)
        fig.append_trace(self.data_structure.get_plot(), row=1, col=1)
        # fig.append_trace(self.ChaikinMoneyFlow.get_plot(), row=4, col=1)
        fig.append_trace(self.BollingerBand.get_plot()[0], row=1, col=1)
        fig.append_trace(self.BollingerBand.get_plot()[1], row=1, col=1)
        fig.append_trace(self.BollingerBand.get_plot()[2], row=1, col=1)
        buy_plot, sell_plot = self.account.get_plot()
        fig.append_trace(buy_plot, row=1, col=1)
        fig.append_trace(sell_plot, row=1, col=1)
        # fig.append_trace(self.ADX.get_plot(), row=2, col=1)
        fig.append_trace(self.RSI.get_plot(), row=2, col=1)
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
