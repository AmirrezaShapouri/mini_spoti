from django.contrib import admin
from .models import *

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ["title", "artist", "album", "genre"]
    list_filter = ["artist", "album", "genre"]
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ["title", "artist", "release_date"]
    list_filter = ["artist", "release_date"]
    prepopulated_fields = {"slug": ("title",)}

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ["user", "song", "created_at"]
    list_filter = ["user", "song", "created_at"]