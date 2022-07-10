from rest_framework import serializers
from .models import TreatmentRequest


class TreatmentRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreatmentRequest        # product 모델 사용
        fields = '__all__'


class TreatmentRequestAcceptSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreatmentRequest        # product 모델 사용
        fields = ('id',)


class TreatmentRequestOutputSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.name')
    patient_name = serializers.CharField(source='patient.name')

    class Meta:
        model = TreatmentRequest        # product 모델 사용
        fields = ('id', 'patient_name', 'doctor_name',
                  'request_treatment_time', 'request_treatment_expiration_time')


class TreatmentRequestInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreatmentRequest        # product 모델 사용
        fields = ('id', 'patient', 'doctor', 'request_treatment_time')