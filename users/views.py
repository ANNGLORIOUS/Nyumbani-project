from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated
from .serializers import RegisterSerializer, UserSerializer
from .models import MaintenanceRequest
from api.serializers import MaintenanceSerializer

# Try to import the project's notifications utility using a dynamic import; if it's not available, provide a safe fallback.
try:
    import importlib
    _notif_utils = importlib.import_module('notifications.utils')
    send_sms = getattr(_notif_utils, 'send_sms')
except Exception:
    import logging
    logger = logging.getLogger(__name__)
    def send_sms(number, message):
        logger.warning("send_sms not available; attempted to send to %s: %s", number, message)
        return False

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]  # only admin sees all users


# Example role-based test view
from rest_framework.views import APIView

class TenantOnlyView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.role != 'tenant':
            return Response({"error": "You are not authorized as a tenant."}, status=403)
        return Response({"message": f"Welcome tenant {request.user.username}!"})
    
class MaintenanceViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceRequest.objects.all()
    serializer_class = MaintenanceSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        request = serializer.save(tenant=self.request.user)
        caretaker_phone = request.property.caretaker.phone_number if request.property.caretaker else None

        # Send SMS to caretaker
        if caretaker_phone:
            send_sms(
                caretaker_phone,
                f"New maintenance issue from {request.tenant.username}: {request.issue_type} - {request.description}"
            )
        print("🧾 Maintenance request saved successfully.")