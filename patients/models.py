from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from accounts.models import CustomUser


class PatientProfile(models.Model):
    GENDER_CHOICES = [('M', 'Nam'), ('F', 'Nữ')]
    TREATMENT_STATUS_CHOICES = [
        ('inpatient', 'Điều trị nội viện'),
        ('home', 'Điều trị tại nhà'),
        ('discharged', 'Đã xuất viện'),
    ]
    DISCHARGE_CONDITION_CHOICES = [
        ('', 'Chưa áp dụng'),
        ('recovered', 'Khỏi / hồi phục tốt'),
        ('improved', 'Đỡ / cải thiện'),
        ('stable', 'Ổn định'),
        ('transferred', 'Chuyển viện'),
        ('ama', 'Xin về / trái chỉ định'),
        ('other', 'Khác'),
    ]
    SURGERY_STATUS_CHOICES = [
        ('none', 'Chưa có chỉ định phẫu thuật'),
        ('indicated', 'Có chỉ định phẫu thuật'),
        ('planned', 'Đã lên kế hoạch phẫu thuật'),
        ('pre_op', 'Đang chuẩn bị tiền phẫu'),
        ('post_op', 'Đang hậu phẫu'),
        ('completed', 'Đã phẫu thuật'),
        ('cancelled', 'Hoãn / hủy phẫu thuật'),
    ]
    POSTOPERATIVE_STATUS_CHOICES = [
        ('', 'Chưa áp dụng'),
        ('stable', 'Hậu phẫu ổn định'),
        ('monitoring', 'Đang theo dõi sát'),
        ('improving', 'Đang cải thiện'),
        ('complication', 'Có biến chứng'),
        ('critical', 'Nặng / cần can thiệp thêm'),
        ('recovered', 'Phục hồi tốt sau mổ'),
    ]
    BLOOD_TYPE_CHOICES = [
        ('', 'Chưa xác định'),
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]

    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE,
        related_name='patient_profile', verbose_name='Tài khoản',
    )
    doctor = models.ForeignKey(
        'doctors.DoctorProfile', on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='patients', verbose_name='Bác sĩ phụ trách',
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name='Giới tính')
    address = models.TextField(blank=True, verbose_name='Địa chỉ')
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPE_CHOICES, blank=True, verbose_name='Nhóm máu')
    diagnosis = models.TextField(blank=True, verbose_name='Chẩn đoán')
    treatment_status = models.CharField(
        max_length=20,
        choices=TREATMENT_STATUS_CHOICES,
        default='inpatient',
        verbose_name='Trạng thái điều trị',
    )
    admission_date = models.DateField(null=True, blank=True, verbose_name='Ngày nhập viện')
    discharge_date = models.DateField(null=True, blank=True, verbose_name='Ngày xuất viện')
    discharge_condition = models.CharField(
        max_length=20,
        choices=DISCHARGE_CONDITION_CHOICES,
        blank=True,
        default='',
        verbose_name='Tình trạng xuất viện',
    )
    surgery_status = models.CharField(
        max_length=20,
        choices=SURGERY_STATUS_CHOICES,
        default='none',
        verbose_name='Trạng thái phẫu thuật',
    )
    surgery_name = models.CharField(max_length=200, blank=True, verbose_name='Tên phẫu thuật / thủ thuật')
    surgery_date = models.DateField(null=True, blank=True, verbose_name='Ngày phẫu thuật')
    postoperative_status = models.CharField(
        max_length=20,
        choices=POSTOPERATIVE_STATUS_CHOICES,
        blank=True,
        default='',
        verbose_name='Tình trạng hậu phẫu',
    )
    emergency_contact_name = models.CharField(max_length=100, blank=True, verbose_name='Người liên hệ khẩn cấp')
    emergency_contact_phone = models.CharField(max_length=15, blank=True, verbose_name='SĐT khẩn cấp')
    notes = models.TextField(blank=True, verbose_name='Ghi chú')

    # ── Tiểu sử bệnh lý ──────────────────────────────────────
    chief_complaint = models.TextField(blank=True, verbose_name='Lý do vào viện / Triệu chứng chính')
    present_illness = models.TextField(blank=True, verbose_name='Bệnh sử hiện tại')
    past_medical_history = models.TextField(blank=True, verbose_name='Tiền sử bệnh lý')
    surgical_history = models.TextField(blank=True, verbose_name='Tiền sử phẫu thuật')
    family_history = models.TextField(blank=True, verbose_name='Tiền sử gia đình')
    social_history = models.TextField(blank=True, verbose_name='Tiền sử xã hội')
    allergies = models.TextField(blank=True, verbose_name='Dị ứng')
    current_medications = models.TextField(blank=True, verbose_name='Thuốc đang dùng')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Hồ sơ bệnh nhân'
        verbose_name_plural = 'Hồ sơ bệnh nhân'

    def __str__(self):
        return f"BN: {self.user.get_full_name()}"

    @property
    def latest_ecg(self):
        return self.ecg_records.first()

    @property
    def latest_recovery(self):
        return self.recovery_records.first()

    @property
    def overall_recovery(self):
        r = self.latest_recovery
        return r.recovery_percentage if r else 0


