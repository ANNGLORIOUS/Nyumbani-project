from django.urls import path
from .views import RegisterView, UserListView, TenantOnlyView,MaintenanceViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView



urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('tenant-only/', TenantOnlyView.as_view(), name='tenant-only'),
    # Maintenance requests
    path('maintenance/', MaintenanceViewSet.as_view({'get': 'list', 'post': 'create'}), name='maintenance-list-create'),
    path('maintenance/<int:pk>/', MaintenanceViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='maintenance-detail'), 
]
