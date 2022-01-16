from typing import List
from AutoTrader.models import Trade, TradesSummary
from AutoTrader.enums import OrderSide
import numpy as np


def get_trades_summary(
        symbol: str,
        source_symbol: str,
        destination_symbol: str,
        initial_balance: float,
        end_balance: float,
        trades: List[Trade]) -> TradesSummary:
    trade_blocks = get_trade_blocks(trades)
    fees = {}

    number_of_winning_trades = 0
    number_of_loosing_trades = 0
    winning_profits = []
    loosing_losses = []
    profits = []

    winning_hold_times = []
    loosing_hold_times = []
    hold_times = []

    largest_profit = 0
    largest_loss = 0

    longest_winning_streak = 0
    longest_loosing_streak = 0
    longest_winning_streak_counter = 0
    longest_loosing_streak_counter = 0

    for trade_block in trade_blocks:
        buy_quote = 0
        sell_quote = 0
        for trade in trade_block:
            # Set commissions
            fees[trade.CommissionSymbol] = fees[trade.CommissionSymbol] + trade.Commission if trade.CommissionSymbol in fees else trade.Commission

            if trade.Side == OrderSide.BUY:
                buy_quote += trade.QuoteQuantity

            if trade.Side == OrderSide.SELL:
                sell_quote += trade.QuoteQuantity - trade.Commission

        profit = sell_quote - buy_quote
        hold_time = abs(trade_block[-1].Time - trade_block[0].Time)

        # Any trade
        hold_times.append(hold_time)
        profits.append(profit)

        if profit >= 0:
            # Winning trade
            number_of_winning_trades += 1
            largest_profit = max(largest_profit, profit)
            winning_hold_times.append(hold_time)
            winning_profits.append(profit)

            longest_winning_streak_counter += 1
            longest_winning_streak = max(longest_winning_streak, longest_winning_streak_counter)
            longest_loosing_streak_counter = 0

        else:
            # Loosing trade
            number_of_loosing_trades += 1
            largest_loss = min(largest_loss, profit)
            loosing_hold_times.append(hold_time)
            loosing_losses.append(profit)

            longest_loosing_streak_counter += 1
            longest_loosing_streak = max(longest_loosing_streak, longest_loosing_streak_counter)
            longest_winning_streak_counter = 0

    return TradesSummary(
        InitialQuoteBalance=initial_balance,
        EndQuoteBalance=end_balance,
        PercentageQuoteChange=round(((end_balance - initial_balance) / initial_balance) * 100, 2),
        NumberOfTrades=len(trade_blocks),
        NumberOfWinningTrades=number_of_winning_trades,
        NumberOfLoosingTrades=number_of_loosing_trades,
        Trades=trades,
        AverageProfitPerTrade=np.mean(profits) if len(profits) > 0 else 0,
        AverageProfitPerWinningTrade=np.mean(winning_profits) if len(winning_profits) > 0 else 0,
        AverageLossPerLoosingTrade=np.mean(loosing_losses) if len(loosing_losses) > 0 else 0,
        AveragePositionHoldTime=int(np.mean(hold_times)) if len(hold_times) > 0 else 0,
        AveragePositionHoldTimeWin=int(np.mean(winning_hold_times)) if len(winning_hold_times) > 0 else 0,
        AveragePositionHoldTimeLoss=int(np.mean(loosing_hold_times)) if len(loosing_hold_times) > 0 else 0,
        LongestNumberOfTradesWinningStreak=longest_winning_streak,
        LongestNumberOfTradesLosingStreak=longest_loosing_streak,
        LargestProfit=largest_profit,
        LargestLoss=largest_loss,
        Fees=fees,
        TotalTradesDuration=trades[-1].Time - trades[0].Time
    )


def get_trade_blocks(trades: List[Trade]) -> List[List[Trade]]:
    trade_blocks = []
    temp_trade_block = []
    started_sell = False
    last_trade = False
    for i in range(len(trades)):

        current_trade = trades[i]
        temp_trade_block.append(current_trade)

        if (i + 1) == len(trades):
            last_trade = True

        if current_trade.Side == OrderSide.SELL:
            started_sell = True

        if not last_trade:
            next_trade = trades[i + 1]

        if last_trade or (started_sell and next_trade.Side == OrderSide.BUY):
            trade_blocks.append(temp_trade_block)
            temp_trade_block = []
            started_sell = False

    return trade_blocks
