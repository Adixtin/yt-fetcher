def print_video(video: dict) -> None:
    print(f"  Title:     {video['title']}")
    print(f"  URL:       {video['url']}")
    print(f"  Published: {video['published']}")
    print(f"  Duration:  {video['duration']}")
    print()


def show_channels(config):
    if not config["channels"]:
        print("No channels saved.")
        return

    print("\nSaved channels:")

    for channel in config["channels"]:
        print("-", channel)
