import anthropic
from config import ANTHROPIC_API_KEY
from logger import logger

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def get_ai_comment(price, short_ma, long_ma, signal):
    """
    Ask Claude AI to write one short sentence about the current BTC market.
    Sends the price + MA data and gets back a plain-English comment.
    """
    if not ANTHROPIC_API_KEY:
        return "No Anthropic API key set — add ANTHROPIC_API_KEY to .env"

    if price is None:
        return "No price data available."

    try:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=80,
            system=[
                {
                    "type": "text",
                    "text": (
                        "You are a concise crypto market analyst. "
                        "Given BTC/USD moving average data and a signal, "
                        "write exactly ONE sentence (max 20 words) describing the market situation. "
                        "Be simple and factual. No emojis."
                    ),
                    "cache_control": {"type": "ephemeral"},
                }
            ],
            messages=[
                {
                    "role": "user",
                    "content": (
                        f"BTC/USD Price: ${price:,.2f}\n"
                        f"Short MA (9 periods): ${short_ma:,.2f}\n"
                        f"Long MA (21 periods): ${long_ma:,.2f}\n"
                        f"Signal: {signal}"
                    ),
                }
            ],
        )
        comment = response.content[0].text.strip()
        logger.info(f"AI comment: {comment}")
        return comment

    except Exception as e:
        logger.error(f"AI analyst error: {e}")
        return "AI comment unavailable."
