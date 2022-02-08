import os
from dotenv import load_dotenv
load_dotenv()
from binance import Client
client = Client(os.getenv('API_KEY'), os.getenv('API_SECRET'))

details = client.get_max_margin_loan(asset='BTC')
print(details)
