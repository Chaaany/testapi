from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import TreatmentRequestViewSet

router = DefaultRouter()
router.register(r'',
                TreatmentRequestViewSet, basename='treatmentrequest')

urlpatterns = [
    path('', include(router.urls)),
]