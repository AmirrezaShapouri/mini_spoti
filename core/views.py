from django.shortcuts import render

from music.models import Album, Favorite, Song

def home(request):
    popular_songs = (
        Song.objects
        .select_related("artist", "album")
        .order_by("-plays", "-created_at")[:6]
    )

    popular_albums = (
        Album.objects
        .select_related("artist")
        .order_by("-release_date", "title")[:6]
    )

    favorite_song_ids = set()

    if request.user.is_authenticated:
        favorite_song_ids = set(
            Favorite.objects.filter(
                user=request.user
            ).values_list("song_id", flat=True)
        )

    context = {
        "popular_songs": popular_songs,
        "popular_albums": popular_albums,
        "favorite_song_ids": favorite_song_ids,
    }

    return render(request, "home.html", context)