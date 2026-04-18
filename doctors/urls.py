from django.urls import path
from . import views

app_name = 'doctors'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('patients/', views.patient_list, name='patient_list'),
    path('patients/<int:patient_id>/', views.patient_detail, name='patient_detail'),
    path('patients/<int:patient_id>/bio/', views.edit_patient_bio, name='edit_patient_bio'),
    # ECG
    path('patients/<int:patient_id>/ecg/add/', views.add_ecg, name='add_ecg'),
    # Leg recovery
    path('patients/<int:patient_id>/recovery/add/', views.add_recovery, name='add_recovery'),
    # Examination (visit history)
    path('patients/<int:patient_id>/exam/add/', views.add_examination, name='add_examination'),
    path('patients/<int:patient_id>/exam/', views.examination_list, name='examination_list'),
    path('patients/<int:patient_id>/exam/<int:exam_id>/', views.examination_detail, name='examination_detail'),
    # Prescription / medication orders
    path('patients/<int:patient_id>/prescriptions/add/', views.add_prescription, name='add_prescription'),
    path('patients/<int:patient_id>/prescriptions/', views.prescription_list, name='prescription_list'),
    path('patients/<int:patient_id>/prescriptions/<int:prescription_id>/', views.prescription_detail, name='prescription_detail'),
    # Rehabilitation assessment
    path('patients/<int:patient_id>/rehab/add/', views.add_rehab_assessment, name='add_rehab_assessment'),
    path('patients/<int:patient_id>/rehab/', views.rehab_assessment_list, name='rehab_assessment_list'),
    path('patients/<int:patient_id>/rehab/<int:ra_id>/', views.rehab_assessment_detail, name='rehab_assessment_detail'),
]
