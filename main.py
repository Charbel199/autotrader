from data.data_fetcher import get_fetcher
from dotenv import load_dotenv
import data_structures
import pandas as pd
load_dotenv()
df = data_structures.PandasTickStructure()
df.add_row({'Time': '1','Open': '2'})
df.add_row({'Time': '1','Open': '2'})
df.add_row({'Time': '1','Open': '2'})
df.add_row({'Time': '1','Open': '2'})

print('DOME ')
print(df.df)



data_fetcher = get_fetcher('binance', 'DOGEUSDT', '1m')
if data_fetcher:
    data = data_fetcher.get_candlesticks('14 Sep, 2021')

    print(data.shape)
    print(type(data))

