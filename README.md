YouTube Automation

This project automates YouTube video uploads, scheduling, metadata management, and analytics using GitHub Actions.

Features

- Upload videos to YouTube.
- Set video titles, descriptions, and tags.
- Schedule videos for publication.
- Export YouTube Analytics reports.
- Run workflows through GitHub Actions.

Setup

1. Configure YouTube Data API v3 and YouTube Analytics API in Google Cloud.
2. Set up OAuth credentials for your YouTube channel.
3. Add the required credentials under GitHub repository Settings → Secrets and variables → Actions.
4. Add video files and metadata to the project.
5. Test the workflow manually before enabling automatic scheduling.

Security

Never commit API secrets, OAuth tokens, or passwords to this repository. Test with private videos first and verify each scheduled publication time.

Only upload videos you own or have permission to use.
