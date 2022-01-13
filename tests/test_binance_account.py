from AutoTrader.trading.accounts.account_binance import AccountBinance
from binance.enums import *

account = AccountBinance()

# print(account._get_account_initial_balance())
#
# # order = account.client.order_limit(
# #     symbol='BTCBUSD',
# #     side=SIDE_BUY,
# #     type=ORDER_TYPE_LIMIT,
# #     timeInForce=TIME_IN_FORCE_GTC,
# #     quantity=0.00069,
# #     price='40000')
# order = account.client.order_market(
#     side=SIDE_BUY,
#     symbol='BTCBUSD',
#     quoteOrderQty= 29)
# print('order ',order)
# for a in account.client.get_all_orders(symbol='BTCBUSD', limit=15):
#     print(a if a['status']!='CANCELED' else '')
# # print(order)
# orders = account.client.get_open_orders(symbol='BTCBUSD')
# print(orders)
#
#
#
# #
# # # orders = account.client.cancel_order(
# # #     symbol='BTCBUSD',
# # #     orderId='4138466449')
# # # print(orders)
# # orders = account.client.get_open_orders(symbol='BTCBUSD')
# # print(orders)
# for i in account.client.get_my_trades(symbol='BTCBUSD'):
#     print(i)

from AutoTrader.enums import *
account.place_order(
    time=1642082724430,
    symbol='BTCBUSD',
    source_symbol='BTC',
    destination_symbol='BUSD',
    order_type= OrderType.MARKET,
    price=1,
    side=OrderSide.BUY,
    amount= 0.00033
)

print(account.get_orders('BTCBUSD'))
print(account.get_trades('BTCBUSD'))
print(account.get_symbol_balance('BTCBUSD'))

account.place_order(
    time=1642082724430,
    symbol='BTCBUSD',
    source_symbol='BTC',
    destination_symbol='BUSD',
    order_type= OrderType.MARKET,
    price=1,
    side=OrderSide.SELL,
    amount= 0.00033
)

print(account.get_orders('BTCBUSD'))
print(account.get_trades('BTCBUSD'))
print(account.get_symbol_balance('BTCBUSD'))