from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated

from api.permissions import IsOwner, IsOwnerOrReadOnly
from api.serializers import InquirySerializer, PropertySerializer
from notifications.models import Notification
from notifications.utils import send_sms
from .models import Inquiry, Property


class PropertyListCreateView(generics.ListCreateAPIView):
    queryset = Property.objects.all().select_related("owner", "caretaker")
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated(), IsOwner()]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        property_obj = serializer.save(owner=self.request.user)
        if property_obj.caretaker:
            Notification.objects.create(
                user=property_obj.caretaker,
                notif_type="system",
                message=f"New listing assigned: {property_obj.name} in {property_obj.location}.",
            )
            if property_obj.caretaker.phone_number:
                send_sms(
                    property_obj.caretaker.phone_number,
                    f"Nyumbani listing alert: {property_obj.name} in {property_obj.location} has been assigned to you.",
                )


class PropertyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.all().select_related("owner", "caretaker")
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


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
        if user.role == "caretaker":
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
            Notification.objects.create(
                user=recipient,
                notif_type="sms",
                message=f"New inquiry for {property_obj.name} from {inquiry.name}: {inquiry.message}",
            )
            if recipient.phone_number:
                send_sms(
                    recipient.phone_number,
                    f"Nyumbani inquiry: {inquiry.name} is interested in {property_obj.name}.",
                )
