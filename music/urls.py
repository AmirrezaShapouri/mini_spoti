from django.urls import path

from .views import (
    increment_plays,
    song_detail,
    song_list,
)

app_name = "music"

urlpatterns = [
    path(
        "songs/",
        song_list,
        name="song_list",
    ),
    path(
        "songs/<slug:slug>/",
        song_detail,
        name="song_detail",
    ),
    path(
        "songs/<slug:slug>/plays/",
        increment_plays,
        name="increment_plays",
    ),
]