class ECGRecord(models.Model):
    RHYTHM_CHOICES = [
        ('normal_sinus', 'Nhịp xoang bình thường'),
        ('sinus_tach', 'Nhịp nhanh xoang (>100 bpm)'),
        ('sinus_brad', 'Nhịp chậm xoang (<60 bpm)'),
        ('afib', 'Rung nhĩ (AF)'),
        ('aflutter', 'Cuồng nhĩ'),
        ('vt', 'Nhịp nhanh thất (VT)'),
        ('vf', 'Rung thất (VF)'),
        ('first_deg_block', 'Block nhĩ thất độ I'),
        ('second_deg_block', 'Block nhĩ thất độ II'),
        ('third_deg_block', 'Block nhĩ thất độ III'),
        ('lbbb', 'Block nhánh trái (LBBB)'),
        ('rbbb', 'Block nhánh phải (RBBB)'),
        ('pvc', 'Ngoại tâm thu thất (PVC)'),
        ('pac', 'Ngoại tâm thu nhĩ (PAC)'),
        ('other', 'Khác'),
    ]

    patient = models.ForeignKey(
        PatientProfile, on_delete=models.CASCADE,
        related_name='ecg_records', verbose_name='Bệnh nhân',
    )
    recorded_at = models.DateTimeField(verbose_name='Thời gian đo')
    recorded_by = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True,
        related_name='recorded_ecgs', verbose_name='Người thực hiện',
    )

    # Core intervals
    heart_rate = models.PositiveIntegerField(verbose_name='Nhịp tim (bpm)')
    pr_interval = models.FloatField(verbose_name='Khoảng PR (ms)')
    qrs_duration = models.FloatField(verbose_name='Thời gian QRS (ms)')
    qt_interval = models.FloatField(verbose_name='Khoảng QT (ms)')
    qtc_interval = models.FloatField(null=True, blank=True, verbose_name='Khoảng QTc (ms)')
    rr_interval = models.FloatField(null=True, blank=True, verbose_name='Khoảng RR (ms)')

    # Wave amplitudes
    p_wave_amplitude = models.FloatField(null=True, blank=True, verbose_name='Biên độ sóng P (mV)')
    qrs_amplitude = models.FloatField(null=True, blank=True, verbose_name='Biên độ QRS (mV)')
    t_wave_amplitude = models.FloatField(null=True, blank=True, verbose_name='Biên độ sóng T (mV)')

    # ST segment
    st_change = models.FloatField(null=True, blank=True, verbose_name='Thay đổi ST (mm)')

    rhythm = models.CharField(max_length=30, choices=RHYTHM_CHOICES, default='normal_sinus', verbose_name='Loại nhịp')
    is_abnormal = models.BooleanField(default=False, verbose_name='Có bất thường')
    notes = models.TextField(blank=True, verbose_name='Nhận xét')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-recorded_at']
        verbose_name = 'Kết quả ECG'
        verbose_name_plural = 'Kết quả ECG'

    def __str__(self):
        return f"ECG – {self.patient.user.get_full_name()} – {self.recorded_at.strftime('%d/%m/%Y %H:%M')}"

    def hr_status(self):
        if self.heart_rate < 60:
            return 'warning', 'Nhịp chậm'
        if self.heart_rate > 100:
            return 'danger', 'Nhịp nhanh'
        return 'success', 'Bình thường'

    def pr_status(self):
        if self.pr_interval < 120 or self.pr_interval > 200:
            return 'danger', 'Bất thường'
        return 'success', 'Bình thường'

    def qrs_status(self):
        if self.qrs_duration >= 120:
            return 'warning', 'Kéo dài'
        return 'success', 'Bình thường'

    def qt_status(self):
        if self.qt_interval > 440:
            return 'danger', 'Kéo dài'
        if self.qt_interval < 350:
            return 'warning', 'Ngắn'
        return 'success', 'Bình thường'


