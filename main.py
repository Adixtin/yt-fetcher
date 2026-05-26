from googleapiclient.discovery import build

from config import load_config
from input import input_date, add_channel, read_channels
from output import print_video
from logic import (
    API_KEY,
    check_api_key,
    extract_handle,
    get_channel_id,
    get_uploads_playlist_id,
    get_videos_after_date,
    download_video,
)

api_key = API_KEY

CHANNELS_FILE = "channels.txt"


def print_and_download_channels(cutoff, raw):
    youtube = build("youtube", "v3", developerKey=api_key)
    channel_urls = read_channels(CHANNELS_FILE)

    print(f"\nLoaded {len(channel_urls)} channel(s) from '{CHANNELS_FILE}'\n")
    print("=" * 60)

    for url in channel_urls:
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


check_api_key()

config = load_config()
date = config['last_date']
cutoff, raw = input_date(config, date)

while True:
    choice = int(input('''
0 - Show recent\n
1 - Add a channel\n
2 - Set a custom date\n
3 - Change API key\n
Select: '''))
    match choice:
        case 0:
            print_and_download_channels(cutoff, raw)
            break
        case 1:
            add_channel(config)
        case 2:
            cutoff, raw = input_date(config)
        case 3:
            api_key = input('\n Enter your api key (for permenent, change .env): ')
        case _:
            print_and_download_channels(cutoff, raw)
            break
