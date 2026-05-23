"""
Quick connection test - run this anytime to verify Alpaca API is working.
This does NOT place any trades.
"""
from alpaca.trading.client import TradingClient
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("ALPACA_API_KEY")
SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")

client = TradingClient(API_KEY, SECRET_KEY, paper=True)
account = client.get_account()

print("Connection successful!")
print(f"Account status : {account.status}")
print(f"Cash balance   : ${float(account.cash):,.2f}")
print(f"Portfolio value: ${float(account.portfolio_value):,.2f}")
print(f"Buying power   : ${float(account.buying_power):,.2f}")
