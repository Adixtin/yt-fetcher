import os
import sys
from datetime import datetime, timezone

from config import save_config, set_date

DATE_FORMAT = "%Y-%m-%d"


def input_date(config, last_date=None):
    while True:
        if last_date is None:
            raw = input("Pick a date - YYYY-MM-DD: ").strip()
        else:
            raw = last_date.strip()
        try:
            cutoff_naive = datetime.strptime(raw, DATE_FORMAT)
            cutoff = cutoff_naive.replace(tzinfo=timezone.utc)
            break
        except ValueError:
            print('Pick a date - YYYY-MM-DD')
            last_date = None  # bad stored value → fall back to user input
    set_date(config, raw)
    return cutoff, raw


def add_channel(config):
    channel = input("Enter channel URL: ")
    config["channels"].append(channel)
    save_config(config)
    print("Channel added.")


def read_channels(filepath: str) -> list[str]:
    """Read channel URLs from a text file, one per line."""
    if not os.path.exists(filepath):
        print(f"Error: File '{filepath}' not found.")
        sys.exit(1)
    with open(filepath, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    return [line for line in lines if not line.startswith("#")]
