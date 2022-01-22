from plotly.graph_objs import Figure

from app.AutoTrader.trading.strategies.strategy import Strategy
from app.AutoTrader.trading.indicators import SuperTrend, HeikinAshi, SellSignal, ADX
from app.AutoTrader.data.data_structures.candlesticks import Candlesticks
from app.AutoTrader.trading.accounts.account import Account
from app.AutoTrader.enums import OrderStatus,OrderSide,OrderType
from plotly.subplots import make_subplots
from app.AutoTrader.helper import logger

log = logger.get_logger(__name__)


class HASStrategy(Strategy):
    def __init__(self,
                 candlesticks: Candlesticks,
                 account: Account,
                 symbol: str,
                 primary_symbol: str,
                 secondary_symbol: str
                 ):

        super().__init__(candlesticks, account, symbol, primary_symbol, secondary_symbol)

    def new_candlestick_logic(self) -> None:
        if self.transactions_allowed and not self.account.get_position(symbol=self.symbol).is_valid() and self.candlesticks.get_number_of_rows() > 200:
            last_two_super_trend_values = self.SuperTrend.get_last_values(n=2)
            last_heikin_ashi = self.HeikinAshi.get_last_values(1)[0]

            if last_two_super_trend_values[-2]['IsUpper'] and not last_two_super_trend_values[-1]['IsUpper'] and last_heikin_ashi['Close'] > last_heikin_ashi['Open'] and self.ADX.get_last_values(1)[0]['ADX']>25:
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
                self.stop_loss = last_heikin_ashi['Low']
                self.target = self.candlesticks.get_tick().Close + (self.candlesticks.get_tick().Close - self.stop_loss) * 2

                self.SellSignal.set_sell_target(self.target)

    def new_tick_logic(self) -> None:
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
                elif self.stop_loss >= self.candlesticks.get_tick().Close:

                    log.warning(f"Hit stop-loss of {self.stop_loss}  at {self.candlesticks.get_tick().Close}")
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
        fig = make_subplots(rows=2, cols=1)

        fig.append_trace(self.HeikinAshi.get_plot()[0], row=1, col=1)
        fig.data[0].increasing.fillcolor = 'blue'
        fig.data[0].increasing.line.color = 'blue'
        fig.data[0].decreasing.fillcolor = 'orange'
        fig.data[0].decreasing.line.color = 'orange'
        fig.append_trace(self.candlesticks.get_plot(), row=1, col=1)
        fig.append_trace(self.SuperTrend.get_plot()[0], row=1, col=1)

        buy_plot, sell_plot = self.account.get_plot(self.symbol)
        fig.append_trace(buy_plot, row=1, col=1)
        fig.append_trace(sell_plot, row=1, col=1)

        fig.append_trace(self.ADX.get_plot()[0], row=2, col=1)

        fig.update_layout(height=2400, width=2800)
        fig.update_xaxes(rangeslider_visible=False)
        fig.update_xaxes(matches='x')
        return fig

    @staticmethod
    def condition(name: str) -> bool:
        return name == 'HAS_strategy'

    def initialize_variables(self):
        self.HeikinAshi = HeikinAshi(self.candlesticks)
        self.SuperTrend = SuperTrend(self.candlesticks)
        self.SellSignal = SellSignal(self.candlesticks, sell_below_max_percentage=1)
        self.ADX = ADX(self.candlesticks)
        self.stop_loss = 0
        self.target = 0
