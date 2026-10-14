from django.urls import path

from . import views


app_name = "music"

urlpatterns = [
    path("search/", views.search, name="search"),

    path("songs/", views.song_list, name="song_list"),

    path(
        "songs/<slug:slug>/",
        views.song_detail,
        name="song_detail",
    ),

    path(
        "songs/<slug:slug>/plays/",
        views.increment_plays,
        name="increment_plays",
    ),

    path(
        "songs/<slug:slug>/favorite/",
        views.toggle_favorite,
        name="toggle_favorite",
    ),

    path("favorites/", views.favorite_list, name="favorite_list"),

    path("albums/", views.album_list, name="album_list"),

    path(
        "albums/<slug:slug>/",
        views.album_detail,
        name="album_detail",
    ),

    path("artists/", views.artist_list, name="artist_list"),
    
    path(
        "artists/<slug:slug>/",
        views.artist_detail,
        name="artist_detail",
    ),
]