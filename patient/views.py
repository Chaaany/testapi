from rest_framework.viewsets import ModelViewSet
from .models import *
from .serializers import *


class PatientViewSet(ModelViewSet):
    serializer_class = PatientSerializer
    queryset = Patient.objects.all()
