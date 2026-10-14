from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from music.models import Album, Artist, Favorite, Song


User = get_user_model()


class HomeViewTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="home_listener",
            password="ValidTestPassword123!",
        )

        self.artist = Artist.objects.create(
            name="Test Artist",
        )

        self.album = Album.objects.create(
            title="Test Album",
            artist=self.artist,
        )

        self.song = Song.objects.create(
            title="Test Song",
            artist=self.artist,
            album=self.album,
            audio_file="songs/test-song.mp3",
            duration=180,
            plays=5,
        )

    def test_home_page_loads(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")

    def test_home_displays_songs_and_albums(self):
        response = self.client.get(reverse("home"))

        self.assertContains(response, "Test Song")
        self.assertContains(response, "Test Album")
        self.assertContains(response, "Test Artist")

    def test_home_provides_empty_favorites_for_guest(self):
        response = self.client.get(reverse("home"))

        self.assertEqual(
            response.context["favorite_song_ids"],
            set(),
        )

    def test_home_provides_favorites_for_authenticated_user(self):
        Favorite.objects.create(
            user=self.user,
            song=self.song,
        )

        self.client.force_login(self.user)

        response = self.client.get(reverse("home"))

        self.assertIn(
            self.song.id,
            response.context["favorite_song_ids"],
        )

    def test_home_orders_popular_songs_by_play_count(self):
        popular_song = Song.objects.create(
            title="Most Popular Song",
            artist=self.artist,
            audio_file="songs/popular-song.mp3",
            duration=200,
            plays=100,
        )

        response = self.client.get(reverse("home"))

        self.assertEqual(
            response.context["popular_songs"][0],
            popular_song,
        )