from django import forms

class spotifyuser(forms.Form):
    sp_dc = forms.CharField(label="Spotify Client ID")
    sp_key = forms.CharField(label="Spotify Client Secret")