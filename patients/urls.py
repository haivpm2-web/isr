from django.urls import path
from . import views

app_name = 'patients'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('ecg/', views.ecg_list, name='ecg_list'),
    path('ecg/<int:record_id>/', views.ecg_detail, name='ecg_detail'),
    path('recovery/', views.recovery_dashboard, name='recovery'),
]
