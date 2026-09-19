from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from notifications.models import Notification
from payments.models import Payment
from properties.models import Inquiry, Property
from users.models import MaintenanceRequest, TenantProfile

User = get_user_model()


class Command(BaseCommand):
    help = "Create demo users, listings, inquiries, payments, and notifications for the Nyumbani project."

    def handle(self, *args, **options):
        owner, _ = User.objects.get_or_create(
            username="landlord_demo",
            defaults={
                "email": "landlord@nyumbani.local",
                "role": "owner",
                "phone_number": "254700111111",
            },
        )
        owner.set_password("DemoPass123")
        owner.save()

        caretaker, _ = User.objects.get_or_create(
            username="agent_demo",
            defaults={
                "email": "agent@nyumbani.local",
                "role": "caretaker",
                "phone_number": "254700222222",
            },
        )
        caretaker.set_password("DemoPass123")
        caretaker.save()

        tenant, _ = User.objects.get_or_create(
            username="tenant_demo",
            defaults={
                "email": "tenant@nyumbani.local",
                "role": "tenant",
                "phone_number": "254700333333",
            },
        )
        tenant.set_password("DemoPass123")
        tenant.save()

        property_one, _ = Property.objects.get_or_create(
            name="Nyumbani Heights",
            owner=owner,
            defaults={
                "location": "Westlands, Nairobi",
                "rent_price": "35000.00",
                "caretaker": caretaker,
                "available_units": 3,
                "description": "Modern apartments close to shopping malls and public transport.",
            },
        )

        property_two, _ = Property.objects.get_or_create(
            name="Garden View Residency",
            owner=owner,
            defaults={
                "location": "Kilimani, Nairobi",
                "rent_price": "28000.00",
                "caretaker": caretaker,
                "available_units": 2,
                "description": "Quiet compound with spacious one-bedroom and two-bedroom units.",
            },
        )

        TenantProfile.objects.get_or_create(
            user=tenant,
            defaults={
                "property": property_one,
                "move_in_date": timezone.localdate(),
                "rent_due_day": 5,
            },
        )

        Payment.objects.get_or_create(
            tenant=tenant,
            property=property_one,
            transaction_id="SIM-DEMO-CONFIRMED",
            defaults={
                "amount": "35000.00",
                "status": "confirmed",
                "confirmed_at": timezone.now(),
            },
        )

        Payment.objects.get_or_create(
            tenant=tenant,
            property=property_one,
            transaction_id="SIM-DEMO-PENDING",
            defaults={
                "amount": "35000.00",
                "status": "pending",
            },
        )

        MaintenanceRequest.objects.get_or_create(
            tenant=tenant,
            property=property_one,
            issue_type="wifi",
            description="Internet is unstable in the living room.",
            defaults={
                "status": "in_progress",
                "caretaker_response": "Router inspection scheduled for tomorrow morning.",
            },
        )

        Inquiry.objects.get_or_create(
            property=property_two,
            phone_number="254711000999",
            defaults={
                "name": "Mary Interested",
                "email": "mary@example.com",
                "message": "Hi, I would like to know if the house is still available and when I can view it.",
            },
        )

        notifications = [
            (tenant, "sms", "Rent reminder: your rent for Nyumbani Heights is due on the 5th."),
            (caretaker, "system", "New listing alert: Nyumbani Heights has been assigned to you."),
            (owner, "sms", "New inquiry received for Garden View Residency from Mary Interested."),
        ]
        for user, notif_type, message in notifications:
            Notification.objects.get_or_create(
                user=user,
                notif_type=notif_type,
                message=message,
            )

        self.stdout.write(self.style.SUCCESS("Demo data created successfully."))
        self.stdout.write("Login accounts:")
        self.stdout.write("  landlord_demo / DemoPass123")
        self.stdout.write("  agent_demo / DemoPass123")
        self.stdout.write("  tenant_demo / DemoPass123")
