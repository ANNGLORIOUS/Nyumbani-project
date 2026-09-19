from django.urls import path

from .views import InquiryListCreateView, PropertyDetailView, PropertyListCreateView

urlpatterns = [
    path('', PropertyListCreateView.as_view(), name='property-list-create'),
    path('<int:pk>/', PropertyDetailView.as_view(), name='property-detail'),
    path('<int:property_id>/inquiries/', InquiryListCreateView.as_view(), name='property-inquiries'),
]
