import csv, os
from datetime import datetime, timezone
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCHEDULE = Path("metadata/schedule.csv")
UPLOADED = Path("metadata/uploaded.csv")

def main():
    keys = ("GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET", "YOUTUBE_REFRESH_TOKEN")
    missing = [k for k in keys if not os.environ.get(k)]
    if missing:
        raise RuntimeError("Missing GitHub Actions secret(s): " + ", ".join(missing))
    with SCHEDULE.open(newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        print("No videos queued.")
        return
    item = rows[0]
    video = Path(item["video_path"])
    if not video.is_file():
        raise FileNotFoundError(f"Video not found: {video}. Add it to the repository and check the CSV path.")
    credentials = Credentials(
        token=None, refresh_token=os.environ["YOUTUBE_REFRESH_TOKEN"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.environ["GOOGLE_CLIENT_ID"],
        client_secret=os.environ["GOOGLE_CLIENT_SECRET"],
        scopes=["https://www.googleapis.com/auth/youtube.upload"],
    )
    yt = build("youtube", "v3", credentials=credentials)
    privacy = (item.get("privacy_status") or "private").strip().lower()
    publish_at = (item.get("publish_at") or "").strip()
    status = {"privacyStatus": privacy}
    if publish_at:
        if privacy != "private":
            raise ValueError("Scheduled publishing requires privacy_status=private.")
        dt = datetime.fromisoformat(publish_at.replace("Z", "+00:00"))
        if dt.tzinfo is None or dt <= datetime.now(timezone.utc):
            raise ValueError("publish_at must be a future timezone-aware time, e.g. 2026-10-25T03:30:00Z")
        status["publishAt"] = dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")
    tags = [x.strip() for x in (item.get("tags") or "").split(";") if x.strip()]
    body = {"snippet": {"title": item["title"][:100], "description": item.get("description", ""),
                         "tags": tags, "categoryId": "22"}, "status": status}
    request = yt.videos().insert(part="snippet,status", body=body,
        media_body=MediaFileUpload(str(video), chunksize=-1, resumable=True))
    response = None
    while response is None:
        _, response = request.next_chunk()
    UPLOADED.parent.mkdir(parents=True, exist_ok=True)
    new_file = not UPLOADED.exists() or UPLOADED.stat().st_size == 0
    with UPLOADED.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if new_file:
            writer.writerow(["uploaded_at", "video_path", "title", "video_id", "status"])
        writer.writerow([datetime.now(timezone.utc).isoformat(), item["video_path"], item["title"], response["id"], status["privacyStatus"]])
    with SCHEDULE.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["video_path","title","description","tags","privacy_status","publish_at"])
        writer.writeheader()
        writer.writerows(rows[1:])
    print("Uploaded video ID:", response["id"])

if __name__ == "__main__":
    main()
