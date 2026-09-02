from datetime import datetime, timedelta, timezone

from config import save_config, set_date

DATE_FORMAT = "%Y-%m-%d"

PRESETS = {
    "1": ("Last 3 days",  timedelta(days=3)),
    "2": ("Last week",    timedelta(weeks=1)),
    "3": ("Last 2 weeks", timedelta(weeks=2)),
    "4": ("Last month",   timedelta(days=30)),
}


def pick_date(config):
    """Let the user choose a preset range, custom date, or use the saved date."""
    last_date = config.get("last_date")

    print("\nPick a time range:")
    for key, (label, _) in PRESETS.items():
        print(f"  {key} - {label}")
    print(f"  5 - Custom date (YYYY-MM-DD)")
    if last_date:
        print(f"  0 - Since last check ({last_date})")

    while True:
        choice = input("Select: ").strip()

        if choice == "0" and last_date:
            return input_date(config, last_date)

        if choice in PRESETS:
            _, delta = PRESETS[choice]
            cutoff = datetime.now(timezone.utc) - delta
            raw = cutoff.strftime(DATE_FORMAT)
            set_date(config, raw)
            return cutoff, raw

        if choice == "5":
            return input_date(config)

        print("Invalid choice, try again.")


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
