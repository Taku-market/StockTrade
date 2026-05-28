import logging
import os
import sys
from datetime import datetime

# Create a "logs" folder if it doesn't exist yet
os.makedirs("logs", exist_ok=True)

# Create a log file name using today's date (e.g. "logs/2026-05-23.log")
log_filename = f"logs/{datetime.now().strftime('%Y-%m-%d')}.log"

# Log format: "2026-05-23 09:35:00 | INFO | message"
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s", datefmt="%Y-%m-%d %H:%M:%S")

# File handler - saves to log file with UTF-8 encoding
file_handler = logging.FileHandler(log_filename, encoding="utf-8")
file_handler.setFormatter(formatter)

# Stream handler - prints to terminal with UTF-8 encoding
# (needed for Japanese Windows which defaults to cp932)
stream_handler = logging.StreamHandler(
    stream=open(sys.stdout.fileno(), mode="w", encoding="utf-8", buffering=1, closefd=False)
)
stream_handler.setFormatter(formatter)

# Create the logger object - we'll import this in other files
logger = logging.getLogger("crypto-bot")
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(stream_handler)
