from django.contrib import admin
from .models import DoctorProfile


@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'department', 'license_number', 'patient_count')
    search_fields = ('user__first_name', 'user__last_name', 'license_number', 'specialization')
    list_filter = ('department',)
