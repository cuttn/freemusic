from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, FileResponse
from django.template import loader
from .forms import spotifyuser
from asgiref.sync import sync_to_async

import os
import asyncio
import shutil
import urllib.parse as parsee
from urllib.request import urlopen
from pathlib import Path
from functools import partial
from asyncio.subprocess import create_subprocess_exec

import spotipy
from spotipy import SpotifyOAuth
import eyed3
import zipfile

from App.models import MusicContainer

# Wrap synchronous spotipy calls
class AsyncSpotify:
    def __init__(self, auth_token):
        self.sp = spotipy.Spotify(auth=auth_token)
        # Base async methods
        self.current_user_playlists = sync_to_async(self.sp.current_user_playlists)
        self.current_user_saved_albums = sync_to_async(self.sp.current_user_saved_albums)
        self.current_user_saved_tracks = sync_to_async(self.sp.current_user_saved_tracks)
        self.current_user_top_artists = sync_to_async(self.sp.current_user_top_artists)
        self.current_user_top_tracks = sync_to_async(self.sp.current_user_top_tracks)
        self.get_playlist_tracks = sync_to_async(self.sp.playlist_tracks)
        self.current_user_recently_played = sync_to_async(self.sp.current_user_recently_played)
        self.async_track = sync_to_async(self.sp.track)
        self.async_album = sync_to_async(self.sp.album)
        self.async_artist = sync_to_async(self.sp.artist)
        self.async_artist_top_tracks = sync_to_async(self.sp.artist_top_tracks)
    async def get_all_playlists(self):
        items = []
        while True:
            result = await self.current_user_playlists(offset=len(items))
            if not result['items']:
                break
            items.extend(result['items'])
        return items

    async def get_all_saved_albums(self):
        items = []
        while True:
            result = await self.current_user_saved_albums(offset=len(items))
            if not result['items']:
                break
            items.extend(result['items'])
        return items

    async def get_all_saved_tracks(self):
        items = []
        while True:
            result = await self.current_user_saved_tracks(offset=len(items))
            if not result['items']:
                break
            items.extend(result['items'])
        return items

    async def get_all_top_artists(self, time_range='medium_term'):
        items = []
        while True:
            result = await self.current_user_top_artists(limit=50, offset=len(items), time_range=time_range)
            if not result['items']:
                break
            items.extend(result['items'])
        return items

    async def get_all_top_tracks(self, time_range='medium_term'):
        items = []
        while True:
            result = await self.current_user_top_tracks(limit=50, offset=len(items), time_range=time_range)
            if not result['items']:
                break
            items.extend(result['items'])
        return items

    async def get_playlist_tracks_paginated(self, playlist_id):
        items = []
        while True:
            result = await self.get_playlist_tracks(playlist_id, offset=len(items))
            if not result['items']:
                break
            items.extend(result['items'])
        return items

    async def get_all_recently_played(self):
        items = []
        while True:
            result = await self.current_user_recently_played(limit=50, after=len(items))
            if not result['items']:
                break
            items.extend(result['items'])
        return items
    

def login(request):
    if request.method == 'POST':
        form = spotifyuser(request.POST)
        if form.is_valid():
            request.session["TOKEN"] = {"id" : form.cleaned_data["sp_dc"], "secret" : form.cleaned_data["sp_key"]}
            return HttpResponseRedirect("token")
    else:
        form = spotifyuser()
    
    return render(request, "getspinfo.html", {"form" : form})

# Create your views here.
def landing(request):
    spauth = SpotifyOAuth(client_id=request.session["TOKEN"]["id"], client_secret=request.session["TOKEN"]["secret"], scope="playlist-read-private user-top-read user-library-read")
    destination = spauth.get_authorize_url()
    return HttpResponseRedirect(destination)
# def landing(request):
#     if(request.method == "POST"):
#         formchecker = spotifyuser(request.POST)
#         if(formchecker.is_valid()):
#             tokendict = spotify_token.start_session(formchecker.cleaned_data["sp_dc"], formchecker.cleaned_data["sp_key"])
#             with open("tokeninfo.json", "w") as j:
#                 json.dump(tokendict, j)
#             return HttpResponseRedirect("home")
#     else:
#         formchecker = spotifyuser()
#     return render(request, "getspinfo.html", {"form" : formchecker})

def tokenn(request):
    fullurl = request.get_full_path()
    plasentaCode = parsee.urlparse(fullurl)
    realCode = parsee.parse_qs(plasentaCode.query)['code'][0]
    spath = SpotifyOAuth(client_id=request.session["TOKEN"]["id"], client_secret=request.session["TOKEN"]["secret"])
    token = spath.get_access_token(realCode, as_dict=False, check_cache=False)
    request.session["TOKEN"] = token
    if(realCode != ""):
        return HttpResponseRedirect("/home/")

def home(request):
    homepage = loader.get_template("home.html")
    return HttpResponse(homepage.render())

