
import os
import csv
from datetime import date, timedelta
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

CLIENT_ID = os.environ["GOOGLE_CLIENT_ID"]
CLIENT_SECRET = os.environ["GOOGLE_CLIENT_SECRET"]
REFRESH_TOKEN = os.environ["YOUTUBE_REFRESH_TOKEN"]

credentials = Credentials(
    None,
    refresh_token=REFRESH_TOKEN,
    token_uri="https://oauth2.googleapis.com/token",
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    scopes=["https://www.googleapis.com/auth/yt-analytics.readonly"],
)

youtube_analytics = build(
    "youtubeAnalytics", "v2", credentials=credentials
)

end_date = date.today()
start_date = end_date - timedelta(days=28)

report = youtube_analytics.reports().query(
    ids="channel==MINE",
    startDate=start_date.isoformat(),
    endDate=end_date.isoformat(),
    metrics="views,likes,comments,estimatedMinutesWatched",
    dimensions="day",
    sort="day",
).execute()

os.makedirs("analytics", exist_ok=True)

with open("analytics/youtube_analytics.csv", "w",
          newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(report.get("columnHeaders", []))
    writer.writerows(report.get("rows", []))

print("Analytics CSV created successfully.")
