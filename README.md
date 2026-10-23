# YouTube Automation Starter

Includes upload and analytics scripts plus GitHub Actions workflows.

## Required GitHub Actions secrets
- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET`
- `YOUTUBE_REFRESH_TOKEN`

Google Cloud: enable YouTube Data API v3 and YouTube Analytics API. The OAuth refresh token must be authorized for both `https://www.googleapis.com/auth/youtube.upload` and `https://www.googleapis.com/auth/yt-analytics.readonly`.

## Use
1. Upload these files into the root of your `youtube-automation` repository, preserving folder paths.
2. Put video files under `videos/`.
3. Edit `metadata/schedule.csv` with the video path, title, description, semicolon-separated tags, privacy status, and optional future UTC publish time.
4. Add the three secrets under repository Settings → Secrets and variables → Actions.
5. In Actions, manually run **YouTube Analytics Export** or **YouTube Video Upload**.

Test with `privacy_status=private` first. Do not put tokens or client secrets in repository files. The sample video row is only an example; replace it before running upload. YouTube API quota, OAuth verification and channel rules may affect results.
