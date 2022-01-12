from AutoTrader.trading.accounts.account_binance import AccountBinance
from binance.enums import *

account = AccountBinance()

print(account._get_balance())

order = account.client.order_limit(
    symbol='BTCBUSD',
    side=SIDE_SELL,
    type=ORDER_TYPE_LIMIT,
    timeInForce=TIME_IN_FORCE_GTC,
    quantity=0.00069,
    price='43000')
print(account.client.get_all_orders(symbol='BTCBUSD', limit=10))

print(order)
orders = account.client.get_open_orders(symbol='BTCBUSD')
print(orders)


# get fee for one symbol
fees = account.client.get_trade_fee(symbol='BTCBUSD')
print(fees)

# orders = account.client.cancel_order(
#     symbol='BTCBUSD',
#     orderId='4138466449')
# print(orders)
orders = account.client.get_open_orders(symbol='BTCBUSD')
print(orders)