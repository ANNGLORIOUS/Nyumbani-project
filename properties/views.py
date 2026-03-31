from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from api.permissions import IsOwner, IsOwnerOrReadOnly
from api.serializers import PropertySerializer
from .models import Property


class PropertyListCreateView(generics.ListCreateAPIView):
    queryset = Property.objects.all().select_related("owner", "caretaker")
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), IsOwner()]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PropertyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.all().select_related("owner", "caretaker")
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
