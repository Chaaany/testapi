from rest_framework import serializers
from .models import Doctor, Hospital, NonpaidCareItem, TreatmentDepartment, TreatmentTime


class DoctorSerializer(serializers.ModelSerializer):
    class HospitalSerializer(serializers.ModelSerializer):
        class Meta:
            model = Hospital
            fields = ('id', 'name')

    class TreatmentDepartmentSerializer(serializers.ModelSerializer):
        class Meta:
            model = TreatmentDepartment
            fields = ('id', 'name')

    class TreatmentDepartmentSerializer(serializers.ModelSerializer):
        class Meta:
            model = NonpaidCareItem
            fields = ('id', 'name')

    class TreatmentTimeSerializer(serializers.ModelSerializer):
        class Meta:
            model = TreatmentTime
            fields = ('id', 'time_type', 'day_type', 'start_time', 'end_time')

    class NonpaidCareItemSerializer(serializers.ModelSerializer):
        class Meta:
            model = NonpaidCareItem
            fields = ('id', 'name')

    class Meta:
        model = Doctor
        fields = ('id', 'name', 'hospital', 'department',
                  'nonpaid_care_item', 'treatment_time')

    treatment_time = TreatmentTimeSerializer


class DoctorSearchbyDateSerializer(serializers.Serializer):
    search_date = serializers.DateTimeField()


class DoctorSearchbyWordSerializer(serializers.Serializer):
    word = serializers.CharField()


class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = '__all__'


class TreatmentDepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreatmentDepartment
        fields = '__all__'


class TreatmentTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreatmentTime
        fields = '__all__'


class NonpaidCareItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = NonpaidCareItem
        fields = '__all__'

