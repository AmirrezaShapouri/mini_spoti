from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


User = get_user_model()


class AccountViewsTests(TestCase):
    def setUp(self):
        self.password = "ValidTestPassword123!"

        self.user = User.objects.create_user(
            username="existing_user",
            password=self.password,
        )

    def test_register_page_loads(self):
        response = self.client.get(
            reverse("accounts:register")
        )

        self.assertEqual(response.status_code, 200)

    def test_register_creates_user_and_logs_in(self):
        response = self.client.post(
            reverse("accounts:register"),
            {
                "username": "new_listener",
                "password1": "StrongTestPassword123!",
                "password2": "StrongTestPassword123!",
            },
        )

        self.assertRedirects(response, reverse("home"))
        self.assertTrue(
            User.objects.filter(username="new_listener").exists()
        )
        self.assertIn("_auth_user_id", self.client.session)

    def test_register_rejects_mismatched_passwords(self):
        response = self.client.post(
            reverse("accounts:register"),
            {
                "username": "new_listener",
                "password1": "StrongTestPassword123!",
                "password2": "DifferentTestPassword456!",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            User.objects.filter(username="new_listener").exists()
        )

    def test_authenticated_user_cannot_open_register_page(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse("accounts:register")
        )

        self.assertRedirects(response, reverse("home"))

    def test_login_page_loads(self):
        response = self.client.get(
            reverse("accounts:login")
        )

        self.assertEqual(response.status_code, 200)

    def test_login_accepts_valid_credentials(self):
        response = self.client.post(
            reverse("accounts:login"),
            {
                "username": "existing_user",
                "password": self.password,
            },
        )

        self.assertRedirects(response, reverse("home"))
        self.assertIn("_auth_user_id", self.client.session)

    def test_login_rejects_invalid_credentials(self):
        response = self.client.post(
            reverse("accounts:login"),
            {
                "username": "existing_user",
                "password": "IncorrectPassword123!",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_authenticated_user_cannot_open_login_page(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse("accounts:login")
        )

        self.assertRedirects(response, reverse("home"))

    def test_logout_logs_user_out(self):
        self.client.force_login(self.user)

        response = self.client.post(
            reverse("accounts:logout")
        )

        self.assertRedirects(response, reverse("home"))
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_logout_rejects_get_requests(self):
        self.client.force_login(self.user)

        response = self.client.get(
            reverse("accounts:logout")
        )

        self.assertEqual(response.status_code, 405)