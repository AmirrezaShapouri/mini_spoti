from django.urls import path

from .views import *

app_name = "music"

urlpatterns = [
    path("search/", search, name="search"),

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

    path(
    "songs/<slug:slug>/favorite/",
    toggle_favorite,
    name="toggle_favorite",
    ),

    path(
    "favorites/",
    favorite_list,
    name="favorite_list",
    ),
]