class LegRecoveryRecord(models.Model):
    AFFECTED_LEG_CHOICES = [
        ('left', 'Chân trái'),
        ('right', 'Chân phải'),
        ('both', 'Cả hai chân'),
    ]
    WALKING_ABILITY_CHOICES = [
        ('0', 'Không thể đi lại'),
        ('1', 'Chỉ nằm/ngồi trên giường'),
        ('2', 'Xe lăn'),
        ('3', 'Khung đỡ (walker)'),
        ('4', 'Nạng (crutches)'),
        ('5', 'Gậy (cane)'),
        ('6', 'Đi độc lập'),
    ]
    MUSCLE_STRENGTH_CHOICES = [
        (0, 'Độ 0 – Không có co cơ'),
        (1, 'Độ 1 – Co cơ nhẹ, không tạo chuyển động'),
        (2, 'Độ 2 – Vận động khi loại bỏ trọng lực'),
        (3, 'Độ 3 – Thắng được trọng lực'),
        (4, 'Độ 4 – Thắng được lực cản nhẹ'),
        (5, 'Độ 5 – Sức mạnh bình thường'),
    ]
    SWELLING_CHOICES = [
        (0, 'Không sưng'),
        (1, 'Sưng nhẹ'),
        (2, 'Sưng vừa'),
        (3, 'Sưng nặng'),
    ]

    patient = models.ForeignKey(
        PatientProfile, on_delete=models.CASCADE,
        related_name='recovery_records', verbose_name='Bệnh nhân',
    )
    recorded_at = models.DateTimeField(verbose_name='Thời gian ghi nhận')
    recorded_by = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True,
        related_name='recorded_recoveries', verbose_name='Người ghi nhận',
    )

    affected_leg = models.CharField(max_length=5, choices=AFFECTED_LEG_CHOICES, verbose_name='Chân bị ảnh hưởng')
    muscle_strength = models.IntegerField(choices=MUSCLE_STRENGTH_CHOICES, verbose_name='Sức mạnh cơ (MRC 0–5)')
    range_of_motion = models.IntegerField(verbose_name='Biên độ vận động (độ)')
    heart_rate = models.IntegerField(null=True, blank=True, verbose_name='Nhịp tim (HR, bpm)')
    spo2 = models.FloatField(null=True, blank=True, verbose_name='SpO₂ (%)')
    fatigue_index = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name='Mức mệt (fatigue index 0–10)',
    )
    imu_velocity = models.FloatField(null=True, blank=True, verbose_name='IMU velocity (m/s)')
    imu_acceleration = models.FloatField(null=True, blank=True, verbose_name='IMU acceleration (m/s²)')
    gait_speed = models.FloatField(null=True, blank=True, verbose_name='Tốc độ dáng đi (m/s)')
    cadence = models.FloatField(null=True, blank=True, verbose_name='Cadence (bước/phút)')
    step_length = models.FloatField(null=True, blank=True, verbose_name='Chiều dài bước (cm)')
    plantar_force = models.FloatField(null=True, blank=True, verbose_name='Lực đạp chân / plantar force (N)')
    pain_level = models.IntegerField(
        choices=[(i, str(i)) for i in range(11)],
        verbose_name='Mức độ đau (VAS 0–10)',
    )
    swelling_level = models.IntegerField(choices=SWELLING_CHOICES, verbose_name='Mức độ sưng')
    walking_ability = models.CharField(max_length=2, choices=WALKING_ABILITY_CHOICES, verbose_name='Khả năng đi lại')
    recovery_percentage = models.IntegerField(default=0, verbose_name='Tỷ lệ phục hồi (%)')
    physical_therapy_notes = models.TextField(blank=True, verbose_name='Ghi chú vật lý trị liệu')
    doctor_notes = models.TextField(blank=True, verbose_name='Ghi chú bác sĩ')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-recorded_at']
        verbose_name = 'Hồ sơ phục hồi'
        verbose_name_plural = 'Hồ sơ phục hồi'

    def __str__(self):
        return f"Phục hồi – {self.patient.user.get_full_name()} – {self.recorded_at.strftime('%d/%m/%Y')}"

    def recovery_color(self):
        p = self.recovery_percentage
        if p < 30:
            return 'danger'
        if p < 60:
            return 'warning'
        if p < 80:
            return 'info'
        return 'success'

    def pain_color(self):
        if self.pain_level <= 3:
            return 'success'
        if self.pain_level <= 6:
            return 'warning'
        return 'danger'

    def muscle_color(self):
        colors = {0: 'danger', 1: 'danger', 2: 'warning', 3: 'info', 4: 'primary', 5: 'success'}
        return colors.get(self.muscle_strength, 'secondary')

    def fatigue_color(self):
        if self.fatigue_index is None:
            return 'secondary'
        if self.fatigue_index <= 3:
            return 'success'
        if self.fatigue_index <= 6:
            return 'warning'
        return 'danger'


