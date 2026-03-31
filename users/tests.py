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
