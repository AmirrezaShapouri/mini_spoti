
from django.shortcuts import render

from music.models import Album, Song

def home(request):
    popular_songs = Song.objects.select_related(
        "artist",
        "album",
    ).order_by(
        "-plays",
        "-created_at",
    )[:6]

    popular_albums = Album.objects.select_related(
        "artist",
    ).order_by(
        "-release_date",
        "title",
    )[:6]

    context = {
        "popular_songs": popular_songs,
        "popular_albums": popular_albums,
    }

    return render(request, "home.html", context)
