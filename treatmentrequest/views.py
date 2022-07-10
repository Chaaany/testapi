from datetime import timedelta
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework import status

from doctor.models import Doctor, TreatmentTime
from patient.models import Patient
from .models import *
from .serializers import *
from datetime import datetime
from rest_framework.decorators import action
from django.utils import timezone


class TreatmentRequestViewSet(ModelViewSet):
    serializer_class = TreatmentRequestInputSerializer
    queryset = TreatmentRequest.objects.all()

    def list(self, request):
        queryset = self.get_queryset()
        serializer = TreatmentRequestSerializer(queryset, many=True)
        return Response(serializer.data)

    # 진료 요청 생성
    def create(self, request):
        def maketime(hour, minute):
            return (int)(hour * 60 + minute)
        
        def maketime_qs(qs):
            hour = (int)(
                qs.strftime("%H:%M:%S")[-8:-6])
            minute = (int)(qs.strftime(
                "%H:%M:%S")[-5:-3])
            return (int)(hour * 60 + minute)

        def maketime_str(time):
            hour = int(str(datetime.strptime(
                time, "%H:%M:%S"))[-8:-6])
            minute = int(str(datetime.strptime(
                time, "%H:%M:%S"))[-5:-3])
            return (int)(hour * 60 + minute)

        def findtime(request_day):
            tmp_day = request_day
            count_day = 0
            
            while True:
                tmp_day += 1
                count_day += 1
                if tmp_day == 8:
                    tmp_day = 1
                doctor_time = TreatmentTime.objects.filter(
                    doctor=doctor_id, day_type=tmp_day)

                if doctor_time:
                    doctor_time = doctor_time[0]
                    start_hour = int(doctor_time.start_time.strftime(
                        "%H:%M:%S")[-8:-6])
                    start_minute = int(doctor_time.start_time.strftime(
                        "%H:%M:%S")[-5:-3])

                    tmp_minute = start_minute + 15

                    if tmp_minute % 60 == 1:
                        start_hour += 1
                        tmp_minute %= 60
                    request_exp_time = maketime(start_hour, tmp_minute)
                    break
                
            return {'count_day': count_day, 'request_exp_time' : request_exp_time}
                
                
        serializer = TreatmentRequestInputSerializer(data=request.data)
        if serializer.is_valid():
            doctor_id = request.data['doctor']
            patient_id = request.data['patient']
            # 요일 확인( 0 : 월 ~ 6: 일)
            request_day = datetime.strptime(
                serializer.data['request_treatment_time'][:10], "%Y-%m-%d").weekday() + 1
            count_day = 0  
            request_exp_time = 0
            oper_chk = True

            doctor_time = TreatmentTime.objects.filter(
                doctor=doctor_id, day_type=request_day)

            request_time = maketime_str(serializer.data['request_treatment_time'][-8:])
            
            # 의사의 해당 요일 진료 시간 검색
            if doctor_time: # 진료중인 요일일 경우
                print(1)
                doctor_time = doctor_time[0]

                start_time = maketime_qs(doctor_time.start_time)
                end_time = maketime_qs(doctor_time.end_time)
                lunch_start_time = maketime_qs(doctor_time.lunch_start_time)
                lunch_end_time = maketime_qs(doctor_time.lunch_end_time)
                
                if lunch_start_time <= request_time and request_time < lunch_end_time: # 점심시간일 경우
                    request_exp_time = lunch_end_time + 15
                    oper_chk = False
                elif start_time <= request_time and request_time < end_time: # 진료 요청 가능 시간일 경우
                    request_exp_time = request_time + 20
                else: # 진료중이지 않을 경우
                    oper_chk = False
                    rs = findtime(request_day)
                    count_day = rs['count_day']
                    request_exp_time = rs['request_exp_time']
                    count_day = rs['count_day']
            else:  # 진료중이지 않은 요일일 경우
                print(5)
                oper_chk = False
                rs = findtime(request_day)
                count_day = rs['count_day']
                request_exp_time = rs['request_exp_time']
                count_day = rs['count_day']
                    

            doctor = get_object_or_404(Doctor, id=doctor_id)
            patient = get_object_or_404(Patient, id=patient_id)
            request_treatment_time = serializer.data['request_treatment_time']
            request_treatment_expiration_time = datetime((int)(request_treatment_time[0:4]), (int)(request_treatment_time[5:7]),
                                                         (int)(request_treatment_time[8:10])) + timedelta(days=count_day) + timedelta(minutes=request_exp_time)
            req = TreatmentRequest(
                doctor=doctor,
                patient=patient,
                request_treatment_time=request_treatment_time,
                is_accepted=False,
                request_treatment_expiration_time=request_treatment_expiration_time
            )
            req.save()

            if not oper_chk:
                return JsonResponse({'warn': '의사의 영업시간이 아님'}, status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #  진료 요청 검색
    @ action(detail=True, methods=['get'], name='treatment_request_list')
    def reqlist(self, request, pk):
        treatment_request_list = TreatmentRequest.objects.filter(
            doctor=pk, is_accepted=False, request_treatment_expiration_time__lt=datetime.now())
        treatment_request_list = self.filter_queryset(treatment_request_list)
        page = self.paginate_queryset(treatment_request_list)
        if page is not None:
            serializer = TreatmentRequestOutputSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = TreatmentRequestOutputSerializer(
            treatment_request_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 진료 요청 수락
    @ action(detail=True, methods=['patch'], name='accept_request')
    def acceptreq(self, request, pk):
        treatment_request = get_object_or_404(
            TreatmentRequest, id=pk, request_treatment_expiration_time__gt=timezone.now())

        treatment_request.is_accepted = True
        treatment_request.save()
        serializer = TreatmentRequestSerializer(treatment_request)

        return Response(serializer.data, status=status.HTTP_200_OK)