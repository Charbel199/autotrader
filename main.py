from data.data_fetcher import get_fetcher
from dotenv import load_dotenv
from data_structures.structure import get_data_structure
load_dotenv()
"""
df = get_data_structure('pandas')

df.add_row({'Time': '1', 'Open': '2'})
df.add_row({'Time': '1', 'Open': '2'})
df.add_row({'Time': '1', 'Open': '2'})
df.add_row({'Time': '1', 'Open': '2'})

print('DOME ')
print(df.get_data())

data_fetcher = get_fetcher('binance', 'DOGEUSDT', '1m')
if data_fetcher:
    data = data_fetcher.get_candlesticks('14 Sep, 2021')
    print(data.shape)
    print(type(data))

import time
from binance import BinanceSocketManager
from binance.enums import *
def btc_trade_history(msg):
    print('msg ',msg)
from binance.client import Client
import os
client = Client(os.getenv('API_KEY'), os.getenv('API_SECRET'))
bm = BinanceSocketManager(client, user_timeout=60)
ks = bm.kline_socket(symbol='btcusdt', interval=KLINE_INTERVAL_30MINUTE)

print(ks)
print('HELLO')
time.sleep(3)
print('JEU')

while True:
    pass

"""
import time
import os
from binance import ThreadedWebsocketManager
from live_data.live_data_fetcher import get_live_fetcher


def handle_socket_message(m):
    print(m)
data_fetcher = get_live_fetcher('binance')
data_fetcher.run('DOGEUSDT', '1m',handle_socket_message)
data_fetcher.run('BNBUSDT', '5m',handle_socket_message)
print('start')
time.sleep(10)

data_fetcher.stop()
print('stop')
time.sleep(5)
print('done')
data_fetcher = get_live_fetcher('binance')
data_fetcher.run('DOGEUSDT', '1m',handle_socket_message)
data_fetcher.run('BNBUSDT', '5m',handle_socket_message)
print('start')
time.sleep(10)

data_fetcher.stop()