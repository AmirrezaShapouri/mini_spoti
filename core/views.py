from django.shortcuts import render
from music.models import Song, Album, Artist, Favorite, Genre
# Create your views here.

def home(request):
    context = {
        'songs': Song.objects.all(),
        'albums': Album.objects.all(),
        'artists': Artist.objects.all(),
        'favorites': Favorite.objects.all(),
        'genres': Genre.objects.all(),
    }

    return render(request, 'home.html', context)