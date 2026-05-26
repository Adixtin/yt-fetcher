import json
from pathlib import Path

CONFIG_FILE = Path("config.json")


def load_config():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)

    return {
        "last_date": None,
        "channels": []
    }


def save_config(config):
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file, indent=4)


def set_date(config, raw: str):
    config["last_date"] = raw
    save_config(config)
