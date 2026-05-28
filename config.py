import os
from dotenv import load_dotenv

# Load the secret keys from the .env file
load_dotenv()

# --- Alpaca API Settings ---
API_KEY = os.getenv("ALPACA_API_KEY")
SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
BASE_URL = "https://paper-api.alpaca.markets"  # Paper trading URL (not real money)
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# --- Trading Settings ---
SYMBOL = "BTC/USD"            # The crypto pair we are trading (Bitcoin)
POSITION_SIZE = 0.10          # Use 10% of account balance per trade
STOP_LOSS_PCT = 0.02          # Sell if price drops 2% from buy price

# --- Strategy Settings ---
SHORT_WINDOW = 9              # Short moving average period (9 candles)
LONG_WINDOW = 21              # Long moving average period (21 candles)
BAR_TIMEFRAME = "5Min"        # Each candle = 5 minutes of price data
MIN_GAP_PERCENT = 0.05        # Minimum % gap between MAs to act on a signal (filters out noise)

# --- Schedule Settings ---
RUN_INTERVAL_MINUTES = 10     # Check for signals every 10 minutes
# Note: No market hours needed! Crypto trades 24/7, 365 days a year
