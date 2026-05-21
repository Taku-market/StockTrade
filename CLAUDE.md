# SPY Paper Trading Bot — Project Context

## What This Project Is
An automated paper trading bot for SPY (S&P 500 ETF) built with Python and Alpaca Markets API.
Goal: Learn AI/Python/investing by building a real automation pipeline, then gradually improve the strategy.

## Owner
- GitHub: Taku-market
- Skill level: Beginner Python, no investment background

## Key Decisions Made
| Decision | Choice | Reason |
|----------|--------|--------|
| Market | US Stocks | Most accessible for beginners |
| Platform | Alpaca (paper trading) | Free API, no real money |
| Stock | SPY | Most traded ETF, stable, good for learning |
| Strategy | Moving Average Crossover (9 vs 21 period) | Simple, classic, easy to understand |
| Schedule | Every 10 min during market hours (9:30am–4:00pm ET) | Automated, easy to debug |
| Position size | 10% of account per trade | Low risk while learning |
| Stop-loss | 2% below buy price | Protects against big losses |
| Monitoring | Log file + console output | Simple, no extra complexity |
| Deployment | Local machine → VPS later | Zero cost while learning |

## Strategy Explained (for beginners)
**Moving Average Crossover:**
- Calculate the average price over the last 9 candles (Short MA)
- Calculate the average price over the last 21 candles (Long MA)
- 📈 Short MA crosses ABOVE Long MA → BUY signal
- 📉 Short MA crosses BELOW Long MA → SELL signal
- Each candle = 5 minutes of price data

## Project Structure (target)
```
spy-bot/
├── CLAUDE.md          ← you are here (project context for Claude)
├── README.md          ← public description for GitHub visitors
├── .gitignore         ← protects .env from being uploaded ✅
├── .env               ← your secret Alpaca API keys (never commit this)
├── .env.example       ← safe template showing what keys are needed ✅
├── requirements.txt   ← Python libraries needed ✅
├── config.py          ← loads API keys and settings ⬜
├── logger.py          ← logs every bot decision to file + console ⬜
├── strategy.py        ← Moving Average crossover logic ⬜
├── trader.py          ← connects to Alpaca, buys/sells SPY ⬜
├── main.py            ← runs everything on a schedule ⬜
└── logs/              ← trade log files (auto-created) ⬜
```
✅ = done | ⬜ = not started yet

## Current Status
- [x] Python 3.14 installed
- [x] VS Code installed
- [x] Git configured (user: Taku-market)
- [x] Project folder created: C:\Users\tubak\Documents\spy-bot
- [x] Libraries installed (alpaca-py, pandas, python-dotenv, schedule)
- [x] .gitignore, .env.example, requirements.txt created and committed
- [ ] Alpaca account API keys → copy .env.example to .env and fill in keys
- [ ] Write config.py
- [ ] Write logger.py
- [ ] Write strategy.py
- [ ] Write trader.py
- [ ] Write main.py
- [ ] Test run with paper trading
- [ ] Push to GitHub and write README.md

## Next Step When Resuming
1. User gets Alpaca API keys from: https://app.alpaca.markets/paper-trading/overview
2. Run: `copy .env.example .env` in terminal
3. Open .env in VS Code and paste real API keys
4. Then we write config.py together

## How to Run (once complete)
```
cd C:\Users\tubak\Documents\spy-bot
python main.py
```

## Future Improvements (Phase 2+)
- Add AI/ML model to replace simple MA crossover
- Add email/Slack notifications on trades
- Expand from SPY to a watchlist of stocks
- Move to cloud VPS for 24/7 running
- Backtest strategy on historical data
