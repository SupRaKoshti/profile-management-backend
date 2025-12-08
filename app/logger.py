import logging
import sys
from datetime import datetime
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

logger = logging.getLogger("profile_management")
logger.setLevel(logging.DEBUG)

# Create formatters
detailed_formatter = logging.Formatter(
    "[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

simple_formatter = logging.Formatter(
    "[%(asctime)s] %(levelname)s: %(message)s",
    datefmt="%H:%M:%S"
)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(simple_formatter)

file_handler = logging.FileHandler(
    LOG_DIR / f"app_{datetime.now().strftime('%Y%m%d')}.log"
)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(detailed_formatter)

error_handler = logging.FileHandler(
    LOG_DIR / f"error_{datetime.now().strftime('%Y%m%d')}.log"
)
error_handler.setLevel(logging.ERROR)
error_handler.setFormatter(detailed_formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)
logger.addHandler(error_handler)

logger.propagate = False