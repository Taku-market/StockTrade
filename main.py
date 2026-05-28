import schedule
import time

from config import RUN_INTERVAL_MINUTES
from strategy import get_signal
from trader import get_current_position, get_account_balance, check_stop_loss, buy_crypto, sell_crypto
from dashboard import show_dashboard
from ai_analyst import get_ai_comment
from logger import logger


def run_bot():
    """
    The main bot logic — runs every 5 minutes.
    Because crypto is 24/7, we no longer need to check market hours!

    1. Check stop-loss (sell if price dropped too much)
    2. Get buy/sell signal from strategy
    3. Execute the trade
    4. Show the dashboard
    """
    logger.info("=" * 50)
    logger.info("Bot running...")

    # Step 1: Check stop-loss first (safety check before anything else)
    position = get_current_position()

    if position is not None:
        if check_stop_loss(position):
            logger.info("Selling due to stop-loss!")
            sell_crypto()
            position = None  # We no longer hold BTC after selling

    # Step 2: Get signal from strategy (BUY / SELL / HOLD + MA values)
    signal, current_price, short_ma, long_ma = get_signal()

    # Step 3: Act on the signal
    if signal == "BUY":
        if position is not None:
            logger.info("Signal is BUY but we already own BTC/USD — skipping")
        else:
            buy_crypto()
            position = get_current_position()  # Refresh position after buying

    elif signal == "SELL":
        if position is None:
            logger.info("Signal is SELL but we don't own BTC/USD — skipping")
        else:
            sell_crypto()
            position = None

    elif signal == "HOLD":
        logger.info("Holding — no action taken")

    # Step 4: Ask AI for a market comment, then show dashboard
    balance    = get_account_balance()
    ai_comment = get_ai_comment(current_price, short_ma, long_ma, signal)
    show_dashboard(current_price, short_ma, long_ma, signal, position, balance, RUN_INTERVAL_MINUTES, ai_comment)

    logger.info("Bot finished this run")
    logger.info("=" * 50)


def main():
    """
    Start the bot and keep it running on a schedule.
    Crypto is open 24/7 so the bot runs any time of day!
    """
    logger.info("Crypto Trading Bot Starting...")
    logger.info(f"Trading pair: BTC/USD")
    logger.info(f"Will check for signals every {RUN_INTERVAL_MINUTES} minutes")

    # Run immediately once when the bot starts
    run_bot()

    # Then run every 5 minutes automatically
    schedule.every(RUN_INTERVAL_MINUTES).minutes.do(run_bot)

    logger.info(f"Scheduler started - next run in {RUN_INTERVAL_MINUTES} minutes")

    # Keep the bot running forever (until you press Ctrl+C to stop)
    while True:
        schedule.run_pending()
        time.sleep(30)


if __name__ == "__main__":
    main()
