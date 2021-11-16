from typing import List
import numpy as np
from AutoTrader.helper import date_helper


def get_trades_summary(transactions: List[dict], initial_balance: float) -> dict:
    trades = []
    hold_times = []
    hold_times_win = []
    hold_times_loss = []

    balance = initial_balance

    number_of_trades = 0
    number_of_losses = 0
    total_loss = 0
    total_win = 0
    longest_winning_streak = 0
    longest_losing_streak = 0
    winning_streak = 0
    losing_streak = 0
    largest_winning_profit = 0
    largest_losing_profit = 0

    if len(transactions) < 2:
        return {}

    total_duration = transactions[-1]['Time'] - transactions[0]['Time']

    for i in range(0, len(transactions), 2):
        profit = (transactions[i + 1]['Price'] - transactions[i]['Price']) * transactions[i]['Amount']
        buy_time = int(transactions[i]['Time'])
        sell_time = int(transactions[i + 1]['Time'])
        hold_time = abs(sell_time - buy_time)

        number_of_trades += 1
        hold_times.append(hold_time)

        if profit < 0:
            winning_streak = 0
            total_loss += profit
            number_of_losses += 1
            hold_times_loss.append(hold_time)
            losing_streak += 1
            if profit < largest_losing_profit:
                largest_losing_profit = profit
        else:
            losing_streak = 0
            total_win += profit
            hold_times_win.append(hold_time)
            winning_streak += 1
            if profit > largest_winning_profit:
                largest_winning_profit = profit

        if winning_streak > longest_winning_streak:
            longest_winning_streak = winning_streak

        if losing_streak > longest_losing_streak:
            longest_losing_streak = losing_streak

        balance += profit
        trades.append({
            'Symbol': transactions[i]['Symbol'],
            'BuyTime': date_helper.from_timestamp_to_date(buy_time),
            'SellTime': date_helper.from_timestamp_to_date(sell_time),
            'Amount': transactions[i]['Amount'],
            'BuyPrice': transactions[i]['Price'],
            'SellPrice': transactions[i + 1]['Price'],
            'Profit': profit,
            'Balance': balance,
            'Outcome': 'Win' if profit > 0 else 'Loss'
        })

    number_of_wins = number_of_trades - number_of_losses
    total_profit = balance - initial_balance
    average_profit = total_profit / number_of_trades if number_of_trades > 0 else 0
    average_win = total_win / number_of_wins if number_of_wins > 0 else 0
    average_loss = total_loss / number_of_losses if number_of_losses > 0 else 0
    summary = {
        'InitialBalance': initial_balance,
        'EndBalance': balance,
        'PercentageChange': ((balance - initial_balance) / initial_balance) * 100 if initial_balance > 0 else 0,
        'NumberOfTrades': number_of_trades,
        'NumberOfWins': number_of_wins,
        'NumberOfLosses': number_of_losses,
        'AllTrades': [],
        'AverageProfit': average_profit,
        'AverageWin': average_win,
        'AverageLoss': average_loss,
        'AverageHoldTime': date_helper.from_seconds_to_time(int(np.mean(hold_times)) if len(hold_times) > 0 else 0),
        'AverageHoldTimeWin': date_helper.from_seconds_to_time(int(np.mean(hold_times_win)) if len(hold_times_win) > 0 else 0),
        'AverageHoldTimeLoss': date_helper.from_seconds_to_time(int(np.mean(hold_times_loss)) if len(hold_times_loss) > 0 else 0),
        'LongestWinningStreak': longest_winning_streak,
        'LongestLosingStreak': longest_losing_streak,
        'LargestWinningProfit': largest_winning_profit,
        'LargestLosingProfit': largest_losing_profit,
        'TotalTradesDuration': date_helper.from_seconds_to_time(total_duration)
    }
    return summary


def print_summary(summary: dict) -> str:
    summary_string = '\n'
    for key, value in summary.items():
        summary_string += f"{key: <23}: {value}\n"
    return summary_string
