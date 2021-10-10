from dotenv import load_dotenv

load_dotenv()

from ml.candlestick_generator import CandlestickGenerator
from ml.candlestickProcessor.candlestick_processor import get_candlestick_processor
from data.previous_data.data_fetcher import get_fetcher
from helper import date_helper
import threading
import plotly.graph_objects as go
import pandas as pd
from data.data_structures.structure import get_data_structure
from plotly.subplots import make_subplots

start_date = "1 Oct, 2018"

data_fetcher = get_fetcher('binance')
data_structure = get_data_structure('pandas')
candlestick_generator_processor = get_candlestick_processor('simple',data_structure)
generator = CandlestickGenerator(candlestick_generator_processor, data_fetcher, data_structure, ['DOGEUSDT', 'BTCUSDT', 'ADAUSDT'], '5m')
generator.fetch_new_candlesticks(date_helper.get_random_timestamp(date_helper.from_binance_date_to_timestamp(start_date)), 8)
while True:
    thread = threading.Thread(target=generator.fetch_new_candlesticks, args=[date_helper.get_random_timestamp(date_helper.from_binance_date_to_timestamp(start_date)), 8])
    thread.start()
    data = generator.get_new_candlesticks()
    candlesticks = data['Ticks']
    print("GOT IT ")
    #print(data['ADX'].to_string())
    df = pd.DataFrame(candlesticks)
    if df.__len__() > 0:
        fig = make_subplots(rows=1, cols=1)
        fig.append_trace(go.Candlestick(x=df['Time'],
                                        open=df['Open'],
                                        high=df['High'],
                                        low=df['Low'],
                                        close=df['Close'], name="Candlesticks"), row=1, col=1)

        fig.show()
    _ = input("Press anything to continue")
    thread.join()
