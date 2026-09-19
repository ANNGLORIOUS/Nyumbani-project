from django.contrib.auth import get_user_model
from django.test import override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from payments.models import Lease, Payment, RentRecord
from properties.models import Property

User = get_user_model()


@override_settings(MPESA_SIMULATE=True, MPESA_CALLBACK_SECRET="test-secret", SMS_ENABLED=False)
class PaymentApiTests(APITestCase):
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
            phone_number="254700000001",
        )
        self.property = Property.objects.create(
            owner=self.owner,
            name="Blue Estate",
            location="Nairobi",
            rent_price="30000.00",
            available_units=3,
        )

    def test_tenant_can_initiate_payment_in_simulation_mode(self):
        self.client.force_authenticate(user=self.tenant)
        response = self.client.post(
            reverse("mpesa-pay"),
            {
                "phone": "254700000001",
                "amount": "30000.00",
                "property": self.property.id,
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Payment.objects.count(), 1)
        self.assertEqual(Payment.objects.first().status, "pending")
        self.assertIn("CheckoutRequestID", response.data["mpesa_response"])

    def test_callback_confirms_payment(self):
        payment = Payment.objects.create(
            tenant=self.tenant,
            property=self.property,
            amount="30000.00",
            transaction_id="SIM-123456",
            status="pending",
        )

        response = self.client.post(
            reverse("mpesa-callback"),
            {
                "Body": {
                    "stkCallback": {
                        "ResultCode": 0,
                        "CheckoutRequestID": "SIM-123456",
                        "MerchantRequestID": "merchant-123",
                    }
                }
            },
            format="json",
            HTTP_X_MPESA_SECRET="test-secret",
        )

        payment.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(payment.status, "confirmed")

    def test_callback_reconciles_linked_rent_record(self):
        from datetime import date
        lease = Lease.objects.create(
            tenant=self.tenant, property=self.property, monthly_rent="30000.00",
            start_date=date(2026, 1, 1), due_day=5,
        )
        rent_record = RentRecord.objects.create(
            lease=lease, period=date(2026, 9, 1), amount_due="30000.00",
            due_date=date(2026, 9, 5),
        )
        Payment.objects.create(
            tenant=self.tenant, property=self.property, rent_record=rent_record,
            amount="15000.00", transaction_id="SIM-RENT-123", status="pending",
        )
        response = self.client.post(
            reverse("mpesa-callback"),
            {"Body": {"stkCallback": {"ResultCode": 0, "CheckoutRequestID": "SIM-RENT-123"}}},
            format="json", HTTP_X_MPESA_SECRET="test-secret",
        )
        rent_record.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(rent_record.amount_paid), "15000.00")
        self.assertEqual(rent_record.status, "partially_paid")
