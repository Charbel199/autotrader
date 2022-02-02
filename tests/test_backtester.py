from dotenv import load_dotenv
from AutoTrader.helper import logger

load_dotenv()
log = logger.setup_applevel_logger(file_name='test_backtester_debug.log')
from AutoTrader.trading.modes.backtester import BackTesterRunner
import time


def back_test_many():
    symbols = ['ADA', 'DOT', 'LINK', 'ETH', 'BTC', 'XRP', 'DOGE', 'TRX', 'BNB', 'SOL', 'LUNA', 'AXS', 'ALGO']
    start_date = "1 Dec, 2021"
    end_date = "30 Jan, 2022"
    strategy_name = 'SHEA_strategy'
    backtesters = []
    for symbol in symbols:
        runner = BackTesterRunner('testAccount')

        backtester = runner.prepare_backtester(symbol=f"{symbol}USDT", primary_symbol='USDT',
                                               secondary_symbol=symbol, timeframe="5m",
                                               strategy_provider=strategy_name, candlesticks_provider="list", data_fetcher_provider="binance",
                                               start_date=start_date, end_date=end_date)

        backtesters.append(backtester)
        runner.launch()
    for bt in backtesters:
        print("For ", bt.symbol)

        bt.backtester_performance(show_fig=False, show_trades=False)


def back_test_specific():
    start = time.time()

    start_date = "1 Dec, 2021"
    # start_date = "1 Oct, 2020"
    end_date = "30 Jan, 2022"
    runner = BackTesterRunner('testAccount')
    strategy_name = 'SHEA_strategy'
    backtester1 = runner.prepare_backtester(symbol="XRPUSDT", primary_symbol='USDT',
                                            secondary_symbol='XRP', timeframe="5m",
                                            strategy_provider=strategy_name, candlesticks_provider="list", data_fetcher_provider="binance",
                                            start_date=start_date, end_date=end_date)

    # backtester2 = runner.prepare_backtester(symbol="XRPBUSD", primary_symbol='BUSD',
    #                                         secondary_symbol='XRP', timeframe="1m",
    #                                         strategy_provider=strategy_name, candlesticks_provider="list", data_fetcher_provider="binance",
    #                                         start_date=start_date, end_date=end_date)
    #
    # backtester3 = runner.prepare_backtester(symbol="LINKBTC", primary_symbol='BTC',
    #                                         secondary_symbol='LINK', timeframe="1m",
    #                                         strategy_provider=strategy_name, candlesticks_provider="list", data_fetcher_provider="binance",
    #                                         start_date=start_date, end_date=end_date)

    runner.launch()

    backtester1.backtester_performance(show_fig=False, show_trades=False)
    # backtester2.backtester_performance(show_fig=False, show_trades=False)
    # backtester3.backtester_performance(show_fig=False, show_trades=False)

    end = time.time()
    log.info(f"Total duration: {(end - start)}")
    log.info(f"End balance: {runner.account.balance}")


back_test_many()
