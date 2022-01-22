from dataclasses import dataclass
from typing import List, Dict
from app.AutoTrader.models import Trade
from app.AutoTrader.helper import date_helper

@dataclass
class TradesSummary(object):
    """
    Trades Summary

    Note: A trade here refers to entering then exiting a position (Buy and Sell)
    """

    # Balance
    InitialQuoteBalance: float = 0
    EndQuoteBalance: float = 0
    PercentageQuoteChange: float = 0

    # Trades
    NumberOfTrades: int = 0
    NumberOfWinningTrades: int = 0
    NumberOfLoosingTrades: int = 0
    Trades: List[Trade] = List

    # Profit
    AverageProfitPerTrade: float = 0
    AverageProfitPerWinningTrade: float = 0
    AverageLossPerLoosingTrade: float = 0

    # Hold time
    AveragePositionHoldTime: float = 0
    AveragePositionHoldTimeWin: float = 0
    AveragePositionHoldTimeLoss: float = 0

    # Streaks
    LongestNumberOfTradesWinningStreak: int = 0
    LongestNumberOfTradesLosingStreak: int = 0

    # Largest Wins and Losses
    LargestProfit: float = 0
    LargestLoss: int = 0

    # Fees
    Fees: Dict[str, float] = Dict

    # Duration
    TotalTradesDuration: int = 0

    def get_text_summary(self, show_trades=False) -> str:
        summary_string = '\n'
        for key, value in vars(self).items():
            if key == 'Trades':
                if not show_trades:
                    continue
                else:
                    summary_string += f"{key: <35}->\n"
                    for trade in value:
                        summary_string += f"\t\t{trade}\n"
            elif key == 'AveragePositionHoldTime' or key == 'AveragePositionHoldTimeWin' or key == 'AveragePositionHoldTimeLoss' or key == 'TotalTradesDuration':
                summary_string += f"{key: <35}-> {date_helper.from_seconds_to_time(value)}\n"
            else:
                summary_string += f"{key: <35}-> {value}\n"
        return summary_string
