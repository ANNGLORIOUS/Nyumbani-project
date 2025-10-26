from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PropertyViewSet, MaintenanceViewSet, PaymentViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'properties', PropertyViewSet, basename='properties')
router.register(r'maintenance', MaintenanceViewSet, basename='maintenance')
router.register(r'payments', PaymentViewSet, basename='payments')

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),   # login => get tokens
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
