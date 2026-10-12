from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from .models import Song


def song_list(request):
    songs = Song.objects.select_related("artist","album","genre").all()

    return render(
        request,"song/songs.html",{"songs": songs})


def song_detail(request, slug):
    song = get_object_or_404(Song.objects.select_related("artist","album","genre"), slug=slug,)

    related_songs = (
        Song.objects.select_related("artist", "album")
        .filter(artist=song.artist)
        .exclude(pk=song.pk)[:6]
    )

    return render(
        request, "song/song-detail.html", {"song": song,"related_songs": related_songs},
    )


@require_POST
def increment_plays(request, slug):
    song = get_object_or_404(Song, slug=slug)

    Song.objects.filter(pk=song.pk).update(
        plays=F("plays") + 1
    )

    return JsonResponse(
        {
            "plays": song.plays + 1,
        }
    )