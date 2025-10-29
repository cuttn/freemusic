import os

# Set environment variables
os.environ['SPOTIPY_REDIRECT_URI'] = 'http://127.0.0.1:8000/App/spotify_callback'
os.environ['DJANGO_SETTINGS_MODULE'] = 'Site.settings'

print('Environment variables set successfully:')
print(f'SPOTIPY_REDIRECT_URI: {os.environ.get("SPOTIPY_REDIRECT_URI")}')
print(f'DJANGO_SETTINGS_MODULE: {os.environ.get("DJANGO_SETTINGS_MODULE")}')
