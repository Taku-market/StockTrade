import csv
import os
from datetime import datetime

TRADE_FILE = "logs/trades.csv"

# Write the header row if the file doesn't exist yet
if not os.path.exists(TRADE_FILE):
    with open(TRADE_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["datetime", "action", "price_usd", "amount_usd", "balance_after", "order_id"])


def log_trade(action, price, amount, balance, order_id):
    """
    Append one row to logs/trades.csv whenever a BUY or SELL happens.
    Opens easily in Excel for reviewing your trade history.
    """
    with open(TRADE_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            action,
            f"{price:.2f}" if price else "",
            f"{amount:.2f}" if amount else "",
            f"{balance:.2f}" if balance else "",
            order_id,
        ])
