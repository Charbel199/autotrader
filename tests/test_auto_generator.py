from dotenv import load_dotenv
from AutoTrader.helper import logger

load_dotenv()
log = logger.setup_applevel_logger(file_name='test_generator_debug.log')
from AutoTrader.ml.candlestick_generator import CandlestickGeneratorAutoRunner

start_date = "1 Oct, 2018"

runner = CandlestickGeneratorAutoRunner(symbols=['DOGEUSDT', 'BTCUSDT', 'ADAUSDT'], timeframe='5m', data_fetcher_provider='binance',
                                        data_structure_provider='list', candlestick_auto_processor_provider='auto', start_date=start_date)

for i in range(30):
    runner.get_new_candlesticks()
