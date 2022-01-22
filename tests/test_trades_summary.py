from app.AutoTrader.models import TradesSummary, Trade

ts = TradesSummary(
    Trades= [Trade()]
)

print(ts.get_text_summary())