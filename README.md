# yt-fetcher

A command-line tool that fetches new videos from your subscribed YouTube channels and lets you download them.

It uses the **YouTube Data API v3** to list recent uploads from configured channels, then downloads the ones you pick with **yt-dlp** — with optional **SponsorBlock** support to cut out sponsor segments.

## Features

- Track multiple channels and see their recent uploads.
- Pick a time range (last 3 days / week / 2 weeks / month, a custom date, or "since last check").
- Preview each video (title, URL, publish date, duration) before downloading.
- Download at best quality via `yt-dlp`.
- Optionally remove SponsorBlock segments (sponsors, intros, self-promos, etc.) from downloads.

## Requirements

- Python 3.11+
- `ffmpeg` on your system (required for SponsorBlock segment cutting and format merging)

## Setup

1. Clone the repo and create a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Get a YouTube Data API v3 key from the [Google Cloud Console](https://developers.google.com/youtube/v3), then create a `.env` file:

   ```bash
   cp .env.example .env
   ```

   and set your key:

   ```
   API_KEY="your_api_key"
   ```

4. Add the channels you want to follow to `config.json` (see below).

5. Run it:

   ```bash
   python main.py
   ```

## Configuration (`config.json`)

The config file is loaded/saved on each run.

```json
{
    "last_date": "2026-09-08",
    "channels": [
        "https://www.youtube.com/@kenforrest",
        "https://www.youtube.com/@LowLevelTV"
    ],
    "download_path": "./videos",
    "sponsorblock_categories": ["sponsor"]
}
```

| Key | Description |
| --- | --- |
| `last_date` | The date of the last check. Update automatically after each run; used by the "Since last check" option. |
| `channels` | List of channel URLs to follow (handles like `@name` work). You can also add channels from the app's menu. |
| `download_path` | Directory where downloaded videos are saved. |
| `sponsorblock_categories` | Segment types removed from downloads. Set to `[]` to disable SponsorBlock. Supported categories: `sponsor`, `intro`, `outro`, `selfpromo`, `interaction`, `music_offtopic`. |

## Usage

When you run the app you get a menu:

```
0 - Fetch videos
1 - Add a channel
2 - Show saved channels
3 - Change API key
```

Selecting **Fetch videos** lets you choose a time range:

```
Pick a time range:
  1 - Last 3 days
  2 - Last week
  3 - Last 2 weeks
  4 - Last month
  5 - Custom date (YYYY-MM-DD)
  0 - Since last check (DATE)
```

Videos found after the cutoff are shown one at a time; type `y` to download each one or anything else to skip. After fetching, `last_date` in `config.json` is updated to today.

## Notes

- The `.env` file holds your API key and is git-ignored — never commit it.
- `download_path` defaults to `./videos` (or `./downloads` if unset).
- SponsorBlock cutting requires `ffmpeg` to be installed.
