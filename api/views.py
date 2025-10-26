from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from properties.models import Property
from users.models import MaintenanceRequest
from payments.models import Payment
from notifications.models import Notification
from .serializers import PropertySerializer, MaintenanceSerializer, PaymentSerializer, NotificationSerializer

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # read allowed for any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return True
        # owners can mutate their own
        return hasattr(obj, 'owner') and obj.owner == request.user

class PropertyViewSet(viewsets.ModelViewSet):
    queryset = Property.objects.all().select_related('owner','caretaker')
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class MaintenanceViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceRequest.objects.all().select_related('tenant','property')
    serializer_class = MaintenanceSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user)

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        if user.role == 'tenant':
            return qs.filter(tenant=user)
        if user.role == 'caretaker':
            return qs.filter(property__caretaker=user)
        if user.role == 'owner':
            return qs.filter(property__owner=user)
        return MaintenanceRequest.objects.none()

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all().select_related('tenant','property')
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(tenant=self.request.user)
