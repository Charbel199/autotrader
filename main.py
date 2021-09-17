from data.data_fetcher import get_fetcher
from dotenv import load_dotenv
from data_structures.structure import get_data_structure
load_dotenv()
import time
from live_data.live_data_fetcher import get_live_fetcher
from strategies.strategy import get_strategy
data_fetcher = get_fetcher('binance','DOGEUSDT', '1m')
candlesticks = data_fetcher.get_candlesticks(start_date='16 Sep, 2021')
print(candlesticks[0])
live_data_fetcher = get_live_fetcher('binance')
# if back testing DONT ADD BULK BUT ADD THROUGH LOOP ON EACH TICK
df = get_data_structure('pandas')
strategy = get_strategy('quickStrategy', df)

#Add bulk old data
live_data_fetcher.run('DOGEUSDT', '1m', df, strategy)
print('start')
time.sleep(30)
live_data_fetcher.stop()
print('stop')

