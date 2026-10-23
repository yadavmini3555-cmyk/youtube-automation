import os
import csv
from datetime import date, timedelta
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

client_id = os.environ["GOOGLE_CLIENT_ID"]
client_secret = os.environ["GOOGLE_CLIENT_SECRET"]
refresh_token = os.environ["YOUTUBE_REFRESH_TOKEN"]

credentials = Credentials(
    None,
    refresh_token=refresh_token,
    token_uri="https://oauth2.googleapis.com/token",
    client_id=client_id,
    client_secret=client_secret,
    scopes=[
        "https://www.googleapis.com/auth/yt-analytics.readonly"
    ],
)

youtube_analytics = build(
    "youtubeAnalytics", "v2", credentials=credentials
)

end_date = date.today() - timedelta(days=1)
start_date = end_date - timedelta(days=27)

response = youtube_analytics.reports().query(
    ids="channel==MINE",
    startDate=start_date.isoformat(),
    endDate=end_date.isoformat(),
    metrics="views,estimatedMinutesWatched,subscribersGained",
    dimensions="day",
).execute()

os.makedirs("analytics", exist_ok=True)

with open("analytics/youtube_analytics.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(response.get("columnHeaders", []))
    writer.writerows(response.get("rows", []))

print("Analytics CSV created successfully.")
