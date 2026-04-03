from django.db.models import Count, Sum
from django.http import JsonResponse
from django.shortcuts import render

from notifications.models import Notification
from payments.models import Payment
from properties.models import Inquiry, Property
from users.models import CustomUser, MaintenanceRequest


def home(request):
    properties = Property.objects.select_related("owner", "caretaker").order_by("-created_at")
    recent_properties = properties[:3]
    recent_inquiries = Inquiry.objects.select_related("property").order_by("-created_at")[:4]
    recent_payments = Payment.objects.select_related("tenant", "property").order_by("-created_at")[:4]
    recent_notifications = Notification.objects.select_related("user").order_by("-created_at")[:4]
    maintenance_requests = MaintenanceRequest.objects.select_related("tenant", "property").order_by("-created_at")[:4]

    users_by_role = dict(
        CustomUser.objects.values_list("role").annotate(total=Count("id"))
    )

    stats = {
        "properties": properties.count(),
        "available_units": sum(property_obj.available_units for property_obj in properties),
        "inquiries": Inquiry.objects.count(),
        "payments": Payment.objects.count(),
        "confirmed_payments_total": Payment.objects.filter(status="confirmed").aggregate(total=Sum("amount"))["total"] or 0,
        "notifications": Notification.objects.count(),
        "tenants": users_by_role.get("tenant", 0),
        "owners": users_by_role.get("owner", 0),
        "agents": users_by_role.get("caretaker", 0),
    }

    demo_accounts = [
        {"role": "Landlord", "username": "landlord_demo", "password": "DemoPass123"},
        {"role": "Agent / Caretaker", "username": "agent_demo", "password": "DemoPass123"},
        {"role": "Tenant", "username": "tenant_demo", "password": "DemoPass123"},
    ]

    context = {
        "stats": stats,
        "recent_properties": recent_properties,
        "recent_inquiries": recent_inquiries,
        "recent_payments": recent_payments,
        "recent_notifications": recent_notifications,
        "maintenance_requests": maintenance_requests,
        "demo_accounts": demo_accounts,
    }
    return render(request, "dashboard/home.html", context)


def api_status(request):
    return JsonResponse({
        "name": "Nyumbani Property Management API",
        "status": "ok",
        "endpoints": {
            "users": "/api/users/",
            "properties": "/api/properties/",
            "payments": "/api/payments/",
            "admin": "/admin/",
        },
    })
