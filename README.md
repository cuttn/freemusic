# Freemusic!!! - spotify localizer developer project

A little wrapper around yt-dlp that integrates with the Spotify API, letting you manage your music library through a cute web interface. You can download all your playlists, songs, albums, recently played, top artists and more!!

## Features

- Sign in with your Spotify account using OAuth2
- Download your entire library, playlists, or specific albums concurrently
- Clean, simple web interface with tailwind + django
- Powered by yt-dlp and uses spotify metadata for accurate tagging and album covers

## How to install:

### Docker (very easy)

The easiest way to get up and running:

```bash
docker compose up --build -d
```

Then just head to `http://localhost:8000` and you're good to go!

### Option 2: Local Setup (super hairy)

If you prefer running things locally:
0. **You must have ffmpeg installed on your machine - https://www.ffmpeg.org/**

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: scripts/activate.ps1
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your environment:
   ```
   export SPOTIPY_REDIRECT_URI='http://127.0.0.1:8000/App/spotify_callback'
   export DJANGO_SETTINGS_MODULE='Site.settings'
   ```
4. Fire it up:
   ```bash
   cd Site
   python manage.py runserver
   ```

## How it works:

1. the user generates a spotify devloper client id and secret
   - note that these creds grant access to one spotify account at first - the user's
2. the site uses these creds to authorize the users account using spotify auth flow and a callback url to get a token
3. this token is used to go through the users music library and generate dynamic django with download links for all their songs, albums etc.
4. when the user wants to download a song or playlist, it is excecuted as a concurrent thread on the server inside of a new tab
   - it gathers the metadata and creates an optimal youtube search with keywords such as the name and artist
   - it then queries youtube and downloads the video of the song
   - it then uses ffmpeg to convert the file to mp3 and tags it with eyed3
   - then it serves it as a zipfile back to the user
5. after the http response is returned, I use a finally block for garbage collection!!!

## next steps:

although I have better things to work on nowadays, next steps for this project would be having a more user-friendly loading screen. When users have extremely large libraries the site can take a while and doesn't inspire much confidence.

