import schedule
import time
from datetime import datetime
import pytz

from config import RUN_INTERVAL_MINUTES, MARKET_OPEN, MARKET_CLOSE
from strategy import get_signal
from trader import get_current_position, check_stop_loss, buy_spy, sell_spy
from logger import logger


# US Eastern timezone (New York) — stock market runs on ET
ET = pytz.timezone("America/New_York")


def is_market_open():
    """
    Check if the US stock market is currently open.
    Market hours: Monday-Friday, 9:30am - 4:00pm ET
    """
    now = datetime.now(ET)

    # Skip weekends (Saturday=5, Sunday=6)
    if now.weekday() >= 5:
        return False

    # Check if current time is within market hours
    market_open = now.replace(hour=9, minute=30, second=0, microsecond=0)
    market_close = now.replace(hour=16, minute=0, second=0, microsecond=0)

    return market_open <= now <= market_close


def run_bot():
    """
    The main bot logic — runs every 10 minutes.
    This is the heart of the automation:
    1. Check if market is open
    2. Check stop-loss (sell if price dropped too much)
    3. Get buy/sell signal from strategy
    4. Execute the trade
    """
    logger.info("=" * 50)
    logger.info("Bot running...")

    # Step 1: Skip if market is closed
    if not is_market_open():
        logger.info("Market is closed — skipping this run")
        return

    # Step 2: Check stop-loss first (safety check before anything else)
    position = get_current_position()

    if position is not None:
        if check_stop_loss(position):
            logger.info("Selling due to stop-loss!")
            sell_spy()
            return  # Done for this run — wait for next cycle

    # Step 3: Get signal from strategy (BUY / SELL / HOLD)
    signal, current_price = get_signal()

    # Step 4: Act on the signal
    if signal == "BUY":
        if position is not None:
            logger.info("Signal is BUY but we already own SPY — skipping")
        else:
            buy_spy()

    elif signal == "SELL":
        if position is None:
            logger.info("Signal is SELL but we don't own SPY — skipping")
        else:
            sell_spy()

    elif signal == "HOLD":
        logger.info("Holding — no action taken")

    logger.info("Bot finished this run")
    logger.info("=" * 50)


def main():
    """
    Start the bot and keep it running on a schedule.
    """
    logger.info("🤖 SPY Trading Bot Starting...")
    logger.info(f"Will check for signals every {RUN_INTERVAL_MINUTES} minutes during market hours")

    # Run immediately once when the bot starts
    run_bot()

    # Then run every 10 minutes automatically
    schedule.every(RUN_INTERVAL_MINUTES).minutes.do(run_bot)

    logger.info(f"Scheduler started — next run in {RUN_INTERVAL_MINUTES} minutes")

    # Keep the bot running forever (until you press Ctrl+C to stop)
    while True:
        schedule.run_pending()
        time.sleep(30)  # Check every 30 seconds if it's time to run


# This line means: only run main() if we start this file directly
# (not if another file imports it)
if __name__ == "__main__":
    main()
