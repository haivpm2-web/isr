from django.db import models
from accounts.models import CustomUser


class DoctorProfile(models.Model):
    DEPARTMENT_CHOICES = [
        ('cardiology', 'Tim mạch'),
        ('rehabilitation', 'Phục hồi chức năng'),
        ('orthopedics', 'Chỉnh hình - Chấn thương'),
        ('neurology', 'Thần kinh'),
        ('internal', 'Nội tổng quát'),
        ('surgery', 'Ngoại tổng quát'),
        ('other', 'Khác'),
    ]

    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE,
        related_name='doctor_profile',
        verbose_name='Tài khoản',
    )
    specialization = models.CharField(max_length=100, verbose_name='Chuyên khoa')
    license_number = models.CharField(max_length=50, unique=True, verbose_name='Số chứng chỉ hành nghề')
    department = models.CharField(
        max_length=20, choices=DEPARTMENT_CHOICES,
        default='rehabilitation', verbose_name='Khoa',
    )
    years_of_experience = models.PositiveIntegerField(default=0, verbose_name='Số năm kinh nghiệm')
    bio = models.TextField(blank=True, verbose_name='Giới thiệu')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Hồ sơ bác sĩ'
        verbose_name_plural = 'Hồ sơ bác sĩ'

    def __str__(self):
        return f"BS. {self.user.get_full_name()} – {self.specialization}"

    @property
    def patient_count(self):
        return self.patients.count()
