from data.data_fetcher import DataFetcher, get_fetcher
from dotenv import load_dotenv

load_dotenv()

subclass = get_fetcher('binance')
if subclass:
    data_fetcher_obj = subclass('DOGEUSDT', '5m')
    data = data_fetcher_obj.get_candlesticks('13 Sep, 2021')
    print(len(data))