# ─────────────────────────────────────────────────────────────────────────────
# Lịch sử khám bệnh
# ─────────────────────────────────────────────────────────────────────────────

class ExaminationRecord(models.Model):
    patient = models.ForeignKey(
        PatientProfile, on_delete=models.CASCADE,
        related_name='examination_records', verbose_name='Bệnh nhân',
    )
    examined_by = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True,
        related_name='examinations_done', verbose_name='Bác sĩ khám',
    )
    exam_date = models.DateTimeField(verbose_name='Ngày giờ khám')

    # Dấu hiệu sinh tồn
    blood_pressure_systolic = models.IntegerField(null=True, blank=True, verbose_name='Huyết áp tâm thu (mmHg)')
    blood_pressure_diastolic = models.IntegerField(null=True, blank=True, verbose_name='Huyết áp tâm trương (mmHg)')
    heart_rate = models.IntegerField(null=True, blank=True, verbose_name='Nhịp tim (bpm)')
    respiratory_rate = models.IntegerField(null=True, blank=True, verbose_name='Nhịp thở (lần/phút)')
    temperature = models.FloatField(null=True, blank=True, verbose_name='Nhiệt độ (°C)')
    spo2 = models.FloatField(null=True, blank=True, verbose_name='SpO₂ (%)')
    weight = models.FloatField(null=True, blank=True, verbose_name='Cân nặng (kg)')
    height = models.FloatField(null=True, blank=True, verbose_name='Chiều cao (cm)')

    # Nội dung khám
    chief_complaint = models.TextField(blank=True, verbose_name='Lý do khám / Triệu chứng')
    clinical_findings = models.TextField(blank=True, verbose_name='Kết quả thăm khám lâm sàng')
    diagnosis = models.TextField(blank=True, verbose_name='Chẩn đoán')
    treatment_plan = models.TextField(blank=True, verbose_name='Hướng điều trị / Kế hoạch')
    prescription = models.TextField(blank=True, verbose_name='Đơn thuốc')
    follow_up_date = models.DateField(null=True, blank=True, verbose_name='Ngày tái khám')
    notes = models.TextField(blank=True, verbose_name='Ghi chú thêm')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-exam_date']
        verbose_name = 'Lịch sử khám'
        verbose_name_plural = 'Lịch sử khám'

    def __str__(self):
        return f"Khám – {self.patient.user.get_full_name()} – {self.exam_date.strftime('%d/%m/%Y')}"

    @property
    def bmi(self):
        if self.weight and self.height and self.height > 0:
            h_m = self.height / 100
            return round(self.weight / (h_m * h_m), 1)
        return None

    def bp_status(self):
        if not self.blood_pressure_systolic:
            return 'secondary', '–'
        s = self.blood_pressure_systolic
        if s >= 180:
            return 'danger', 'Tăng rất cao'
        if s >= 140:
            return 'warning', 'Tăng huyết áp'
        if s < 90:
            return 'info', 'Huyết áp thấp'
        return 'success', 'Bình thường'


