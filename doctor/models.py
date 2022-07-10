from django.db import models

class Hospital(models.Model):
    name = models.CharField(max_length=30, verbose_name='병원명')
    address = models.CharField(max_length=100, blank=True, verbose_name='병원주소')
    phone_number = models.CharField(
        max_length=20, blank=True, verbose_name='병원대표전화')
    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name='병원데이터 생성 일자')
    deleted_date = models.DateTimeField(null=True, verbose_name='병원데이터 삭제 일자')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'hospital'
        verbose_name = '병원'


class Doctor(models.Model):
    name = models.CharField(max_length=30, verbose_name='의사명')
    license_number = models.CharField(
        max_length=20, blank=True, verbose_name='의사면허번호')
    introduction = models.CharField(
        max_length=100, blank=True, verbose_name='소개내용')
    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name='의사데이터 생성일자')
    modified_date = models.DateTimeField(
        auto_now=True, null=True, verbose_name='의사데이터 수정일자')
    deleted_date = models.DateTimeField(null=True, verbose_name='의사데이터 삭제일자')
    hospital = models.ForeignKey('Hospital', on_delete=models.SET_NULL,
                                 null=True, related_name='hospital')  # 병원 폐원 시에도 의사 기록 유지
    department = models.ManyToManyField(
        'TreatmentDepartment', related_name='department')
    nonpaid_care_item = models.ManyToManyField(
        'NonpaidCareItem', blank=True, related_name='nonpaid_care_item')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'doctor'
        verbose_name = '의사'
        indexes = [
           models.Index(fields=['name']),
        ]


class TreatmentDepartment(models.Model):
    name = models.CharField(max_length=30, verbose_name='진료과 명')
    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name='진료과 데이터 생성일자')
    deleted_date = models.DateTimeField(
        null=True, verbose_name='진료과 데이터 삭제 일자')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'treatment_department'
        verbose_name = '진료과'


class NonpaidCareItem(models.Model):
    name = models.CharField(max_length=30, verbose_name='비급여 진료항목명')
    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name='비급여 진료항목 데이터 생성일자')
    deleted_date = models.DateTimeField(
        null=True, verbose_name='비급여 진료항목 데이터 삭제일자')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'nonpaid_care_item'
        verbose_name = '비급여 진료항목'


class TreatmentTime(models.Model):
    doctor = models.ForeignKey(
        'Doctor', on_delete=models.CASCADE, related_name='treatment_time')
    day_type = models.IntegerField(null=True, verbose_name='요일 설정(1:월 ~ 7:일)')
    start_time = models.TimeField(verbose_name='시작 시간')
    end_time = models.TimeField(verbose_name='종료 시간')
    lunch_start_time = models.TimeField(null=True, verbose_name='점심 시작 시간')
    lunch_end_time = models.TimeField(null=True, verbose_name='점심 종료 시간')

    def __str__(self):
        return '{}의 {}번째 요일 진료 시간 {} to {}'.format(self.doctor, self.day_type, self.start_time, self.end_time)

    class Meta:
        db_table = 'treatment_time'
        verbose_name = '진료 또는 점심시간'
        indexes = [
           models.Index(fields=['doctor','day_type']),
        ]

class Profile(models.Model):
    doctor = models.ForeignKey(
        'Doctor', on_delete=models.CASCADE, related_name='profile')
    content = models.CharField(max_length=100, verbose_name='약력내용')
    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name='병원 데이터 생성 일자')
    deleted_date = models.DateTimeField(null=True, verbose_name='병원 데이터 삭제 일자')

    def __str__(self):
        return '{}의 약력'.format(self.doctor)

    class Meta:
        db_table = 'profile'
        verbose_name = '의사 약력'
