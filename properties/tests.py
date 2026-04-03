from django.contrib.auth import get_user_model
from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from notifications.models import Notification
from properties.models import Property

User = get_user_model()


@override_settings(SMS_ENABLED=False)
class PropertyApiTests(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_user(
            username="owner1",
            password="StrongPass123",
            role="owner",
            email="owner@example.com",
        )
        self.tenant = User.objects.create_user(
            username="tenant1",
            password="StrongPass123",
            role="tenant",
            email="tenant@example.com",
        )

    def test_owner_can_create_property(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(
            reverse("property-list-create"),
            {
                "name": "Sunrise Apartments",
                "location": "Nairobi",
                "rent_price": "25000.00",
                "available_units": 4,
                "description": "Two-bedroom units",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Property.objects.count(), 1)
        self.assertEqual(Property.objects.first().owner, self.owner)

    def test_tenant_cannot_create_property(self):
        self.client.force_authenticate(user=self.tenant)
        response = self.client.post(
            reverse("property-list-create"),
            {
                "name": "Sunrise Apartments",
                "location": "Nairobi",
                "rent_price": "25000.00",
                "available_units": 4,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_property_inquiry_creates_notification(self):
        property_obj = Property.objects.create(
            owner=self.owner,
            name="Garden Residency",
            location="Nairobi",
            rent_price="18000.00",
            available_units=2,
        )

        response = self.client.post(
            reverse("property-inquiries", kwargs={"property_id": property_obj.id}),
            {
                "name": "Interested Tenant",
                "phone_number": "254700444444",
                "email": "lead@example.com",
                "message": "I would like to schedule a viewing for this weekend.",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Notification.objects.filter(user=self.owner, message__icontains="New inquiry").exists())
