
import os
import csv
from datetime import datetime, timezone
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload"
]

def get_youtube():
    credentials = Credentials(
        None,
        refresh_token=os.environ["YOUTUBE_REFRESH_TOKEN"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.environ["GOOGLE_CLIENT_ID"],
        client_secret=os.environ["GOOGLE_CLIENT_SECRET"],
        scopes=SCOPES,
    )
    return build("youtube", "v3", credentials=credentials)

def main():
    youtube = get_youtube()
    schedule_file = "metadata/schedule.csv"

    with open(schedule_file, newline="", encoding="utf-8") as file:
        videos = list(csv.DictReader(file))

    if not videos:
        print("No videos scheduled.")
        return

    video = videos[0]
    video_path = video["video_path"]

    if not os.path.isfile(video_path):
        raise FileNotFoundError(f"Video not found: {video_path}")

    publish_at = datetime.fromisoformat(
        video["publish_at"].replace("Z", "+00:00")
    )
    if publish_at.tzinfo is None:
        publish_at = publish_at.replace(tzinfo=timezone.utc)

    body = {
        "snippet": {
            "title": video["title"],
            "description": video["description"],
            "tags": [tag.strip() for tag in video["tags"].split(",") if tag.strip()],
            "categoryId": video.get("category_id", "22"),
        },
        "status": {
            "privacyStatus": "private",
            "publishAt": publish_at.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
            "selfDeclaredMadeForKids": False,
        },
    }

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=MediaFileUpload(video_path, resumable=True),
    )
    result = request.execute()
    print("Upload successful. Video ID:", result["id"])

if __name__ == "__main__":
    main()
  