class PrescriptionRecord(models.Model):
    patient = models.ForeignKey(
        PatientProfile, on_delete=models.CASCADE,
        related_name='prescriptions', verbose_name='Bệnh nhân',
    )
    examination = models.ForeignKey(
        ExaminationRecord, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='prescriptions', verbose_name='Lần khám liên quan',
    )
    prescribed_by = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True,
        related_name='prescriptions_issued', verbose_name='Bác sĩ chỉ định',
    )
    issued_at = models.DateTimeField(verbose_name='Ngày giờ cấp thuốc')

    diagnosis = models.TextField(blank=True, verbose_name='Chẩn đoán dùng cho đơn')
    clinical_notes = models.TextField(blank=True, verbose_name='Tóm tắt lâm sàng / chỉ định')
    medications = models.TextField(verbose_name='Thuốc được kê')
    dosage_instructions = models.TextField(blank=True, verbose_name='Cách dùng / hướng dẫn dùng thuốc')
    advice = models.TextField(blank=True, verbose_name='Dặn dò thêm')
    follow_up_date = models.DateField(null=True, blank=True, verbose_name='Ngày tái khám')

    blood_pressure_systolic = models.IntegerField(null=True, blank=True, verbose_name='Huyết áp tâm thu (mmHg)')
    blood_pressure_diastolic = models.IntegerField(null=True, blank=True, verbose_name='Huyết áp tâm trương (mmHg)')
    heart_rate = models.IntegerField(null=True, blank=True, verbose_name='Nhịp tim (bpm)')
    respiratory_rate = models.IntegerField(null=True, blank=True, verbose_name='Nhịp thở (lần/phút)')
    temperature = models.FloatField(null=True, blank=True, verbose_name='Nhiệt độ (°C)')
    spo2 = models.FloatField(null=True, blank=True, verbose_name='SpO₂ (%)')
    weight = models.FloatField(null=True, blank=True, verbose_name='Cân nặng (kg)')
    pain_score = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name='Mức độ đau (0–10)',
    )
    blood_glucose = models.FloatField(null=True, blank=True, verbose_name='Đường huyết mao mạch (mmol/L)')
    notes = models.TextField(blank=True, verbose_name='Ghi chú nội bộ')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-issued_at']
        verbose_name = 'Phiếu chỉ định thuốc'
        verbose_name_plural = 'Phiếu chỉ định thuốc'

    def __str__(self):
        return f"Đơn thuốc – {self.patient.user.get_full_name()} – {self.issued_at.strftime('%d/%m/%Y')}"

    @property
    def blood_pressure_display(self):
        if self.blood_pressure_systolic and self.blood_pressure_diastolic:
            return f'{self.blood_pressure_systolic}/{self.blood_pressure_diastolic}'
        return '–'


# ─────────────────────────────────────────────────────────────────────────────
# Đánh giá phục hồi chức năng tổng thể
# ─────────────────────────────────────────────────────────────────────────────

