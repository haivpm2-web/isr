from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_ADMIN = 'admin'
    ROLE_DOCTOR = 'doctor'
    ROLE_NURSE = 'nurse'
    ROLE_PATIENT = 'patient'

    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Quản trị viên'),
        (ROLE_DOCTOR, 'Bác sĩ'),
        (ROLE_NURSE, 'Điều dưỡng / Y tá'),
        (ROLE_PATIENT, 'Bệnh nhân'),
    ]

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=ROLE_PATIENT,
        verbose_name='Vai trò',
    )
    phone_number = models.CharField(max_length=15, blank=True, verbose_name='Số điện thoại')
    date_of_birth = models.DateField(null=True, blank=True, verbose_name='Ngày sinh')

    def is_admin_user(self):
        return self.role == self.ROLE_ADMIN or self.is_superuser

    def is_doctor(self):
        return self.role == self.ROLE_DOCTOR

    def is_nurse_user(self):
        return self.role == self.ROLE_NURSE

    def is_clinical_staff(self):
        return self.role in {self.ROLE_DOCTOR, self.ROLE_NURSE}

    def is_patient_user(self):
        return self.role == self.ROLE_PATIENT

    class Meta:
        verbose_name = 'Người dùng'
        verbose_name_plural = 'Người dùng'

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"
