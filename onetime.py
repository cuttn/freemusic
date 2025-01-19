import spotipy
import os
oath = spotipy.SpotifyOAuth(client_id=os.getenv("SPOTIPY_CLIENT_ID"), client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"), redirect_uri="https://example.org", scope="playlist-read-private user-top-read user-library-read playlist-modify-public playlist-modify-private", show_dialog=True)
sp = spotipy.Spotify(auth_manager=oath)
ffset = 600
while ffset % 50 == 0:
        print("aaaaaa")
        x = sp.playlist_tracks(playlist_id="2kCvkRKCr3BFqjxWx2nj8t", offset=ffset, limit=50)
        ids = [str(x["items"][i]["track"]["id"]) for i in range(len(x["items"])) if x["items"][i]["track"]["id"] is not None]
        for id in ids:
            print(id)
        sp.playlist_add_items(playlist_id="0gNyyq4WzpeXtxYfs7CLa0", items=ids, position=None)
        ffset += len(x["items"])