from django.contrib import admin
from .models import Doctor, Hospital, NonpaidCareItem, Profile, TreatmentDepartment, TreatmentTime


# Register your models here.
admin.site.register(Doctor)
admin.site.register(Hospital)
admin.site.register(TreatmentDepartment)
admin.site.register(NonpaidCareItem)
admin.site.register(TreatmentTime)
admin.site.register(Profile)
