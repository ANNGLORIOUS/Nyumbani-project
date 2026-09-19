from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from .permissions import CanManageProperty, IsPropertyOwnerOrAgent
from .serializers import InquirySerializer, PropertySerializer
from notifications.services import notify
from notifications.templates import new_inquiry
from .models import Inquiry, Property


class PropertyListCreateView(generics.ListCreateAPIView):
    queryset = Property.objects.all().select_related("owner", "caretaker")
    serializer_class = PropertySerializer
    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), CanManageProperty()]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        property_obj = serializer.save(owner=self.request.user)
        if property_obj.caretaker:
            notify(property_obj.caretaker, f"New listing assigned: {property_obj.name} in {property_obj.location}.", 'system')


class PropertyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.all().select_related("owner", "caretaker")
    serializer_class = PropertySerializer
    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.request.method in ('GET', 'HEAD', 'OPTIONS'):
            return [AllowAny()]
        return [IsAuthenticated(), IsPropertyOwnerOrAgent()]


class InquiryListCreateView(generics.ListCreateAPIView):
    serializer_class = InquirySerializer
    queryset = Inquiry.objects.all().select_related("property", "sender", "property__owner", "property__caretaker")
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == "POST":
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        property_id = self.kwargs["property_id"]
        qs = self.queryset.filter(property_id=property_id)
        user = self.request.user
        if not user.is_authenticated:
            return Inquiry.objects.none()
        if user.role == "owner":
            return qs.filter(property__owner=user)
        if user.role in ("caretaker", "agent"):
            return qs.filter(property__caretaker=user)
        return qs.filter(sender=user)

    def perform_create(self, serializer):
        property_obj = Property.objects.select_related("owner", "caretaker").get(pk=self.kwargs["property_id"])
        sender = self.request.user if self.request.user.is_authenticated else None
        inquiry = serializer.save(property=property_obj, sender=sender)

        recipients = [property_obj.owner]
        if property_obj.caretaker:
            recipients.append(property_obj.caretaker)

        for recipient in recipients:
            notify(recipient, new_inquiry(property_obj.name, inquiry.name))
