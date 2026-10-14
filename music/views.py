from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render,redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .models import Song,Favorite

def get_favorite_song_ids(request):


    if not request.user.is_authenticated:
        return set()

    return set(
        Favorite.objects.filter(
            user=request.user
        ).values_list(
            "song_id",
            flat=True,
        )
    )

def song_list(request):
    songs = (
        Song.objects
        .select_related("artist", "album", "genre")
        .all()
    )

    context = {
        "songs": songs,
        "favorite_song_ids": get_favorite_song_ids(request),
    }

    return render(
        request,
        "song/songs.html",
        context,
    )



def song_detail(request, slug):
    song = get_object_or_404(
        Song.objects.select_related(
            "artist",
            "album",
            "genre",
        ),
        slug=slug,
    )

    related_songs = (
        Song.objects
        .select_related("artist", "album")
        .filter(artist=song.artist)
        .exclude(pk=song.pk)[:6]
    )

    context = {
        "song": song,
        "related_songs": related_songs,
        "favorite_song_ids": get_favorite_song_ids(request),
    }

    return render(
        request,
        "song/song-detail.html",
        context,
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




@login_required
@require_POST
def toggle_favorite(request, slug):
    song = get_object_or_404(Song, slug=slug)

    favorite = Favorite.objects.filter(
        user=request.user,
        song=song,
    ).first()

    if favorite:
        favorite.delete()
        is_favorite = False
    else:
        Favorite.objects.create(
            user=request.user,
            song=song,
        )
        is_favorite = True

    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return JsonResponse({
            "success": True,
            "is_favorite": is_favorite,
        })

    return redirect(request.META.get("HTTP_REFERER", "home"))


@login_required
def favorite_list(request):
    favorites = (
        Favorite.objects
        .filter(user=request.user)
        .select_related(
            "song",
            "song__artist",
            "song__album",
        )
        .order_by("-created_at")
    )

    songs = [favorite.song for favorite in favorites]

    favorite_song_ids = set(
        favorites.values_list("song_id", flat=True)
    )

    return render(
        request,
        "favorites/favorites.html",
        {
            "songs": songs,
            "favorite_song_ids": favorite_song_ids,
        },
    )