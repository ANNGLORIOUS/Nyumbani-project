from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class UserApiTests(APITestCase):
    def test_user_can_register_and_receive_tokens(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "tenant1",
                "email": "tenant1@example.com",
                "password": "StrongPass123",
                "password_confirm": "StrongPass123",
                "role": "tenant",
                "phone_number": "254700000001",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], "tenant1")
        self.assertIn("tokens", response.data)

    def test_authenticated_user_can_fetch_their_identity(self):
        user = get_user_model().objects.create_user(
            username="owner1", password="StrongPass123", role="owner"
        )
        self.client.force_authenticate(user=user)
        response = self.client.get(reverse("current-user"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["role"], "owner")
