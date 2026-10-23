
import os
import csv
from pathlib import Path
from datetime import date, timedelta

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/yt-analytics.readonly"
]

def main():
    credentials = Credentials(
        None,
        refresh_token=os.environ["YOUTUBE_REFRESH_TOKEN"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.environ["GOOGLE_CLIENT_ID"],
        client_secret=os.environ["GOOGLE_CLIENT_SECRET"],
        scopes=SCOPES,
    )

    service = build(
        "youtubeAnalytics", "v2",
        credentials=credentials
    )

    end_date = date.today() - timedelta(days=2)
    start_date = end_date - timedelta(days=27)

    result = service.reports().query(
        ids="channel==MINE",
        startDate=start_date.isoformat(),
        endDate=end_date.isoformat(),
        metrics="views,estimatedMinutesWatched,subscribersGained,subscribersLost",
        dimensions="day",
        sort="day",
    ).execute()

    headers = [
        item["name"]
        for item in result.get("columnHeaders", [])
    ]

    Path("reports").mkdir(exist_ok=True)

    with open(
        "reports/youtube_analytics.csv",
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(result.get("rows", []))

    print("Analytics CSV exported successfully.")

if __name__ == "__main__":
    main()
  
