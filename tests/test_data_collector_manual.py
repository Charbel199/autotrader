from dotenv import load_dotenv
from AutoTrader.helper import logger
from AutoTrader.ml.data_collector.modes.data_collector_manual import DataCollectorManual

load_dotenv()
log = logger.setup_applevel_logger(file_name='test_data_collector_manual_debug.log')

start_date = "1 Oct, 2018"

runner = DataCollectorManual(symbols=['DOGEUSDT', 'BTCUSDT', 'ADAUSDT'], timeframe='5m', data_fetcher_provider='binance',
                             candlesticks_provider='list', candlestick_generator_processor_provider='continuous',
                             features_generator_provider='simple', start_date=start_date)
runner.launch_manual_collector()
