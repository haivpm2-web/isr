import os
from datetime import timedelta

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from accounts.models import CustomUser
from doctors.models import DoctorProfile
from patients.models import (
    ECGRecord,
    ExaminationRecord,
    LegRecoveryRecord,
    PatientProfile,
    PrescriptionRecord,
    RehabilitationAssessment,
)


DEFAULT_PASSWORD = os.getenv('DJANGO_DEMO_PASSWORD', 'Demo@12345')


class Command(BaseCommand):
    help = 'Create demo users and realistic clinical sample data for template testing.'

    @transaction.atomic
    def handle(self, *args, **options):
        doctor_user = self._upsert_user(
            username='doctor_demo',
            role=CustomUser.ROLE_DOCTOR,
            first_name='Minh',
            last_name='Nguyen',
            email='doctor_demo@example.com',
            phone_number='0901000002',
            is_staff=True,
        )
        doctor_profile, _ = DoctorProfile.objects.update_or_create(
            user=doctor_user,
            defaults={
                'specialization': 'Phục hồi chức năng thần kinh',
                'license_number': 'LIC-DEMO-001',
                'department': 'rehabilitation',
                'years_of_experience': 9,
                'bio': 'Phụ trách theo dõi ca phục hồi sau phẫu thuật và chấn thương vận động.',
            },
        )

        nurse_user = self._upsert_user(
            username='nurse_demo',
            role=CustomUser.ROLE_NURSE,
            first_name='Lan',
            last_name='Tran',
            email='nurse_demo@example.com',
            phone_number='0901000003',
            is_staff=True,
        )

        admin_user = self._upsert_user(
            username='admin_demo',
            role=CustomUser.ROLE_ADMIN,
            first_name='Hai',
            last_name='Vu',
            email='admin_demo@example.com',
            phone_number='0901000001',
            is_staff=True,
            is_superuser=True,
        )

        patient_primary = self._upsert_patient(
            username='patient_demo',
            first_name='An',
            last_name='Pham',
            email='patient_demo@example.com',
            gender='M',
            doctor=doctor_profile,
            blood_type='O+',
            diagnosis='Sau phẫu thuật tái tạo dây chằng chéo trước, cần theo dõi ECG và phục hồi chức năng chi dưới.',
            treatment_status='inpatient',
            surgery_status='post_op',
            surgery_name='Nội soi tái tạo dây chằng chéo trước gối phải',
            postoperative_status='improving',
            phone_number='0901000004',
        )

        patient_secondary = self._upsert_patient(
            username='patient_demo_2',
            first_name='Linh',
            last_name='Le',
            email='patient_demo_2@example.com',
            gender='F',
            doctor=doctor_profile,
            blood_type='A+',
            diagnosis='Phục hồi sau gãy mâm chày trái, tiến triển ổn định.',
            treatment_status='home',
            surgery_status='completed',
            surgery_name='Kết hợp xương mâm chày trái',
            postoperative_status='stable',
            phone_number='0901000005',
        )

        self._seed_primary_case(patient_primary, nurse_user, doctor_user)
        self._seed_secondary_case(patient_secondary, nurse_user, doctor_user)

        self.stdout.write(self.style.SUCCESS('Demo data ready.'))
        self.stdout.write(f'Admin   : admin_demo / {DEFAULT_PASSWORD}')
        self.stdout.write(f'Doctor  : doctor_demo / {DEFAULT_PASSWORD}')
        self.stdout.write(f'Nurse   : nurse_demo / {DEFAULT_PASSWORD}')
        self.stdout.write(f'Patient : patient_demo / {DEFAULT_PASSWORD}')
        self.stdout.write(f'Patient2: patient_demo_2 / {DEFAULT_PASSWORD}')
        self.stdout.write(f'Admin object id: {admin_user.id}')

    def _upsert_user(
        self,
        *,
        username,
        role,
        first_name,
        last_name,
        email,
        phone_number,
        is_staff=False,
        is_superuser=False,
    ):
        user, created = CustomUser.objects.get_or_create(username=username)
        user.role = role
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.phone_number = phone_number
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.is_active = True
        if created or not user.check_password(DEFAULT_PASSWORD):
            user.set_password(DEFAULT_PASSWORD)
        user.save()
        return user

    def _upsert_patient(
        self,
        *,
        username,
        first_name,
        last_name,
        email,
        gender,
        doctor,
        blood_type,
        diagnosis,
        treatment_status,
        surgery_status,
        surgery_name,
        postoperative_status,
        phone_number,
    ):
        user = self._upsert_user(
            username=username,
            role=CustomUser.ROLE_PATIENT,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            is_staff=False,
        )
        today = timezone.localdate()
        profile, _ = PatientProfile.objects.update_or_create(
            user=user,
            defaults={
                'doctor': doctor,
                'gender': gender,
                'address': 'Quận 1, TP. Hồ Chí Minh',
                'blood_type': blood_type,
                'diagnosis': diagnosis,
                'treatment_status': treatment_status,
                'admission_date': today - timedelta(days=12),
                'discharge_date': today - timedelta(days=2) if treatment_status == 'discharged' else None,
                'discharge_condition': 'improved' if treatment_status == 'discharged' else '',
                'surgery_status': surgery_status,
                'surgery_name': surgery_name,
                'surgery_date': today - timedelta(days=10),
                'postoperative_status': postoperative_status,
                'emergency_contact_name': 'Người nhà demo',
                'emergency_contact_phone': '0901999999',
                'notes': 'Hồ sơ mẫu phục vụ test template và dashboard.',
                'chief_complaint': 'Đau khớp gối, hạn chế vận động và cần theo dõi chức năng vận động.',
                'present_illness': 'Bệnh nhân hậu phẫu, đang tập đi với trợ giúp và cần theo dõi sức bền.',
                'past_medical_history': 'Tăng huyết áp nhẹ, không ghi nhận bệnh tim mạch nặng.',
                'surgical_history': 'Đã phẫu thuật chỉnh hình gần đây theo kế hoạch điều trị.',
                'family_history': 'Gia đình có tiền sử thoái hóa khớp.',
                'social_history': 'Không hút thuốc, vận động trước chấn thương ở mức trung bình.',
                'allergies': 'Không ghi nhận dị ứng thuốc.',
                'current_medications': 'Paracetamol, celecoxib, vitamin nhóm B.',
            },
        )
        return profile

    def _seed_primary_case(self, patient, nurse_user, doctor_user):
        now = timezone.now()
        ecg_samples = [
            {'days': 9, 'heart_rate': 108, 'pr': 152, 'qrs': 94, 'qt': 430, 'qtc': 458, 'rr': 556, 'rhythm': 'sinus_tach', 'abnormal': True, 'st': 0.8, 'note': 'Nhịp nhanh xoang sau đau hậu phẫu.'},
            {'days': 6, 'heart_rate': 96, 'pr': 148, 'qrs': 92, 'qt': 422, 'qtc': 440, 'rr': 625, 'rhythm': 'normal_sinus', 'abnormal': False, 'st': 0.2, 'note': 'Chỉ số dần ổn định.'},
            {'days': 3, 'heart_rate': 88, 'pr': 150, 'qrs': 90, 'qt': 418, 'qtc': 432, 'rr': 682, 'rhythm': 'normal_sinus', 'abnormal': False, 'st': 0.1, 'note': 'ECG gần đây ổn định, tiếp tục theo dõi.'},
        ]
        for sample in ecg_samples:
            recorded_at = now - timedelta(days=sample['days'])
            ECGRecord.objects.update_or_create(
                patient=patient,
                recorded_at=recorded_at,
                defaults={
                    'recorded_by': nurse_user,
                    'heart_rate': sample['heart_rate'],
                    'pr_interval': sample['pr'],
                    'qrs_duration': sample['qrs'],
                    'qt_interval': sample['qt'],
                    'qtc_interval': sample['qtc'],
                    'rr_interval': sample['rr'],
                    'p_wave_amplitude': 0.16,
                    'qrs_amplitude': 1.2,
                    't_wave_amplitude': 0.32,
                    'st_change': sample['st'],
                    'rhythm': sample['rhythm'],
                    'is_abnormal': sample['abnormal'],
                    'notes': sample['note'],
                },
            )

        recovery_samples = [
            {'days': 10, 'strength': 2, 'rom': 55, 'pain': 8, 'swelling': 2, 'walking': '2', 'recovery': 28, 'fatigue': 8, 'gait': 0.35, 'force': 180},
            {'days': 6, 'strength': 3, 'rom': 78, 'pain': 6, 'swelling': 1, 'walking': '3', 'recovery': 48, 'fatigue': 6, 'gait': 0.52, 'force': 240},
            {'days': 2, 'strength': 4, 'rom': 102, 'pain': 4, 'swelling': 1, 'walking': '5', 'recovery': 72, 'fatigue': 4, 'gait': 0.83, 'force': 330},
        ]
        for sample in recovery_samples:
            recorded_at = now - timedelta(days=sample['days'])
            LegRecoveryRecord.objects.update_or_create(
                patient=patient,
                recorded_at=recorded_at,
                defaults={
                    'recorded_by': nurse_user,
                    'affected_leg': 'right',
                    'muscle_strength': sample['strength'],
                    'range_of_motion': sample['rom'],
                    'heart_rate': 84,
                    'spo2': 98.0,
                    'fatigue_index': sample['fatigue'],
                    'imu_velocity': round(sample['gait'] * 1.18, 2),
                    'imu_acceleration': 0.72,
                    'gait_speed': sample['gait'],
                    'cadence': 82.0 + sample['strength'] * 4,
                    'step_length': 28.0 + sample['strength'] * 6,
                    'plantar_force': sample['force'],
                    'pain_level': sample['pain'],
                    'swelling_level': sample['swelling'],
                    'walking_ability': sample['walking'],
                    'recovery_percentage': sample['recovery'],
                    'physical_therapy_notes': 'Tập mạnh cơ tứ đầu đùi, ROM gối và tập đứng chuyển trọng lượng.',
                    'doctor_notes': 'Tiến triển tốt, tăng dần cường độ tập và theo dõi đau sau vận động.',
                },
            )

        exam = ExaminationRecord.objects.update_or_create(
            patient=patient,
            exam_date=now - timedelta(days=1),
            defaults={
                'examined_by': nurse_user,
                'blood_pressure_systolic': 126,
                'blood_pressure_diastolic': 78,
                'heart_rate': 82,
                'respiratory_rate': 18,
                'temperature': 36.9,
                'spo2': 98.0,
                'weight': 67.5,
                'height': 171.0,
                'chief_complaint': 'Đau gối phải tăng sau tập cuối buổi chiều.',
                'clinical_findings': 'Vết mổ khô, ROM cải thiện, chịu lực bán phần tốt.',
                'diagnosis': patient.diagnosis,
                'treatment_plan': 'Duy trì vật lý trị liệu 2 buổi/ngày, tăng bài tập dáng đi với gậy.',
                'prescription': 'Celecoxib 200mg, Paracetamol 500mg khi đau, calcium + vitamin D.',
                'follow_up_date': timezone.localdate() + timedelta(days=7),
                'notes': 'Tiếp tục đánh giá sức bền và dáng đi ở lần tái khám sau.',
            },
        )[0]

        PrescriptionRecord.objects.update_or_create(
            patient=patient,
            issued_at=now - timedelta(hours=16),
            defaults={
                'examination': exam,
                'prescribed_by': doctor_user,
                'diagnosis': patient.diagnosis,
                'clinical_notes': 'Sau mổ ACL, đau mức trung bình, không có dấu hiệu biến chứng tim mạch.',
                'medications': '1. Celecoxib 200mg\n2. Paracetamol 500mg\n3. Calcium + Vitamin D',
                'dosage_instructions': 'Celecoxib ngày 2 lần sau ăn. Paracetamol khi đau, tối đa 4 viên/ngày.',
                'advice': 'Chườm lạnh sau tập, nâng chân cao khi nghỉ, tái khám sau 7 ngày.',
                'follow_up_date': timezone.localdate() + timedelta(days=7),
                'blood_pressure_systolic': 126,
                'blood_pressure_diastolic': 78,
                'heart_rate': 82,
                'respiratory_rate': 18,
                'temperature': 36.9,
                'spo2': 98.0,
                'weight': 67.5,
                'pain_score': 4,
                'blood_glucose': 5.6,
                'notes': 'Đơn mẫu phục vụ test template in toa thuốc.',
            },
        )

        RehabilitationAssessment.objects.update_or_create(
            patient=patient,
            assessed_at=now - timedelta(hours=12),
            defaults={
                'assessed_by': nurse_user,
                'assessment_type': 'progress',
                'barthel_index': 75,
                'fim_score': 98,
                'mrs_score': 2,
                'fugl_meyer_upper': 60,
                'fugl_meyer_lower': 26,
                'rivermead_motor_index': 11,
                'mas_score': 36,
                'motricity_index_upper': 84,
                'motricity_index_lower': 68,
                'rom_notes': 'Gối phải gấp 0-102 độ, duỗi gần hoàn toàn.',
                'berg_balance_scale': 42,
                'dynamic_gait_index': 17,
                'six_minute_walk': 268.0,
                'pain_rating': 4,
                'dash_score': 18.5,
                'nihss_score': 0,
                'bp_systolic': 124,
                'bp_diastolic': 80,
                'heart_rate': 80,
                'respiratory_rate': 18,
                'notes': 'Có thể nâng mục tiêu sang đi lại với gậy trong nhà và tự chăm sóc cơ bản.',
            },
        )

    def _seed_secondary_case(self, patient, nurse_user, doctor_user):
        now = timezone.now()
        ECGRecord.objects.update_or_create(
            patient=patient,
            recorded_at=now - timedelta(days=4),
            defaults={
                'recorded_by': nurse_user,
                'heart_rate': 76,
                'pr_interval': 146,
                'qrs_duration': 88,
                'qt_interval': 402,
                'qtc_interval': 426,
                'rr_interval': 790,
                'p_wave_amplitude': 0.15,
                'qrs_amplitude': 1.1,
                't_wave_amplitude': 0.30,
                'st_change': 0.0,
                'rhythm': 'normal_sinus',
                'is_abnormal': False,
                'notes': 'Ca ổn định, ECG phục vụ hiển thị bệnh nhân phục hồi tốt.',
            },
        )
        LegRecoveryRecord.objects.update_or_create(
            patient=patient,
            recorded_at=now - timedelta(days=1),
            defaults={
                'recorded_by': nurse_user,
                'affected_leg': 'left',
                'muscle_strength': 5,
                'range_of_motion': 125,
                'heart_rate': 76,
                'spo2': 99.0,
                'fatigue_index': 2,
                'imu_velocity': 1.18,
                'imu_acceleration': 0.84,
                'gait_speed': 1.02,
                'cadence': 108.0,
                'step_length': 57.0,
                'plantar_force': 410,
                'pain_level': 2,
                'swelling_level': 0,
                'walking_ability': '6',
                'recovery_percentage': 91,
                'physical_therapy_notes': 'Có thể chuyển sang bài tập sức bền và thăng bằng nâng cao.',
                'doctor_notes': 'Đủ điều kiện theo dõi ngoại trú, hẹn đánh giá lại sau 2 tuần.',
            },
        )
        exam = ExaminationRecord.objects.update_or_create(
            patient=patient,
            exam_date=now - timedelta(days=2),
            defaults={
                'examined_by': nurse_user,
                'blood_pressure_systolic': 118,
                'blood_pressure_diastolic': 74,
                'heart_rate': 76,
                'respiratory_rate': 17,
                'temperature': 36.7,
                'spo2': 99.0,
                'weight': 54.0,
                'height': 160.0,
                'chief_complaint': 'Mỏi nhẹ sau đi bộ dài.',
                'clinical_findings': 'Dáng đi gần như bình thường, không còn sưng nề đáng kể.',
                'diagnosis': patient.diagnosis,
                'treatment_plan': 'Theo dõi ngoại trú, tiếp tục bài tập tại nhà.',
                'prescription': 'Vitamin D, calcium, gel bôi giảm đau tại chỗ khi cần.',
                'follow_up_date': timezone.localdate() + timedelta(days=14),
                'notes': 'Ca phục hồi tốt dùng để hiển thị trạng thái ổn định trên dashboard.',
            },
        )[0]
        PrescriptionRecord.objects.update_or_create(
            patient=patient,
            issued_at=now - timedelta(days=2, hours=2),
            defaults={
                'examination': exam,
                'prescribed_by': doctor_user,
                'diagnosis': patient.diagnosis,
                'clinical_notes': 'Tiến triển tốt, chỉ cần hỗ trợ giảm đau nhẹ khi vận động nhiều.',
                'medications': '1. Calcium\n2. Vitamin D3\n3. Gel diclofenac bôi ngoài da',
                'dosage_instructions': 'Dùng theo đơn, ưu tiên tập tại nhà đều đặn.',
                'advice': 'Đi bộ tăng dần quãng đường, tránh xoay gối đột ngột.',
                'follow_up_date': timezone.localdate() + timedelta(days=14),
                'blood_pressure_systolic': 118,
                'blood_pressure_diastolic': 74,
                'heart_rate': 76,
                'respiratory_rate': 17,
                'temperature': 36.7,
                'spo2': 99.0,
                'weight': 54.0,
                'pain_score': 2,
                'blood_glucose': 5.1,
                'notes': 'Đơn mẫu cho ca hồi phục tốt.',
            },
        )
        RehabilitationAssessment.objects.update_or_create(
            patient=patient,
            assessed_at=now - timedelta(days=1, hours=4),
            defaults={
                'assessed_by': nurse_user,
                'assessment_type': 'discharge',
                'barthel_index': 95,
                'fim_score': 118,
                'mrs_score': 1,
                'fugl_meyer_upper': 64,
                'fugl_meyer_lower': 31,
                'rivermead_motor_index': 14,
                'mas_score': 44,
                'motricity_index_upper': 92,
                'motricity_index_lower': 88,
                'rom_notes': 'ROM khớp gối trái gần trọn vẹn.',
                'berg_balance_scale': 52,
                'dynamic_gait_index': 22,
                'six_minute_walk': 430.0,
                'pain_rating': 2,
                'dash_score': 8.0,
                'nihss_score': 0,
                'bp_systolic': 118,
                'bp_diastolic': 74,
                'heart_rate': 74,
                'respiratory_rate': 17,
                'notes': 'Thích hợp theo dõi tại nhà, tập duy trì sức mạnh và thăng bằng.',
            },
        )