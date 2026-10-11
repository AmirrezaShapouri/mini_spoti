
from django.shortcuts import render

from music.models import Album, Song


def format_duration(seconds):
    minutes, remaining_seconds = divmod(seconds, 60)
    return f"{minutes}:{remaining_seconds:02d}"


def home(request):
    popular_songs = list(
        Song.objects.select_related(
            "artist",
            "album",
        ).order_by("-plays", "-created_at")[:6]
    )

    popular_albums = Album.objects.select_related(
        "artist",
    ).order_by("-release_date", "title")[:6]

    for song in popular_songs:
        song.duration_display = format_duration(song.duration)

    context = {
        "popular_songs": popular_songs,
        "popular_albums": popular_albums,
    }

    return render(request, "home.html", context)
