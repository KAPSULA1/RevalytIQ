from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase


User = get_user_model()


class PasswordResetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="reset-user",
            email="reset@example.com",
            password="OldPass123!",
        )

    def test_reset_password_happy_path(self):
        forgot = self.client.post(
            "/api/auth/password/forgot/",
            {"email": self.user.email},
            format="json",
        )
        self.assertEqual(forgot.status_code, status.HTTP_200_OK)
        payload = forgot.data
        self.assertIn("uid", payload)
        self.assertIn("token", payload)

        reset = self.client.post(
            "/api/auth/password/reset/",
            {
                "email": self.user.email,
                "uid": payload["uid"],
                "token": payload["token"],
                "new_password": "NewPass123!",
                "new_password2": "NewPass123!",
            },
            format="json",
        )
        self.assertEqual(reset.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("NewPass123!"))

    def test_reset_password_rejects_invalid_token(self):
        response = self.client.post(
            "/api/auth/password/reset/",
            {
                "email": self.user.email,
                "uid": "ZmFrZQ==",
                "token": "bad-token",
                "new_password": "NewPass123!",
                "new_password2": "NewPass123!",
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
