from django.db import models

class TreatmentRequest(models.Model):
    doctor = models.ForeignKey(
        'doctor.Doctor', on_delete=models.CASCADE, related_name='patient_req')
    patient = models.ForeignKey(
        'patient.Patient', on_delete=models.CASCADE, related_name='treatment_req')
    symptom = models.CharField(max_length=100, blank=True, verbose_name='증상')
    request_treatment_time = models.DateTimeField(verbose_name='진료 희망 날짜시간')
    created_date = models.DateTimeField(
        auto_now_add=True, verbose_name='진료 요청 데이터 생성일자')
    is_accepted = models.BooleanField(blank=True, verbose_name='진료 요청 수락여부')
    accepted_date = models.DateTimeField(null=True, verbose_name='진료 요청 수락 일시')
    request_treatment_expiration_time = models.DateTimeField(
        verbose_name='진료 요청 만료 일시')

    def __str__(self):
        return '{}가 {} 의사에게 진료 요청'.format(self.patient, self.doctor)

    class Meta:
        db_table = 'treatment_request'
        verbose_name = '진료 요청'
        indexes = [
           models.Index(fields=['doctor','day_type']),
           models.Index(fields=['doctor','is_accepted','request_treatment_expiration_time']),
        ]
