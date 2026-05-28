from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

from config import API_KEY, SECRET_KEY, SYMBOL, POSITION_SIZE, STOP_LOSS_PCT
from logger import logger
from trade_log import log_trade


# Connect to Alpaca for trading (paper trading - not real money!)
trading_client = TradingClient(API_KEY, SECRET_KEY, paper=True)


def get_account_balance():
    """
    Get how much cash we have available to spend.
    Alpaca gives $100,000 by default for paper trading.
    """
    account = trading_client.get_account()
    balance = float(account.cash)
    logger.info(f"Account cash balance: ${balance:,.2f}")
    return balance


def get_current_position():
    """
    Check if we already own BTC/USD.
    Returns the position object if we own it, or None if we don't.
    """
    try:
        position = trading_client.get_open_position(SYMBOL.replace("/", ""))
        qty = float(position.qty)
        avg_price = float(position.avg_entry_price)
        current_price = float(position.current_price)
        logger.info(f"Current position: {qty:.6f} BTC | Avg buy price: ${avg_price:,.2f} | Current: ${current_price:,.2f}")
        return position
    except Exception:
        # No position found — we don't own BTC right now
        logger.info("No current position in BTCUSD")
        return None


def check_stop_loss(position):
    """
    Check if the price has dropped 2% below our buy price.
    If yes, we should sell immediately to cut our losses.
    """
    avg_buy_price = float(position.avg_entry_price)
    current_price = float(position.current_price)
    stop_loss_price = avg_buy_price * (1 - STOP_LOSS_PCT)  # 2% below buy price

    if current_price <= stop_loss_price:
        logger.info(f"Stop-loss triggered! Bought at ${avg_buy_price:,.2f}, now ${current_price:,.2f} (limit was ${stop_loss_price:,.2f})")
        return True

    return False


def buy_crypto():
    """
    Buy BTC/USD using 10% of our available cash balance.
    Uses a Market Order — buys immediately at the current market price.
    Uses GTC (Good Till Cancelled) because crypto has no end-of-day closing.
    """
    balance = get_account_balance()
    amount_to_spend = balance * POSITION_SIZE  # 10% of account

    # Place the order using dollar amount (fractional BTC is allowed)
    order = MarketOrderRequest(
        symbol=SYMBOL,
        notional=round(amount_to_spend, 2),  # Dollar amount to spend
        side=OrderSide.BUY,
        time_in_force=TimeInForce.GTC  # Good Till Cancelled — works for 24/7 crypto
    )

    result = trading_client.submit_order(order)
    logger.info(f"BUY order placed: ${amount_to_spend:,.2f} worth of {SYMBOL} | Order ID: {result.id}")
    balance_after = get_account_balance()
    log_trade("BUY", None, amount_to_spend, balance_after, result.id)
    return result


def sell_crypto():
    """
    Sell ALL BTC/USD we currently own.
    Uses a Market Order — sells immediately at the current market price.
    """
    position = get_current_position()

    if position is None:
        logger.info("Tried to sell but we don't own any BTCUSD")
        return None

    qty = float(position.qty)

    order = MarketOrderRequest(
        symbol=SYMBOL,
        qty=round(qty, 8),       # Sell all BTC we own (8 decimal places for crypto)
        side=OrderSide.SELL,
        time_in_force=TimeInForce.GTC  # Good Till Cancelled
    )

    result = trading_client.submit_order(order)
    logger.info(f"SELL order placed: {qty:.6f} BTC of {SYMBOL} | Order ID: {result.id}")
    sell_price = float(position.current_price)
    balance_after = get_account_balance()
    log_trade("SELL", sell_price, qty * sell_price, balance_after, result.id)
    return result
