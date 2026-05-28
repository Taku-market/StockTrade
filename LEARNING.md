# My Python Learning Notes 📝
> Personal cheat sheet — written in plain English

---

## How `import` works

```python
from dotenv import load_dotenv
import os
```

**Plain English:**
- `from dotenv import load_dotenv` → "From the toolbox called **dotenv**, pick up the tool called **load_dotenv**"
- `import os` → "Grab the **os** toolbox — it lets Python talk to the operating system"

---

## Reading `.env` files — 2 steps

```python
load_dotenv()                        # Step 1: open the .env file, put values in memory
os.getenv("ALPACA_API_KEY")          # Step 2: read one specific value by name
```

**The analogy:**
- `load_dotenv()` = puts post-it notes up on the wall
- `os.getenv()` = reads whichever post-it note you ask for

**Example:**
If `.env` contains:
```
ALPACA_API_KEY=abc123
```
Then `os.getenv("ALPACA_API_KEY")` gives you back `"abc123"`

---

## Key insight
- `dotenv` → opens the file
- `os` → reads the values

They work as a team. You need both.

---

## Questions I asked (good ones!)
- ❓ "Can't you use `.` because the file is named `.env`?"
  → The `.` in `.env` (hidden file) and `dotenv` (library name) are completely different things

- ❓ "Does `import os` teach how to read the API inside `.env`?"
  → Close! `load_dotenv` opens the file, `os.getenv` reads the values. Two separate jobs.

---

---

## Variables — storing values in a box

```python
API_KEY = os.getenv("ALPACA_API_KEY")
```

**Plain English:** "Read the value named `ALPACA_API_KEY` from `.env`, and store it in a box called `API_KEY`"

**Two things to remember:**
- A **variable** is just a labeled box — put a value in, use the label to get it back later
- `=` in Python doesn't mean "equals" — it means **"store this into this box"** (read right-to-left)

---

## Reading multiple keys from `.env`

One line per key — each line opens one specific "locker":

```python
API_KEY    = os.getenv("ALPACA_API_KEY")
SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
BASE_URL   = os.getenv("ALPACA_BASE_URL")
```

**The locker room analogy:**
- `.env` = the whole locker room
- `os.getenv("NAME")` = open only the locker labeled `NAME`
- The label in `.env` must **exactly match** what's inside `os.getenv()`

**.env file looks like this:**
```
ALPACA_API_KEY=abc123
ALPACA_SECRET_KEY=xyz789
ALPACA_BASE_URL=https://paper-api.alpaca.markets
```

---

## ⚠️ Important security rule
- You CAN open `.env` yourself in VS Code — it's on your local machine
- **NEVER paste `.env` contents on GitHub, Discord, or anywhere public**
- Those are real secrets — anyone who gets them can use your account

---

## The complete config.py (just 7 lines!)

```python
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY    = os.getenv("ALPACA_API_KEY")
SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
BASE_URL   = os.getenv("ALPACA_BASE_URL")
```

---

## Questions I asked (good ones!)
- ❓ "How can it manage many API keys if it only calls one?"
  → One line per key! Each `os.getenv()` call reads one specific value by name

---

---

## Numbers in Python

- `0.10` = 10% (decimal form)
- `0.50` = 50%
- `1.0` = 100%

So `POSITION_SIZE = 0.10` means "spend 10% of account balance per trade"

---

## ALL_CAPS variables

```python
POSITION_SIZE = 0.10
RUN_INTERVAL_MINUTES = 10
```

Convention: ALL_CAPS means "this is a setting that doesn't change while the bot runs"
The names are **made up by us** — Python doesn't care what you call them

---

## Where does code come from?

| Thing | Where it comes from |
|-------|-------------------|
| Variable names (`SYMBOL`, `POSITION_SIZE`) | Made up by us — name anything |
| URLs (`https://paper-api.alpaca.markets`) | Alpaca's documentation |
| Functions (`os.getenv`, `load_dotenv`) | Libraries — other people's free code |

---

## Libraries — the biggest "aha" moment 💡

