from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status
from .models import *
from treatmentrequest.models import *
from .serializers import *
from datetime import datetime
from rest_framework.decorators import action
import itertools


class DoctorViewSet(ModelViewSet):
    serializer_class = DoctorSerializer
    action_serializers = {
        'searchbyword': DoctorSearchbyWordSerializer,
        'searchbydate': DoctorSearchbyDateSerializer
    }
    queryset = Doctor.objects.all()

    def get_serializer_class(self):
        if hasattr(self, 'action_serializers'):
            return self.action_serializers.get(self.action, self.serializer_class)

        return super(DoctorViewSet, self).get_serializer_class()

    @action(detail=False, methods=['post'], name='doctor_search_word')
    def searchbyword(self, request):
        serializer = DoctorSearchbyWordSerializer(data=request.data)

        if serializer.is_valid():
            result = []
            keyword = request.data['word'].split()
            temp = 3 - len(keyword)
            while temp:
                temp -= 1
                keyword.append("")
            keyword = list(itertools.permutations(keyword))

            # 병원 진료과 이름 순으로 filter
            for kw in keyword:
                qk = []
                for tmp in kw:
                    qk.append(tmp)
                tmp = ""
                if qk[0] and qk[1] and qk[2]:
                    tmp = Doctor.objects.filter(
                        hospital__name__icontains=qk[0], department__name__icontains=qk[1], name__icontains=qk[2])
                elif qk[0] and qk[1] and not qk[2]:
                    tmp = Doctor.objects.filter(
                        hospital__name__icontains=qk[0], department__name__icontains=qk[1])
                elif qk[0] and not qk[1] and qk[2]:
                    tmp = Doctor.objects.filter(
                        hospital__name__icontains=qk[0], name__icontains=qk[2])
                elif not qk[0] and qk[1] and qk[2]:
                    tmp = Doctor.objects.filter(
                        department__name__icontains=qk[1], name__icontains=qk[2])
                elif qk[0] and not qk[1] and not qk[2]:
                    tmp = Doctor.objects.filter(
                        hospital__name__icontains=qk[0])
                elif not qk[0] and qk[1] and not qk[2]:
                    tmp = Doctor.objects.filter(
                        department__name__icontains=qk[1])
                elif not qk[0] and not qk[1] and qk[2]:
                    tmp = Doctor.objects.filter(name__icontains=qk[2])

                if tmp:
                    for doctor in tmp:
                        result.append(doctor.name+"의사")
            result = list(set((result)))
            result.sort()
            if result:
                return JsonResponse({'doctor': result}, status=status.HTTP_200_OK)

            return Response(status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], name='doctor_search_date')
    def searchbydate(self, request):
        serializer = DoctorSearchbyDateSerializer(data=request.data)
        if serializer.is_valid():
            result = []
            search_day = datetime.strptime(
                serializer.data['search_date'][:10], "%Y-%m-%d").weekday() + 1
            search_hour = int(str(datetime.strptime(
                serializer.data['search_date'][-8:], "%H:%M:%S"))[-8:-6])
            search_minute = int(str(datetime.strptime(
                serializer.data['search_date'][-8:], "%H:%M:%S"))[-5:-3])
            doctor_list = Doctor.objects.filter(
                treatment_time__day_type=search_day, treatment_time__start_time__hour__lt=search_hour, treatment_time__end_time__hour__gt=search_hour)

            for doctor in doctor_list:
                result.append(doctor.name+"의사")

            doctor_list = Doctor.objects.filter(
                treatment_time__day_type=search_day, treatment_time__start_time__hour=search_hour, treatment_time__start_time__minute__lte=search_minute)

            for doctor in doctor_list:
                result.append(doctor.name+"의사")

            doctor_list = Doctor.objects.filter(
                treatment_time__day_type=search_day, treatment_time__end_time__hour=search_hour, treatment_time__end_time__minute__gt=search_minute)

            for doctor in doctor_list:
                result.append(doctor.name+"의사")
            result = list(set((result)))
            result.sort()

            return JsonResponse({'doctor': result}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class HospitalViewSet(ModelViewSet):
    serializer_class = HospitalSerializer
    queryset = Hospital.objects.all()


class TreatmentDepartmentViewSet(ModelViewSet):
    serializer_class = TreatmentDepartmentSerializer
    queryset = TreatmentDepartment.objects.all()


class TreatmentTimeViewSet(ModelViewSet):
    serializer_class = TreatmentTimeSerializer
    queryset = TreatmentTime.objects.all()


class NonpaidCareItemViewSet(ModelViewSet):
    serializer_class = NonpaidCareItemSerializer
    queryset = NonpaidCareItem.objects.all()

