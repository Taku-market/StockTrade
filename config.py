import os
from dotenv import load_dotenv

# Load the secret keys from the .env file
load_dotenv()

# --- Alpaca API Settings ---
API_KEY = os.getenv("ALPACA_API_KEY")
SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
BASE_URL = "https://paper-api.alpaca.markets"  # Paper trading URL (not real money)

# --- Trading Settings ---
SYMBOL = "SPY"                # The stock we are trading
POSITION_SIZE = 0.10          # Use 10% of account balance per trade
STOP_LOSS_PCT = 0.02          # Sell if price drops 2% from buy price

# --- Strategy Settings ---
SHORT_WINDOW = 9              # Short moving average period (9 candles)
LONG_WINDOW = 21              # Long moving average period (21 candles)
BAR_TIMEFRAME = "5Min"        # Each candle = 5 minutes of price data

# --- Schedule Settings ---
RUN_INTERVAL_MINUTES = 10     # Check for signals every 10 minutes
MARKET_OPEN = "09:30"         # Market opens at 9:30am ET
MARKET_CLOSE = "16:00"        # Market closes at 4:00pm ET
