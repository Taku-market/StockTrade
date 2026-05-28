"""
reset_positions.py — Close all open positions and cancel all orders.

Run this once to clean up stuck positions:
  python reset_positions.py
"""

from alpaca.trading.client import TradingClient
from config import API_KEY, SECRET_KEY

client = TradingClient(API_KEY, SECRET_KEY, paper=True)


def reset():
    # Step 1: Cancel all open orders
    print("Cancelling all open orders...")
    client.cancel_orders()
    print("Done.\n")

    # Step 2: Show current positions before closing
    positions = client.get_all_positions()
    if not positions:
        print("No open positions found.")
    else:
        print(f"Found {len(positions)} open position(s):")
        for p in positions:
            print(f"  {p.symbol}: {p.qty} units | Avg buy: ${float(p.avg_entry_price):,.2f} | Current: ${float(p.current_price):,.2f}")

        # Step 3: Close all positions at market price
        print("\nClosing all positions...")
        client.close_all_positions(cancel_orders=True)
        print("Done.\n")

    # Step 4: Show final balance
    account = client.get_account()
    print(f"Cash balance after close: ${float(account.cash):,.2f}")
    print(f"Total equity:             ${float(account.equity):,.2f}")


if __name__ == "__main__":
    print("=" * 50)
    print("RESET: Closing all BTC positions")
    print("=" * 50 + "\n")
    reset()
    print("\nDone! Your account is clean.")
