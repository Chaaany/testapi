from django.db import models

class Patient(models.Model):
    name = models.CharField(max_length=30, verbose_name='환자 성명')
    resident_registration_number = models.CharField(
        max_length=30, blank=True, verbose_name='환자 주민등록번호')
    phone_number = models.CharField(
        max_length=20, blank=True, verbose_name='환자 전화번호')
    address = models.CharField(
        max_length=100, blank=True, verbose_name='환자 주소')
    email = models.EmailField(
        max_length=128, blank=True, verbose_name='환자 이메일 주소')
    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name='환자데이터 생성일자')
    modified_date = models.DateTimeField(
        auto_now=True, null=True, verbose_name='환자데이터 수정일자')
    deleted_date = models.DateTimeField(null=True, verbose_name='환자데이터 삭제일자')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'patient'
        verbose_name = '환자'
