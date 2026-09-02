import json
from datetime import timezone
import os
import re
import sys
from datetime import datetime
# pyrefly: ignore [missing-import]
from googleapiclient.errors import HttpError
import yt_dlp
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")


def check_api_key():
    if not API_KEY:
        print("Error: No API key found.")
        print("Set it up inside your .env")
        sys.exit(1)


def build_youtube_client(api_key=None):
    """Build and return a YouTube Data API v3 service object."""
    # pyrefly: ignore [missing-import]
    from googleapiclient.discovery import build
    return build("youtube", "v3", developerKey=api_key or API_KEY)


def parse_duration(iso_duration: str) -> str:
    pattern = r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?"
    match = re.fullmatch(pattern, iso_duration)
    if not match:
        return "Unknown"
    hours = int(match.group(1) or 0)
    minutes = int(match.group(2) or 0)
    seconds = int(match.group(3) or 0)
    if hours:
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    return f"{minutes}:{seconds:02d}"


def extract_handle(url: str) -> str | None:
    match = re.search(r"youtube\.com/@([\w.-]+)", url)
    return match.group(1) if match else None


def get_channel_id(youtube, handle: str) -> str | None:
    try:
        response = youtube.channels().list(
            part="id",
            forHandle=handle
        ).execute()
        items = response.get("items", [])
        return items[0]["id"] if items else None
    except HttpError as e:
        print(f"[API error resolving handle @{handle}]: {e}")
        return None


def get_uploads_playlist_id(youtube, channel_id: str) -> str | None:
    try:
        response = youtube.channels().list(
            part="contentDetails",
            id=channel_id
        ).execute()
        items = response.get("items", [])
        if not items:
            return None
        return items[0]["contentDetails"]["relatedPlaylists"]["uploads"]
    except HttpError as e:
        print(f"  [API error fetching playlist for {channel_id}]: {e}")
        return None


def get_video_durations(youtube, video_ids: list[str]) -> dict[str, str]:
    """Batch-fetch durations for a list of video IDs."""
    if not video_ids:
        return {}
    try:
        response = youtube.videos().list(
            part="contentDetails",
            id=",".join(video_ids)
        ).execute()
    except HttpError as e:
        print(f"  [API error fetching durations]: {e}")
        return {}

    return {
        item["id"]: parse_duration(item["contentDetails"]["duration"])
        for item in response.get("items", [])
    }


def get_videos_after_date(youtube, playlist_id: str, after: datetime) -> list[dict]:
    videos = []
    next_page_token = None

    while True:
        try:
            response = youtube.playlistItems().list(
                part="snippet,contentDetails",
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page_token
            ).execute()
        except HttpError as e:
            print(f"  [API error fetching playlist items]: {e}")
            break

        items = response.get("items", [])
        if not items:
            break

        video_ids = [item["contentDetails"]["videoId"] for item in items]
        durations = get_video_durations(youtube, video_ids)

        stop_early = False
        for item in items:
            snippet = item["snippet"]
            raw_date = snippet.get("publishedAt", "")
            published = datetime.fromisoformat(raw_date.replace("Z", "+00:00"))

            if published < after:
                stop_early = True
                continue

            video_id = item["contentDetails"]["videoId"]
            videos.append({
                "title":     snippet.get("title", "Unknown Title"),
                "url":       f"https://www.youtube.com/watch?v={video_id}",
                "published": published.strftime("%Y-%m-%d"),
                "duration":  durations.get(video_id, "Unknown"),
            })

        next_page_token = response.get("nextPageToken")
        if not next_page_token or stop_early:
            break

    return videos


def download_video(url, output_path="./downloads"):
    options = {
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
        'format': 'best',
    }
    with yt_dlp.YoutubeDL(options) as ydl:
        ydl.download([url])

def set_current_date():
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    with open("./config.json", "r") as f:
        config = json.load(f)
    config["last_date"] = now
    with open("./config.json", "w") as f:
        json.dump(config, f, indent=4)
    print(f"Set last date to {now}")