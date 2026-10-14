from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Album, Artist, Favorite, Genre, Song


User = get_user_model()


class MusicViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="test_listener",
            password="TestPassword123!",
        )

        self.artist = Artist.objects.create(
            name="Moon Artist",
            bio="A test artist biography.",
        )

        self.genre = Genre.objects.create(
            name="Test Pop",
        )

        self.album = Album.objects.create(
            title="Moon Album",
            artist=self.artist,
        )

        self.song = Song.objects.create(
            title="Moon Song",
            artist=self.artist,
            album=self.album,
            genre=self.genre,
            audio_file="songs/moon-song.mp3",
            duration=210,
            plays=5,
        )

    def test_search_returns_matching_song_album_and_artist(self):
        response = self.client.get(
            reverse("music:search"),
            {"q": "Moon"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Moon Song")
        self.assertContains(response, "Moon Album")
        self.assertContains(response, "Moon Artist")
        self.assertEqual(response.context["result_count"], 3)

    def test_search_song_filter(self):
        response = self.client.get(
            reverse("music:search"),
            {"q": "Moon", "type": "songs"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["songs"].count(), 1)
        self.assertEqual(response.context["albums"].count(), 0)
        self.assertEqual(response.context["artists"].count(), 0)

    def test_search_artist_filter(self):
        response = self.client.get(
            reverse("music:search"),
            {"q": "Moon", "type": "artists"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["artists"].count(), 1)
        self.assertEqual(response.context["songs"].count(), 0)

    def test_search_with_no_results(self):
        response = self.client.get(
            reverse("music:search"),
            {"q": "NoMatchingMusic123"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["result_count"], 0)
        self.assertContains(response, "No results found")

    def test_album_list_page(self):
        response = self.client.get(
            reverse("music:album_list")
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Moon Album")

    def test_album_detail_page(self):
        response = self.client.get(
            reverse(
                "music:album_detail",
                args=[self.album.slug],
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Moon Album")
        self.assertContains(response, "Moon Song")

    def test_artist_list_page(self):
        response = self.client.get(
            reverse("music:artist_list")
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Moon Artist")

    def test_artist_detail_page(self):
        response = self.client.get(
            reverse(
                "music:artist_detail",
                args=[self.artist.slug],
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Moon Artist")
        self.assertContains(response, "Moon Song")
        self.assertContains(response, "Moon Album")

    def test_favorite_toggle_adds_and_removes_song(self):
        self.client.force_login(self.user)

        url = reverse(
            "music:toggle_favorite",
            args=[self.song.slug],
        )

        response = self.client.post(
            url,
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["is_favorite"])
        self.assertTrue(
            Favorite.objects.filter(
                user=self.user,
                song=self.song,
            ).exists()
        )

        response = self.client.post(
            url,
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.json()["is_favorite"])
        self.assertFalse(
            Favorite.objects.filter(
                user=self.user,
                song=self.song,
            ).exists()
        )

    def test_favorites_page_requires_login(self):
        response = self.client.get(
            reverse("music:favorite_list")
        )

        self.assertEqual(response.status_code, 302)

    def test_favorites_page_shows_saved_songs(self):
        Favorite.objects.create(
            user=self.user,
            song=self.song,
        )

        self.client.force_login(self.user)

        response = self.client.get(
            reverse("music:favorite_list")
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Moon Song")

    def test_increment_plays_increases_play_count(self):
        response = self.client.post(
            reverse(
                "music:increment_plays",
                args=[self.song.slug],
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["plays"], 6)

        self.song.refresh_from_db()
        self.assertEqual(self.song.plays, 6)