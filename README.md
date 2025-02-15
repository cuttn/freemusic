# 🎵 Spotify-DL: Your Music, Your Way

A sleek wrapper around yt-dlp that integrates with the Spotify API, letting you manage your music library through a clean web interface. Download your playlists and favorite tracks with just a few clicks!

## ✨ Features

- Sign in with your Spotify account using OAuth2
- Download your entire library, playlists, or specific albums
- Clean, simple web interface
- Powered by yt-dlp under the hood
- Built with Django for reliability

## 🚀 Getting Started

### Option 1: Docker (Recommended)

The easiest way to get up and running:

```bash
docker compose up --build -d
```

Then just head to `http://localhost:8000` and you're good to go!

### Option 2: Local Setup

If you prefer running things locally:

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Fire it up:
   ```bash
   django-admin runserver
   ```

## 🔑 API Setup

You'll need to create your own Spotify API key. If you have a large music collection, the setup process is well worth the effort! This tool was created to help music lovers have more control over their personal libraries.

*(Website coming soon! Keep an eye on this space for updates.)*

## 📝 Note

This is a tool for personal use. Please respect artists and support them by using official platforms whenever possible.
