from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import DoctorViewSet, HospitalViewSet, NonpaidCareItemViewSet, TreatmentDepartmentViewSet,TreatmentTimeViewSet

router_doctor = DefaultRouter()
router_doctor.register(r'', DoctorViewSet, basename='doctor')

router_info = DefaultRouter()

router_info.register(r'hospital', HospitalViewSet, basename='hospital')
router_info.register(r'department', TreatmentDepartmentViewSet,
                basename='department')
router_info.register(r'treatmenttime', TreatmentTimeViewSet,
                basename='treatmenttime')
router_info.register(r'nonpaiditem', NonpaidCareItemViewSet, basename='nonpaiditem')

urlpatterns = [
    path('info/', include(router_doctor.urls)),
    path('etc/', include(router_info.urls)),
]