async def browser(request, reqType):
    apicaller = AsyncSpotify(auth_token=request.session["TOKEN"])
    apicall = print
    match reqType:
        case "playlist-Lib":
            apicall = apicaller.get_all_playlists
        case "album-Lib":
            apicall = apicaller.get_all_saved_albums
        case "track-Lib":
            apicall = apicaller.get_all_saved_tracks
        case "artist-Top":
            apicall = apicaller.get_all_top_artists
        case "track-Top":
            apicall = apicaller.get_all_top_tracks
        # case "album-Top":
        #     apicall = topalbums
        case "track-Rec":
            apicall = apicaller.get_all_recently_played
    
    musicshit = []
    
    items = await apicall()
    
    for item in items:
        try:
            musicshit.append({
                'spotifyid': item["id"],
                'title': item["name"],
                'type': reqType[:-5]
            })
        except:
            musicshit.append({
                'spotifyid': item[reqType[:-4]]["id"],
                'title': item[reqType[:-4]]["name"],
                'type': reqType[:-4]
            })

    context = {
        "musicshit" : musicshit,
        "type" : reqType[:4]
    }
    
    browserr = loader.get_template("browser.html")
    return HttpResponse(browserr.render(context, request))

async def download(request, reqType, ids):
    sp = AsyncSpotify(request.session["TOKEN"])

    name = "music"
    os.makedirs(name, exist_ok=True)
    
    # Get track metadata based on type
    async def get_metadata(spotify_id):
        items = []
        if reqType.startswith("trac"):
            x = await sp.async_track(spotify_id)
            items.append({
                "search": f"{x['artists'][0]['name']} {x['name']}",
                "name": x['name'],
                "album": x['album']['name'],
                "image": x['album']['images'][0]['url'],
                "artist": x['artists'][0]['name']
            })
        elif reqType.startswith("play"):
            tracks = await sp.get_playlist_tracks_paginated(spotify_id)
            for track in tracks:
                try:
                    track = track["track"]
                    items.append({
                        "search": f"{track['artists'][0]['name']} {track['name']}",
                        "name": track['name'],
                        "album": track['album']['name'],
                        "image": track['album']['images'][0]['url'],
                        "artist": track['artists'][0]['name']
                    })
                except:
                    pass
        elif reqType.startswith("albu"):
            album = await sp.async_album(spotify_id)
            for track in album['tracks']['items']:
                items.append({
                    "search": f"{track['artists'][0]['name']} {track['name']}",
                    "name": track['name'],
                    "album": album['name'],
                    "image": album['images'][0]['url'],
                    "artist": track['artists'][0]['name']
                })
        elif reqType.startswith("arti"):
            tracks = await sp.async_artist_top_tracks(spotify_id)
            for track in tracks['tracks']:
                items.append({
                    "search": f"{track['artists'][0]['name']} {track['name']}",
                    "name": track['name'],
                    "album": track['album']['name'],
                    "image": track['album']['images'][0]['url'],
                    "artist": track['artists'][0]['name']
                })
        return items
    
    items = await get_metadata(ids)
    async def download_and_tag_song(item):
        safename = "".join(c for c in item['name'] if c.isalpha() or c.isdigit() or c==' ').rstrip()
        output_path = f"{name}/{safename}.mp3"
        
        # Download with yt-dlp
        cmd = [
            "yt-dlp",
            "-o", output_path,
            "-x",
            "--cookies", "cookies.txt",
            "--audio-format", "mp3",
            "--audio-quality", "1",
            f"ytsearch:{item['search']}(audio)"
        ]
        
        process = await create_subprocess_exec(*cmd)
        await process.communicate()
        
        # Tag the file (synchronous operation wrapped in sync_to_async)
        @sync_to_async
        def tag_file():
            try:
                mySong = eyed3.load(output_path)
                mySong.initTag()
                imagedata = urlopen(item["image"]).read()
                mySong.tag.images.set(3, imagedata, "image/jpeg", u"")
                mySong.tag.artist = item["artist"]
                mySong.tag.album = item["album"]
                mySong.tag.title = item["name"]
                mySong.tag.save(output_path)
            except:
                pass
        
        await tag_file()
    
    # Download and tag songs concurrently (with a limit to avoid overwhelming the system)
    chunk_size = 3  # Adjust based on your system's capabilities
    for i in range(0, len(items), chunk_size):
        chunk = items[i:i + chunk_size]
        await asyncio.gather(*[download_and_tag_song(item) for item in chunk])
    
    # Create zip file (synchronous operation wrapped in sync_to_async)
    @sync_to_async
    def create_zip():
        with zipfile.ZipFile(f'Z{name}.zip', 'w', zipfile.ZIP_DEFLATED) as zip_object:
            for filename in os.listdir(f"{name}/"):
                if filename.endswith("webm"):
                    filename = filename[:-4] + "mp3"
                zip_object.write(f"{name}/{filename}", f"Z{name}/{filename}")
    
    await create_zip()
    
    # Return response and cleanup
    response = FileResponse(
        open(f'Z{name}.zip', 'rb'),
        content_type='application/zip',
        as_attachment=True,
        filename=f"{reqType}.zip"
    )
    
    # Cleanup in background
    async def cleanup():
        await asyncio.sleep(5)
        try:
            shutil.rmtree(f"{name}")
            os.remove(f"Z{name}.zip")
        except:
            pass
    
    asyncio.create_task(cleanup())
    
    return response