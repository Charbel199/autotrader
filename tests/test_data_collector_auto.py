from dotenv import load_dotenv
from app.AutoTrader.helper import logger
from app.AutoTrader.ml.data_collector.modes.data_collector_auto import DataCollectorAuto

load_dotenv()
log = logger.setup_applevel_logger(file_name='test_data_collector_auto_debug.log')

start_date = "1 Oct, 2018"

runner = DataCollectorAuto(symbols=['DOGEUSDT', 'BTCUSDT', 'ADAUSDT'], timeframe='5m', data_fetcher_provider='binance',
                           candlesticks_provider='list', candlestick_generator_processor_provider='continuous',
                           features_generator_provider='auto', start_date=start_date)

runner.launch_auto_collector()
