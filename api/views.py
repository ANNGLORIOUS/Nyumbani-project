from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import MaintenanceRequestSerializer
from properties.models import MaintenanceRequest

class MaintenanceRequestViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceRequest.objects.all()
    serializer_class = MaintenanceRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == 'tenant':
            return self.queryset.filter(tenant=user)
        elif user.role == 'caretaker':
            return self.queryset.filter(property__caretaker=user)
        elif user.role == 'owner':
            return self.queryset.filter(property__owner=user)
        return self.queryset.none()
