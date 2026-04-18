from django.contrib import admin
from .models import PatientProfile, ECGRecord, LegRecoveryRecord, ExaminationRecord, PrescriptionRecord, RehabilitationAssessment


@admin.register(PatientProfile)
class PatientProfileAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'gender', 'blood_type', 'treatment_status', 'surgery_status', 'discharge_condition', 'doctor', 'admission_date')
    search_fields = ('user__first_name', 'user__last_name', 'diagnosis')
    list_filter = ('gender', 'blood_type', 'treatment_status', 'surgery_status', 'discharge_condition')


@admin.register(ECGRecord)
class ECGRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'recorded_at', 'heart_rate', 'rhythm', 'is_abnormal')
    list_filter = ('is_abnormal', 'rhythm')
    search_fields = ('patient__user__first_name', 'patient__user__last_name')
    ordering = ('-recorded_at',)


@admin.register(LegRecoveryRecord)
class LegRecoveryRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'recorded_at', 'affected_leg', 'recovery_percentage', 'walking_ability')
    list_filter = ('affected_leg',)
    ordering = ('-recorded_at',)


@admin.register(ExaminationRecord)
class ExaminationRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'exam_date', 'examined_by', 'diagnosis')
    ordering = ('-exam_date',)


@admin.register(PrescriptionRecord)
class PrescriptionRecordAdmin(admin.ModelAdmin):
    list_display = ('patient', 'issued_at', 'prescribed_by', 'follow_up_date')
    search_fields = ('patient__user__first_name', 'patient__user__last_name', 'diagnosis', 'medications')
    ordering = ('-issued_at',)


@admin.register(RehabilitationAssessment)
class RehabilitationAssessmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'assessed_at', 'assessment_type', 'barthel_index', 'berg_balance_scale')
    list_filter = ('assessment_type',)
    ordering = ('-assessed_at',)
