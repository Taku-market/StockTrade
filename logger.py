import logging
import os
from datetime import datetime

# Create a "logs" folder if it doesn't exist yet
os.makedirs("logs", exist_ok=True)

# Create a log file name using today's date (e.g. "logs/2026-05-23.log")
log_filename = f"logs/{datetime.now().strftime('%Y-%m-%d')}.log"

# Set up the logger
logging.basicConfig(
    level=logging.INFO,  # Log everything at INFO level and above
    format="%(asctime)s | %(levelname)s | %(message)s",  # e.g. "2026-05-23 09:35:00 | INFO | Bought SPY at $512.30"
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[
        logging.FileHandler(log_filename),   # Save logs to a file
        logging.StreamHandler()              # Also print logs to the terminal
    ]
)

# Create the logger object — we'll import this in other files
logger = logging.getLogger("spy-bot")
