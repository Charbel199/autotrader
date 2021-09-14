from data.data_fetcher import get_fetcher
from dotenv import load_dotenv
from data_logger import logger
load_dotenv()

data_fetcher = get_fetcher('binance', 'DOGEUSDT', '25m')
if data_fetcher:
    data = data_fetcher.get_candlesticks('13 Sep, 2021')
    print(data)
    print(type(data))

