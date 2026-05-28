from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame
from datetime import datetime, timezone, timedelta
import pandas as pd

from config import API_KEY, SECRET_KEY, SYMBOL, SHORT_WINDOW, LONG_WINDOW, MIN_GAP_PERCENT
from logger import logger


# Connect to Alpaca to fetch crypto price data (read-only, no trading here)
# Crypto data is public — no API keys required, but we pass them anyway
data_client = CryptoHistoricalDataClient(API_KEY, SECRET_KEY)


def get_price_data():
    """
    Fetch the last 50 candles of BTC/USD price data from Alpaca.
    Each candle = 5 minutes of price activity.
    We need at least 21 candles to calculate our Long Moving Average.

    Because crypto is 24/7, we look back 5 hours to get enough candles.
    """
    request = CryptoBarsRequest(
        symbol_or_symbols=SYMBOL,
        timeframe=TimeFrame.Minute,
        start=datetime.now(timezone.utc) - timedelta(hours=5),  # Last 5 hours of data
        limit=50  # Get last 50 candles (plenty for 9 and 21 period MAs)
    )

    bars = data_client.get_crypto_bars(request)
    df = bars.df  # Convert to a table (DataFrame) we can work with

    # If there are multiple symbols, only keep BTC/USD rows
    if isinstance(df.index, pd.MultiIndex):
        df = df.xs(SYMBOL, level="symbol")

    return df


def calculate_signals(df):
    """
    Calculate the Moving Average Crossover signal.

    Short MA (9 periods)  = average of last 9 candle closing prices
    Long MA  (21 periods) = average of last 21 candle closing prices

    Signal logic:
    - BUY  when Short MA crosses ABOVE Long MA (price trending up)
    - SELL when Short MA crosses BELOW Long MA (price trending down)
    - HOLD when no crossover happened
    """
    # Calculate moving averages using closing prices
    df["short_ma"] = df["close"].rolling(window=SHORT_WINDOW).mean()
    df["long_ma"] = df["close"].rolling(window=LONG_WINDOW).mean()

    # Get the two most recent rows to detect a crossover
    last = df.iloc[-1]      # Most recent candle
    prev = df.iloc[-2]      # Candle before that

    current_price = last["close"]
    short_ma = last["short_ma"]
    long_ma = last["long_ma"]

    # Calculate how far apart the two MAs are (as a percentage)
    gap_percent = abs(float(short_ma) - float(long_ma)) / float(long_ma) * 100

    logger.info(f"BTC/USD Price: ${current_price:,.2f} | Short MA: ${short_ma:,.2f} | Long MA: ${long_ma:,.2f} | Gap: {gap_percent:.4f}%")

    # If the MAs are too close together, the crossover is probably just noise — ignore it
    if gap_percent < MIN_GAP_PERCENT:
        logger.info(f"Signal: HOLD — MA gap {gap_percent:.4f}% is below minimum {MIN_GAP_PERCENT}% (too close, likely false signal)")
        return "HOLD", current_price, float(short_ma), float(long_ma)

    # BUY signal: Short MA just crossed above Long MA with enough gap
    if prev["short_ma"] <= prev["long_ma"] and last["short_ma"] > last["long_ma"]:
        logger.info("Signal: BUY - Short MA crossed above Long MA")
        return "BUY", current_price, float(short_ma), float(long_ma)

    # SELL signal: Short MA just crossed below Long MA with enough gap
    elif prev["short_ma"] >= prev["long_ma"] and last["short_ma"] < last["long_ma"]:
        logger.info("Signal: SELL - Short MA crossed below Long MA")
        return "SELL", current_price, float(short_ma), float(long_ma)

    # No crossover — do nothing
    else:
        logger.info("Signal: HOLD — No crossover detected")
        return "HOLD", current_price, float(short_ma), float(long_ma)


def get_signal():
    """
    Main function called by the bot every 10 minutes.
    Returns: ("BUY" or "SELL" or "HOLD", current_price)
    """
    try:
        df = get_price_data()
        return calculate_signals(df)
    except Exception as e:
        logger.error(f"Strategy error: {e}")
        return "HOLD", None, None, None  # If anything goes wrong, do nothing (safe default)
