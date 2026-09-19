import logging

from django.contrib.auth import get_user_model
from rest_framework import generics, permissions, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from notifications.services import notify
from notifications.templates import maintenance_alert
from .models import MaintenanceRequest
from .serializers import MaintenanceSerializer, RegisterSerializer, UserSerializer

logger = logging.getLogger(__name__)

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]  # only admin sees all users


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
            notify(request.property.caretaker, maintenance_alert(request.tenant.username, request.issue_type))
        logger.info("Maintenance request %s saved successfully.", request.id)
