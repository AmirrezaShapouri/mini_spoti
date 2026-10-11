from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Artist(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(unique=True, blank=True)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to="artists/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Album(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    artist = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE,
        related_name="albums",
    )
    cover = models.ImageField(upload_to="albums/", blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ["-release_date", "title"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Song(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)

    artist = models.ForeignKey(
        Artist,
        on_delete=models.CASCADE,
        related_name="songs",
    )

    album = models.ForeignKey(
        Album,
        on_delete=models.SET_NULL,
        related_name="songs",
        blank=True,
        null=True,
    )

    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        related_name="songs",
        blank=True,
        null=True,
    )

    audio_file = models.FileField(upload_to="songs/")
    cover = models.ImageField(
        upload_to="songs/covers/",
        blank=True,
        null=True,
    )

    duration = models.PositiveIntegerField(
        help_text="Duration in seconds."
    )

    plays = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Favorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="favorites",
    )

    song = models.ForeignKey(
        Song,
        on_delete=models.CASCADE,
        related_name="favorites",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "song"],
                name="unique_user_song_favorite",
            )
        ]

    def __str__(self):
        return f"{self.user} - {self.song}"