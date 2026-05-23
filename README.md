# StockTrade - Automated SPY Paper Trading Bot

An automated stock trading bot built with Python and Alpaca Markets API.
This is a learning project to explore AI, automation, and investing — starting with paper trading (no real money).

---

## What It Does

Every 10 minutes during US market hours, the bot automatically:

1. Fetches live SPY (S&P 500 ETF) price data from Alpaca
2. Calculates Moving Averages to detect market momentum
3. Decides to BUY, SELL, or HOLD based on the strategy
4. Executes the trade via Alpaca paper trading account
5. Logs every decision with timestamp and reason

---

## Strategy — Moving Average Crossover

The bot uses a classic **9-period vs 21-period Moving Average Crossover** strategy.

```
Short MA (9 periods)  = average of last 45 minutes of price data  → reacts fast
Long MA  (21 periods) = average of last 105 minutes of price data → shows trend

BUY  signal: Short MA crosses ABOVE Long MA (price gaining momentum)
SELL signal: Short MA crosses BELOW Long MA (price losing momentum)
HOLD:        No crossover detected (wait and see)
```

---

## Risk Management

| Setting | Value | Meaning |
|---------|-------|---------|
| Position size | 10% of account | Spend $10,000 per trade on a $100,000 account |
| Stop-loss | 2% | Auto-sell if price drops 2% from buy price |
| Market hours | 9:30am - 4:00pm ET | Only trades when market is open |

---

## Project Structure

```
StockTrade/
├── main.py          → Entry point — runs the bot on a schedule
├── strategy.py      → Moving Average Crossover logic (brain of the bot)
├── trader.py        → Connects to Alpaca API to buy/sell SPY
├── logger.py        → Logs every decision to terminal and log file
├── config.py        → All settings in one place (symbol, risk, schedule)
├── requirements.txt → Python libraries needed
├── .env.example     → Template showing what API keys are needed
└── .env             → Your secret API keys (never uploaded to GitHub)
```

---

## How to Run

### 1. Clone the repo
```
git clone https://github.com/Taku-market/StockTrade.git
cd StockTrade
```

### 2. Install dependencies
```
pip install -r requirements.txt
```

### 3. Set up API keys
```
copy .env.example .env
```
Then open `.env` and add your Alpaca paper trading API keys from:
https://app.alpaca.markets/paper-trading/overview

```
ALPACA_API_KEY=your_api_key_here
ALPACA_SECRET_KEY=your_secret_key_here
```

### 4. Run the bot
```
python main.py
```

Press `Ctrl+C` to stop.

---

## Example Output

```
2026-05-26 09:35:00 | INFO | SPY Trading Bot Starting...
2026-05-26 09:35:00 | INFO | Bot running...
2026-05-26 09:35:00 | INFO | No current position in SPY
2026-05-26 09:35:00 | INFO | SPY Price: $512.30 | Short MA: $511.20 | Long MA: $510.80
2026-05-26 09:35:00 | INFO | Signal: BUY - Short MA crossed above Long MA
2026-05-26 09:35:00 | INFO | Account cash balance: $100,000.00
2026-05-26 09:35:00 | INFO | BUY order placed: $10,000.00 worth of SPY
```

---

## Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.14 | Core programming language |
| alpaca-py | Alpaca Markets API client |
| pandas | Price data processing and moving average calculation |
| schedule | Runs the bot every 10 minutes automatically |
| python-dotenv | Safely loads API keys from .env file |

---

## Roadmap

- [x] Base automation pipeline (Moving Average Crossover)
- [x] Risk management (position sizing + stop-loss)
- [x] Scheduled execution during market hours
- [x] Logging to file and terminal
- [ ] Add AI/ML model to improve signals
- [ ] Email/Slack notifications on trades
- [ ] Backtesting on historical data
- [ ] Deploy to cloud server (VPS) for 24/7 running
- [ ] Expand to multiple stocks

---

## Notes

- This is a **paper trading** project — no real money is used
- Built as a learning project to explore Python, automation, and investing
- Strategy will be improved over time as investment knowledge grows

---

*Built with Python + Alpaca Markets API*
