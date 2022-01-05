from AutoTrader.trading.strategies.strategy import Strategy
from AutoTrader.trading.indicators.rsi_indicator import RSI
from AutoTrader.trading.indicators.candlestick_type import CandlestickType
from AutoTrader.trading.indicators.sell_signal import SellSignal
from AutoTrader.trading.indicators.vwap_indicator import VWAP
from AutoTrader.trading.indicators.bollinger_band_indicator import BollingerBand
from AutoTrader.trading.indicators.ichimoku_indicator import Ichimoku
from AutoTrader.trading.indicators.chaikin_money_flow_indicator import ChaikinMoneyFlow
from plotly.subplots import make_subplots
from AutoTrader.helper import logger
from AutoTrader.data.data_structures.structure import TickStructure
from AutoTrader.trading.accounts.account import Account
from plotly.graph_objs import Figure
import numpy as np
log = logger.get_logger(__name__)


class QuickStrategy(Strategy):
    def __init__(self,
                 data_structure: TickStructure,
                 account: Account,
                 symbol: str):
        super().__init__(data_structure, account, symbol)
        # self.ADX = ADX(data_structure)
        self.CandlestickType = CandlestickType(data_structure)
        self.RSI = RSI(data_structure)
        self.VWAP = VWAP(data_structure)
        self.Ichimoku = Ichimoku(data_structure)
        self.BollingerBand = BollingerBand(data_structure)
        self.ChaikinMoneyFlow = ChaikinMoneyFlow(data_structure)
        self.SellSignal = SellSignal(data_structure, sell_below_max_percentage=0.997)
        self.firstStep = False
        self.secondStep = False
        self.thirdStep = False

        self.start_counter = False
        self.counter = 0

    def process_new_candlestick(self) -> None:
        # self.data_structure.reduce()

        # print('Got new candlestick')
        # self.ADX.process_new_candlestick()
        # self.CandlestickType.process_new_candlestick()
        self.RSI.process_new_candlestick()
        # self.BollingerBand.process_new_candlestick()
        self.VWAP.process_new_candlestick()
        self.Ichimoku.process_new_candlestick()

        # print(self.Ichimoku.get_last_values())
        # self.ChaikinMoneyFlow.process_new_candlestick()

        if self.transactions_allowed and not self.account.get_position().is_valid() and self.data_structure.get_number_of_rows() > 330:

            if self.VWAP.get_last_values()[-1]['VWAP'] < self.data_structure.get_last_candlestick().Close \
                    and self.RSI.get_all_values()[-2]['RSI'] < 30 \
                    and self.RSI.get_last_values()[-1]['RSI'] > 40 \
                    and (self.data_structure.get_last_candlestick().Close - self.VWAP.get_last_values()[-1]['VWAP']) / self.data_structure.get_last_candlestick().Close <= 0.01:
                last_vwaps = np.array([d['VWAP'] for d in self.VWAP.get_last_values()[-14:]])
                last_closes = np.array([c.Close for c in self.data_structure.get_last_candlesticks(14)])
                if (last_closes>last_vwaps).all():
                    self.account.buy(self.data_structure.get_tick().Time, self.symbol, self.data_structure.get_tick_close())
                    self.SellSignal.set_sell_target(self.data_structure.get_tick_close() * 1.015)


    def process_new_tick(self) -> None:
        # print('Got new tick in strat ', self.data_structure.get_tick())
        if self.transactions_allowed:
            if self.account.get_position().is_valid():
                # Sell logic
                if self.SellSignal.process_new_tick():
                    self.number_of_trades += 1
                    self.account.sell(self.data_structure.get_tick().Time, self.symbol, self.data_structure.get_tick_close())
                # Stop loss
                elif float(self.account.get_position().Price) * 0.98 >= self.data_structure.get_tick_close():
                    self.number_of_trades += 1
                    self.number_of_stop_losses += 1
                    log.warning(f"Hit stoploss of {float(self.account.get_position().Price) * 0.98}  at {self.data_structure.get_tick_close()}")
                    self.account.sell(self.data_structure.get_tick().Time, self.symbol, self.data_structure.get_tick_close())

    def get_figure(self) -> Figure:
        fig = make_subplots(rows=3, cols=1)
        fig.append_trace(self.data_structure.get_plot(), row=1, col=1)
        # fig.append_trace(self.VWAP.get_plot(), row=1, col=1)
        # fig.append_trace(self.ChaikinMoneyFlow.get_plot(), row=3, col=1)
        # fig.append_trace(self.BollingerBand.get_plot()[0], row=1, col=1)
        # fig.append_trace(self.BollingerBand.get_plot()[1], row=1, col=1)
        # fig.append_trace(self.BollingerBand.get_plot()[2], row=1, col=1)

        fig.append_trace(self.Ichimoku.get_plot()[0], row=1, col=1)
        fig.append_trace(self.Ichimoku.get_plot()[1], row=1, col=1)
        fig.append_trace(self.Ichimoku.get_plot()[2], row=1, col=1)
        fig.append_trace(self.Ichimoku.get_plot()[3], row=1, col=1)
        fig.append_trace(self.Ichimoku.get_plot()[4], row=1, col=1)


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

        fig.update_layout(height=1600, width=1800, xaxis_rangeslider_visible=False)
        fig.update_xaxes(matches='x')
        return fig

    @staticmethod
    def condition(name: str) -> bool:
        return name == 'quickStrategy'
