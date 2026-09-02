from config import load_config
from input import pick_date, add_channel
from output import print_video, show_channels
from logic import (
    check_api_key,
    build_youtube_client,
    set_current_date,
    extract_handle,
    get_channel_id,
    get_uploads_playlist_id,
    get_videos_after_date,
    download_video,
)


def fetch_and_show(youtube, channels, cutoff, raw):
    print(f"\nLoaded {len(channels)} channel(s)\n")
    print("=" * 60)

    for url in channels:
        handle = extract_handle(url)
        if not handle:
            print(f"Skipping unrecognised URL: {url}\n")
            continue

        print(f"\nChannel: @{handle}")
        print(f"URL: {url}")
        print("-" * 60)

        channel_id = get_channel_id(youtube, handle)
        if not channel_id:
            print(f"Could not resolve @{handle} to a channel ID. Skipping.\n")
            continue

        playlist_id = get_uploads_playlist_id(youtube, channel_id)
        if not playlist_id:
            print(f"Could not find uploads playlist. Skipping.\n")
            continue

        videos = get_videos_after_date(youtube, playlist_id, cutoff)

        if not videos:
            print(f"No videos found after {raw}.\n")
        else:
            print(f"Found {len(videos)} video(s) after {raw}:\n")
            for video in videos:
                print_video(video)
                if input("Download Y/n: ") in ("Y", "y", ""):
                    download_video(video['url'])

    print("=" * 60)
    print("Done.")


def main():
    check_api_key()
    config = load_config()
    youtube = build_youtube_client()

    while True:
        choice = input(
            "\n0 - Fetch videos\n"
            "1 - Add a channel\n"
            "2 - Show saved channels\n"
            "3 - Change API key\n"
            "Select: "
        )

        if not choice.isdigit():
            print("Please enter a number.")
            continue

        match int(choice):
            case 0:
                cutoff, raw = pick_date(config)
                fetch_and_show(youtube, config["channels"], cutoff, raw)
                set_current_date()
                break
            case 1:
                add_channel(config)
            case 2:
                show_channels(config)
            case 3:
                key = input('\nEnter your API key (for permanent, change .env): ')
                youtube = build_youtube_client(key)
            case _:
                print("Invalid option.")


if __name__ == "__main__":
    main()
