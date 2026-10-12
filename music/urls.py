from django.urls import path

from .views import *

app_name = "music"

urlpatterns = [
    path(
        "songs/<slug:slug>/plays/", increment_plays, name="increment_plays"),
]