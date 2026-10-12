from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from .models import Song


@require_POST
def increment_plays(request, slug):
    song = get_object_or_404(Song, slug=slug)

    Song.objects.filter(pk=song.pk).update(
        plays=F("plays") + 1
    )

    return JsonResponse({"plays": song.plays + 1})