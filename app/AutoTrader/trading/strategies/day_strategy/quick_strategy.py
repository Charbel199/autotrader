from app.AutoTrader.trading.strategies.strategy import Strategy
from app.AutoTrader.trading.indicators import RSI, CandlestickType, VWAP, Ichimoku, BollingerBand, \
    ChaikinMoneyFlow, MACD, ATR, FibonacciRetracement, SellSignal, HeikinAshi, SuperTrend

from plotly.subplots import make_subplots
from app.AutoTrader.helper import logger
from app.AutoTrader.data.data_structures.candlesticks import Candlesticks
from app.AutoTrader.trading.accounts.account import Account
from plotly.graph_objs import Figure

log = logger.get_logger(__name__)


class QuickStrategy(Strategy):

    def initialize_variables(self):
        # Indicators
        self.CandlestickType = CandlestickType(self.candlesticks)
        self.RSI = RSI(self.candlesticks)
        self.VWAP = VWAP(self.candlesticks)
        self.Ichimoku = Ichimoku(self.candlesticks)
        self.BollingerBand = BollingerBand(self.candlesticks)
        self.ChaikinMoneyFlow = ChaikinMoneyFlow(self.candlesticks)
        self.MACD = MACD(self.candlesticks)
        self.ATR = ATR(self.candlesticks)
        self.FibonacciRetracement = FibonacciRetracement(self.candlesticks)
        self.SellSignal = SellSignal(self.candlesticks, sell_below_max_percentage=0.997)
        self.HeikinAshi= HeikinAshi(self.candlesticks)
        self.SuperTrend = SuperTrend(self.candlesticks)

        # Strategy variables
        self.firstStep = False
        self.secondStep = False
        self.thirdStep = False

        self.start_counter = False
        self.counter = 0

    def __init__(self,
                 candlesticks: Candlesticks,
                 account: Account,
                 symbol: str,
                 primary_symbol: str,
                 secondary_symbol: str
                 ):

        super().__init__(candlesticks, account, symbol, primary_symbol, secondary_symbol)

    def new_candlestick_logic(self) -> None:

        if self.start_counter:
            self.counter += 1
            if self.counter >= 10:
                self.firstStep = False
                self.start_counter = False
                self.counter = 0

        if self.transactions_allowed and not self.account.get_position(symbol=self.symbol).is_valid() and self.candlesticks.get_number_of_rows() > 330:

            # TEST STRAT

            # if self.VWAP.get_last_values()[-1]['VWAP'] < self.data_structure.get_last_candlestick().Close \
            #         and self.RSI.get_all_values()[-2]['RSI'] < 30 \
            #         and self.RSI.get_last_values()[-1]['RSI'] > 40 \
            #         and (self.data_structure.get_last_candlestick().Close - self.VWAP.get_last_values()[-1]['VWAP']) / self.data_structure.get_last_candlestick().Close <= 0.01:
            #     last_vwaps = np.array([d['VWAP'] for d in self.VWAP.get_last_values()[-14:]])
            #     last_closes = np.array([c.Close for c in self.data_structure.get_last_candlesticks(14)])
            #     if (last_closes>last_vwaps).all():
            #         self.account.buy(self.data_structure.get_tick().Time, self.symbol, self.data_structure.get_tick().Close
            #         self.SellSignal.set_sell_target(self.data_structure.get_tick( .Close* 1.015)

            # Test STRAT 2

            if self.candlesticks.get_last_candlestick().Close > self.Ichimoku.get_last_values()[-1][
                'SenkouSpanA'] > self.candlesticks.get_last_candlestick().Open > self.Ichimoku.get_last_values()[-1]['SenkouSpanB'] and self.candlesticks.get_last_candlestick().Close > \
                    self.Ichimoku.get_last_values()[-1]['SenkouSpanB']:
                self.firstStep = True
                self.start_counter = True

            if self.firstStep:
                if self.Ichimoku.get_last_values()[-1]['TenkanSen'] > self.Ichimoku.get_last_values()[-1]['KijunSen'] and \
                        self.Ichimoku.get_last_values(n=2)[-2]['TenkanSen'] < self.Ichimoku.get_last_values(n=2)[-2]['KijunSen'] and \
                        self.candlesticks.get_last_candlestick().Close > self.Ichimoku.get_last_values()[-1]['SenkouSpanA']:
                    # self.account.buy(self.data_structure.get_tick().Time, self.symbol,
                    #                  self.data_structure.get_tick().Close
                    self.account.place_order(
                        time=self.candlesticks.get_tick().Time,
                        symbol=self.symbol,
                        source_symbol=self.primary_symbol,
                        destination_symbol=self.secondary_symbol,
                        price=self.candlesticks.get_tick().Close,
                        amount=self.account.balance[self.primary_symbol] / self.candlesticks.get_tick().Close,
                        side=OrderSide.BUY,
                        order_type=OrderType.MARKET
                    )
                    self.SellSignal.set_sell_target(self.candlesticks.get_tick().Close * 1.01)

    def new_tick_logic(self) -> None:
        # print('Got new tick in strat ', self.data_structure.get_tick())
        if self.transactions_allowed:
            if self.account.get_position(symbol=self.symbol).is_valid():
                # Sell logic
                if self.SellSignal.get_last_values(1)[-1]['SellSignal'] == 'Sell':

                    # self.account.sell(self.data_structure.get_tick().Time, self.symbol, self.data_structure.get_tick().Close
                    self.account.place_order(
                        time=self.candlesticks.get_tick().Time,
                        symbol=self.symbol,
                        source_symbol=self.primary_symbol,
                        destination_symbol=self.secondary_symbol,
                        price=self.candlesticks.get_tick().Close,
                        side=OrderSide.SELL,
                        order_type=OrderType.MARKET,
                        amount=self.account.get_position(symbol=self.symbol).Quantity
                    )
                # Stop loss
                elif float(self.account.get_position(symbol=self.symbol).AveragePrice) * 0.99 >= self.candlesticks.get_tick().Close:

                    log.warning(f"Hit stop-loss of {float(self.account.get_position(symbol=self.symbol).AveragePrice) * 0.99}  at {self.candlesticks.get_tick().Close}")
                    # self.account.sell(self.data_structure.get_tick().Time, self.symbol, self.data_structure.get_tick().Close
                    self.account.place_order(
                        time=self.candlesticks.get_tick().Time,
                        symbol=self.symbol,
                        source_symbol=self.primary_symbol,
                        destination_symbol=self.secondary_symbol,
                        price=self.candlesticks.get_tick().Close,
                        side=OrderSide.SELL,
                        order_type=OrderType.MARKET,
                        amount=self.account.get_position(symbol=self.symbol).Quantity
                    )

    def get_figure(self) -> Figure:
        fig = make_subplots(rows=3, cols=1)

        fig.append_trace(self.candlesticks.get_plot(), row=1, col=1)
        fig.append_trace(self.HeikinAshi.get_plot()[0], row=2, col=1)
        fig.append_trace(self.SuperTrend.get_plot()[0], row=1, col=1)

        # fig.append_trace(self.VWAP.get_plot()[0], row=1, col=1)
        # fig.append_trace(self.ChaikinMoneyFlow.get_plot()[0], row=3, col=1)
        # fig.append_trace(self.BollingerBand.get_plot()[0], row=1, col=1)
        # fig.append_trace(self.BollingerBand.get_plot()[1], row=1, col=1)
        # fig.append_trace(self.BollingerBand.get_plot()[2], row=1, col=1)

        # fig.append_trace(self.Ichimoku.get_plot()[0], row=1, col=1)
        # fig.append_trace(self.Ichimoku.get_plot()[1], row=1, col=1)
        # fig.append_trace(self.Ichimoku.get_plot()[2], row=1, col=1)
        # fig.append_trace(self.Ichimoku.get_plot()[3], row=1, col=1)
        # fig.append_trace(self.Ichimoku.get_plot()[4], row=1, col=1)

        # fig.append_trace(self.MACD.get_plot()[0], row=2, col=1)
        # fig.append_trace(self.MACD.get_plot()[1], row=2, col=1)

        # fig.append_trace(self.ADX.get_plot()[0], row=2, col=1)

        # fig.append_trace(self.RSI.get_plot()[0], row=2, col=1)

        # fig.append_trace(self.ATR.get_plot()[0], row=2, col=1)

        # Fibonacci retracements
        # for plot in self.FibonacciRetracement.get_plot():
        #     fig.append_trace(plot, row=1, col=1)

        # Buy and sell
        buy_plot, sell_plot = self.account.get_plot(self.symbol)
        fig.append_trace(buy_plot, row=1, col=1)
        fig.append_trace(sell_plot, row=1, col=1)
        coordinates = self.SellSignal.get_plot()
        for coordinate in coordinates:
            fig.add_vrect(
                x0=coordinate["x0"], x1=coordinate["x1"],
                fillcolor="LightSalmon", opacity=0.5,
                layer="below", line_width=0, row=1, col=1
            )

        fig.update_layout(height=4600, width=2800)
        fig.update_xaxes(rangeslider_visible=False)
        fig.update_xaxes(matches='x')
        return fig

    @staticmethod
    def condition(name: str) -> bool:
        return name == 'quickStrategy'
