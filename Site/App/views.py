from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, FileResponse
from django.template import loader
import spotipy
from spotipy import SpotifyOAuth
import os
import urllib.parse as parsee
import eyed3
from urllib.request import urlopen
import time
from App.models import MusicContainer
import shutil
import subprocess
import zipfile

# def topalbums(limit=20, time_range="medium_term", offset=0):
#     token = []
#     with open("tokeninfo.json", "r") as j: 
#         token = json.load(j)
#     sp = spotipy.Spotify(auth=token[0])
#     tracks = sp.current_user_top_tracks(limit, offset, time_range)
#     albumids = []
#     for track in tracks["items"]:
#         albumids.append(track["track"]["album"]["id"])
#     return sp.albums(albumids)

# Create your views here.
def landing(request, id=os.getenv("SPOTIPY_CLIENT_ID"), secret=os.getenv("SPOTIPY_CLIENT_SECRET")):
    spauth = SpotifyOAuth(client_id=id, client_secret=secret, redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"), scope="playlist-read-private user-top-read user-library-read")
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
    spath = SpotifyOAuth()
    token = spath.get_access_token(realCode, as_dict=False, check_cache=False)
    request.session["TOKEN"] = token
    if(realCode != ""):
        return HttpResponseRedirect("/home/")

def home(request):
    homepage = loader.get_template("home.html")
    return HttpResponse(homepage.render())

def browser(request, reqType, selected):
    sp = spotipy.Spotify(auth=request.session["TOKEN"])
    apicall = print
    match reqType:
        case "playlist-Lib":
            apicall = sp.current_user_playlists
        case "album-Lib":
            apicall = sp.current_user_saved_albums
        case "track-Lib":
            apicall = sp.current_user_saved_tracks
        case "artist-Top":
            apicall = sp.current_user_top_artists
        case "track-Top":
            apicall = sp.current_user_top_tracks
        # case "album-Top":
        #     apicall = topalbums
        case "track-Rec":
            apicall = sp.current_user_recently_played
    
    musicshit = MusicContainer.objects.none().values()

    items = []
    if apicall != sp.current_user_top_tracks:
        while len(items)%20 == 0:
            newshit = apicall(limit=20, offset=len(items))
            if(len(newshit['items']) != 0):
                items.extend(newshit['items'])
            else:
                break
    else:
        while len(items)<100:
            newshit = apicall(limit=20, offset=len(items))
            if(len(newshit['items']) != 0):
                items.extend(newshit['items'])
            else:
                break
    
    for item in items:
        exists = False
        try:
            exists = MusicContainer.objects.filter(spotifyid=item["id"]).exists()
            if not exists:
                music = MusicContainer(spotifyid=item["id"], title=item["name"], type=reqType[:-5])
                music.save()
            musicshit = musicshit | MusicContainer.objects.filter(spotifyid=item["id"]).values()
        except:
            exists = MusicContainer.objects.filter(spotifyid=item[reqType[:-4]]["id"]).exists()
            if not exists:
                music = MusicContainer(spotifyid=item[reqType[:-4]]["id"], title=item[reqType[:-4]]["name"], type=reqType[:-4])
                music.save()
            musicshit = musicshit | MusicContainer.objects.filter(spotifyid=item[reqType[:-4]]["id"]).values()

    context = {
        "musicshit" : musicshit,
        "selected" : [eval(i) for i in selected.split("-")[1:-1]],
        "selectedstr" : selected,
        "type" : reqType[:4]
    }
    
    browserr = loader.get_template("browser.html")
    return HttpResponse(browserr.render(context, request))
    
def download(request, reqType, ids):
    sp = spotipy.Spotify(auth=request.session["TOKEN"])
    apicall = range
    match reqType[:4]:
        case "play":
            apicall = sp.playlist_tracks
        case "albu":
            apicall = sp.album
        case "trac":
            apicall = sp.track
        case "arti":
            apicall = sp.artist_top_tracks
    musicshit = MusicContainer.objects.filter(id__in=list(set(ids.split("-")[1:-1]))).values_list("spotifyid")
    items = []
    name = str(time.time_ns())
    for i in list(musicshit):
        x = apicall(i[0])
        if reqType[:4] == "trac":
            meta = {"search" : x["artists"][0]["name"] + " " + x["name"], "name" : x["name"],"album" : x["album"]["name"], "image" : x["album"]["images"][0]["url"] ,"artist" : x["artists"][0]["name"]}
            items.append(meta)
        elif reqType[:4] == "play":
            while len(items)%100 == 0:
                x = apicall(i[0], offset=len(items))
                if(len(x['items']) != 0):
                    for track in x["items"]:
                        try:
                            track = track["track"]
                            meta = {"search" : track["artists"][0]["name"] + " " + track["name"], "name" : track["name"],"album" : track["album"]["name"], "image" : track["album"]["images"][0]["url"] ,"artist" : track["artists"][0]["name"]}
                            items.append(meta)
                        except:
                            pass
                else:
                    break
        elif reqType[:4] == "albu":
            albname = x["name"]
            cover = x["images"][0]["url"]
            artist = x["artists"][0]["name"]
            for track in x["tracks"]["items"]:
                meta = {"search" : artist + " " + track["name"], "name" : track["name"],"album" : albname, "image" : cover ,"artist" : artist}
                items.append(meta)
        elif reqType[:4] == "arti":
            for song in x["tracks"]:
                meta = {"search" : song["artists"][0]["name"] + " " + song["name"], "name" : song["name"],"album" : song["album"]["name"], "image" : song["album"]["images"][0]["url"] ,"artist" : song["artists"][0]["name"]}
                items.append(meta)

    for item in items:
        safename = "".join(c for c in item['name'] if c.isalpha() or c.isdigit() or c==' ').rstrip()
        subprocess.run(["yt-dlp", "-o", f"{name}/{safename}.mp3", "-x", "--audio-format", "mp3", "--audio-quality", "1", f"ytsearch:{item['search']}(audio)"])
        try:
            mySong = eyed3.load(f"{name}/{safename}.mp3")
            mySong.initTag()
            imagedata = urlopen(item["image"]).read()
            mySong.tag.images.set(3, imagedata , "image/jpeg" ,u"")
            mySong.tag.artist = item["artist"]
            mySong.tag.album = item["album"]
            mySong.tag.title = item["name"]
            mySong.tag.save(f"{name}/{safename}.mp3")
        except:
            pass

    with zipfile.ZipFile(f'Z{name}.zip', 'w', zipfile.ZIP_DEFLATED) as zip_object:
        # Traverse all files in directory
        for filename in os.listdir(f"{name}/"):
            # Add files to zip file
            zip_object.write(f"{name}/{filename}", f"Z{name}/{filename}")

    zippy = open(f'Z{name}.zip', 'rb')
    response = HttpResponse(zippy, content_type='music/force-download')
    response['Content-Disposition'] = f'attachment; filename="FreeMusic-{reqType}.zip"'
    try:
        return response
    finally:
        shutil.rmtree(f"{name}")
        os.remove(f"Z{name}.zip")