Someone writes a useful tool → shares it free on **PyPI** (Python's app store)

```
pip install python-dotenv   # = downloading the app
import dotenv               # = opening the app
```

- **PyPI** = App Store (everything free)
- **`pip install`** = downloading the app
- **`import`** = opening/using the app

**That's why every Python file starts with a bunch of imports — it's gathering all the tools it needs before starting. Like a chef listing ingredients before cooking.**

90% of real programming = knowing which tools exist and combining them.

---

*More notes coming as we build the bot together...*

---

---

## 🔄 Change Log: SPY Stocks → BTC/USD Crypto (2026-05-27)

**Why we changed:**
- SPY (US stocks) only trades **weekdays 9:30am–4pm US time** = 10:30pm–5am Japan time
- BTC/USD (Bitcoin) trades **24 hours, 7 days** = can run the bot any time in Japan!

---

## File 1: `config.py` — the settings file

**What changed:**
```python
# Before
SYMBOL = "SPY"

# After
SYMBOL = "BTC/USD"
```

Also **removed** these two lines (no longer needed):
```python
MARKET_OPEN = "09:30"
MARKET_CLOSE = "16:00"
```

**Why:** Crypto has no opening or closing time, so we don't need to store those values.

---

## File 2: `strategy.py` — where we fetch price data

**What changed:**

```python
# Before (stocks)
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest

data_client = StockHistoricalDataClient(API_KEY, SECRET_KEY)
bars = data_client.get_stock_bars(request)

# After (crypto)
from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest

data_client = CryptoHistoricalDataClient(API_KEY, SECRET_KEY)
bars = data_client.get_crypto_bars(request)
```

**Plain English:**
- Alpaca has **separate tools** for stocks and crypto
- `Stock___` = reads stock market data
- `Crypto___` = reads crypto market data
- Same idea, different tool — like switching from a Japanese dictionary to an English one

---

## File 3: `trader.py` — where we place buy/sell orders

**What changed:**

```python
# Before (stocks)
time_in_force=TimeInForce.DAY

# After (crypto)
time_in_force=TimeInForce.GTC
```

**What is `time_in_force`?**
It tells Alpaca: "if this order can't be filled right now, how long should you keep trying?"

| Value | Meaning | Used for |
|-------|---------|---------|
| `DAY` | Cancel at end of trading day | Stocks only |
| `GTC` | Keep trying until filled ("Good Till Cancelled") | Crypto (no end of day!) |

**Why stocks use DAY:**
The stock market closes at 4pm — any unfilled orders must be cancelled.

**Why crypto uses GTC:**
Crypto never closes — an order placed at 3am is still valid at 3pm. Keep trying!

---

## File 4: `main.py` — the scheduler / brain

**What was removed:**
The entire `is_market_open()` function:

```python
# This whole block was DELETED:
def is_market_open():
    now = datetime.now(ET)
    if now.weekday() >= 5:      # skip weekends
        return False
    return market_open <= now <= market_close

# And this check inside run_bot() was also deleted:
if not is_market_open():
    logger.info("Market is closed - skipping")
    return
```

**Why deleted:**
Crypto is always open, so checking hours would always return True — pointless code!
Removing code that does nothing = **good habit as a programmer** ✅

---

## File 5: `logger.py` — the log writer

**What changed:**
```python
# Before
logger = logging.getLogger("spy-bot")

# After
logger = logging.getLogger("crypto-bot")
```

**Plain English:**
The logger gets a name (like a label on a notebook). We renamed it to match what the bot actually does now. Small change, but keeps things honest and readable.

---

## 🎯 Key lesson from today

**Same strategy, different market.**
The Moving Average Crossover logic in `strategy.py` didn't change at all — we just pointed it at crypto data instead of stock data. This is a great example of **reusable code**:

> Write the logic once → swap the data source → works in a new market

This is how real programmers think! 🧠

---

## 🧪 Try it yourself — challenge!

Want to practice? Try switching the crypto from **BTC/USD** to **ETH/USD** (Ethereum) by yourself:

1. Open [config.py](config.py)
2. Find the line: `SYMBOL = "BTC/USD"`
3. Change it to: `SYMBOL = "ETH/USD"`
4. Save the file
5. Run `python main.py` and see if it works!

That's the only line you need to change — everything else adapts automatically! 💪

---

*More notes coming as we build the bot together...*

---

---

## ⏱️ Change Log: Run Interval 10min → 5min (2026-05-27)

**What changed — just one line in [config.py](config.py):**

```python
# Before
RUN_INTERVAL_MINUTES = 10     # Check for signals every 10 minutes

# After
RUN_INTERVAL_MINUTES = 5      # Check for signals every 5 minutes
```

**Why:** Catching a BUY/SELL crossover signal faster — the bot now checks twice as often.

---

## How does this one number control the whole schedule?

The value flows from `config.py` all the way into `main.py` automatically:

```python
# config.py — we set the number here
RUN_INTERVAL_MINUTES = 5

# main.py — it uses that number here (we never touch this line)
schedule.every(RUN_INTERVAL_MINUTES).minutes.do(run_bot)
```

**Plain English:**
- `config.py` = the **settings panel** (change numbers here)
- `main.py` = the **engine** (reads from the settings panel, runs the schedule)

This is why settings live in a separate file — you only ever need to change ONE place, not hunt through all the code!

---

## 🧪 Try it yourself — challenge!

1. Open [config.py](config.py)
2. Find: `RUN_INTERVAL_MINUTES = 5`
3. Change it to any number you like — try `1` or `15`
4. Run `python main.py` and watch the logs to confirm it runs at your new interval

➡️ **Rule of thumb:** Shorter interval = catches signals faster, but uses more API calls. 5 min is a good balance for crypto.

---

---

## 🖥️ Change Log: Terminal Dashboard UI (2026-05-28)

**What was added:** A live dashboard that displays after every bot run, so you can see what the bot is doing at a glance — instead of reading raw log lines.

**What it looks like:**
```
+--------------------------- Crypto Bot Dashboard ----------------------------+
|   BTC/USD Price         $   74,715.40                                       |
|   Short MA  (9)         $   74,721.68                                       |
|   Long MA  (21)         $   74,756.63                                       |
|                                                                             |
|   Signal                HOLD   ← green=BUY, red=SELL, yellow=HOLD          |
|   Position              None                                                |
|   Cash Balance          $100,000.00                                         |
|                                                                             |
|   Last run              07:14:48                                            |
|   Next run at           07:19:48                                            |
+-------------- BTC/USD | Paper Trading | Press Ctrl+C to stop ---------------+
```

---

## New file: `dashboard.py`

```python
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
```

**Plain English — what each import does:**

| Import | What it is | Real-world analogy |
|--------|-----------|-------------------|
| `Console` | The "printer" — sends output to terminal | A printer |
| `Table` | Rows and columns of data | A spreadsheet |
| `Panel` | A box with a border and title | A picture frame |
| `Text` | Text with a color or style | A highlighter pen |

---

## What is the `rich` library?

`rich` is a free Python library that makes terminal output beautiful.
- Without `rich`: plain white text, no borders
- With `rich`: colors, boxes, tables, progress bars

We installed it with:
```
pip install rich
```
And added it to `requirements.txt` so anyone else installing the project gets it too.

---

## How data flows into the dashboard

This is the key lesson — **functions passing data to each other**:

```
strategy.py         → returns (signal, price, short_ma, long_ma)
trader.py           → returns balance, position
         ↓
main.py             → collects all the data
         ↓
dashboard.py        → receives data → displays it
```

**Plain English:** Each file does one job. `dashboard.py` only knows how to *display* — it doesn't fetch prices or place orders. `main.py` is the coordinator that collects data from everyone and hands it to the dashboard.

---

## Why `strategy.py` changed too

Before, `get_signal()` returned 2 values:
```python
return "HOLD", current_price
```

After, it returns 4 values (added short_ma and long_ma so the dashboard can show them):
```python
return "HOLD", current_price, float(short_ma), float(long_ma)
```

And in `main.py` we unpack all 4:
```python
signal, current_price, short_ma, long_ma = get_signal()
#  ↑         ↑            ↑         ↑
# box 1    box 2        box 3     box 4
```

**Analogy:** Like ordering a combo meal — before you got burger + drink (2 items), now you get burger + drink + fries + sauce (4 items). You need 4 boxes to hold them all.

---

## 🧪 Try it yourself — challenge!

**Easy:** Change the dashboard border color from blue to another color.

1. Open [dashboard.py](dashboard.py)
2. Find this line near the bottom:
   ```python
   border_style="blue",
   ```
3. Change `"blue"` to `"green"` or `"magenta"` or `"red"`
4. Run `python main.py` and see the new color!

**Other colors you can try:** `"cyan"`, `"yellow"`, `"white"`, `"bright_blue"`

---

---

## 🤖 Change Log: AI Market Comment (2026-05-28)

**What was added:** After every 5-minute run, the bot now asks Claude AI to write one sentence about the current BTC market and shows it in the dashboard:

```
+------------- Crypto Bot Dashboard --------------+
|  BTC/USD Price      $74,715.40                  |
|  Signal             HOLD                        |
|  Cash Balance       $100,000.00                 |
|                                                 |
|  AI says   Short MA is just below Long MA,      |
|            watching for a potential crossover.  |
|                                                 |
|  Last run           07:14:48                    |
|  Next run at        07:19:48                    |
+-------------------------------------------------+
```

---

## New file: `ai_analyst.py`

```python
import anthropic

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

response = client.messages.create(
    model="claude-haiku-4-5-20251001",
    max_tokens=80,
    system=[{"type": "text", "text": "You are a crypto analyst...", "cache_control": {"type": "ephemeral"}}],
    messages=[{"role": "user", "content": "BTC price: $74,715 | Signal: HOLD"}]
)
```

**Plain English — key concepts:**

| Term | What it means |
|------|--------------|
| `anthropic.Anthropic(api_key=...)` | Open a connection to Claude AI, like logging in |
| `client.messages.create(...)` | Send a question to Claude and get a reply |
| `model="claude-haiku-..."` | Which Claude model to use (Haiku = fastest & cheapest) |
| `max_tokens=80` | Max length of the reply (1 token ≈ 1 word) |
| `system=[...]` | Instructions for Claude — "you are a crypto analyst" |
| `messages=[...]` | The actual question we're asking Claude |
| `cache_control` | Saves money — tells Claude to remember the system instructions so we don't pay for them every time |

---

## What is `cache_control`?

Every time we call the AI, we send two things:
1. **System instructions** — "you are a crypto analyst, write one sentence..."
2. **The actual question** — today's price and signal

Without caching: we pay for BOTH every single call (every 5 minutes).
With `cache_control`: Claude remembers the system instructions → we only pay for the question.

For 288 runs per day (every 5 min), this saves roughly **50% of the API cost**. Small project = small savings, but it's a professional habit worth learning early.

---

## How the data flows now (updated)

```
strategy.py    → (signal, price, short_ma, long_ma)
trader.py      → balance, position
ai_analyst.py  → ai_comment  ← NEW
      ↓
main.py        → collects everything
      ↓
dashboard.py   → displays it all
```

`ai_analyst.py` does one job: ask Claude a question and return the answer as a string. `main.py` passes that string to the dashboard.

---

## Why it shows "AI comment unavailable" if no key

In `ai_analyst.py` there's a safety check at the top:

```python
if not ANTHROPIC_API_KEY:
    return "No Anthropic API key set — add ANTHROPIC_API_KEY to .env"
```

`if not` = "if this value is empty or missing". This means the bot won't crash if you forget the key — it just shows a friendly message instead. This is called **graceful error handling** — a good coding habit.

---

## 🧪 Try it yourself — challenge!

Once you have your Anthropic API key working, try changing the AI's personality:

1. Open [ai_analyst.py](ai_analyst.py)
2. Find the system instruction text:
   ```python
   "You are a concise crypto market analyst..."
   ```
3. Change it to something fun, like:
   ```python
   "You are a pirate. Describe the crypto market in pirate language in one sentence."
   ```
4. Run `python main.py` — see what the AI says! 🏴‍☠️

---

---

## 📄 Change Log: Trade Export to CSV (2026-05-28)

**What was added:** Every time the bot places a real BUY or SELL order, it now saves a row to `logs/trades.csv` — a file you can open in Excel to review your trade history.

**What the file looks like:**
```
datetime,            action, price_usd, amount_usd, balance_after, order_id
2026-05-28 07:34:28, BUY,    74727.25,  10000.00,   90200.11,      f98b7ff5-...
2026-05-28 08:12:44, SELL,   75100.00,   9823.45,   99823.45,      a1b2c3d4-...
```

---

## New file: `trade_log.py`

```python
import csv
import os
from datetime import datetime

TRADE_FILE = "logs/trades.csv"

# Write the header row if the file doesn't exist yet
if not os.path.exists(TRADE_FILE):
    with open(TRADE_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["datetime", "action", "price_usd", ...])
```

**Plain English — key concepts:**

| Code | What it means |
|------|--------------|
| `import csv` | Load Python's built-in tool for reading/writing CSV files |
| `os.path.exists(TRADE_FILE)` | "Does this file already exist on disk?" |
| `open(..., "w")` | Open a file for **w**riting (creates it if it doesn't exist) |
| `open(..., "a")` | Open a file for **a**ppending (adds to bottom, never overwrites) |
| `csv.writer(f)` | A helper that formats data as comma-separated values |
| `writer.writerow([...])` | Write one row of data |

---

## The difference between `"w"` and `"a"`

This is an important concept in file handling:

```python
open(file, "w")   # WRITE   — starts fresh every time (erases old content!)
open(file, "a")   # APPEND  — adds to the bottom (keeps old content safe)
```

**Real-world analogy:**
- `"w"` = a whiteboard — you erase it and write fresh each time
- `"a"` = a notebook — you flip to the next blank page and add a new entry

We use `"w"` only once (to create the header), then always use `"a"` to add trade rows — so we never accidentally erase our history.

---

## What is CSV?

**CSV = Comma Separated Values** — the simplest possible spreadsheet format.

```
datetime,action,price_usd
2026-05-28 07:34:28,BUY,74727.25
```

Every program can read it: Excel, Google Sheets, Numbers, even Notepad. It's the universal language of data.

---

## 🧪 Try it yourself — challenge!

Want to open your trade history in Excel?

1. Wait for a BUY or SELL signal to happen (or let the current BUY run)
2. Open **File Explorer** → navigate to `C:\Users\tubak\Documents\spy-bot\logs\`
3. Double-click `trades.csv` — Excel opens it automatically
4. You'll see your trade history as a spreadsheet! 📊

---

---

## ⏱️ Change Log: Interval 5min → 10min (2026-05-28)

**What changed — one line in [config.py](config.py):**

```python
# Before
RUN_INTERVAL_MINUTES = 5

# After
RUN_INTERVAL_MINUTES = 10
```

**Why:** Going away for 8 hours. 5 min × 8 hrs = 96 log entries. 10 min × 8 hrs = 48 entries. Cleaner logs, same result.

---

## How to think about interval length

| Interval | Runs per 8 hrs | Good for |
|----------|---------------|---------|
| 1 min | 480 | Watching live, high frequency |
| 5 min | 96 | Active monitoring |
| 10 min | 48 | Stepping away for a few hours |
| 30 min | 16 | Leaving overnight |
| 60 min | 8 | Very slow / low activity periods |

**Key insight:** Changing the interval doesn't change the *strategy* — just how often it checks. A crossover that happens at 2pm will still be caught whether you check every 5 min or every 10 min (might just be caught a few minutes later).

---

## 🧪 Try it yourself

Before you leave, try setting it to `30` and see how few log lines appear when you come back. Then change it back to `10` when you want more frequent checks.

---

---

## 🐛 Bug Fix + Strategy Improvement (2026-05-29)

### Problem 1 — The bot kept buying over and over

**What happened:**
On 2026-05-28, the bot placed **5 BUY orders** in one day when it should have placed 1 at most. The account balance dropped from $100,000 → $59,700.

**Root cause:** A typo in `trader.py`. Alpaca stores positions with the symbol `"BTCUSD"` (no slash), but our code was asking for `"BTC/USD"` (with slash). Alpaca couldn't find it → said "no position" → bot bought again and again.

```python
# Before (broken) — asking for the wrong name
position = trading_client.get_open_position(SYMBOL)        # "BTC/USD" ← wrong!

# After (fixed) — remove the slash before asking
position = trading_client.get_open_position(SYMBOL.replace("/", ""))  # "BTCUSD" ← correct
```

**The analogy:** It's like searching for a contact named "田中 太郎" but the phonebook stores them as "田中太郎" (no space). You search, find nothing, and think the person doesn't exist — but they do, you just asked the wrong way.

---

### Problem 2 — False BUY signals on tiny movements

**What happened:**
Even with the position bug fixed, the strategy was too sensitive. At 15:50, the Short MA and Long MA were only **$0.02 apart** on a $74,000 price — and the bot still triggered a BUY. That's a 0.003% difference, basically noise.

**The fix — add a minimum gap rule in `strategy.py`:**

```python
# New setting in config.py
MIN_GAP_PERCENT = 0.05   # MAs must be at least 0.05% apart to act

# New check in strategy.py
gap_percent = abs(short_ma - long_ma) / long_ma * 100

if gap_percent < MIN_GAP_PERCENT:
    return "HOLD"   # Too close — probably just noise, don't act
```

**The analogy:** Imagine you only cross the road when the traffic light is clearly green — not when it's flickering between green and yellow. The gap filter is that "clearly green" check.

**Before vs after (yesterday's 5 BUYs):**

| Time | Gap | Before fix | After fix |
|------|-----|-----------|-----------|
| 07:34 | 0.006% | BUY ❌ | HOLD ✅ |
| 08:28 | 0.001% | BUY ❌ | HOLD ✅ |
| 09:58 | 0.001% | BUY ❌ | HOLD ✅ |
| 15:50 | 0.000% | BUY ❌ | HOLD ✅ |
| 18:41 | 0.006% | BUY ❌ | HOLD ✅ |

Result: **5 false BUYs → 0 false BUYs** ✅

---

### New tool — `reset_positions.py`

We also wrote a standalone script to close all open positions via API (useful for emergencies):

```python
python reset_positions.py
```

What it does:
1. Cancels all open orders
2. Shows all open BTC positions
3. Sells everything at current market price
4. Prints your final cash balance

**Why this is useful:** Sometimes the Alpaca website doesn't show a "Reset" button clearly. This script lets you clean up directly from the terminal without touching the website.

---

## 📊 Trading lesson — how often should a bot trade?

With a Moving Average Crossover strategy, the ideal pattern per day is:

```
Wait → BUY (trend starts) → Hold → SELL (trend ends) → Wait → repeat
```

**Ideal: 1–2 trades per day.** More than that usually means false signals in a sideways market.

**Sideways market** = price moves up and down in a small range with no clear direction. The MAs keep crossing each other because neither side has momentum. This is when bots generate the most false signals.

**Trending market** = price clearly going up or clearly going down. MAs separate cleanly. One BUY at the start, one SELL at the end. Perfect.

---

## 🧪 Try it yourself — challenge!

Try adjusting the gap filter and see how it changes the bot's behavior:

1. Open [config.py](config.py)
2. Find: `MIN_GAP_PERCENT = 0.05`
3. Try changing it to `0.10` (stricter — even fewer signals)
4. Or try `0.02` (looser — more signals, but more false ones too)

Watch the logs — you'll see the gap % printed every run. When does it trigger? When does it block?

**Rule of thumb:** Higher gap = fewer but higher quality signals. Lower gap = more signals but more noise.
