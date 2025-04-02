from django import forms
from .models import Song

class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['song_url','song_lyrics','song_name' ,'image_url']