import csv
import os
from datetime import date, timedelta
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def main():
    keys = ("GOOGLE_CLIENT_ID", "GOOGLE_CLIENT_SECRET", "YOUTUBE_REFRESH_TOKEN")
    missing = [k for k in keys if not os.environ.get(k)]
    if missing:
        raise RuntimeError("Missing GitHub Actions secret(s): " + ", ".join(missing))
    credentials = Credentials(
        token=None, refresh_token=os.environ["YOUTUBE_REFRESH_TOKEN"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.environ["GOOGLE_CLIENT_ID"],
        client_secret=os.environ["GOOGLE_CLIENT_SECRET"],
        scopes=["https://www.googleapis.com/auth/yt-analytics.readonly"],
    )
    api = build("youtubeAnalytics", "v2", credentials=credentials)
    end = date.today() - timedelta(days=1)
    start = end - timedelta(days=27)
    data = api.reports().query(
        ids="channel==MINE", startDate=start.isoformat(), endDate=end.isoformat(),
        metrics="views,estimatedMinutesWatched,averageViewDuration,subscribersGained,subscribersLost,likes,comments,shares",
        dimensions="day", sort="day"
    ).execute()
    folder = Path("reports")
    folder.mkdir(exist_ok=True)
    path = folder / "youtube_analytics_last_28_days.csv"
    with path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow([h["name"] for h in data.get("columnHeaders", [])])
        writer.writerows(data.get("rows", []))
    print(f"Saved {len(data.get('rows', []))} daily rows to {path}")

if __name__ == "__main__":
    main()
