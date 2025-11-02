from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthTests(APITestCase):
    def setUp(self):
        self.username = "testuser"
        self.password = "TestPass123!"
        self.user = User.objects.create_user(username=self.username, password=self.password)

    def test_jwt_token_obtain(self):
        """✅ Should return access & refresh tokens"""
        url = reverse("token_obtain_pair")  # matches your /api/auth/token/
        response = self.client.post(url, {"username": self.username, "password": self.password}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_invalid_credentials(self):
        """❌ Should fail on wrong password"""
        url = reverse("token_obtain_pair")
        response = self.client.post(url, {"username": self.username, "password": "wrong"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