class RehabilitationAssessment(models.Model):
    patient = models.ForeignKey(
        PatientProfile, on_delete=models.CASCADE,
        related_name='rehab_assessments', verbose_name='Bệnh nhân',
    )
    assessed_by = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True,
        related_name='rehab_assessments_done', verbose_name='Người đánh giá',
    )
    assessed_at = models.DateTimeField(verbose_name='Thời điểm đánh giá')
    assessment_type = models.CharField(
        max_length=20,
        choices=[
            ('initial', 'Đánh giá ban đầu'),
            ('progress', 'Đánh giá tiến trình'),
            ('discharge', 'Đánh giá xuất viện'),
        ],
        default='progress',
        verbose_name='Loại đánh giá',
    )

    # ── 1. ADL – Sinh hoạt hàng ngày ─────────────────────────
    barthel_index = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name='Chỉ số Barthel (0–100)',
        help_text='0=phụ thuộc hoàn toàn, 100=hoàn toàn độc lập',
    )
    fim_score = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(18), MaxValueValidator(126)],
        verbose_name='FIM – Đo lường độc lập chức năng (18–126)',
        help_text='18=phụ thuộc hoàn toàn, 126=độc lập hoàn toàn',
    )
    mrs_score = models.IntegerField(
        null=True, blank=True,
        choices=[(i, f'Độ {i}') for i in range(7)],
        verbose_name='Thang Rankin có sửa đổi – mRS (0–6)',
        help_text='0=không triệu chứng, 6=tử vong',
    )

    # ── 2. Vận động & sức mạnh cơ ────────────────────────────
    fugl_meyer_upper = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(66)],
        verbose_name='Fugl-Meyer chi trên (0–66)',
    )
    fugl_meyer_lower = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(34)],
        verbose_name='Fugl-Meyer chi dưới (0–34)',
    )
    rivermead_motor_index = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(15)],
        verbose_name='Chỉ số vận động Rivermead – RMI (0–15)',
    )
    mas_score = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(48)],
        verbose_name='Thang vận động MAS (0–48)',
    )
    motricity_index_upper = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name='Chỉ số vận động chi trên (Motricity Index)',
    )
    motricity_index_lower = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name='Chỉ số vận động chi dưới (Motricity Index)',
    )
    rom_notes = models.TextField(
        blank=True,
        verbose_name='Tầm vận động khớp – ROM (ghi chú góc khớp)',
    )

    # ── 3. Thăng bằng, dáng đi & di chuyển ─────────────────
    berg_balance_scale = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(56)],
        verbose_name='Thang thăng bằng Berg (0–56)',
        help_text='< 45: nguy cơ ngã cao',
    )
    dynamic_gait_index = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(24)],
        verbose_name='Chỉ số dáng đi động – DGI (0–24)',
        help_text='< 19: nguy cơ ngã',
    )
    six_minute_walk = models.FloatField(
        null=True, blank=True,
        verbose_name='Kiểm tra đi bộ 6 phút – 6MWT (mét)',
    )

    # ── 4. Đau, nhận thức & tâm lý ──────────────────────────
    pain_rating = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        verbose_name='Thang điểm đau (NRS 0–10)',
    )
    dash_score = models.FloatField(
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name='Thang điểm DASH – chức năng chi trên (0–100)',
        help_text='0=không hạn chế, 100=hạn chế nặng',
    )
    nihss_score = models.IntegerField(
        null=True, blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(42)],
        verbose_name='Thang điểm NIHSS – lượng giá đột quỵ (0–42)',
    )

    # ── 5. Dấu hiệu sinh tồn nền ────────────────────────────
    bp_systolic = models.IntegerField(null=True, blank=True, verbose_name='Huyết áp tâm thu (mmHg)')
    bp_diastolic = models.IntegerField(null=True, blank=True, verbose_name='Huyết áp tâm trương (mmHg)')
    heart_rate = models.IntegerField(null=True, blank=True, verbose_name='Nhịp tim (bpm)')
    respiratory_rate = models.IntegerField(null=True, blank=True, verbose_name='Nhịp thở (lần/phút)')

    notes = models.TextField(blank=True, verbose_name='Nhận xét tổng thể')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-assessed_at']
        verbose_name = 'Đánh giá phục hồi chức năng'
        verbose_name_plural = 'Đánh giá phục hồi chức năng'

    def __str__(self):
        return f"Đánh giá – {self.patient.user.get_full_name()} – {self.assessed_at.strftime('%d/%m/%Y')}"

    @property
    def fugl_meyer_total(self):
        u = self.fugl_meyer_upper or 0
        l = self.fugl_meyer_lower or 0
        if self.fugl_meyer_upper is not None or self.fugl_meyer_lower is not None:
            return u + l
        return None

    def barthel_level(self):
        if self.barthel_index is None:
            return 'secondary', '–'
        b = self.barthel_index
        if b <= 20:
            return 'danger', 'Phụ thuộc hoàn toàn'
        if b <= 60:
            return 'warning', 'Phụ thuộc nặng'
        if b <= 90:
            return 'info', 'Phụ thuộc nhẹ-vừa'
        return 'success', 'Độc lập'

    def berg_level(self):
        if self.berg_balance_scale is None:
            return 'secondary', '–'
        b = self.berg_balance_scale
        if b < 20:
            return 'danger', 'Nguy cơ ngã rất cao'
        if b < 40:
            return 'warning', 'Nguy cơ ngã trung bình'
        if b < 45:
            return 'info', 'Nguy cơ ngã thấp'
        return 'success', 'Thăng bằng tốt'

    def nihss_level(self):
        if self.nihss_score is None:
            return 'secondary', '–'
        n = self.nihss_score
        if n == 0:
            return 'success', 'Không triệu chứng'
        if n <= 4:
            return 'info', 'Nhẹ'
        if n <= 15:
            return 'warning', 'Trung bình'
        if n <= 20:
            return 'danger', 'Nặng – trung bình'
        return 'danger', 'Rất nặng'

