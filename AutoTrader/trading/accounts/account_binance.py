from AutoTrader.trading.accounts.account import Account
from AutoTrader.helper import logger
from AutoTrader.models import Order, Trade
from AutoTrader.enums import OrderType, OrderSide, OrderStatus
from AutoTrader.helper.date_helper import from_timestamp_to_date
from typing import Dict, List
from binance.client import Client
from binance.enums import *
import os
from dotenv import load_dotenv
import numpy as np

load_dotenv()
log = logger.get_logger(__name__)


class AccountBinance(Account):
    transaction_percentage = 0.1 / 100
    transaction_fee = 0
    client = Client(os.getenv('API_KEY'), os.getenv('API_SECRET'))

    def __init__(self):
        super().__init__()

    def place_order(self,
                    time: int,
                    symbol: str,
                    source_symbol: str,
                    destination_symbol: str,
                    order_type: OrderType,
                    price: float,
                    side: OrderSide,
                    amount: float) -> None:

        if side == OrderSide.BUY:
            if order_type == OrderType.MARKET:
                self._market_order(
                    symbol=symbol,
                    quantity=amount,
                    side=side
                )

        if side == OrderSide.SELL:
            if order_type == OrderType.MARKET:
                self._market_order(
                    symbol=symbol,
                    quantity=amount,
                    side=side
                )

        self.refresh_balance()

    def _market_order(self, symbol: str, quantity: float, side: OrderSide):
        # Launch order
        market_buy_order = self.client.order_market(
            side=SIDE_BUY if side == OrderSide.BUY else SIDE_SELL,
            symbol=symbol,
            quantity=quantity)
        # Record order
        order_trades = market_buy_order['fills']
        order = Order(
            Time=int(market_buy_order['transactTime']),
            Side=side,
            OriginalQuantity=float(market_buy_order['origQty']),
            ExecutedQuantity=float(market_buy_order['executedQty']),
            Symbol=symbol,
            Type=OrderType.MARKET,
            Price=self._get_average_asset_price_from_order_trades(order_trades),
            CumulativeQuoteQuantity=float(market_buy_order['cummulativeQuoteQty']),
            Status=OrderStatus.OPEN if float(market_buy_order['origQty']) != float(market_buy_order['executedQty']) else OrderStatus.FILLED,
            OrderId=market_buy_order['orderId']
        )
        self.add_order(symbol=symbol,
                       order=order)
        # Record trade
        for trade in order_trades:
            self.add_trade(symbol=symbol,
                           trade=Trade(
                               Time=int(market_buy_order['transactTime']),
                               Symbol=symbol,
                               Side=OrderSide.BUY,
                               IsMaker=False,
                               Price=float(trade['price']),
                               Quantity=float(trade['qty']),
                               QuoteQuantity=float(trade['price']) * float(trade['qty']),
                               CommissionSymbol=trade['commissionAsset'],
                               Commission=float(trade['commission']),
                               TradeId=trade['tradeId']
                           ))
        # Update position
        self.set_position(symbol, order) if side == OrderSide.BUY else self.reset_position(symbol)

        log.info(
            f"{from_timestamp_to_date(order.Time)} - Market {str(side)} Order - {order.CumulativeQuoteQuantity} of {symbol} for a price of {order.Price}")

    def _get_average_asset_price_from_order_trades(self, order_trades: List[Dict]) -> float:
        return sum([float(fill['price']) * float(fill['qty']) for fill in order_trades]) / sum([float(fill['qty']) for fill in order_trades])

    def _get_account_initial_balance(self) -> Dict[str, float]:
        return self._get_binance_balance()

    def get_current_balance(self) -> Dict[str, float]:
        return self._get_binance_balance()

    def _get_binance_balance(self) -> Dict[str, float]:
        binance_balance = self.client.get_account()['balances']
        balance = {}
        for b in binance_balance:
            balance[b['asset']] = float(b['free'])
        return balance

    @staticmethod
    def condition(name: str) -> bool:
        return name == "binanceAccount"
